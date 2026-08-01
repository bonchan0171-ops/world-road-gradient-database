"""JSON writer for road statistics."""

from __future__ import annotations

import json
from pathlib import Path

from wrgd.models.road_statistics import RoadStatistics


def write_json(statistics: RoadStatistics, output_path: Path) -> None:
    """Write a RoadStatistics instance to a JSON file.

    Parameters
    ----------
    statistics : RoadStatistics
        The road statistics to export.
    output_path : Path
        Destination path for the JSON file.

    Notes
    -----
    The JSON file stores the statistics as a single object with one field
    per RoadStatistics attribute.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "distance": statistics.distance,
        "ascent": statistics.ascent,
        "descent": statistics.descent,
        "highest_elevation": statistics.highest_elevation,
        "lowest_elevation": statistics.lowest_elevation,
        "max_gradient": statistics.max_gradient,
        "average_gradient": statistics.average_gradient,
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        json_file.write("\n")
