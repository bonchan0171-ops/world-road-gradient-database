import pytest

from src.road.builder import RoadSegmentBuilder


class FakeDEMLoader:
    """Fake DEM loader for testing."""

    def get_elevation(
        self,
        lat: float,
        lon: float,
    ) -> float:
        """Return a fixed elevation."""
        return 100.0


class ErrorDEMLoader:
    """Fake DEM loader that always raises an error."""

    def get_elevation(
        self,
        lat: float,
        lon: float,
    ) -> float:
        raise ValueError("Outside DEM coverage.")


def test_build_road_segment() -> None:
    """Test building a RoadSegment."""
    builder = RoadSegmentBuilder(FakeDEMLoader())

    coordinates = [
        (35.0, 139.0),
        (35.001, 139.001),
    ]

    segment = builder.build(coordinates)

    assert len(segment.coordinates) == 2
    assert len(segment.elevations) == 2
    assert len(segment.distances) == 1
    assert len(segment.gradients) == 1


def test_elevations() -> None:
    """Test elevation retrieval."""
    builder = RoadSegmentBuilder(FakeDEMLoader())

    coordinates = [
        (35.0, 139.0),
        (35.001, 139.001),
    ]

    segment = builder.build(coordinates)

    assert segment.elevations == [100.0, 100.0]


def test_gradients() -> None:
    """Gradient should be zero if elevations are equal."""
    builder = RoadSegmentBuilder(FakeDEMLoader())

    coordinates = [
        (35.0, 139.0),
        (35.001, 139.001),
    ]

    segment = builder.build(coordinates)

    assert segment.gradients == [0.0]


def test_empty_coordinates() -> None:
    """Empty coordinate list should raise ValueError."""
    builder = RoadSegmentBuilder(FakeDEMLoader())

    with pytest.raises(ValueError):
        builder.build([])


def test_single_coordinate() -> None:
    """A single coordinate should raise ValueError."""
    builder = RoadSegmentBuilder(FakeDEMLoader())

    with pytest.raises(ValueError):
        builder.build(
            [
                (35.0, 139.0),
            ]
        )


def test_dem_loader_error() -> None:
    """Errors from DEMLoader should propagate."""
    builder = RoadSegmentBuilder(ErrorDEMLoader())

    coordinates = [
        (35.0, 139.0),
        (35.001, 139.001),
    ]

    with pytest.raises(ValueError):
        builder.build(coordinates)
