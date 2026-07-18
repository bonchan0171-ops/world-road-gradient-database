"""
Coordinate model.

This module defines the Coordinate data model used throughout WRGD.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    """
    Geographic coordinate.

    Attributes
    ----------
    latitude : float
        Latitude in decimal degrees.
    longitude : float
        Longitude in decimal degrees.
    """

    latitude: float
    longitude: float