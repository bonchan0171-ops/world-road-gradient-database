from wrgd.io.geojson_style import create_default_style


def test_create_default_style() -> None:
    style = create_default_style()

    assert style == {
        "version": 1,
        "property": "color",
        "line": {
            "width": 4,
            "opacity": 0.9,
        },
    }
