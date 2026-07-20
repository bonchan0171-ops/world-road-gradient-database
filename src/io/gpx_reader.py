"""
GPX reader.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from src.models import Coordinate


class GPXReader:
    """
    Reader for GPX Track files.
    """

    def __init__(self, filepath: str | Path) -> None:
        """
        Initialize the GPX reader.

        Parameters
        ----------
        filepath : str | Path
            Path to the GPX file.
        """
        self.filepath = Path(filepath)

    def read(self) -> list[Coordinate]:
        """
        Read coordinates from a GPX Track.

        Returns
        -------
        list[Coordinate]
            Coordinates extracted from the first TrackSegment.

        Raises
        ------
        FileNotFoundError
            If the GPX file does not exist.
        ValueError
            If the GPX structure is invalid.
        """
        try:
            tree = ET.parse(self.filepath)
        except ET.ParseError as e:
            raise ValueError("Invalid GPX file.") from e

        root = tree.getroot()

        namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

        track = root.find("gpx:trk", namespace)

        if track is None:
            raise ValueError("Track not found.")

        segment = track.find("gpx:trkseg", namespace)

        if segment is None:
            raise ValueError("TrackSegment not found.")

        points = segment.findall("gpx:trkpt", namespace)

        if not points:
            raise ValueError("TrackPoint not found.")

        result: list[Coordinate] = []

        for point in points:
            lat = point.get("lat")
            lon = point.get("lon")

            if lat is None or lon is None:
                raise ValueError("Invalid TrackPoint.")

            result.append(
                Coordinate(
                    latitude=float(lat),
                    longitude=float(lon),
                )
            )

        return result
