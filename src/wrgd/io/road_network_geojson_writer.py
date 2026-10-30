"""GeoJSON export for complete road networks."""

from __future__ import annotations

import json
import math
from pathlib import Path

from wrgd.models.network_edge import NetworkEdge
from wrgd.network.road_network import RoadNetwork


def _validate_edge_geometry(edge: NetworkEdge) -> None:
    if len(edge.geometry) < 2:
        raise ValueError(f"Edge {edge.id} geometry must contain at least two points.")

    for index, coordinate in enumerate(edge.geometry):
        latitude = coordinate.latitude
        longitude = coordinate.longitude
        if (
            not isinstance(latitude, (int, float))
            or not isinstance(longitude, (int, float))
            or not math.isfinite(latitude)
            or not math.isfinite(longitude)
            or not -90 <= latitude <= 90
            or not -180 <= longitude <= 180
        ):
            raise ValueError(
                f"Edge {edge.id} has an invalid coordinate at index {index}."
            )


def write_road_network_geojson(
    network: RoadNetwork,
    output_path: str | Path,
) -> None:
    """Write every network edge as a LineString Feature."""
    features = []

    for edge in sorted(network.edges.values(), key=lambda item: item.id):
        _validate_edge_geometry(edge)
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [coordinate.longitude, coordinate.latitude]
                        for coordinate in edge.geometry
                    ],
                },
                "properties": {
                    "edge_id": edge.id,
                    "start_node_id": edge.start_node.id,
                    "end_node_id": edge.end_node.id,
                    "distance_m": edge.distance,
                    "road_type": edge.road_type,
                    "oneway": edge.oneway,
                    "bridge": edge.bridge,
                    "tunnel": edge.tunnel,
                },
            }
        )

    data = {"type": "FeatureCollection", "features": features}
    with Path(output_path).open("w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)
        output_file.write("\n")
