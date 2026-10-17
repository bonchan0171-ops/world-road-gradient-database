import json
from pathlib import Path

from wrgd.io import write_road_network_summary_json
from wrgd.models import RoadNetworkSummary


def test_write_road_network_summary_json(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "network-summary.json"
    summary = RoadNetworkSummary(
        node_count=4,
        edge_count=3,
        total_distance=38.0,
        road_type_counts={"primary": 2, "tertiary": 1},
        road_type_distances={"primary": 30.5, "tertiary": 7.5},
        bridge_edge_count=2,
        tunnel_edge_count=1,
        oneway_edge_count=2,
    )

    write_road_network_summary_json(summary, output)

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "node_count": 4,
        "edge_count": 3,
        "total_distance_m": 38.0,
        "road_type_counts": {"primary": 2, "tertiary": 1},
        "road_type_distances_m": {"primary": 30.5, "tertiary": 7.5},
        "bridge_edge_count": 2,
        "tunnel_edge_count": 1,
        "oneway_edge_count": 2,
    }
