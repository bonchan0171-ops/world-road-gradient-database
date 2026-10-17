import json
from pathlib import Path

from wrgd.io import write_network_route_geojson
from wrgd.models.coordinate import Coordinate
from wrgd.models.network_edge import NetworkEdge
from wrgd.models.network_node import NetworkNode
from wrgd.models.network_path import NetworkPath
from wrgd.models.network_path_summary import NetworkPathSummary
from wrgd.models.network_route_analysis import NetworkRouteAnalysis
from wrgd.models.road_statistics import RoadStatistics
from wrgd.network import RoadNetwork


def test_write_network_route_geojson(tmp_path: Path) -> None:
    output = tmp_path / "route.geojson"
    start = NetworkNode(1, 35.0, 139.0, 100.0)
    end = NetworkNode(2, 35.1, 139.1, 110.0)
    network = RoadNetwork()
    network.add_node(start)
    network.add_node(end)
    network.add_edge(
        NetworkEdge(
            id=10,
            start_node=start,
            end_node=end,
            distance=300.0,
            average_gradient=4.0,
            road_type="primary",
            oneway=False,
            geometry=[
                Coordinate(35.0, 139.0),
                Coordinate(35.1, 139.1),
            ],
        )
    )
    path = NetworkPath(node_ids=[1, 2], edge_ids=[10], distance=321.5)
    analysis = NetworkRouteAnalysis(
        summary=NetworkPathSummary(
            distance=300.0,
            edge_count=1,
            bridge_count=1,
            tunnel_count=0,
            road_type_counts={"primary": 1},
        ),
        statistics=RoadStatistics(
            distance=300.0,
            ascent=10.0,
            descent=2.0,
            highest_elevation=110.0,
            lowest_elevation=100.0,
            max_gradient=8.0,
            average_gradient=4.0,
            average_curvature=0.01,
            max_curvature=0.02,
            min_radius=50.0,
            average_radius=None,
            sharp_curve_count=2,
        ),
    )

    write_network_route_geojson(network, path, analysis, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    feature = data["features"][0]
    assert data["type"] == "FeatureCollection"
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "LineString"
    assert feature["geometry"]["coordinates"] == [[139.0, 35.0], [139.1, 35.1]]
    assert feature["properties"] == {
        "node_ids": [1, 2],
        "edge_ids": [10],
        "distance_m": 321.5,
        "edge_count": 1,
        "bridge_count": 1,
        "tunnel_count": 0,
        "road_type_counts": {"primary": 1},
        "ascent_m": 10.0,
        "descent_m": 2.0,
        "highest_elevation_m": 110.0,
        "lowest_elevation_m": 100.0,
        "max_gradient_pct": 8.0,
        "average_gradient_pct": 4.0,
        "average_curvature_per_m": 0.01,
        "max_curvature_per_m": 0.02,
        "min_radius_m": 50.0,
        "average_radius_m": None,
        "sharp_curve_count": 2,
    }
