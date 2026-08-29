from pathlib import Path

from wrgd.visualization.leaflet import export_leaflet_map

output = Path("output")
output.mkdir(exist_ok=True)

export_leaflet_map(
    geojson_path="output/segments.geojson",
    html_path="output/gradient_map.html",
)

print("Created:", output / "gradient_map.html")
