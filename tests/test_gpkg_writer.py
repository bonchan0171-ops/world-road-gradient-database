import json
import sqlite3
import struct
from pathlib import Path

import pytest

from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.io.gpkg_writer import GeoPackageWriter
from wrgd.models.difficulty import DifficultyLevel
from wrgd.road.segment import RoadSegment


def _road_segment() -> RoadSegment:
    return RoadSegment(
        coordinates=[(35.0, 139.0), (35.1, 139.2), (35.2, 139.1)],
        elevations=[10.0, 12.5, 9.0],
        distances=[123.4, 567.8],
        gradients=[-2.5, 7.5],
    )


def test_write_segments_creates_gpkg_schema_and_attributes(tmp_path: Path) -> None:
    output = tmp_path / "segments.gpkg"

    GeoPackageWriter(output).write_segments(_road_segment())

    with sqlite3.connect(output) as connection:
        columns = {
            row[1]: row[2]
            for row in connection.execute("PRAGMA table_info(road_segments)")
        }
        rows = connection.execute("""
            SELECT segment_id, distance_m, gradient_pct, elevation_m,
                   difficulty, score, color
            FROM road_segments
            ORDER BY segment_id
            """).fetchall()
        layer = connection.execute("""
            SELECT data_type, identifier, srs_id
            FROM gpkg_contents
            WHERE table_name = 'road_segments'
            """).fetchone()
        geometry = connection.execute("""
            SELECT geometry_type_name, srs_id, z, m
            FROM gpkg_geometry_columns
            WHERE table_name = 'road_segments'
            """).fetchone()

    assert columns == {
        "segment_id": "INTEGER",
        "distance_m": "REAL",
        "gradient_pct": "REAL",
        "elevation_m": "REAL",
        "difficulty": "TEXT",
        "score": "INTEGER",
        "color": "TEXT",
        "geom": "BLOB",
    }
    assert rows == [
        (0, 123.4, -2.5, 10.0, None, None, "#00D42A"),
        (1, 567.8, 7.5, 12.5, None, None, "#808000"),
    ]
    assert layer == ("features", "road_segments", 4326)
    assert geometry == ("LINESTRING", 4326, 0, 0)


def test_geometry_uses_longitude_latitude_and_epsg4326(tmp_path: Path) -> None:
    output = tmp_path / "segments.gpkg"

    GeoPackageWriter(output).write_segments(_road_segment())

    with sqlite3.connect(output) as connection:
        geometry = connection.execute(
            "SELECT geom FROM road_segments WHERE segment_id = 0"
        ).fetchone()[0]

    assert geometry[:2] == b"GP"
    assert geometry[3] == 3
    assert struct.unpack_from("<i", geometry, 4)[0] == 4326

    wkb_offset = 40
    byte_order, geometry_type, point_count = struct.unpack_from(
        "<BII", geometry, wkb_offset
    )
    coordinates = struct.unpack_from("<4d", geometry, wkb_offset + 9)

    assert (byte_order, geometry_type, point_count) == (1, 2, 2)
    assert coordinates == (139.0, 35.0, 139.2, 35.1)


def test_attributes_match_geojson_values(tmp_path: Path) -> None:
    road_segment = _road_segment()
    difficulty = DifficultyLevel(level=2, name="易しい", score=1.5)
    score = 42
    gpkg_output = tmp_path / "segments.gpkg"
    geojson_output = tmp_path / "segments.geojson"

    GeoPackageWriter(gpkg_output).write_segments(
        road_segment,
        difficulty=difficulty,
        score=score,
    )
    GeoJSONWriter(geojson_output).write_segments(
        road_segment,
        difficulty=difficulty,
        score=score,
    )

    with sqlite3.connect(gpkg_output) as connection:
        gpkg_rows = connection.execute("""
            SELECT segment_id, distance_m, gradient_pct, elevation_m,
                   difficulty, score, color
            FROM road_segments
            ORDER BY segment_id
            """).fetchall()

    geojson_rows = [
        (
            feature["properties"]["segment_id"],
            feature["properties"]["distance_m"],
            feature["properties"]["gradient_pct"],
            feature["properties"]["elevation_m"],
            feature["properties"]["difficulty"],
            feature["properties"]["score"],
            feature["properties"]["color"],
        )
        for feature in json.loads(geojson_output.read_text(encoding="utf-8"))[
            "features"
        ]
    ]

    assert gpkg_rows == geojson_rows
    assert all(isinstance(row[5], int) for row in gpkg_rows)


def test_writer_accepts_only_road_segment(tmp_path: Path) -> None:
    with pytest.raises(TypeError, match="road_segment must be a RoadSegment"):
        GeoPackageWriter(tmp_path / "segments.gpkg").write_segments([])
