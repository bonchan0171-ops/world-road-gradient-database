import json
from pathlib import Path

import pytest

from wrgd.io.road_network_geojson_writer import write_road_network_geojson
from wrgd.models.coordinate import Coordinate
from wrgd.models.network_edge import NetworkEdge
from wrgd.models.network_node import NetworkNode
from wrgd.network import RoadNetwork


def _edge(
    edge_id: int,
    start_node: NetworkNode,
    end_node: NetworkNode,
    geometry: list[Coordinate],
) -> NetworkEdge:
    return NetworkEdge(
        id=edge_id,
        start_node=start_node,
        end_node=end_node,
        distance=float(edge_id * 10),
        average_gradient=0.0,
        road_type=f"road-{edge_id}",
        oneway=edge_id % 2 == 0,
        geometry=geometry,
        bridge=edge_id % 3 == 0,
        tunnel=edge_id % 4 == 0,
    )


def test_write_road_network_geojson(tmp_path: Path) -> None:
    output = tmp_path / "network.geojson"
    start = NetworkNode(1, 35.0, 139.0, None)
    middle = NetworkNode(2, 35.1, 139.1, None)
    end = NetworkNode(3, 35.2, 139.2, None)
    network = RoadNetwork()
    network.add_edge(
        _edge(
            20,
            middle,
            end,
            [Coordinate(35.1, 139.1), Coordinate(35.2, 139.2)],
        )
    )
    network.add_edge(
        _edge(
            10,
            start,
            middle,
            [
                Coordinate(35.0, 139.0),
                Coordinate(35.05, 139.05),
                Coordinate(35.1, 139.1),
            ],
        )
    )

    write_road_network_geojson(network, output)

    text = output.read_text(encoding="utf-8")
    data = json.loads(text)
    assert text.endswith("\n")
    assert data["type"] == "FeatureCollection"
    assert [feature["properties"]["edge_id"] for feature in data["features"]] == [
        10,
        20,
    ]
    assert data["features"][0] == {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [139.0, 35.0],
                [139.05, 35.05],
                [139.1, 35.1],
            ],
        },
        "properties": {
            "edge_id": 10,
            "start_node_id": 1,
            "end_node_id": 2,
            "distance_m": 100.0,
            "road_type": "road-10",
            "oneway": True,
            "bridge": False,
            "tunnel": False,
        },
    }
    assert data["features"][1]["properties"] == {
        "edge_id": 20,
        "start_node_id": 2,
        "end_node_id": 3,
        "distance_m": 200.0,
        "road_type": "road-20",
        "oneway": True,
        "bridge": False,
        "tunnel": True,
    }


def test_write_road_network_geojson_empty_network(tmp_path: Path) -> None:
    output = tmp_path / "empty.geojson"

    write_road_network_geojson(RoadNetwork(), output)

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "type": "FeatureCollection",
        "features": [],
    }


def test_write_road_network_geojson_rejects_short_geometry(
    tmp_path: Path,
) -> None:
    node = NetworkNode(1, 35.0, 139.0, None)
    network = RoadNetwork()
    network.add_edge(_edge(42, node, node, [Coordinate(35.0, 139.0)]))

    with pytest.raises(ValueError, match="Edge 42"):
        write_road_network_geojson(network, tmp_path / "invalid.geojson")


@pytest.mark.parametrize(
    "coordinate",
    [
        Coordinate(float("nan"), 139.0),
        Coordinate(35.0, float("inf")),
        Coordinate(91.0, 139.0),
        Coordinate(35.0, 181.0),
    ],
)
def test_write_road_network_geojson_rejects_invalid_coordinates(
    tmp_path: Path,
    coordinate: Coordinate,
) -> None:
    start = NetworkNode(1, 35.0, 139.0, None)
    end = NetworkNode(2, 36.0, 140.0, None)
    network = RoadNetwork()
    network.add_edge(_edge(43, start, end, [coordinate, Coordinate(36.0, 140.0)]))

    with pytest.raises(ValueError, match="Edge 43"):
        write_road_network_geojson(network, tmp_path / "invalid.geojson")
