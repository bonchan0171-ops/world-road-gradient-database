import json
from pathlib import Path

import pytest

from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.models import Coordinate


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


def test_write_geojson_with_properties(tmp_path) -> None:
    """GeoJSON should include feature properties."""

    output_file = tmp_path / "route.geojson"

    writer = GeoJSONWriter(output_file)

    writer.write(
        [
            Coordinate(latitude=35.0, longitude=135.0),
            Coordinate(latitude=35.1, longitude=135.1),
        ],
        properties={
            "difficulty": "普通",
            "score": 42.0,
        },
    )

    data = json.loads(output_file.read_text(encoding="utf-8"))

    feature = data["features"][0]

    assert feature["properties"]["difficulty"] == "普通"
    assert feature["properties"]["score"] == 42.0
