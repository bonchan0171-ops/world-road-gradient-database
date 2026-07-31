"""WRGD demonstration application."""

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
    """Run the WRGD demo."""

    print("=" * 40)
    print(" WRGD Road Analysis Report")
    print("=" * 40)

    project_root = Path(__file__).resolve().parents[1]

    print(f"Project : {project_root}")

    route_file = project_root / "data" / "sample" / "sample.gpx"

    coordinates = load_route(route_file)

    print(f"Loaded {len(coordinates)} points")

    builder_coordinates = to_builder_coordinates(coordinates)

    print(f"Builder coordinates : {len(builder_coordinates)}")

    dem_file = project_root / "data" / "raw" / "output_hh.tif"

    dem_loader = DEMLoader(dem_file)

    dem_loader.load()

    builder = RoadSegmentBuilder(dem_loader)

    road_segment = builder.build(builder_coordinates)

    print_report(road_segment)

    output_file = project_root / "output" / "elevation_profile.png"

    plot_elevation_profile(
        road_segment,
        output_file,
    )

    print()
    print("Elevation profile saved to:")
    print(output_file)


if __name__ == "__main__":
    main()
