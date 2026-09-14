"""
Network path model.

This module defines the NetworkPath data model used for road network routes.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class NetworkPath:
    """
    Path through a road network.

    Attributes
    ----------
    node_ids : list[int]
        Node identifiers in traversal order.
    edge_ids : list[int]
        Edge identifiers in traversal order.
    distance : float
        Total path distance in metres.
    """

    node_ids: list[int]
    edge_ids: list[int]
    distance: float
