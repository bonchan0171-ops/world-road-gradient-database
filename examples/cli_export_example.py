"""CLI export example that matches the README command-line workflow.

Run this from the repository root:
    python -m examples.cli_export_example
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def main() -> None:
    """Invoke the installed wrgd CLI with CSV, JSON, and PNG exports."""

    project_root = Path(__file__).resolve().parents[1]

    route_file = project_root / "data" / "sample" / "sample.gpx"
    dem_file = project_root / "data" / "raw" / "output_hh.tif"
    csv_file = project_root / "output" / "road_statistics.csv"
    json_file = project_root / "output" / "road_statistics.json"
    png_file = project_root / "output" / "elevation_profile_cli.png"

    command = [
        "wrgd",
        "--route",
        str(route_file),
        "--dem",
        str(dem_file),
        "--csv",
        str(csv_file),
        "--json",
        str(json_file),
        "--output",
        str(png_file),
    ]

    completed = subprocess.run(command, check=False)

    if completed.returncode != 0:
        raise SystemExit(completed.returncode)

    print("Exported files:")
    print(csv_file)
    print(json_file)
    print(png_file)


if __name__ == "__main__":
    main()
