"""
Tests for gradient calculation.
"""

import pytest

from src.geometry.gradient import calculate_gradient


def test_uphill_gradient():
    """Gradient should be positive for uphill."""

    gradient = calculate_gradient(
        elevation1=100.0,
        elevation2=110.0,
        distance=100.0,
    )

    assert gradient == pytest.approx(10.0)


def test_downhill_gradient():
    """Gradient should be negative for downhill."""

    gradient = calculate_gradient(
        elevation1=110.0,
        elevation2=100.0,
        distance=100.0,
    )

    assert gradient == pytest.approx(-10.0)


def test_zero_distance():
    """Zero distance should raise ValueError."""

    with pytest.raises(ValueError):
        calculate_gradient(
            elevation1=100.0,
            elevation2=110.0,
            distance=0.0,
        )
