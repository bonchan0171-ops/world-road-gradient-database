"""Summary model for an entire road network."""

from dataclasses import dataclass


@dataclass(slots=True)
class RoadNetworkSummary:
    """Aggregate counts and distances for a road network."""

    node_count: int
    edge_count: int
    total_distance: float
    road_type_counts: dict[str, int]
    road_type_distances: dict[str, float]
    bridge_edge_count: int
    tunnel_edge_count: int
    oneway_edge_count: int
