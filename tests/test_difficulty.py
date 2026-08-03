from wrgd.analysis.difficulty import calculate_difficulty
from wrgd.models.road_statistics import RoadStatistics


def test_calculate_difficulty_returns_level_for_easy_route() -> None:
    statistics = RoadStatistics(
        distance=100.0,
        ascent=5.0,
        descent=3.0,
        highest_elevation=100.0,
        lowest_elevation=95.0,
        max_gradient=2.0,
        average_gradient=1.0,
    )

    difficulty = calculate_difficulty(statistics)

    assert difficulty.level == 1
    assert difficulty.name == "非常に易しい"
    assert difficulty.score >= 0.0


def test_calculate_difficulty_returns_level_for_hard_route() -> None:
    statistics = RoadStatistics(
        distance=5000.0,
        ascent=800.0,
        descent=200.0,
        highest_elevation=400.0,
        lowest_elevation=50.0,
        max_gradient=18.0,
        average_gradient=8.0,
    )

    difficulty = calculate_difficulty(statistics)

    assert difficulty.level == 5
    assert difficulty.name == "非常に難しい"
    assert difficulty.score >= 0.0
