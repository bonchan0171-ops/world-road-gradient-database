"""CSV writer for road statistics."""

from __future__ import annotations

import csv
from pathlib import Path

from wrgd.models.difficulty import DifficultyLevel
from wrgd.models.road_statistics import RoadStatistics


def write_csv(
    statistics: RoadStatistics,
    output_path: Path,
    difficulty: DifficultyLevel | None = None,
    score: float | None = None,
) -> None:
    """Write a RoadStatistics instance to a CSV file with a header row.

    Parameters
    ----------
    statistics : RoadStatistics
        The road statistics to export.
    output_path : Path
        Destination path for the CSV file.

    Notes
    -----
    The CSV file contains a single data row with a header row describing
    each statistic field.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "distance",
        "ascent",
        "descent",
        "highest_elevation",
        "lowest_elevation",
        "max_gradient",
        "average_gradient",
        "difficulty_level",
        "difficulty_name",
        "score",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "distance": statistics.distance,
                "ascent": statistics.ascent,
                "descent": statistics.descent,
                "highest_elevation": statistics.highest_elevation,
                "lowest_elevation": statistics.lowest_elevation,
                "max_gradient": statistics.max_gradient,
                "average_gradient": statistics.average_gradient,
                "difficulty_level": difficulty.level if difficulty else "",
                "difficulty_name": difficulty.name if difficulty else "",
                "score": score if score is not None else "",
            }
        )
