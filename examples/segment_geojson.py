"""Export road segments as GeoJSON Features."""

from pathlib import Path

from wrgd.app import load_route, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.road.builder import RoadSegmentBuilder


def main() -> None:
    route = Path("data/sample/sample.gpx")
    dem = Path("data/raw/output_hh.tif")
    output = Path("output/segments.geojson")

    coordinates = load_route(route)
    builder_coords = to_builder_coordinates(coordinates)

    loader = DEMLoader(dem)
    loader.load()

    segment = RoadSegmentBuilder(loader).build(builder_coords)

    GeoJSONWriter(output).write_segments(
        coordinates=coordinates,
        gradients=segment.gradients,
        distances=segment.distances,
    )

    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
