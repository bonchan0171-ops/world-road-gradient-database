from pathlib import Path

from wrgd.io.csv_writer import write_csv
from wrgd.models import RoadStatistics


def test_write_csv(tmp_path: Path) -> None:
    statistics = RoadStatistics(
        distance=1000.0,
        ascent=50.0,
        descent=20.0,
        highest_elevation=150.0,
        lowest_elevation=100.0,
        max_gradient=5.0,
        average_gradient=2.0,
    )

    output_path = tmp_path / "statistics.csv"

    write_csv(statistics, output_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "distance,ascent,descent" in content
    assert "1000.0,50.0,20.0" in content
