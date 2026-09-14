"""
Network node model.

This module defines the NetworkNode data model used in WRGD road networks.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class NetworkNode:
    """
    Node in a road network.

    Attributes
    ----------
    id : int
        Unique node identifier.
    latitude : float
        Latitude in decimal degrees.
    longitude : float
        Longitude in decimal degrees.
    elevation : float | None
        Elevation in metres, or ``None`` when it is not available.
    """

    id: int
    latitude: float
    longitude: float
    elevation: float | None
