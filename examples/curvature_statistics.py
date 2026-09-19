"""Display curvature statistics for the sample route."""

from __future__ import annotations

from pathlib import Path

from wrgd.analysis.statistics import calculate_statistics
from wrgd.app import load_route, to_builder_coordinates
from wrgd.geometry.curvature import analyze_curvature
from wrgd.io.dem_loader import DEMLoader
from wrgd.profile import ElevationProfile
from wrgd.road.builder import RoadSegmentBuilder


def main() -> None:
    """Analyze the sample route's horizontal curvature."""
    project_root = Path(__file__).resolve().parents[1]
    route_file = project_root / "data" / "sample" / "sample.gpx"
    dem_file = project_root / "data" / "raw" / "output_hh.tif"

    coordinates = load_route(route_file)
    dem_loader = DEMLoader(dem_file)
    dem_loader.load()
    road_segment = RoadSegmentBuilder(dem_loader).build(
        to_builder_coordinates(coordinates)
    )

    results = analyze_curvature(road_segment.coordinates)
    statistics = calculate_statistics(ElevationProfile(road_segment))

    print(f"Curvature windows: {len(results)}")
    print(f"Minimum radius: {statistics.min_radius}")
    print(f"Average radius: {statistics.average_radius}")
    print(f"Sharp curve count: {statistics.sharp_curve_count}")


if __name__ == "__main__":
    main()
