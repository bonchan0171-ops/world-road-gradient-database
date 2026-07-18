"""
GeoJSON writer.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.models import Coordinate


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

    def write(self, coordinates: list[Coordinate]) -> None:
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
                            [coord.longitude, coord.latitude]
                            for coord in coordinates
                        ],
                    },
                    "properties": {},
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