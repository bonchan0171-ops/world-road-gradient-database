"""GPX writer."""

from pathlib import Path
from typing import Sequence
import xml.etree.ElementTree as ET


class GPXWriter:
    """Writer for GPX 1.1 files."""

    def write(
        self,
        coordinates: Sequence[tuple[float, float]],
        output_file: str | Path,
    ) -> None:
        """
        Write coordinates to a GPX file.

        Parameters
        ----------
        coordinates
            Sequence of (latitude, longitude).
        output_file
            Output GPX file.
        """

        gpx = ET.Element(
            "gpx",
            attrib={
                "version": "1.1",
                "creator": "WRGD",
                "xmlns": "http://www.topografix.com/GPX/1/1",
            },
        )

        trk = ET.SubElement(gpx, "trk")
        trkseg = ET.SubElement(trk, "trkseg")

        for lat, lon in coordinates:
            ET.SubElement(
                trkseg,
                "trkpt",
                attrib={
                    "lat": str(lat),
                    "lon": str(lon),
                },
            )

        tree = ET.ElementTree(gpx)

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        tree.write(
            output_file,
            encoding="utf-8",
            xml_declaration=True,
        )