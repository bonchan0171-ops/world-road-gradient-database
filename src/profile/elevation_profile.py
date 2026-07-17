"""
Elevation profile analysis.

This module provides the ElevationProfile class for analyzing
elevation data stored in a RoadSegment.
"""

from __future__ import annotations

from src.road.segment import RoadSegment


class ElevationProfile:
    """
    Analyze elevation information of a RoadSegment.

    Parameters
    ----------
    segment : RoadSegment
        Road segment to analyze.
    """

    def __init__(self, segment: RoadSegment) -> None:
        """
        Initialize the elevation profile.

        Parameters
        ----------
        segment : RoadSegment
            Road segment to analyze.
        """
        self._segment = segment

    def cumulative_distances(self) -> list[float]:
        """
        Calculate cumulative distances along the road segment.

        Returns
        -------
        list[float]
            Cumulative distance from the start point.
        """
        cumulative = [0.0]
        total = 0.0

        for distance in self._segment.distances:
            total += distance
            cumulative.append(total)

        return cumulative

    def max_elevation(self) -> float:
        """
        Return the maximum elevation.

        Returns
        -------
        float
            Maximum elevation in meters.
        """
        return max(self._segment.elevations)

    def min_elevation(self) -> float:
        """
        Return the minimum elevation.

        Returns
        -------
        float
            Minimum elevation in meters.
        """
        return min(self._segment.elevations)

    def elevation_profile(self) -> list[float]:
        """
        Return the elevation profile.

        Returns
        -------
        list[float]
            Elevation values.
        """
        return list(self._segment.elevations)

    def total_ascent(self) -> float:
        """
        Calculate the total ascent.

        Returns
        -------
        float
            Total ascent in meters.
        """
        ascent = 0.0

        elevations = self._segment.elevations

        for previous, current in zip(elevations, elevations[1:]):
            if current > previous:
                ascent += current - previous

        return ascent

    def total_descent(self) -> float:
        """
        Calculate the total descent.

        Returns
        -------
        float
            Total descent in meters.
        """
        descent = 0.0

        elevations = self._segment.elevations

        for previous, current in zip(elevations, elevations[1:]):
            if current < previous:
                descent += previous - current

        return descent
