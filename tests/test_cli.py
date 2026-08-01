"""Tests for WRGD CLI."""

from pathlib import Path
from unittest.mock import patch

from wrgd.cli import main
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
            )
