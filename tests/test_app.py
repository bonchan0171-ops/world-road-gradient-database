"""Tests for application functions."""

from math import isfinite
from pathlib import Path

import pytest
from pytest import CaptureFixture

from wrgd.app import (
    analyze_network_path,
    load_route,
    plot_elevation_profile,
    print_report,
    to_builder_coordinates,
)
from wrgd.io.dem_loader import DEMLoader
from wrgd.models import Coordinate, NetworkEdge, NetworkNode, NetworkPath
from wrgd.network import RoadNetwork
from wrgd.road.segment import RoadSegment


def test_to_builder_coordinates() -> None:
    """Coordinates should convert to builder format."""

    coordinates = [
        Coordinate(latitude=35.0, longitude=135.0),
        Coordinate(latitude=35.1, longitude=135.1),
    ]

    result = to_builder_coordinates(coordinates)

    assert result == [
        (35.0, 135.0),
        (35.1, 135.1),
    ]


def test_analyze_network_path_returns_road_statistics() -> None:
    """NetworkPath should use the existing DEM statistics pipeline."""
    nodes = [
        NetworkNode(1, 35.7700, 139.7200, None),
        NetworkNode(2, 35.7700, 139.7210, None),
        NetworkNode(3, 35.7710, 139.7210, None),
    ]
    network = RoadNetwork()
    for node in nodes:
        network.add_node(node)

    network.add_edge(
        NetworkEdge(
            id=10,
            start_node=nodes[0],
            end_node=nodes[1],
            distance=100.0,
            average_gradient=0.0,
            road_type="residential",
            oneway=False,
            geometry=[
                Coordinate(35.7700, 139.7200),
                Coordinate(35.7700, 139.7210),
            ],
        )
    )
    network.add_edge(
        NetworkEdge(
            id=20,
            start_node=nodes[1],
            end_node=nodes[2],
            distance=100.0,
            average_gradient=0.0,
            road_type="residential",
            oneway=False,
            geometry=[
                Coordinate(35.7700, 139.7210),
                Coordinate(35.7710, 139.7210),
            ],
        )
    )

    dem_loader = DEMLoader("tests/data/sample_dem.tif")
    dem_loader.load()
    statistics = analyze_network_path(
        network,
        NetworkPath(node_ids=[1, 2, 3], edge_ids=[10, 20], distance=200.0),
        dem_loader,
    )

    assert statistics.distance > 0.0
    assert isfinite(statistics.min_radius)
    assert statistics.average_radius == pytest.approx(statistics.min_radius)


def test_load_route_unsupported_format(tmp_path: Path) -> None:
    """Unsupported route format should raise ValueError."""

    route_file = tmp_path / "route.txt"
    route_file.write_text("test")

    try:
        load_route(route_file)
    except ValueError as error:
        assert "Unsupported file format" in str(error)
    else:
        assert False, "ValueError was not raised"


def test_print_report(capsys: CaptureFixture[str]) -> None:
    """Report should be printed."""

    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
        ],
        elevations=[
            100.0,
            110.0,
        ],
        distances=[
            100.0,
        ],
        gradients=[
            10.0,
        ],
    )

    print_report(segment)

    captured = capsys.readouterr()

    assert "Road Analysis Report" in captured.out
    assert "Distance" in captured.out
    assert "Max Gradient" in captured.out


def test_plot_elevation_profile(tmp_path: Path) -> None:
    """Elevation profile image should be created."""

    segment = RoadSegment(
        coordinates=[
            (35.0, 135.0),
            (35.1, 135.1),
        ],
        elevations=[
            100.0,
            110.0,
        ],
        distances=[
            100.0,
        ],
        gradients=[
            10.0,
        ],
    )

    output = tmp_path / "profile.png"

    plot_elevation_profile(
        segment,
        output,
    )

    assert output.exists()


def test_load_route_gpx() -> None:
    """GPX route should be loaded."""

    route = Path("data/sample/sample.gpx")

    coordinates = load_route(route)

    assert len(coordinates) > 0


def test_load_route_geojson(tmp_path: Path) -> None:
    """GeoJSON route should be loaded."""

    route = tmp_path / "route.geojson"

    route.write_text(
        """
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [135.0, 35.0],
          [135.1, 35.1]
        ]
      }
    }
  ]
}
""",
        encoding="utf-8",
    )

    coordinates = load_route(route)

    assert len(coordinates) == 2
