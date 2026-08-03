"""Top-level package exports for WRGD."""

# 既存の公開APIを壊さずに、追加の分析用関数も上位レベルから利用できるようにします。
from wrgd.analysis.statistics import calculate_statistics
from wrgd.io.dem_loader import DEMLoader
from wrgd.models import Coordinate, RoadStatistics
from wrgd.road.builder import RoadSegmentBuilder
from wrgd.road.segment import RoadSegment

__all__ = [
    "Coordinate",
    "DEMLoader",
    "RoadSegment",
    "RoadSegmentBuilder",
    "RoadStatistics",
    "calculate_statistics",
]
