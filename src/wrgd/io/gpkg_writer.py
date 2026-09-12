"""GeoPackage writer for road segments."""

from __future__ import annotations

import sqlite3
import struct
from datetime import datetime, timezone
from pathlib import Path

from wrgd.models.difficulty import DifficultyLevel
from wrgd.road.segment import RoadSegment
from wrgd.visualization import gradient_to_color

LAYER_NAME = "road_segments"
SRS_ID = 4326

_WGS84_WKT = (
    'GEOGCS["WGS 84",DATUM["WGS_1984",'
    'SPHEROID["WGS 84",6378137,298.257223563]],'
    'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],'
    'AUTHORITY["EPSG","4326"]]'
)


class GeoPackageWriter:
    """Write ``RoadSegment`` data to a GeoPackage feature table."""

    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def write_segments(
        self,
        road_segment: RoadSegment,
        *,
        difficulty: DifficultyLevel | None = None,
        score: int | None = None,
    ) -> None:
        """Write one ``LineString`` feature for each road segment."""
        if not isinstance(road_segment, RoadSegment):
            raise TypeError("road_segment must be a RoadSegment.")

        if len(road_segment.coordinates) < 2:
            raise ValueError("At least two coordinates are required.")

        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.filepath) as connection:
            self._create_schema(connection)
            self._insert_segments(connection, road_segment, difficulty, score)

    def _create_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute("PRAGMA application_id = 1196444487")
        connection.execute("PRAGMA user_version = 10300")

        connection.executescript("""
            DROP TABLE IF EXISTS road_segments;
            DROP TABLE IF EXISTS gpkg_geometry_columns;
            DROP TABLE IF EXISTS gpkg_contents;
            DROP TABLE IF EXISTS gpkg_spatial_ref_sys;

            CREATE TABLE gpkg_spatial_ref_sys (
                srs_name TEXT NOT NULL,
                srs_id INTEGER PRIMARY KEY,
                organization TEXT NOT NULL,
                organization_coordsys_id INTEGER NOT NULL,
                definition TEXT NOT NULL,
                description TEXT
            );

            CREATE TABLE gpkg_contents (
                table_name TEXT NOT NULL PRIMARY KEY,
                data_type TEXT NOT NULL,
                identifier TEXT UNIQUE,
                description TEXT DEFAULT '',
                last_change DATETIME NOT NULL,
                min_x DOUBLE,
                min_y DOUBLE,
                max_x DOUBLE,
                max_y DOUBLE,
                srs_id INTEGER,
                FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys (srs_id)
            );

            CREATE TABLE gpkg_geometry_columns (
                table_name TEXT NOT NULL,
                column_name TEXT NOT NULL,
                geometry_type_name TEXT NOT NULL,
                srs_id INTEGER NOT NULL,
                z TINYINT NOT NULL,
                m TINYINT NOT NULL,
                PRIMARY KEY (table_name, column_name),
                FOREIGN KEY (table_name) REFERENCES gpkg_contents (table_name),
                FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys (srs_id)
            );

            CREATE TABLE road_segments (
                segment_id INTEGER NOT NULL PRIMARY KEY,
                distance_m REAL NOT NULL,
                gradient_pct REAL NOT NULL,
                elevation_m REAL NOT NULL,
                difficulty TEXT,
                score INTEGER,
                color TEXT NOT NULL,
                geom BLOB NOT NULL
            );
            """)

        connection.executemany(
            """
            INSERT INTO gpkg_spatial_ref_sys (
                srs_name,
                srs_id,
                organization,
                organization_coordsys_id,
                definition,
                description
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Undefined Cartesian SRS",
                    -1,
                    "NONE",
                    -1,
                    "undefined",
                    "undefined cartesian coordinate reference system",
                ),
                (
                    "Undefined geographic SRS",
                    0,
                    "NONE",
                    0,
                    "undefined",
                    "undefined geographic coordinate reference system",
                ),
                (
                    "WGS 84",
                    SRS_ID,
                    "EPSG",
                    SRS_ID,
                    _WGS84_WKT,
                    "WGS 84 geographic 2D coordinate reference system",
                ),
            ],
        )

        connection.execute(
            """
            INSERT INTO gpkg_contents (
                table_name,
                data_type,
                identifier,
                description,
                last_change,
                srs_id
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                LAYER_NAME,
                "features",
                LAYER_NAME,
                "WRGD road segments",
                datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                SRS_ID,
            ),
        )
        connection.execute(
            """
            INSERT INTO gpkg_geometry_columns (
                table_name,
                column_name,
                geometry_type_name,
                srs_id,
                z,
                m
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (LAYER_NAME, "geom", "LINESTRING", SRS_ID, 0, 0),
        )

    def _insert_segments(
        self,
        connection: sqlite3.Connection,
        road_segment: RoadSegment,
        difficulty: DifficultyLevel | None,
        score: int | None,
    ) -> None:
        rows = []
        for index, (start, end) in enumerate(
            zip(road_segment.coordinates[:-1], road_segment.coordinates[1:])
        ):
            start_latitude, start_longitude = start
            end_latitude, end_longitude = end
            gradient = road_segment.gradients[index]
            rows.append(
                (
                    index,
                    road_segment.distances[index],
                    gradient,
                    road_segment.elevations[index],
                    difficulty.name if difficulty is not None else None,
                    int(score) if score is not None else None,
                    gradient_to_color(gradient),
                    self._encode_linestring(
                        start_longitude,
                        start_latitude,
                        end_longitude,
                        end_latitude,
                    ),
                )
            )

        connection.executemany(
            """
            INSERT INTO road_segments (
                segment_id,
                distance_m,
                gradient_pct,
                elevation_m,
                difficulty,
                score,
                color,
                geom
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    @staticmethod
    def _encode_linestring(
        start_longitude: float,
        start_latitude: float,
        end_longitude: float,
        end_latitude: float,
    ) -> bytes:
        min_longitude = min(start_longitude, end_longitude)
        min_latitude = min(start_latitude, end_latitude)
        max_longitude = max(start_longitude, end_longitude)
        max_latitude = max(start_latitude, end_latitude)

        header = b"GP" + struct.pack("<BBi", 0, 3, SRS_ID)
        envelope = struct.pack(
            "<4d",
            min_longitude,
            min_latitude,
            max_longitude,
            max_latitude,
        )
        wkb = struct.pack("<BIi", 1, 2, 2) + struct.pack(
            "<4d",
            start_longitude,
            start_latitude,
            end_longitude,
            end_latitude,
        )
        return header + envelope + wkb
