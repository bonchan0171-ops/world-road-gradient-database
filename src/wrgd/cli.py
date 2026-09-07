"""Command-line interface for WRGD."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import rasterio.errors

from wrgd.analysis.difficulty import calculate_difficulty
from wrgd.analysis.score import calculate_score
from wrgd.app import (
    load_route,
    print_report,
    to_builder_coordinates,
)
from wrgd.io.csv_writer import write_csv
from wrgd.io.dem_loader import DEMLoader
from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.io.json_writer import write_json
from wrgd.profile import ElevationProfile
from wrgd.road.builder import RoadSegmentBuilder
from wrgd.visualization.leaflet import export_leaflet_map


def run_map(args) -> None:
    output_path = Path(args.output)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    geojson_path = output_dir / "segments.geojson"

    coordinates = load_route(Path(args.route))
    builder_coordinates = to_builder_coordinates(coordinates)

    dem_loader = DEMLoader(Path(args.dem))
    dem_loader.load()

    road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)

    writer = GeoJSONWriter(geojson_path)
    writer.write_segments(road_segment)

    export_leaflet_map(
        geojson_path=str(geojson_path),
        html_path=str(output_path),
    )

    print("WRGD Interactive Map")
    print("====================")
    print(f"Route    : {args.route}")
    print(f"DEM      : {args.dem}")
    print(f"Segments : {len(road_segment.segments)}")
    print(f"HTML     : {output_path}")


def write_interactive_outputs(
    road_segment,
    output_dir: Path,
    difficulty,
    score: float,
) -> None:
    """Write the segment GeoJSON and interactive map to a directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    geojson_path = output_dir / "segments.geojson"
    html_path = output_dir / "interactive_map.html"

    GeoJSONWriter(geojson_path).write_segments(
        road_segment,
        difficulty=difficulty,
        score=score,
    )
    export_leaflet_map(
        geojson_path=str(geojson_path),
        html_path=str(html_path),
    )


def main() -> None:
    """Run the WRGD command-line interface."""

    parser = argparse.ArgumentParser(
        prog="wrgd",
        description="World Road Geometry Database",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )
    analyze = subparsers.add_parser(
        "analyze",
        help="Analyze a route",
    )

    analyze.add_argument(
        "--route",
        required=True,
        help="Route file (.gpx or .geojson)",
    )

    analyze.add_argument(
        "--dem",
        required=True,
        help="DEM file (.tif)",
    )

    analyze.add_argument(
        "--csv",
        help="Optional output CSV path for road statistics",
    )

    analyze.add_argument(
        "--json",
        help="Optional output JSON path for road statistics",
    )

    analyze.add_argument(
        "--output",
        help="Optional output PNG path for the elevation profile image",
    )

    analyze.add_argument(
        "--interactive",
        type=Path,
        help="Optional directory for interactive map outputs",
    )

    map_parser = subparsers.add_parser(
        "map",
        help="Generate interactive Leaflet map",
    )

    map_parser.add_argument("--route", required=True)
    map_parser.add_argument("--dem", required=True)
    map_parser.add_argument(
        "--output",
        default="output/gradient_map.html",
        help="Output HTML path",
    )

    argv = sys.argv[1:]
    if argv and argv[0].startswith("-"):
        argv = ["analyze", *argv]

    args = parser.parse_args(argv)

    if args.command == "map":
        run_map(args)
        return

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
        difficulty = calculate_difficulty(statistics)
        score = calculate_score(statistics)

        if args.csv:
            write_csv(
                statistics,
                Path(args.csv),
                difficulty=difficulty,
                score=score,
            )

        if args.json:
            write_json(
                statistics,
                Path(args.json),
                difficulty=difficulty,
                score=score,
            )

        if args.output:
            ElevationProfile(road_segment).save_image(Path(args.output))

        if args.interactive:
            write_interactive_outputs(
                road_segment,
                args.interactive,
                difficulty,
                score,
            )

        print("WRGD CLI")
        print(f"Route : {route_file}")
        print(f"DEM   : {dem_file}")
        print(f"Points: {len(coordinates)}")
        print_report(road_segment)

        print(f"Difficulty        : {difficulty.name}")
        print(f"Difficulty Level  : {difficulty.level}")
        print(f"Evaluation Score  : {score:.1f}")
    except (ValueError, RuntimeError, rasterio.errors.RasterioIOError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
