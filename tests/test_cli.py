"""Tests for WRGD CLI."""

import unittest.mock as mock
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
