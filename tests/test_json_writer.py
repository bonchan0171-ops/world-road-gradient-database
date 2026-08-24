import json

from wrgd.io.json_writer import write_json
from wrgd.models import DifficultyLevel, RoadStatistics


def test_write_json_with_analysis(tmp_path) -> None:
    output = tmp_path / "result.json"

    stats = RoadStatistics(
        distance=1000.0,
        ascent=50.0,
        descent=20.0,
        highest_elevation=150.0,
        lowest_elevation=100.0,
        max_gradient=6.0,
        average_gradient=3.0,
    )

    difficulty = DifficultyLevel(
        level=2,
        name="易しい",
        score=18.0,
    )

    write_json(
        stats,
        output,
        difficulty=difficulty,
        score=18.0,
    )

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["difficulty"]["level"] == 2
    assert data["difficulty"]["name"] == "易しい"
    assert data["score"] == 18.0
