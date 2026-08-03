"""Quick-start example that matches the README workflow.

Run this from the repository root:
    python -m examples.quickstart
"""

from __future__ import annotations

from pathlib import Path

from wrgd.app import (
    load_route,
    plot_elevation_profile,
    print_report,
    to_builder_coordinates,
)
from wrgd.io.dem_loader import DEMLoader
from wrgd.road.builder import RoadSegmentBuilder


def main() -> None:
    """Load the sample route and DEM, then print the report."""

    project_root = Path(__file__).resolve().parents[1]

    route_file = project_root / "data" / "sample" / "sample.gpx"
    dem_file = project_root / "data" / "raw" / "output_hh.tif"
    output_file = project_root / "output" / "elevation_profile.png"

    coordinates = load_route(route_file)
    builder_coordinates = to_builder_coordinates(coordinates)

    dem_loader = DEMLoader(dem_file)
    dem_loader.load()

    road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)

    print("Loaded route points:", len(coordinates))
    print_report(road_segment)

    plot_elevation_profile(road_segment, output_file)
    print()
    print("Elevation profile saved to:")
    print(output_file)


if __name__ == "__main__":
    main()
