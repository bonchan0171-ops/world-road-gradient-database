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
from wrgd.io.gpkg_writer import GeoPackageWriter
from wrgd.io.json_writer import write_json
from wrgd.network import OSMReader
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


def run_network(args: argparse.Namespace) -> None:
    """Load an OSM road network and optionally apply DEM elevations."""
    network_file = Path(args.network)

    has_start_node = args.start_node is not None
    has_end_node = args.end_node is not None

    if has_start_node != has_end_node:
        print("Error: --start-node and --end-node must be specified together.")
        return

    route_mode = has_start_node and has_end_node
    if route_mode and args.output is None:
        print("Error: --output is required for Network Route mode.")
        return

    if route_mode and args.csv:
        print("Error: --csv is not supported in Network Route mode.")
        return

    if route_mode and args.json:
        print("Error: --json is not supported in Network Route mode.")
        return

    if not network_file.exists():
        print(f"Error: network file not found: {network_file}")
        return

    try:
        network = OSMReader(network_file).read()

        if args.dem:
            dem_file = Path(args.dem)
            if not dem_file.exists():
                print(f"Error: DEM file not found: {dem_file}")
                return

            dem_loader = DEMLoader(dem_file)
            dem_loader.load()
            network.apply_elevation(dem_loader)
        else:
            network.apply_elevation()

        if route_mode:
            path = network.shortest_route(args.start_node, args.end_node)
            if path is None:
                print("Error: no route found between the specified nodes.")
                return

            coordinates = network.path_coordinates(path)
            GeoJSONWriter(Path(args.output)).write(
                coordinates,
                properties={
                    "node_ids": path.node_ids,
                    "edge_ids": path.edge_ids,
                    "distance_m": path.distance,
                },
            )
            print("WRGD Network Route")
            print(f"Network: {network_file}")
            print(f"Start  : {args.start_node}")
            print(f"End    : {args.end_node}")
            print(f"Output : {args.output}")
            return

        print("WRGD Road Network")
        print(f"Network: {network_file}")
        print(f"Nodes: {network.node_count()}")
        print(f"Edges: {network.edge_count()}")
    except (
        KeyError,
        ValueError,
        RuntimeError,
        rasterio.errors.RasterioIOError,
    ) as error:
        print(f"Error: {error}")


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

    input_group = analyze.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--route",
        help="Route file (.gpx or .geojson)",
    )
    input_group.add_argument(
        "--network",
        help="OSM road network file (.osm)",
    )

    analyze.add_argument(
        "--start-node",
        type=int,
        help="Start node ID for Network Route mode",
    )

    analyze.add_argument(
        "--end-node",
        type=int,
        help="End node ID for Network Route mode",
    )

    analyze.add_argument(
        "--dem",
        help="DEM file (.tif), required with --route",
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

    analyze.add_argument(
        "--gpkg",
        type=Path,
        help="Optional output GeoPackage path for road segments",
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

    if args.network:
        run_network(args)
        return

    if args.dem is None:
        parser.error("--dem is required with --route")

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

        if args.gpkg:
            args.gpkg.parent.mkdir(parents=True, exist_ok=True)
            GeoPackageWriter(args.gpkg).write_segments(
                road_segment,
                difficulty=difficulty,
                score=int(score),
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
