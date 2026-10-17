"""Find and analyze an OSM route, then export GeoJSON and optional JSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from wrgd.app import analyze_network_route
from wrgd.io import write_network_route_geojson, write_network_route_json
from wrgd.io.dem_loader import DEMLoader
from wrgd.network import OSMReader


def parse_args() -> argparse.Namespace:
    """Parse required network analysis inputs and output paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--network",
        type=Path,
        required=True,
        help="OSM XML road network file",
    )
    parser.add_argument(
        "--dem",
        type=Path,
        required=True,
        help="DEM GeoTIFF used for elevation and road statistics",
    )
    parser.add_argument(
        "--start-node",
        type=int,
        required=True,
        help="OSM node ID where the route starts",
    )
    parser.add_argument(
        "--end-node",
        type=int,
        required=True,
        help="OSM node ID where the route ends",
    )
    parser.add_argument(
        "--avoid-bridges",
        action="store_true",
        help="Exclude bridge edges from the route",
    )
    parser.add_argument(
        "--avoid-tunnels",
        action="store_true",
        help="Exclude tunnel edges from the route",
    )
    parser.add_argument(
        "--road-types",
        nargs="+",
        choices=sorted(OSMReader.SUPPORTED_HIGHWAYS),
        metavar="TYPE",
        help="Restrict the route to these OSM highway types",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output GeoJSON path",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional full-analysis JSON output path",
    )
    return parser.parse_args()


def main() -> None:
    """Analyze and export one shortest route from an OSM network."""
    args = parse_args()
    network = OSMReader(args.network).read()
    route = network.shortest_route(
        args.start_node,
        args.end_node,
        avoid_bridges=args.avoid_bridges,
        avoid_tunnels=args.avoid_tunnels,
        allowed_road_types=args.road_types,
    )

    if route is None:
        raise ValueError("No route was found between the specified nodes.")

    dem_loader = DEMLoader(args.dem)
    dem_loader.load()
    analysis = analyze_network_route(network, route, dem_loader)
    summary = analysis.summary
    statistics = analysis.statistics

    print("Route summary:")
    print(f"Distance: {summary.distance:.1f} m")
    print(f"Edges: {summary.edge_count}")
    print(f"Bridges: {summary.bridge_count}")
    print(f"Tunnels: {summary.tunnel_count}")
    print("Road types:")
    for road_type, count in sorted(summary.road_type_counts.items()):
        print(f"  {road_type}: {count}")

    average_radius = (
        "n/a"
        if statistics.average_radius is None
        else f"{statistics.average_radius:.1f} m"
    )
    print("Road statistics:")
    print(f"Distance: {statistics.distance:.1f} m")
    print(f"Ascent: {statistics.ascent:.1f} m")
    print(f"Descent: {statistics.descent:.1f} m")
    print(
        f"Elevation: {statistics.lowest_elevation:.1f}-"
        f"{statistics.highest_elevation:.1f} m"
    )
    print(
        f"Gradient: max {statistics.max_gradient:.2f}%, "
        f"average {statistics.average_gradient:.2f}%"
    )
    print(
        f"Curvature: average {statistics.average_curvature:.6f}, "
        f"maximum {statistics.max_curvature:.6f}"
    )
    print(f"Radius: minimum {statistics.min_radius:.1f} m, average {average_radius}")
    print(f"Sharp curves: {statistics.sharp_curve_count}")

    if args.json:
        write_network_route_json(analysis, args.json)
        print(f"JSON: {args.json}")

    write_network_route_geojson(network, route, analysis, args.output)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
