"""JSON writer for whole-network summaries."""

from __future__ import annotations

import json
from pathlib import Path

from wrgd.models.road_network_summary import RoadNetworkSummary


def write_road_network_summary_json(
    summary: RoadNetworkSummary,
    output_path: Path,
) -> None:
    """Write a road network summary as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "node_count": summary.node_count,
        "edge_count": summary.edge_count,
        "total_distance_m": summary.total_distance,
        "road_type_counts": summary.road_type_counts,
        "road_type_distances_m": summary.road_type_distances,
        "bridge_edge_count": summary.bridge_edge_count,
        "tunnel_edge_count": summary.tunnel_edge_count,
        "oneway_edge_count": summary.oneway_edge_count,
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        json_file.write("\n")
