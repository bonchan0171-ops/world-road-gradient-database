"""Command-line interface for WRGD."""

from __future__ import annotations

import argparse


def main() -> None:
    """Run the WRGD command-line interface."""

    parser = argparse.ArgumentParser(
        prog="wrgd",
        description="World Road Geometry Database",
    )

    parser.add_argument(
        "--route",
        required=True,
        help="Route file (.gpx or .geojson)",
    )

    parser.add_argument(
        "--dem",
        required=True,
        help="DEM file (.tif)",
    )

    args = parser.parse_args()

    print("WRGD CLI")
    print(f"Route : {args.route}")
    print(f"DEM   : {args.dem}")


if __name__ == "__main__":
    main()
