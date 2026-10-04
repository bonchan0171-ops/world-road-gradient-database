"""JSON writer for complete network route analysis results."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from wrgd.models.difficulty import DifficultyLevel
from wrgd.models.network_route_analysis import NetworkRouteAnalysis


def write_network_route_json(
    analysis: NetworkRouteAnalysis,
    output_path: Path,
    difficulty: DifficultyLevel | None = None,
    score: float | None = None,
) -> None:
    """Write route summary and statistics to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "summary": asdict(analysis.summary),
        "statistics": asdict(analysis.statistics),
    }

    if difficulty is not None:
        data["statistics"]["difficulty"] = {
            "level": difficulty.level,
            "name": difficulty.name,
        }

    if score is not None:
        data["statistics"]["score"] = score

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        json_file.write("\n")
