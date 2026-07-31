"""
Gradient calculation utilities.

This module provides functions for calculating
road gradient from elevation and distance.
"""


def calculate_gradient(
    elevation1: float,
    elevation2: float,
    distance: float,
) -> float:
    """
    Calculate road gradient (%).

    Parameters
    ----------
    elevation1 : float
        Elevation of the first point (meters).
    elevation2 : float
        Elevation of the second point (meters).
    distance : float
        Horizontal distance between points (meters).

    Returns
    -------
    float
        Gradient in percent.

    Raises
    ------
    ValueError
        If distance is less than or equal to zero.
    """

    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    elevation_difference = elevation2 - elevation1

    return (elevation_difference / distance) * 100.0
