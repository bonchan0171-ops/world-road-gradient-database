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
        """
        Initialize the GeoJSON reader.

        Parameters
        ----------
        filepath : str | Path
            Path to the GeoJSON file.
        """
        self.filepath = Path(filepath)

    def read(self) -> list[Coordinate]:
        """
        Read coordinates from a GeoJSON FeatureCollection.

        Returns
        -------
        list[Coordinate]
            A list of geographic coordinates extracted from the first
            LineString feature.

        Raises
        ------
        FileNotFoundError
            If the GeoJSON file does not exist.
        ValueError
            If the GeoJSON structure is invalid or does not contain a
            supported LineString geometry.
        """

        try:
            with self.filepath.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid GeoJSON file.") from e

        if data.get("type") != "FeatureCollection":
            raise ValueError("GeoJSON must be a FeatureCollection.")

        features = data.get("features", [])

        if not features:
            raise ValueError("No features found.")

        feature = features[0]

        geometry = feature.get("geometry")

        if geometry is None:
            raise ValueError("Geometry not found.")

        if geometry.get("type") != "LineString":
            raise ValueError("Only LineString is supported.")

        coordinates = geometry.get("coordinates", [])

        if not coordinates:
            raise ValueError("LineString contains no coordinates.")

        result: list[Coordinate] = []

        for coordinate in coordinates:
            if len(coordinate) < 2:
                raise ValueError("Invalid coordinate.")

            lon, lat = coordinate[:2]

            result.append(
                Coordinate(
                    latitude=lat,
                    longitude=lon,
                )
            )

        return result