import json

from wrgd.visualization.leaflet import export_leaflet_map


def test_export_leaflet_map(tmp_path):
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [139.72, 35.77],
                        [139.721, 35.7705],
                    ],
                },
                "properties": {
                    "segment_id": 0,
                    "distance": 105.97,
                    "gradient": 1.25,
                    "color": "#19E600",
                },
            }
        ],
    }

    geojson_path = tmp_path / "segments.geojson"
    html_path = tmp_path / "gradient_map.html"

    geojson_path.write_text(
        json.dumps(geojson),
        encoding="utf-8",
    )

    export_leaflet_map(
        geojson_path=str(geojson_path),
        html_path=str(html_path),
    )

    assert html_path.exists()

    html = html_path.read_text(encoding="utf-8")

    assert "WRGD Gradient Heatmap" in html
    assert "const geojsonData =" in html
    assert '"segment_id": 0' in html
    assert "#19E600" in html
    assert "WRGD Segment" in html
    assert "bindPopup" in html
    assert 'fetch("segments.geojson")' not in html
