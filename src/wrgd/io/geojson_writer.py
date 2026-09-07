"""
GeoJSON writer.
"""

from __future__ import annotations

import json
from pathlib import Path

from wrgd.models import Coordinate
from wrgd.models.difficulty import DifficultyLevel
from wrgd.road.segment import RoadSegment
from wrgd.visualization import gradient_to_color


class GeoJSONWriter:
    """
    Write geographic coordinates to a GeoJSON FeatureCollection.
    """

    def __init__(self, filepath: str | Path) -> None:
        """
        Initialize the GeoJSON writer.

        Parameters
        ----------
        filepath : str | Path
            Path to the output GeoJSON file.
        """
        self.filepath = Path(filepath)

    def write(
        self,
        coordinates: list[Coordinate],
        properties: dict[str, object] | None = None,
    ) -> None:
        """
        Write coordinates to a GeoJSON FeatureCollection.

        Parameters
        ----------
        coordinates : list[Coordinate]
            Geographic coordinates to write.

        Raises
        ------
        ValueError
            If the coordinate list is empty.
        OSError
            If the output file cannot be written.
        """

        if not coordinates:
            raise ValueError("Coordinate list is empty.")

        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [coord.longitude, coord.latitude] for coord in coordinates
                        ],
                    },
                    "properties": properties or {},
                }
            ],
        }

        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
            )
            f.write("\n")

    def write_segments(
        self,
        coordinates: list[Coordinate] | RoadSegment,
        gradients: list[float] | None = None,
        distances: list[float] | None = None,
        difficulty: DifficultyLevel | None = None,
        score: float | None = None,
    ) -> None:
        """Write each road segment as an individual GeoJSON Feature."""

        elevations: list[float] | None = None
        if isinstance(coordinates, RoadSegment):
            road_segment = coordinates
            coordinates = [
                Coordinate(latitude=latitude, longitude=longitude)
                for latitude, longitude in road_segment.coordinates
            ]
            elevations = road_segment.elevations
            gradients = road_segment.gradients
            distances = road_segment.distances

        if gradients is None or distances is None:
            raise ValueError("Gradients and distances are required.")

        if len(coordinates) < 2:
            raise ValueError("At least two coordinates are required.")

        if len(gradients) != len(coordinates) - 1:
            raise ValueError("Gradient count does not match segment count.")

        if len(distances) != len(coordinates) - 1:
            raise ValueError("Distance count does not match segment count.")

        features = []

        for index in range(len(gradients)):
            start = coordinates[index]
            end = coordinates[index + 1]

            properties = {
                "segment_id": index,
                "distance": distances[index],
                "gradient": gradients[index],
                "distance_m": distances[index],
                "gradient_pct": gradients[index],
                "color": gradient_to_color(gradients[index]),
            }

            if elevations is not None:
                properties["elevation_m"] = elevations[index]
            if difficulty is not None:
                properties["difficulty"] = difficulty.name
            if score is not None:
                properties["score"] = score

            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [start.longitude, start.latitude],
                            [end.longitude, end.latitude],
                        ],
                    },
                    "properties": properties,
                }
            )

        data = {
            "type": "FeatureCollection",
            "features": features,
        }

        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
