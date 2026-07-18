from pathlib import Path

from src.io.geojson_reader import GeoJSONReader
from src.models import Coordinate


def test_read_geojson() -> None:
    reader = GeoJSONReader(Path("tests/data/sample.geojson"))

    coordinates = reader.read()

    assert len(coordinates) == 3

    assert coordinates[0] == Coordinate(
        latitude=35.681236,
        longitude=139.767125,
    )

    assert coordinates[-1] == Coordinate(
        latitude=35.682000,
        longitude=139.769000,
    )