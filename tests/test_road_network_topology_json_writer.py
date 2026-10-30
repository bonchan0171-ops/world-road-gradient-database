import json
from pathlib import Path

import pytest

from wrgd.io.road_network_topology_json_writer import (
    write_road_network_topology_json,
)
from wrgd.models.road_network_topology_summary import RoadNetworkTopologySummary


def test_write_road_network_topology_json(tmp_path: Path) -> None:
    output = tmp_path / "topology.json"
    summary = RoadNetworkTopologySummary(
        node_count=4,
        edge_count=3,
        component_count=2,
        node_degrees={1: 1, 2: 2, 3: 1, 4: 0},
        isolated_node_ids=[4],
        dead_end_node_ids=[1, 3],
        intersection_node_ids=[],
        connected_components=[[1, 2, 3], [4]],
    )

    write_road_network_topology_json(summary, output)

    content = output.read_bytes()
    assert content.endswith(b"\n")
    assert json.loads(content.decode("utf-8")) == {
        "node_count": 4,
        "edge_count": 3,
        "component_count": 2,
        "node_degrees": {"1": 1, "2": 2, "3": 1, "4": 0},
        "isolated_node_ids": [4],
        "dead_end_node_ids": [1, 3],
        "intersection_node_ids": [],
        "connected_components": [[1, 2, 3], [4]],
    }
    assert content.startswith(b"{")
    assert b'\n  "node_count"' in content


def test_write_empty_road_network_topology_json(tmp_path: Path) -> None:
    output = tmp_path / "empty.json"
    summary = RoadNetworkTopologySummary(
        node_count=0,
        edge_count=0,
        component_count=0,
        node_degrees={},
        isolated_node_ids=[],
        dead_end_node_ids=[],
        intersection_node_ids=[],
        connected_components=[],
    )

    write_road_network_topology_json(summary, output)

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "node_count": 0,
        "edge_count": 0,
        "component_count": 0,
        "node_degrees": {},
        "isolated_node_ids": [],
        "dead_end_node_ids": [],
        "intersection_node_ids": [],
        "connected_components": [],
    }


def test_write_road_network_topology_json_does_not_create_parent(
    tmp_path: Path,
) -> None:
    output_directory = tmp_path / "missing"
    summary = RoadNetworkTopologySummary(
        node_count=0,
        edge_count=0,
        component_count=0,
        node_degrees={},
        isolated_node_ids=[],
        dead_end_node_ids=[],
        intersection_node_ids=[],
        connected_components=[],
    )

    with pytest.raises(FileNotFoundError):
        write_road_network_topology_json(summary, output_directory / "topology.json")

    assert not output_directory.exists()
