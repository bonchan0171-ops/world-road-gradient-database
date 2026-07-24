"""WRGD demonstration application."""

from pathlib import Path

import matplotlib.pyplot as plt

from src.io.dem_loader import DEMLoader
from src.io.geojson_reader import GeoJSONReader
from src.io.gpx_reader import GPXReader
from src.models import Coordinate
from src.road.builder import RoadSegmentBuilder
from src.road.segment import RoadSegment


def to_builder_coordinates(
    coordinates: list[Coordinate],
) -> list[tuple[float, float]]:
    """
    Convert Coordinate objects to RoadSegmentBuilder format.
    """
    return [(point.latitude, point.longitude) for point in coordinates]


def load_route(path: Path) -> list[Coordinate]:
    """Load coordinates from a GPX or GeoJSON file."""

    suffix = path.suffix.lower()

    if suffix == ".gpx":
        return GPXReader(path).read()

    if suffix == ".geojson":
        return GeoJSONReader(path).read()

    raise ValueError(f"Unsupported file format: {suffix}")


def plot_elevation_profile(
    road_segment: RoadSegment,
    output_path: Path,
) -> None:
    """Generate an elevation profile image."""

    distances = [0.0]

    for distance in road_segment.distances:
        distances.append(distances[-1] + distance)

    plt.figure(figsize=(10, 4))

    plt.plot(
        distances,
        road_segment.elevations,
        linewidth=2,
    )

    plt.title("WRGD Elevation Profile")
    plt.xlabel("Distance (m)")
    plt.ylabel("Elevation (m)")
    plt.grid(True)

    # ← この1行を追加
    plt.tight_layout()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(output_path, dpi=150)
    plt.close()


def print_report(road_segment: RoadSegment) -> None:
    """Print a road analysis report."""

    print()
    print("=" * 40)
    print(" Road Analysis Report")
    print("=" * 40)

    print(f"Distance           : {road_segment.total_distance():8.1f} m")
    print(f"Total Ascent       : {road_segment.total_ascent():8.1f} m")
    print(f"Total Descent      : {road_segment.total_descent():8.1f} m")

    print()

    print(f"Highest Elevation  : {road_segment.highest_elevation():8.1f} m")
    print(f"Lowest Elevation   : {road_segment.lowest_elevation():8.1f} m")

    print()

    print(f"Max Gradient       : {road_segment.max_gradient():8.2f} %")
    print(f"Average Gradient   : {road_segment.average_gradient():8.2f} %")


def main() -> None:
    """Run the WRGD demo."""

    print("=" * 40)
    print(" WRGD Road Analysis Report")
    print("=" * 40)

    project_root = Path(__file__).resolve().parents[1]

    print(f"Project : {project_root}")

    route_file = project_root / "data" / "sample" / "sample.gpx"

    coordinates = load_route(route_file)

    print(f"Loaded {len(coordinates)} points")

    builder_coordinates = to_builder_coordinates(coordinates)

    print(f"Builder coordinates : {len(builder_coordinates)}")

    dem_file = project_root / "data" / "raw" / "output_hh.tif"

    dem_loader = DEMLoader(dem_file)

    dem_loader.load()

    builder = RoadSegmentBuilder(dem_loader)

    road_segment = builder.build(builder_coordinates)

    print_report(road_segment)

    output_file = project_root / "output" / "elevation_profile.png"

    plot_elevation_profile(
        road_segment,
        output_file,
    )

    print()
    print("Elevation profile saved to:")
    print(output_file)


if __name__ == "__main__":
    main()
