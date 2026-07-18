"""
GeoJSON reader.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.models import Coordinate


class GeoJSONReader:
    """
    Reader for GeoJSON LineString files.
    """

    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def read(self) -> list[Coordinate]:
        """
        Read coordinates from a GeoJSON FeatureCollection.

        Returns
        -------
        list[Coordinate]
            Coordinates extracted from the LineString.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the GeoJSON format is invalid.
        """

        with self.filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("type") != "FeatureCollection":
            raise ValueError("GeoJSON must be a FeatureCollection.")

        features = data.get("features", [])

        if not features:
            raise ValueError("No features found.")

        geometry = features[0].get("geometry")

        if geometry is None:
            raise ValueError("Geometry not found.")

        if geometry.get("type") != "LineString":
            raise ValueError("Only LineString is supported.")

        coordinates = geometry.get("coordinates", [])

        return [
            Coordinate(latitude=lat, longitude=lon)
            for lon, lat in coordinates
        ]