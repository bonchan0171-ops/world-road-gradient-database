"""Tests for WRGD CLI."""

import unittest.mock as mock
from pathlib import Path
from unittest.mock import patch

import pytest

from wrgd.cli import main
from wrgd.models.coordinate import Coordinate
from wrgd.models.network_path import NetworkPath
from wrgd.models.road_statistics import RoadStatistics


def test_cli() -> None:
    """CLI should parse arguments."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "sample.gpx",
            "--dem",
            "sample.tif",
        ],
    ):
        main()


def test_cli_reads_network(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI should load and report an OSM road network."""

    with patch("sys.argv", ["wrgd", "--network", "roads.osm"]):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("wrgd.cli.OSMReader") as mock_reader_class,
        ):
            mock_network = mock_reader_class.return_value.read.return_value
            mock_network.node_count.return_value = 12
            mock_network.edge_count.return_value = 20

            main()

            mock_reader_class.assert_called_once_with(Path("roads.osm"))
            mock_network.apply_elevation.assert_called_once_with()

    output = capsys.readouterr().out
    assert "Nodes: 12" in output
    assert "Edges: 20" in output


def test_cli_reads_network_with_dem() -> None:
    """CLI should apply a DEM when --network and --dem are provided."""

    with patch(
        "sys.argv",
        ["wrgd", "--network", "roads.osm", "--dem", "elevation.tif"],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("wrgd.cli.OSMReader") as mock_reader_class,
            patch("wrgd.cli.DEMLoader") as mock_dem_class,
        ):
            mock_network = mock_reader_class.return_value.read.return_value

            main()

            mock_dem_class.assert_called_once_with(Path("elevation.tif"))
            mock_dem_class.return_value.load.assert_called_once_with()
            mock_network.apply_elevation.assert_called_once_with(
                mock_dem_class.return_value
            )


def test_cli_exports_network_route_geojson(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI should export a NetworkPath as GeoJSON."""

    output = Path("route.geojson")
    path = NetworkPath(node_ids=[100, 200], edge_ids=[10], distance=123.0)
    coordinates = [Coordinate(latitude=35.0, longitude=139.0)]

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--network",
            "roads.osm.xml",
            "--start-node",
            "100",
            "--end-node",
            "200",
            "--output",
            str(output),
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("wrgd.cli.OSMReader") as mock_reader_class,
            patch("wrgd.cli.GeoJSONWriter") as mock_writer_class,
        ):
            mock_network = mock_reader_class.return_value.read.return_value
            mock_network.shortest_route.return_value = path
            mock_network.path_coordinates.return_value = coordinates

            main()

            mock_network.shortest_route.assert_called_once_with(100, 200)
            mock_network.path_coordinates.assert_called_once_with(path)
            mock_writer_class.assert_called_once_with(output)
            mock_writer_class.return_value.write.assert_called_once_with(
                coordinates,
                properties={
                    "node_ids": [100, 200],
                    "edge_ids": [10],
                    "distance_m": 123.0,
                },
            )

    assert "WRGD Network Route" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (
            ["--start-node", "100"],
            "--start-node and --end-node must be specified together",
        ),
        (
            ["--end-node", "200"],
            "--start-node and --end-node must be specified together",
        ),
        (
            ["--start-node", "100", "--end-node", "200"],
            "--output is required for Network Route mode",
        ),
        (
            [
                "--start-node",
                "100",
                "--end-node",
                "200",
                "--output",
                "route.geojson",
                "--csv",
                "route.csv",
            ],
            "--csv is not supported in Network Route mode",
        ),
        (
            [
                "--start-node",
                "100",
                "--end-node",
                "200",
                "--output",
                "route.geojson",
                "--json",
                "route.json",
            ],
            "--json is not supported in Network Route mode",
        ),
    ],
)
def test_cli_rejects_invalid_network_route_options(
    extra_args: list[str],
    message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI should reject incomplete or incompatible Network Route options."""

    with patch("sys.argv", ["wrgd", "--network", "roads.osm.xml", *extra_args]):
        main()

    assert message in capsys.readouterr().out


def test_cli_reports_unknown_network_route_node(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI should report an unknown Network Route node."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--network",
            "roads.osm.xml",
            "--start-node",
            "100",
            "--end-node",
            "200",
            "--output",
            "route.geojson",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("wrgd.cli.OSMReader") as mock_reader_class,
        ):
            mock_network = mock_reader_class.return_value.read.return_value
            mock_network.shortest_route.side_effect = KeyError(100)

            main()

    assert "Error: 100" in capsys.readouterr().out


def test_cli_reports_unreachable_network_route(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI should report an unreachable Network Route."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--network",
            "roads.osm.xml",
            "--start-node",
            "100",
            "--end-node",
            "200",
            "--output",
            "route.geojson",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("wrgd.cli.OSMReader") as mock_reader_class,
        ):
            mock_network = mock_reader_class.return_value.read.return_value
            mock_network.shortest_route.return_value = None

            main()

    assert "no route found" in capsys.readouterr().out


def test_cli_rejects_route_and_network_together() -> None:
    """CLI should reject mutually exclusive route and network inputs."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "sample.gpx",
            "--network",
            "roads.osm",
            "--dem",
            "sample.tif",
        ],
    ):
        with pytest.raises(SystemExit):
            main()


def test_cli_without_input_preserves_argparse_error() -> None:
    """CLI should keep rejecting invocations without an input."""

    with patch("sys.argv", ["wrgd"]):
        with pytest.raises(SystemExit):
            main()


def test_cli_writes_csv_when_option_is_given() -> None:
    """CLI should export road statistics to CSV when --csv is provided."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
            "--csv",
            "output.csv",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader") as mock_dem_loader,
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.write_csv") as mock_write_csv,
        ):
            mock_dem_loader.return_value
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )

            main()

            mock_write_csv.assert_called_once_with(
                mock_segment.statistics.return_value,
                Path("output.csv"),
                difficulty=mock.ANY,
                score=mock.ANY,
            )


