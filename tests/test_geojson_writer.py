import json
from pathlib import Path

import pytest

from src.io.geojson_writer import GeoJSONWriter
from src.models import Coordinate


def test_write_geojson(tmp_path: Path) -> None:
    output = tmp_path / "road.geojson"

    coordinates = [
        Coordinate(35.681236, 139.767125),
        Coordinate(35.681500, 139.768000),
    ]

    writer = GeoJSONWriter(output)
    writer.write(coordinates)

    assert output.exists()

    with output.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1

    geometry = data["features"][0]["geometry"]

    assert geometry["type"] == "LineString"

    assert geometry["coordinates"] == [
        [139.767125, 35.681236],
        [139.768000, 35.681500],
    ]


def test_write_empty_coordinates(tmp_path: Path) -> None:
    writer = GeoJSONWriter(tmp_path / "road.geojson")

    with pytest.raises(
        ValueError,
        match="Coordinate list is empty.",
    ):
        writer.write([])    