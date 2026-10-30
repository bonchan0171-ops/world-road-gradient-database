"""JSON writer for road network topology summaries."""

from __future__ import annotations

import json
from pathlib import Path

from wrgd.models.road_network_topology_summary import RoadNetworkTopologySummary


def write_road_network_topology_json(
    summary: RoadNetworkTopologySummary,
    output_path: Path,
) -> None:
    """Write a road network topology summary as JSON."""
    data = {
        "node_count": summary.node_count,
        "edge_count": summary.edge_count,
        "component_count": summary.component_count,
        "node_degrees": summary.node_degrees,
        "isolated_node_ids": summary.isolated_node_ids,
        "dead_end_node_ids": summary.dead_end_node_ids,
        "intersection_node_ids": summary.intersection_node_ids,
        "connected_components": summary.connected_components,
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        json_file.write("\n")
