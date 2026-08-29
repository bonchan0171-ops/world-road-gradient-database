from __future__ import annotations

import json
from pathlib import Path

from .legend import build_legend


def export_leaflet_map(
    geojson_path: str,
    html_path: str,
    title: str = "WRGD Gradient Heatmap",
) -> None:
    """Export an interactive Leaflet map as a standalone HTML file."""

    geojson = json.loads(Path(geojson_path).read_text(encoding="utf-8"))
    legend = build_legend()

    legend_html = "".join(
        f'<div><span style="background:{item["color"]};"></span>'
        f'{item["label"]}</div>'
        for item in legend
    )

    geojson_json = json.dumps(geojson, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>

<link rel="stylesheet"
 href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>

<style>
html, body {{
    margin: 0;
    height: 100%;
}}

#map {{
    width: 100%;
    height: 100%;
}}

.legend {{
    background: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 0 8px rgba(0,0,0,.25);
    font: 12px sans-serif;
}}

.legend h4 {{
    margin: 0 0 8px;
    font-size: 13px;
}}

.legend div {{
    display: flex;
    align-items: center;
    margin-bottom: 4px;
}}

.legend span {{
    width: 18px;
    height: 8px;
    display: inline-block;
    margin-right: 6px;
}}
</style>
</head>

<body>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
const geojsonData = {geojson_json};

const map = L.map("map");

L.tileLayer(
    "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",
    {{
        attribution: "&copy; OpenStreetMap contributors"
    }}
).addTo(map);

const layer = L.geoJSON(geojsonData, {{
    style: feature => ({{
        color: feature.properties.color || "#00AA00",
        weight: 5,
        opacity: 0.95
    }}),

    onEachFeature: (feature, layer) => {{
        const properties = feature.properties;

        const gradient = Number(properties.gradient);

        const gradientText =
            Number.isFinite(gradient)
                ? `${{gradient >= 0 ? "+" : ""}}${{gradient.toFixed(2)}} %`
                : "N/A";

        const popup = `
            <strong>WRGD Segment</strong><br>
            <br>
            Segment ID : ${{properties.segment_id}}<br>
            Distance : ${{Number(properties.distance).toFixed(2)}} m<br>
            Gradient : ${{gradientText}}
        `;

        layer.bindPopup(popup);
    }}
}}).addTo(map);

if (layer.getBounds().isValid()) {{
    map.fitBounds(layer.getBounds());
}}

const legend = L.control({{
    position: "bottomright"
}});

legend.onAdd = function() {{
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML =
        "<h4>Gradient</h4>" +
        {json.dumps(legend_html)};
    return div;
}};

legend.addTo(map);
</script>
</body>
</html>
"""

    Path(html_path).write_text(html, encoding="utf-8")
