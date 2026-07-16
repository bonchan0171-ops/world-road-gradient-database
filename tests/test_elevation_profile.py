"""Tests for ElevationProfile."""

from src.profile import ElevationProfile
from src.road.segment import RoadSegment


def create_segment() -> RoadSegment:
    """Create a sample RoadSegment for testing."""
    return RoadSegment(
        coordinates=[
            (35.0, 139.0),
            (35.1, 139.1),
            (35.2, 139.2),
            (35.3, 139.3),
        ],
        elevations=[100.0, 120.0, 110.0, 140.0],
        distances=[100.0, 100.0, 100.0],
        gradients=[20.0, -10.0, 30.0],
    )


def test_cumulative_distances() -> None:
    """Test cumulative distance calculation."""
    profile = ElevationProfile(create_segment())

    assert profile.cumulative_distances() == [
        0.0,
        100.0,
        200.0,
        300.0,
    ]


def test_max_elevation() -> None:
    """Test maximum elevation."""
    profile = ElevationProfile(create_segment())

    assert profile.max_elevation() == 140.0


def test_min_elevation() -> None:
    """Test minimum elevation."""
    profile = ElevationProfile(create_segment())

    assert profile.min_elevation() == 100.0


def test_total_ascent() -> None:
    """Test total ascent."""
    profile = ElevationProfile(create_segment())

    assert profile.total_ascent() == 50.0


def test_total_descent() -> None:
    """Test total descent."""
    profile = ElevationProfile(create_segment())

    assert profile.total_descent() == 10.0