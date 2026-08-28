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


def test_write_segments_invalid_lengths(tmp_path) -> None:
    writer = GeoJSONWriter(tmp_path / "segments.geojson")

    coords = [
        Coordinate(35.0, 135.0),
        Coordinate(35.1, 135.1),
    ]

    with pytest.raises(ValueError):
        writer.write_segments(
            coordinates=coords,
            gradients=[],
            distances=[100.0],
        )


def test_write_segments_requires_two_points(tmp_path) -> None:
    writer = GeoJSONWriter(tmp_path / "segments.geojson")

    with pytest.raises(ValueError):
        writer.write_segments(
            coordinates=[Coordinate(35.0, 135.0)],
            gradients=[],
            distances=[],
        )


def test_write_segments_includes_color(tmp_path: Path) -> None:
    output = tmp_path / "segments.geojson"

    coordinates = [
        Coordinate(35.0, 135.0),
        Coordinate(35.1, 135.1),
        Coordinate(35.2, 135.2),
    ]

    writer = GeoJSONWriter(output)

    writer.write_segments(
        coordinates=coordinates,
        gradients=[0.0, 15.0],
        distances=[100.0, 200.0],
    )

    data = json.loads(output.read_text(encoding="utf-8"))

    assert len(data["features"]) == 2

    first_properties = data["features"][0]["properties"]
    second_properties = data["features"][1]["properties"]

    assert first_properties["gradient"] == 0.0
    assert first_properties["color"] == "#00FF00"

    assert second_properties["gradient"] == 15.0
    assert second_properties["color"] == "#FF0000"
