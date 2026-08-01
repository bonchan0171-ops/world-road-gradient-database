"""Command-line interface for WRGD."""

from __future__ import annotations

import argparse
from pathlib import Path

import rasterio.errors

from wrgd.app import (
    load_route,
    print_report,
    to_builder_coordinates,
)
from wrgd.io.csv_writer import write_csv
from wrgd.io.dem_loader import DEMLoader
from wrgd.io.json_writer import write_json
from wrgd.road.builder import RoadSegmentBuilder


def main() -> None:
    """Run the WRGD command-line interface."""

    parser = argparse.ArgumentParser(
        prog="wrgd",
        description="World Road Geometry Database",
    )

    parser.add_argument(
        "--route",
        required=True,
        help="Route file (.gpx or .geojson)",
    )

    parser.add_argument(
        "--dem",
        required=True,
        help="DEM file (.tif)",
    )

    parser.add_argument(
        "--csv",
        help="Optional output CSV path for road statistics",
    )

    parser.add_argument(
        "--json",
        help="Optional output JSON path for road statistics",
    )

    args = parser.parse_args()

    route_file = Path(args.route)
    dem_file = Path(args.dem)

    if not route_file.exists():
        print(f"Error: route file not found: {route_file}")
        return

    if route_file.suffix.lower() not in {".gpx", ".geojson"}:
        print(
            "Error: unsupported route format: "
            f"{route_file.suffix or 'no extension'}; supported formats: GPX, GeoJSON"
        )
        return

    if not dem_file.exists():
        print(f"Error: DEM file not found: {dem_file}")
        return

    try:
        coordinates = load_route(route_file)
        builder_coordinates = to_builder_coordinates(coordinates)

        dem_loader = DEMLoader(dem_file)
        dem_loader.load()

        road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)
        statistics = road_segment.statistics()

        if args.csv:
            write_csv(statistics, Path(args.csv))

        if args.json:
            write_json(statistics, Path(args.json))

        print("WRGD CLI")
        print(f"Route : {route_file}")
        print(f"DEM   : {dem_file}")
        print(f"Points: {len(coordinates)}")
        print_report(road_segment)
    except (ValueError, RuntimeError, rasterio.errors.RasterioIOError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
