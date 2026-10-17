"""GeoJSON export for analyzed network routes."""

from pathlib import Path

from wrgd.models.network_path import NetworkPath
from wrgd.models.network_route_analysis import NetworkRouteAnalysis
from wrgd.network.road_network import RoadNetwork

from .geojson_writer import GeoJSONWriter


def write_network_route_geojson(
    network: RoadNetwork,
    path: NetworkPath,
    analysis: NetworkRouteAnalysis,
    output_path: Path,
) -> None:
    """Write a network route and its summary/statistics as GeoJSON."""
    summary = analysis.summary
    statistics = analysis.statistics
    properties = {
        "node_ids": path.node_ids,
        "edge_ids": path.edge_ids,
        "distance_m": path.distance,
        "edge_count": summary.edge_count,
        "bridge_count": summary.bridge_count,
        "tunnel_count": summary.tunnel_count,
        "road_type_counts": summary.road_type_counts,
        "ascent_m": statistics.ascent,
        "descent_m": statistics.descent,
        "highest_elevation_m": statistics.highest_elevation,
        "lowest_elevation_m": statistics.lowest_elevation,
        "max_gradient_pct": statistics.max_gradient,
        "average_gradient_pct": statistics.average_gradient,
        "average_curvature_per_m": statistics.average_curvature,
        "max_curvature_per_m": statistics.max_curvature,
        "min_radius_m": statistics.min_radius,
        "average_radius_m": statistics.average_radius,
        "sharp_curve_count": statistics.sharp_curve_count,
    }
    GeoJSONWriter(output_path).write(
        network.path_coordinates(path),
        properties=properties,
    )
