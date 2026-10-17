"""Summary helpers for complete road networks."""

from wrgd.models.road_network_summary import RoadNetworkSummary

from .road_network import RoadNetwork


def summarize_road_network(network: RoadNetwork) -> RoadNetworkSummary:
    """Aggregate node, edge, distance, and road-attribute counts."""
    total_distance = 0.0
    road_type_counts: dict[str, int] = {}
    road_type_distances: dict[str, float] = {}
    bridge_edge_count = 0
    tunnel_edge_count = 0
    oneway_edge_count = 0

    for edge in network.edges.values():
        total_distance += edge.distance
        road_type_counts[edge.road_type] = road_type_counts.get(edge.road_type, 0) + 1
        road_type_distances[edge.road_type] = (
            road_type_distances.get(edge.road_type, 0.0) + edge.distance
        )
        bridge_edge_count += edge.bridge
        tunnel_edge_count += edge.tunnel
        oneway_edge_count += edge.oneway

    return RoadNetworkSummary(
        node_count=network.node_count(),
        edge_count=network.edge_count(),
        total_distance=total_distance,
        road_type_counts=road_type_counts,
        road_type_distances=road_type_distances,
        bridge_edge_count=bridge_edge_count,
        tunnel_edge_count=tunnel_edge_count,
        oneway_edge_count=oneway_edge_count,
    )
