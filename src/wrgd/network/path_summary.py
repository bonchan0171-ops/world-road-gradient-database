"""Summary helpers for road network paths."""

from wrgd.models.network_path import NetworkPath
from wrgd.models.network_path_summary import NetworkPathSummary

from .road_network import RoadNetwork


def summarize_network_path(
    network: RoadNetwork,
    path: NetworkPath,
) -> NetworkPathSummary:
    """Aggregate distance and road attributes from a path's edges."""
    distance = 0.0
    bridge_count = 0
    tunnel_count = 0
    road_type_counts: dict[str, int] = {}

    for edge_id in path.edge_ids:
        edge = network.get_edge(edge_id)
        distance += edge.distance
        bridge_count += edge.bridge
        tunnel_count += edge.tunnel
        road_type_counts[edge.road_type] = road_type_counts.get(edge.road_type, 0) + 1

    return NetworkPathSummary(
        distance=distance,
        edge_count=len(path.edge_ids),
        bridge_count=bridge_count,
        tunnel_count=tunnel_count,
        road_type_counts=road_type_counts,
    )
