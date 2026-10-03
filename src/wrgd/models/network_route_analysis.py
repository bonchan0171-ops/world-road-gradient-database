"""Combined network route summary and statistics model."""

from dataclasses import dataclass

from .network_path_summary import NetworkPathSummary
from .road_statistics import RoadStatistics


@dataclass(slots=True)
class NetworkRouteAnalysis:
    """Summary and DEM-backed statistics for a network route."""

    summary: NetworkPathSummary
    statistics: RoadStatistics
