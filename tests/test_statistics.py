"""Tests for WRGD statistics utilities."""

import pytest

from wrgd.analysis.statistics import calculate_statistics
from wrgd.profile import ElevationProfile
from wrgd.road.segment import RoadSegment


def create_segment() -> RoadSegment:
    """Create a sample RoadSegment for statistics testing."""
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


def test_calculate_statistics_from_elevation_profile() -> None:
    """calculate_statistics should return RoadStatistics from ElevationProfile."""
    profile = ElevationProfile(create_segment())

    statistics = calculate_statistics(profile)

    assert statistics.distance == 300.0
    assert statistics.ascent == 50.0
    assert statistics.descent == 10.0
    assert statistics.highest_elevation == 140.0
    assert statistics.lowest_elevation == 100.0
    assert statistics.max_gradient == 30.0
    assert statistics.average_gradient == pytest.approx(13.3333333333)


def test_calculate_statistics_raises_for_insufficient_profile_points() -> None:
    """calculate_statistics should reject a profile with fewer than two points."""
    segment = RoadSegment(
        coordinates=[(35.0, 139.0)],
        elevations=[100.0],
        distances=[],
        gradients=[],
    )
    profile = ElevationProfile(segment)

    with pytest.raises(ValueError, match="At least two profile points are required"):
        calculate_statistics(profile)


def test_calculate_statistics_raises_for_non_monotonic_distances() -> None:
    """calculate_statistics should reject a profile with non-increasing distances."""
    segment = RoadSegment(
        coordinates=[
            (35.0, 139.0),
            (35.1, 139.1),
            (35.2, 139.2),
        ],
        elevations=[100.0, 110.0, 90.0],
        distances=[100.0, -50.0],
        gradients=[10.0, -20.0],
    )
    profile = ElevationProfile(segment)

    with pytest.raises(ValueError, match="Distance values must increase monotonically"):
        calculate_statistics(profile)