def test_cli_writes_json_when_option_is_given() -> None:
    """CLI should export road statistics to JSON when --json is provided."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
            "--json",
            "output.json",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader") as mock_dem_loader,
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.write_json") as mock_write_json,
        ):
            mock_dem_loader.return_value
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )

            main()

            mock_write_json.assert_called_once_with(
                mock_segment.statistics.return_value,
                Path("output.json"),
                difficulty=mock.ANY,
                score=mock.ANY,
            )


def test_cli_writes_png_when_output_option_is_given() -> None:
    """CLI should save an elevation profile image when --output is provided."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
            "--output",
            "output.png",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader") as mock_dem_loader,
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.ElevationProfile") as mock_profile_class,
        ):
            mock_dem_loader.return_value
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )
            mock_profile = mock_profile_class.return_value

            main()

            mock_profile_class.assert_called_once_with(mock_segment)
            mock_profile.save_image.assert_called_once_with(Path("output.png"))


def test_cli_writes_interactive_outputs_when_option_is_given(tmp_path) -> None:
    """CLI should export GeoJSON and HTML to the interactive output directory."""

    interactive_dir = tmp_path / "interactive"
    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
            "--interactive",
            str(interactive_dir),
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader") as mock_dem_loader,
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.GeoJSONWriter") as mock_writer_class,
            patch("wrgd.cli.export_leaflet_map") as mock_export_map,
        ):
            mock_dem_loader.return_value
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )

            main()

            geojson_path = interactive_dir / "segments.geojson"
            html_path = interactive_dir / "interactive_map.html"
            mock_writer_class.assert_called_once_with(geojson_path)
            mock_writer_class.return_value.write_segments.assert_called_once_with(
                mock_segment,
                difficulty=mock.ANY,
                score=mock.ANY,
            )
            mock_export_map.assert_called_once_with(
                geojson_path=str(geojson_path),
                html_path=str(html_path),
            )


def test_cli_writes_gpkg_when_option_is_given(tmp_path: Path) -> None:
    """CLI should export road segments to GeoPackage when requested."""

    gpkg_path = tmp_path / "nested" / "segments.gpkg"
    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
            "--gpkg",
            str(gpkg_path),
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader") as mock_dem_loader,
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.GeoPackageWriter") as mock_writer_class,
        ):
            mock_dem_loader.return_value
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )

            main()

            assert gpkg_path.parent.exists()
            mock_writer_class.assert_called_once_with(gpkg_path)
            mock_writer_class.return_value.write_segments.assert_called_once_with(
                mock_segment,
                difficulty=mock.ANY,
                score=mock.ANY,
            )


def test_cli_does_not_write_gpkg_without_option() -> None:
    """CLI should not create a GeoPackage unless requested."""

    with patch(
        "sys.argv",
        [
            "wrgd",
            "--route",
            "tests/data/sample.geojson",
            "--dem",
            "sample.tif",
        ],
    ):
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "wrgd.cli.load_route",
                return_value=[],
            ),
            patch("wrgd.cli.to_builder_coordinates", return_value=[]),
            patch("wrgd.cli.DEMLoader"),
            patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
            patch("wrgd.cli.GeoPackageWriter") as mock_writer_class,
        ):
            mock_segment = mock_builder.return_value.build.return_value
            mock_segment.statistics.return_value = RoadStatistics(
                distance=0.0,
                ascent=0.0,
                descent=0.0,
                highest_elevation=0.0,
                lowest_elevation=0.0,
                max_gradient=0.0,
                average_gradient=0.0,
            )

            main()

            mock_writer_class.assert_not_called()
