import pytest

from src.geometry.distance import calculate_distance


def test_same_point():
    """同じ座標なら距離は0m"""

    distance = calculate_distance(
        35.0,
        139.0,
        35.0,
        139.0,
    )

    assert distance == pytest.approx(0.0)


def test_symmetry():
    """A→B と B→A は同じ距離"""

    d1 = calculate_distance(
        35.0,
        139.0,
        35.001,
        139.002,
    )

    d2 = calculate_distance(
        35.001,
        139.002,
        35.0,
        139.0,
    )

    assert d1 == pytest.approx(d2)


def test_known_distance():
    """緯度1度の距離は約111.2km"""

    distance = calculate_distance(
        0.0,
        0.0,
        1.0,
        0.0,
    )

    assert distance == pytest.approx(
        111195,
        abs=100,
    )
