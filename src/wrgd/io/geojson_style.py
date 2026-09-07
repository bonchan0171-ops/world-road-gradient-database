"""Default style definition for GeoJSON visualization."""

from __future__ import annotations


def create_default_style() -> dict[str, object]:
    """Return the default style for GeoJSON road features."""

    return {
        "version": 1,
        "property": "color",
        "line": {
            "width": 4,
            "opacity": 0.9,
        },
    }
