from __future__ import annotations

from src.geometry.distance import calculate_distance
from src.geometry.gradient import calculate_gradient
from src.io.dem_loader import DEMLoader
from src.road.segment import RoadSegment

Coordinate = tuple[float, float]
Coordinates = list[Coordinate]


class RoadSegmentBuilder:
    """Build a RoadSegment from a sequence of coordinates."""

    def __init__(self, dem_loader: DEMLoader) -> None:
        """
        Initialize the builder.

        Parameters
        ----------
        dem_loader : DEMLoader
            DEM loader used to retrieve elevation values.
        """
        self._dem_loader = dem_loader

    def build(self, coordinates: Coordinates) -> RoadSegment:
        """
        Build a RoadSegment from coordinates.

        Parameters
        ----------
        coordinates : Coordinates
            List of (latitude, longitude) pairs.

        Returns
        -------
        RoadSegment
            Constructed RoadSegment.
        """
        self._validate_coordinates(coordinates)

        elevations = self._get_elevations(coordinates)
        distances = self._calculate_distances(coordinates)
        gradients = self._calculate_gradients(
            elevations,
            distances,
        )

        return RoadSegment(
            coordinates=coordinates,
            elevations=elevations,
            distances=distances,
            gradients=gradients,
        )

    def _validate_coordinates(
        self,
        coordinates: Coordinates,
    ) -> None:
        """
        Validate the input coordinates.

        Raises
        ------
        ValueError
            If fewer than two coordinates are provided.
        """
        if len(coordinates) < 2:
            raise ValueError(
                "At least two coordinates are required."
            )

    def _get_elevations(
        self,
        coordinates: Coordinates,
    ) -> list[float]:
        """
        Retrieve elevations for all coordinates.
        """
        return [
            self._dem_loader.get_elevation(lat, lon)
            for lat, lon in coordinates
        ]

    def _calculate_distances(
        self,
        coordinates: Coordinates,
    ) -> list[float]:
        """
        Calculate distances between consecutive coordinates.
        """
        distances: list[float] = []

        for (lat1, lon1), (lat2, lon2) in zip(
            coordinates[:-1],
            coordinates[1:],
        ):
            distances.append(
                calculate_distance(
                    lat1,
                    lon1,
                    lat2,
                    lon2,
                )
            )

        return distances

    def _calculate_gradients(
        self,
        elevations: list[float],
        distances: list[float],
    ) -> list[float]:
        """
        Calculate gradients between consecutive points.
        """
        gradients: list[float] = []

        for elevation1, elevation2, distance in zip(
            elevations[:-1],
            elevations[1:],
            distances,
        ):
            gradients.append(
                calculate_gradient(
                    elevation1,
                    elevation2,
                    distance,
                )
            )

        return gradients