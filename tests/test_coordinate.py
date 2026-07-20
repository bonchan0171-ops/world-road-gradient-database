from src.models import Coordinate


def test_coordinate_creation() -> None:
    coord = Coordinate(35.681236, 139.767125)

    assert coord.latitude == 35.681236
    assert coord.longitude == 139.767125
