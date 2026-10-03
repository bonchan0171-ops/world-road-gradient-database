"""Export a shortest OSM network route as GeoJSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.network import OSMReader, summarize_network_path


def parse_args() -> argparse.Namespace:
    """Parse the OSM input, node IDs, and GeoJSON output path."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", type=Path, required=True)
    parser.add_argument("--start-node", type=int, required=True)
    parser.add_argument("--end-node", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    """Find and export one shortest route from an OSM network."""
    args = parse_args()
    network = OSMReader(args.network).read()
    route = network.shortest_route(args.start_node, args.end_node)

    if route is None:
        raise ValueError("No route was found between the specified nodes.")

    summary = summarize_network_path(network, route)
    print(f"Distance: {summary.distance:.1f} m")
    print(f"Edges: {summary.edge_count}")
    print(f"Bridges: {summary.bridge_count}")
    print(f"Tunnels: {summary.tunnel_count}")
    print("Road types:")
    for road_type, count in sorted(summary.road_type_counts.items()):
        print(f"  {road_type}: {count}")

    coordinates = network.path_coordinates(route)
    GeoJSONWriter(args.output).write(coordinates)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
