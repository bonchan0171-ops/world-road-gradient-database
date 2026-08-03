"""Minimal Python API example matching the README.

Run this from the repository root:
    python -m examples.python_api_example
"""

from __future__ import annotations

from pathlib import Path

from wrgd.app import load_route, print_report, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.profile import ElevationProfile
from wrgd.road.builder import RoadSegmentBuilder


def main() -> None:
    """Show the minimal Python workflow described in the README."""

    project_root = Path(__file__).resolve().parents[1]
    route_file = project_root / "data" / "sample" / "sample.gpx"
    dem_file = project_root / "data" / "raw" / "output_hh.tif"

    coordinates = load_route(route_file)
    builder_coordinates = to_builder_coordinates(coordinates)

    dem_loader = DEMLoader(dem_file)
    dem_loader.load()

    road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)
    profile = ElevationProfile(road_segment)

    print_report(road_segment)
    print()
    print(profile.to_dict())


if __name__ == "__main__":
    main()
