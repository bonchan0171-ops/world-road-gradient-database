"""Tests for RoadSegment."""

import pytest

from src.road.segment import RoadSegment


def test_create_road_segment() -> None:
    """RoadSegment can be created successfully."""
    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
        ],
        elevations=[100.0, 105.0],
        distances=[120.0],
        gradients=[4.2],
    )

    assert segment.point_count() == 2
    assert segment.segment_count() == 1
    assert segment.total_distance() == 120.0
    assert segment.average_gradient() == 4.2


def test_empty_road_segment() -> None:
    """Empty RoadSegment should be handled correctly."""
    segment = RoadSegment(
        coordinates=[],
        elevations=[],
        distances=[],
        gradients=[],
    )

    assert segment.point_count() == 0
    assert segment.segment_count() == 0
    assert segment.total_distance() == 0.0
    assert segment.average_gradient() == 0.0


def test_invalid_elevation_length() -> None:
    """coordinates and elevations must have the same length."""
    with pytest.raises(ValueError):
        RoadSegment(
            coordinates=[
                (35.0, 135.0),
                (35.1, 135.1),
            ],
            elevations=[100.0],
            distances=[120.0],
            gradients=[4.2],
        )


def test_invalid_distance_length() -> None:
    """Invalid distance list length should raise ValueError."""
    with pytest.raises(ValueError):
        RoadSegment(
            coordinates=[
                (35.0, 135.0),
                (35.1, 135.1),
            ],
            elevations=[100.0, 105.0],
            distances=[],
            gradients=[4.2],
        )


def test_invalid_gradient_length() -> None:
    """Invalid gradient list length should raise ValueError."""
    with pytest.raises(ValueError):
        RoadSegment(
            coordinates=[
                (35.0, 135.0),
                (35.1, 135.1),
            ],
            elevations=[100.0, 105.0],
            distances=[120.0],
            gradients=[],
        )


def test_total_distance() -> None:
    """Total distance should be calculated correctly."""
    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
            (35.2, 135.2),
        ],
        elevations=[100.0, 110.0, 120.0],
        distances=[100.0, 200.0],
        gradients=[10.0, 5.0],
    )

    assert segment.total_distance() == 300.0


def test_average_gradient() -> None:
    """Average gradient should be calculated correctly."""
    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
            (35.2, 135.2),
        ],
        elevations=[100.0, 110.0, 120.0],
        distances=[100.0, 200.0],
        gradients=[6.0, 4.0],
    )

    assert segment.average_gradient() == 5.0


def test_statistics() -> None:
    """Statistics should return summary values correctly."""
    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
            (35.2, 135.2),
        ],
        elevations=[100.0, 110.0, 120.0],
        distances=[100.0, 200.0],
        gradients=[6.0, 4.0],
    )

    stats = segment.statistics()

    assert stats["distance"] == segment.total_distance()
    assert stats["ascent"] == segment.total_ascent()
    assert stats["descent"] == segment.total_descent()
    assert stats["highest_elevation"] == segment.highest_elevation()
    assert stats["lowest_elevation"] == segment.lowest_elevation()
    assert stats["max_gradient"] == segment.max_gradient()
    assert stats["average_gradient"] == segment.average_gradient()
