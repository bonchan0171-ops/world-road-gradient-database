from wrgd.analysis.score import calculate_score
from wrgd.models.road_statistics import RoadStatistics


def test_calculate_score_returns_value_between_zero_and_hundred() -> None:
    statistics = RoadStatistics(
        distance=1000.0,
        ascent=50.0,
        descent=20.0,
        highest_elevation=150.0,
        lowest_elevation=100.0,
        max_gradient=2.0,
        average_gradient=1.0,
    )

    score = calculate_score(statistics)

    assert 0.0 <= score <= 100.0
    assert score == 8.0


def test_calculate_score_is_clamped_to_hundred() -> None:
    statistics = RoadStatistics(
        distance=10000.0,
        ascent=10000.0,
        descent=5000.0,
        highest_elevation=1000.0,
        lowest_elevation=0.0,
        max_gradient=50.0,
        average_gradient=20.0,
    )

    score = calculate_score(statistics)

    assert score == 100.0


def test_calculate_score_is_clamped_to_zero() -> None:
    statistics = RoadStatistics(
        distance=-1000.0,
        ascent=-100.0,
        descent=0.0,
        highest_elevation=0.0,
        lowest_elevation=0.0,
        max_gradient=-2.0,
        average_gradient=0.0,
    )

    score = calculate_score(statistics)

    assert score == 0.0
