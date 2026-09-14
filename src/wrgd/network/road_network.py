"""
Road network model.

This module defines the RoadNetwork container used in WRGD road analysis.
"""

import heapq
from dataclasses import dataclass, field

from ..io.dem_loader import DEMLoader
from ..models.coordinate import Coordinate
from ..models.network_edge import NetworkEdge
from ..models.network_node import NetworkNode
from ..models.network_path import NetworkPath
from ..models.road_statistics import RoadStatistics


@dataclass(slots=True)
class RoadNetwork:
    """
    Collection of nodes and edges that form a road network.

    Attributes
    ----------
    nodes : dict[int, NetworkNode]
        Nodes indexed by their identifiers.
    edges : dict[int, NetworkEdge]
        Edges indexed by their identifiers.
    """

    nodes: dict[int, NetworkNode] = field(default_factory=dict)
    edges: dict[int, NetworkEdge] = field(default_factory=dict)

    def add_node(self, node: NetworkNode) -> None:
        """Add a node to the road network."""
        self.nodes[node.id] = node

    def add_edge(self, edge: NetworkEdge) -> None:
        """Add an edge to the road network."""
        self.edges[edge.id] = edge

    def node_count(self) -> int:
        """Return the number of nodes in the road network."""
        return len(self.nodes)

    def edge_count(self) -> int:
        """Return the number of edges in the road network."""
        return len(self.edges)

    def get_node(self, node_id: int) -> NetworkNode:
        """Return the node with the specified identifier."""
        return self.nodes[node_id]

    def get_edge(self, edge_id: int) -> NetworkEdge:
        """Return the edge with the specified identifier."""
        return self.edges[edge_id]

    def get_neighbors(self, node_id: int) -> list[int]:
        """Return the node identifiers reachable from a node."""
        neighbors: list[int] = []

        for edge in self.edges.values():
            if edge.start_node.id == node_id:
                neighbors.append(edge.end_node.id)
            elif not edge.oneway and edge.end_node.id == node_id:
                neighbors.append(edge.start_node.id)

        return neighbors

    def shortest_path(
        self,
        start_node_id: int,
        end_node_id: int,
    ) -> list[int] | None:
        """
        Find the shortest path between two nodes using Dijkstra's algorithm.

        Parameters
        ----------
        start_node_id : int
            Identifier of the starting node.
        end_node_id : int
            Identifier of the destination node.

        Returns
        -------
        list[int] | None
            Node identifiers in the shortest path, or ``None`` when the
            destination cannot be reached.

        Raises
        ------
        KeyError
            If either node identifier does not exist in the network.
        """
        self.get_node(start_node_id)
        self.get_node(end_node_id)

        if start_node_id == end_node_id:
            return [start_node_id]

        distances = {start_node_id: 0.0}
        previous: dict[int, int] = {}
        queue: list[tuple[float, int]] = [(0.0, start_node_id)]

        while queue:
            current_distance, current_node_id = heapq.heappop(queue)

            if current_distance > distances[current_node_id]:
                continue

            if current_node_id == end_node_id:
                return self._build_path(previous, start_node_id, end_node_id)

            for neighbor_id, edge_distance in self._outgoing_edges(current_node_id):
                if edge_distance < 0:
                    continue

                new_distance = current_distance + edge_distance
                if new_distance >= distances.get(neighbor_id, float("inf")):
                    continue

                distances[neighbor_id] = new_distance
                previous[neighbor_id] = current_node_id
                heapq.heappush(queue, (new_distance, neighbor_id))

        return None

    def shortest_route(
        self,
        start_node_id: int,
        end_node_id: int,
    ) -> NetworkPath | None:
        """
        Find the shortest route with node and edge details.

        Parameters
        ----------
        start_node_id : int
            Identifier of the starting node.
        end_node_id : int
            Identifier of the destination node.

        Returns
        -------
        NetworkPath | None
            Shortest route details, or ``None`` when the destination cannot
            be reached.

        Raises
        ------
        KeyError
            If either node identifier does not exist in the network.
        """
        self.get_node(start_node_id)
        self.get_node(end_node_id)

        if start_node_id == end_node_id:
            return NetworkPath(
                node_ids=[start_node_id],
                edge_ids=[],
                distance=0.0,
            )

        distances = {start_node_id: 0.0}
        previous: dict[int, tuple[int, int]] = {}
        queue: list[tuple[float, int]] = [(0.0, start_node_id)]

        while queue:
            current_distance, current_node_id = heapq.heappop(queue)

            if current_distance > distances[current_node_id]:
                continue

            if current_node_id == end_node_id:
                return self._build_network_path(
                    previous,
                    start_node_id,
                    end_node_id,
                    current_distance,
                )

            for edge in self._outgoing_network_edges(current_node_id):
                if edge.distance < 0:
                    continue

                neighbor_id = (
                    edge.end_node.id
                    if edge.start_node.id == current_node_id
                    else edge.start_node.id
                )
                new_distance = current_distance + edge.distance
                if new_distance >= distances.get(neighbor_id, float("inf")):
                    continue

                distances[neighbor_id] = new_distance
                previous[neighbor_id] = (current_node_id, edge.id)
                heapq.heappush(queue, (new_distance, neighbor_id))

        return None

    def calculate_statistics(self, path: NetworkPath) -> RoadStatistics:
        """
        Calculate road statistics for a network path.

        Parameters
        ----------
        path : NetworkPath
            Network path to analyze.

        Returns
        -------
        RoadStatistics
            Distance, elevation, and gradient statistics for the path.
        """
        edges = [self.get_edge(edge_id) for edge_id in path.edge_ids]
        elevations = [self.get_node(node_id).elevation for node_id in path.node_ids]

        known_elevations = [
            elevation for elevation in elevations if elevation is not None
        ]
        ascent = 0.0
        descent = 0.0

        for previous, current in zip(elevations, elevations[1:]):
            if previous is None or current is None:
                continue
            if current > previous:
                ascent += current - previous
            elif current < previous:
                descent += previous - current

        gradients = [edge.average_gradient for edge in edges]

        return RoadStatistics(
            distance=sum(edge.distance for edge in edges),
            ascent=ascent,
            descent=descent,
            highest_elevation=max(known_elevations, default=0.0),
            lowest_elevation=min(known_elevations, default=0.0),
            max_gradient=max(gradients, default=0.0),
            average_gradient=(sum(gradients) / len(gradients) if gradients else 0.0),
        )

    def path_coordinates(self, path: NetworkPath) -> list[Coordinate]:
        """
        Build a continuous coordinate sequence for a network path.

        Parameters
        ----------
        path : NetworkPath
            Network path whose edge geometries should be combined.

        Returns
        -------
        list[Coordinate]
            Coordinates in path traversal order.

        Raises
        ------
        ValueError
            If the node and edge sequences do not form a valid path.
        KeyError
            If a referenced node or edge does not exist in the network.
        """
        if len(path.node_ids) != len(path.edge_ids) + 1:
            raise ValueError("NetworkPath node and edge counts are inconsistent.")

        for node_id in path.node_ids:
            self.get_node(node_id)

        coordinates: list[Coordinate] = []

        for index, edge_id in enumerate(path.edge_ids):
            edge = self.get_edge(edge_id)
            start_node_id = path.node_ids[index]
            end_node_id = path.node_ids[index + 1]

            if edge.start_node.id == start_node_id and edge.end_node.id == end_node_id:
                geometry = edge.geometry
            elif (
                edge.start_node.id == end_node_id and edge.end_node.id == start_node_id
            ):
                geometry = list(reversed(edge.geometry))
            else:
                raise ValueError("NetworkPath edge direction is inconsistent.")

            if not geometry:
                continue

            if coordinates and coordinates[-1] == geometry[0]:
                coordinates.extend(geometry[1:])
            else:
                coordinates.extend(geometry)

        return coordinates

    def _outgoing_edges(self, node_id: int) -> list[tuple[int, float]]:
        """Return reachable node IDs and edge distances from a node."""
        outgoing: list[tuple[int, float]] = []

        for edge in self.edges.values():
            if edge.start_node.id == node_id:
                outgoing.append((edge.end_node.id, edge.distance))
            elif not edge.oneway and edge.end_node.id == node_id:
                outgoing.append((edge.start_node.id, edge.distance))

        return outgoing

    def _outgoing_network_edges(self, node_id: int) -> list[NetworkEdge]:
        """Return directed edges reachable from a node."""
        outgoing: list[NetworkEdge] = []

        for edge in self.edges.values():
            if edge.start_node.id == node_id:
                outgoing.append(edge)
            elif not edge.oneway and edge.end_node.id == node_id:
                outgoing.append(edge)

        return outgoing

    @staticmethod
    def _build_network_path(
        previous: dict[int, tuple[int, int]],
        start_node_id: int,
        end_node_id: int,
        distance: float,
    ) -> NetworkPath:
        """Reconstruct a NetworkPath from predecessor data."""
        node_ids = [end_node_id]
        edge_ids: list[int] = []
        current_node_id = end_node_id

        while current_node_id != start_node_id:
            previous_node_id, edge_id = previous[current_node_id]
            node_ids.append(previous_node_id)
            edge_ids.append(edge_id)
            current_node_id = previous_node_id

        node_ids.reverse()
        edge_ids.reverse()
        return NetworkPath(node_ids, edge_ids, distance)

    @staticmethod
    def _build_path(
        previous: dict[int, int],
        start_node_id: int,
        end_node_id: int,
    ) -> list[int]:
        """Reconstruct a path from Dijkstra predecessor data."""
        path = [end_node_id]
        current_node_id = end_node_id

        while current_node_id != start_node_id:
            current_node_id = previous[current_node_id]
            path.append(current_node_id)

        path.reverse()
        return path

    def apply_elevation(self, dem_loader: DEMLoader | None = None) -> None:
        """
        Apply DEM elevations to nodes and recalculate edge gradients.

        Parameters
        ----------
        dem_loader : DEMLoader | None
            Loaded DEM loader. When omitted, node elevations are set to
            ``None`` and edge gradients are set to ``0.0``.
        """
        for node in self.nodes.values():
            node.elevation = self._get_elevation(node, dem_loader)

        for edge in self.edges.values():
            edge.average_gradient = self._calculate_gradient(edge)

    @staticmethod
    def _get_elevation(
        node: NetworkNode,
        dem_loader: DEMLoader | None,
    ) -> float | None:
        """Return a node elevation, or ``None`` when it is unavailable."""
        if dem_loader is None:
            return None

        try:
            return dem_loader.get_elevation(node.latitude, node.longitude)
        except (RuntimeError, ValueError):
            return None

    @staticmethod
    def _calculate_gradient(edge: NetworkEdge) -> float:
        """Calculate an edge gradient from its endpoint elevations."""
        start_elevation = edge.start_node.elevation
        end_elevation = edge.end_node.elevation

        if start_elevation is None or end_elevation is None or edge.distance == 0:
            return 0.0

        return (end_elevation - start_elevation) / edge.distance * 100
