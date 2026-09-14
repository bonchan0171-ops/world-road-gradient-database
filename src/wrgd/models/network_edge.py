"""
Network edge model.

This module defines the NetworkEdge data model used in WRGD road networks.
"""

from dataclasses import dataclass

from .coordinate import Coordinate
from .network_node import NetworkNode


@dataclass(slots=True)
class NetworkEdge:
    """
    Edge connecting two nodes in a road network.

    Attributes
    ----------
    id : int
        Unique edge identifier.
    start_node : NetworkNode
        Node where the edge starts.
    end_node : NetworkNode
        Node where the edge ends.
    distance : float
        Edge length in metres.
    average_gradient : float
        Average road gradient as a percentage.
    road_type : str
        Road classification.
    oneway : bool
        Whether travel is restricted to one direction.
    geometry : list[Coordinate]
        Coordinates describing the edge geometry.
    """

    id: int
    start_node: NetworkNode
    end_node: NetworkNode
    distance: float
    average_gradient: float
    road_type: str
    oneway: bool
    geometry: list[Coordinate]
