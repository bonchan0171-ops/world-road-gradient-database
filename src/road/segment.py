"""Road segment model."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class RoadSegment:
    """Represents a road segment with geometric information.

    Attributes:
        coordinates: List of (latitude, longitude) tuples.
        elevations: Elevation values corresponding to each coordinate (m).
        distances: Distances between adjacent coordinates (m).
        gradients: Gradients between adjacent coordinates (%).
    """

    coordinates: list[tuple[float, float]]
    elevations: list[float]
    distances: list[float] = field(default_factory=list)
    gradients: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the consistency of the stored data."""
        point_count = len(self.coordinates)

        if point_count != len(self.elevations):
            raise ValueError("coordinates and elevations must have the same length.")

        expected_segments = max(0, point_count - 1)

        if len(self.distances) != expected_segments:
            raise ValueError(f"distances must contain {expected_segments} elements.")

        if len(self.gradients) != expected_segments:
            raise ValueError(f"gradients must contain {expected_segments} elements.")

    def point_count(self) -> int:
        """Return the number of coordinate points."""
        return len(self.coordinates)

    def segment_count(self) -> int:
        """Return the number of road segments."""
        return len(self.distances)

    def total_distance(self) -> float:
        """Return the total distance in meters."""
        return sum(self.distances)

        return sum(self.gradients) / len(self.gradients)

    def max_gradient(self) -> float:
        """Return the maximum gradient (%)."""
        if not self.gradients:
            return 0.0

        return max(self.gradients)

    def highest_elevation(self) -> float:
        """Return the highest elevation (m)."""
        if not self.elevations:
            return 0.0

        return max(self.elevations)

    def lowest_elevation(self) -> float:
        """Return the lowest elevation (m)."""
        if not self.elevations:
            return 0.0

        return min(self.elevations)

    def total_ascent(self) -> float:
        """Return the total ascent (m)."""
        return sum(
            max(0.0, current - previous)
            for previous, current in zip(
                self.elevations[:-1],
                self.elevations[1:],
            )
        )

    def total_descent(self) -> float:
        """Return the total descent (m)."""
        return sum(
            max(0.0, previous - current)
            for previous, current in zip(
                self.elevations[:-1],
                self.elevations[1:],
            )
        )

    def average_gradient(self) -> float:
        """Return the average gradient (%)."""
        if not self.gradients:
            return 0.0

        return sum(self.gradients) / len(self.gradients)

    def statistics(self) -> dict[str, float]:
        return {
            "distance": self.total_distance(),
            "ascent": self.total_ascent(),
            "descent": self.total_descent(),
            "highest_elevation": self.highest_elevation(),
            "lowest_elevation": self.lowest_elevation(),
            "max_gradient": self.max_gradient(),
            "average_gradient": self.average_gradient(),
        }
