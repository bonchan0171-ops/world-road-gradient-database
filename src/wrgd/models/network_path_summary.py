"""Summary model for road network paths."""

from dataclasses import dataclass


@dataclass(slots=True)
class NetworkPathSummary:
    """Aggregate distance and road attributes for a network path."""

    distance: float
    edge_count: int
    bridge_count: int
    tunnel_count: int
    road_type_counts: dict[str, int]
