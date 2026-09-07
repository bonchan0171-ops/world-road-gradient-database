"""Generate an interactive Leaflet map from the segment GeoJSON output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EXAMPLES_DIR.parent
DEFAULT_INPUT = PROJECT_ROOT / "output" / "segments.geojson"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "interactive_map.html"
DEFAULT_TEMPLATE = EXAMPLES_DIR / "template.html"
TEMPLATE_MARKER = "__GEOJSON_DATA__"


def generate_map(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
    template_path: Path = DEFAULT_TEMPLATE,
) -> None:
    """Embed a GeoJSON file in the Leaflet HTML template."""
    geojson = json.loads(input_path.read_text(encoding="utf-8"))
    template = template_path.read_text(encoding="utf-8")

    if TEMPLATE_MARKER not in template:
        raise ValueError(f"Template marker not found: {TEMPLATE_MARKER}")

    geojson_text = json.dumps(geojson, ensure_ascii=False, separators=(",", ":"))
    html = template.replace(TEMPLATE_MARKER, geojson_text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse optional paths while keeping the demo runnable without arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_map(args.input, args.output, args.template)
    print(f"Created: {args.output}")


if __name__ == "__main__":
    main()
