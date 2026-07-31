from dataclasses import dataclass


@dataclass(slots=True)
class RoadStatistics:
    """Summary statistics for a road segment."""

    distance: float
    ascent: float
    descent: float
    highest_elevation: float
    lowest_elevation: float
    max_gradient: float
    average_gradient: float
