"""Tests for GPXWriter."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from src.io.gpx_writer import GPXWriter


def test_write_gpx(tmp_path: Path) -> None:
    """GPX file is created successfully."""

    coordinates = [
        (35.681236, 139.767125),
        (35.682000, 139.768000),
        (35.683000, 139.769000),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()
    writer.write(coordinates, output_file)

    assert output_file.exists()


def test_gpx_structure(tmp_path: Path) -> None:
    """Generated GPX has the correct structure."""

    coordinates = [
        (35.681236, 139.767125),
        (35.682000, 139.768000),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()
    writer.write(coordinates, output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()

    namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

    trk = root.find("gpx:trk", namespace)
    assert trk is not None

    trkseg = trk.find("gpx:trkseg", namespace)
    assert trkseg is not None

    trkpts = trkseg.findall("gpx:trkpt", namespace)

    assert len(trkpts) == 2


def test_coordinates_are_written(tmp_path: Path) -> None:
    """Latitude and longitude are written correctly."""

    coordinates = [
        (35.681236, 139.767125),
        (35.682000, 139.768000),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()
    writer.write(coordinates, output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()

    namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

    trkpts = root.findall(".//gpx:trkpt", namespace)

    assert trkpts[0].attrib["lat"] == "35.681236"
    assert trkpts[0].attrib["lon"] == "139.767125"

    assert trkpts[1].attrib["lat"] == "35.682"
    assert trkpts[1].attrib["lon"] == "139.768"


def test_elevation_is_written(tmp_path: Path) -> None:
    """Elevation is written when provided."""

    coordinates = [
        (35.681236, 139.767125, 12.3),
        (35.682000, 139.768000, 15.8),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()
    writer.write(coordinates, output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()

    namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

    trkpts = root.findall(".//gpx:trkpt", namespace)

    ele1 = trkpts[0].find("gpx:ele", namespace)
    ele2 = trkpts[1].find("gpx:ele", namespace)

    assert ele1 is not None
    assert ele2 is not None

    assert ele1.text == "12.3"
    assert ele2.text == "15.8"


def test_elevation_is_optional(tmp_path: Path) -> None:
    """Elevation element is omitted when not provided."""

    coordinates = [
        (35.681236, 139.767125),
        (35.682000, 139.768000),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()
    writer.write(coordinates, output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()

    namespace = {"gpx": "http://www.topografix.com/GPX/1/1"}

    trkpts = root.findall(".//gpx:trkpt", namespace)

    assert trkpts[0].find("gpx:ele", namespace) is None
    assert trkpts[1].find("gpx:ele", namespace) is None


def test_invalid_coordinate_length(tmp_path: Path) -> None:
    """Invalid coordinate length raises ValueError."""

    coordinates = [
        (35.681236,),
    ]

    output_file = tmp_path / "route.gpx"

    writer = GPXWriter()

    with pytest.raises(ValueError):
        writer.write(coordinates, output_file)
