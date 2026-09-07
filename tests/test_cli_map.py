from pathlib import Path
from unittest.mock import patch

from wrgd.cli import run_map


class Args:
    route = "sample.gpx"
    dem = "sample.tif"
    output = "output/map.html"


def test_run_map_generates_html(tmp_path):
    args = Args()
    args.output = str(tmp_path / "map.html")

    with (
        patch("wrgd.cli.load_route", return_value=[]),
        patch("wrgd.cli.to_builder_coordinates", return_value=[]),
        patch("wrgd.cli.DEMLoader") as mock_dem,
        patch("wrgd.cli.RoadSegmentBuilder") as mock_builder,
        patch("wrgd.cli.GeoJSONWriter") as mock_writer,
        patch("wrgd.cli.export_leaflet_map") as mock_leaflet,
    ):
        mock_dem.return_value.load.return_value = None

        mock_segment = mock_builder.return_value.build.return_value
        mock_segment.segments = [1, 2, 3]

        run_map(args)

        mock_writer.assert_called_once()
        mock_leaflet.assert_called_once()

        geojson_path = Path(args.output).parent / "segments.geojson"

        mock_leaflet.assert_called_with(
            geojson_path=str(geojson_path),
            html_path=args.output,
        )
