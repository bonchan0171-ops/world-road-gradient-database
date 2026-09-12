"""Tests for curvature calculation."""

from math import isinf

import pytest

from wrgd.geometry.curvature import (
    CurvatureResult,
    analyze_curvature,
    calculate_curvature,
    calculate_turn_angle,
)


def test_calculate_turn_angle() -> None:
    """A right-angle route should have a 90-degree turn."""
    angle = calculate_turn_angle(
        (0.0, 0.0),
        (0.0, 0.001),
        (0.001, 0.001),
    )

    assert angle == pytest.approx(90.0)


def test_straight_line_has_zero_curvature() -> None:
    """A straight route should have infinite radius and zero curvature."""
    result = calculate_curvature(
        (0.0, 0.0),
        (0.0, 0.001),
        (0.0, 0.002),
    )

    assert isinstance(result, CurvatureResult)
    assert result.segment_index == 0
    assert result.turn_direction == "straight"
    assert isinf(result.radius_m)
    assert result.curvature_per_m == 0.0
    assert not result.is_sharp_curve


def test_curve_result_and_segment_indices() -> None:
    """Each three-point window should receive its starting index."""
    results = analyze_curvature(
        [
            (0.0, 0.0),
            (0.0, 0.001),
            (0.001, 0.001),
            (0.001, 0.002),
        ]
    )

    assert [result.segment_index for result in results] == [0, 1]
    assert results[0].turn_direction == "left"
    assert results[0].radius_m == pytest.approx(78.6, rel=0.01)
    assert results[0].curvature_per_m == pytest.approx(1 / results[0].radius_m)
    assert results[0].is_sharp_curve


def test_duplicate_consecutive_points_raise_value_error() -> None:
    """Duplicate points cannot define a direction vector."""
    with pytest.raises(ValueError):
        calculate_turn_angle(
            (0.0, 0.0),
            (0.0, 0.0),
            (0.001, 0.001),
        )


def test_fewer_than_three_points_returns_empty_list() -> None:
    """A coordinate sequence needs three points for one result."""
    assert analyze_curvature([(0.0, 0.0), (0.0, 0.001)]) == []
