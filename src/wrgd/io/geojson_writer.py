"""
GeoJSON writer.
"""

from __future__ import annotations

import json
from pathlib import Path

from wrgd.models import Coordinate


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
        coordinates: list[Coordinate],
        gradients: list[float],
        distances: list[float],
    ) -> None:
        """Write each road segment as an individual GeoJSON Feature."""

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
                    "properties": {
                        "segment_id": index,
                        "distance": distances[index],
                        "gradient": gradients[index],
                    },
                }
            )

        data = {
            "type": "FeatureCollection",
            "features": features,
        }

        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
