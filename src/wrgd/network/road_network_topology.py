"""Physical topology analysis for road networks."""

from collections import deque

from wrgd.models.road_network_topology_summary import RoadNetworkTopologySummary

from .road_network import RoadNetwork


def analyze_network_topology(
    network: RoadNetwork,
) -> RoadNetworkTopologySummary:
    """Analyze undirected physical connectivity in a road network."""
    node_ids = sorted(network.nodes)
    node_degrees = {node_id: 0 for node_id in node_ids}
    adjacency: dict[int, set[int]] = {node_id: set() for node_id in node_ids}

    for edge in network.edges.values():
        start_node_id = edge.start_node.id
        end_node_id = edge.end_node.id

        if start_node_id not in node_degrees:
            raise ValueError(f"Edge {edge.id} references missing node {start_node_id}.")
        if end_node_id not in node_degrees:
            raise ValueError(f"Edge {edge.id} references missing node {end_node_id}.")

        node_degrees[start_node_id] += 1
        node_degrees[end_node_id] += 1
        adjacency[start_node_id].add(end_node_id)
        adjacency[end_node_id].add(start_node_id)

    connected_components: list[list[int]] = []
    visited: set[int] = set()

    for node_id in node_ids:
        if node_id in visited:
            continue

        component: list[int] = []
        queue = deque([node_id])
        visited.add(node_id)

        while queue:
            current_node_id = queue.popleft()
            component.append(current_node_id)

            for neighbor_id in adjacency[current_node_id]:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)

        connected_components.append(sorted(component))

    connected_components.sort(key=lambda component: component[0])

    return RoadNetworkTopologySummary(
        node_count=len(network.nodes),
        edge_count=len(network.edges),
        component_count=len(connected_components),
        node_degrees=node_degrees,
        isolated_node_ids=[
            node_id for node_id, degree in node_degrees.items() if degree == 0
        ],
        dead_end_node_ids=[
            node_id for node_id, degree in node_degrees.items() if degree == 1
        ],
        intersection_node_ids=[
            node_id for node_id, degree in node_degrees.items() if degree >= 3
        ],
        connected_components=connected_components,
    )
