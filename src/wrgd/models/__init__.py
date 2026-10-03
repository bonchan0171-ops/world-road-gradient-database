"""
WRGD data models.
"""

from .coordinate import Coordinate
from .difficulty import DifficultyLevel
from .network_edge import NetworkEdge
from .network_node import NetworkNode
from .network_path import NetworkPath
from .network_route_analysis import NetworkRouteAnalysis
from .road_statistics import RoadStatistics

__all__ = [
    "Coordinate",
    "DifficultyLevel",
    "NetworkEdge",
    "NetworkNode",
    "NetworkPath",
    "NetworkRouteAnalysis",
    "RoadStatistics",
]
