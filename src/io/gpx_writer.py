"""GPX Writer."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Sequence


class GPXWriter:
    """Write points to a GPX 1.1 file."""

    def write(
        self,
        points: Sequence[tuple[float, ...]],
        output_path: str | Path,
    ) -> None:
        """Write points to a GPX file.

        Args:
            points:
                Sequence of:
                - (latitude, longitude)
                - (latitude, longitude, elevation)
            output_path:
                Output GPX file path.
        """

        gpx = ET.Element(
            "gpx",
            version="1.1",
            creator="WRGD",
            xmlns="http://www.topografix.com/GPX/1/1",
        )

        trk = ET.SubElement(gpx, "trk")
        seg = ET.SubElement(trk, "trkseg")

        for point in points:
            if len(point) == 2:
                lat, lon = point
                ele = None

            elif len(point) == 3:
                lat, lon, ele = point

            else:
                raise ValueError(
                    "Each point must be " "(lat, lon) or (lat, lon, elevation)."
                )

            trkpt = ET.SubElement(
                seg,
                "trkpt",
                lat=str(lat),
                lon=str(lon),
            )

            if ele is not None:
                ele_elem = ET.SubElement(trkpt, "ele")
                ele_elem.text = str(ele)

        tree = ET.ElementTree(gpx)
        ET.indent(tree, space="    ")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        tree.write(
            output_path,
            encoding="utf-8",
            xml_declaration=True,
        )
