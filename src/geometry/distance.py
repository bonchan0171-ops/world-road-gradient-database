"""
Distance calculation utilities.

This module provides functions for calculating the distance
between two geographic coordinates.
"""

from math import atan2, cos, radians, sin, sqrt

# Mean radius of the Earth (meters)
EARTH_RADIUS = 6_371_000.0


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate the great-circle distance between two points
    using the Haversine formula.

    Parameters
    ----------
    lat1 : float
        Latitude of first point (degrees)
    lon1 : float
        Longitude of first point (degrees)
    lat2 : float
        Latitude of second point (degrees)
    lon2 : float
        Longitude of second point (degrees)

    Returns
    -------
    float
        Distance in meters.
    """

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS * c
