"""Topology summary model for a road network."""

from dataclasses import dataclass


@dataclass(slots=True)
class RoadNetworkTopologySummary:
    """Physical connectivity summary for a road network."""

    node_count: int
    edge_count: int
    component_count: int
    node_degrees: dict[int, int]
    isolated_node_ids: list[int]
    dead_end_node_ids: list[int]
    intersection_node_ids: list[int]
    connected_components: list[list[int]]
