"""Tests for WRGD CLI."""

from unittest.mock import patch

from wrgd.cli import main


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
