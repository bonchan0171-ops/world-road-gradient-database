# World Road Geometry Database (WRGD)

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

WRGD is a Python library for analyzing road geometry from Digital Elevation Model (DEM) data.
It reads a route file in GPX or GeoJSON format, loads a GeoTIFF DEM, and calculates road statistics such as total distance, ascent, descent, highest and lowest elevation, and average gradient.

This project is a good fit for:

- 🚴 Cycling route analysis
- 🚗 Navigation and route planning
- 🚛 Logistics optimization
- 🗺 GIS and terrain analysis
- 🌎 Road elevation profiling

---

## Features

WRGD currently supports:

- DEM (GeoTIFF) loading
- Elevation lookup from latitude and longitude
- Haversine distance calculation
- Road gradient calculation
- `RoadSegment` and `RoadSegmentBuilder`
- `ElevationProfile` analysis and PNG export
- GPX and GeoJSON route reading
- CSV and JSON export for road statistics
- Analysis helpers for statistics, difficulty, and score evaluation via the `wrgd.analysis` API
- CLI support via the `wrgd` command
- Road difficulty evaluation (5 levels)
- Road evaluation score (0–100)
- Segment-based GeoJSON export for GIS
- Gradient-based color attributes for GeoJSON visualization
---

## Installation

Install the project in editable mode from the repository root:

```bash
python -m pip install -e .
```

After installation, the `wrgd` command becomes available in your environment.

---

## Quick Start

The fastest way to try WRGD is to use the sample route and DEM included in the repository.

```bash
wrgd --route data/sample/sample.gpx --dem data/raw/output_hh.tif
```

Example output:

```text
WRGD CLI
Route : data\sample\sample.gpx
DEM   : data\raw\output_hh.tif
Points: 5

========================================
 Road Analysis Report
========================================
Distance           :    423.9 m
Total Ascent       :      3.0 m
Total Descent      :      1.3 m

Highest Elevation  :     11.7 m
Lowest Elevation   :      8.7 m

Max Gradient       :     1.45 %
Average Gradient   :     0.41 %
```

The demo also shows how to create an elevation profile image:

```bash
python -m examples.demo
```

This writes:

```text
output/elevation_profile.png
```

---

## Minimal Python API Example

You can also use WRGD directly from Python.

```python
from pathlib import Path

from wrgd.app import load_route, print_report, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.profile import ElevationProfile
from wrgd.road.builder import RoadSegmentBuilder

route_file = Path("data/sample/sample.gpx")
dem_file = Path("data/raw/output_hh.tif")

coordinates = load_route(route_file)
builder_coordinates = to_builder_coordinates(coordinates)

dem_loader = DEMLoader(dem_file)
dem_loader.load()

road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)

print_report(road_segment)

profile = ElevationProfile(road_segment)
print(profile.to_dict())
```

This returns a JSON-serializable structure with distance and elevation data.

---

## CLI Usage Example

The installed CLI accepts a route file, a DEM file, and optional export paths.

```bash
wrgd --route data/sample/sample.gpx --dem data/raw/output_hh.tif \
  --csv output/road_statistics.csv \
  --json output/road_statistics.json \
  --output output/elevation_profile.png
```

The options are:

- `--route`: GPX or GeoJSON route file
- `--dem`: GeoTIFF DEM file
- `--csv`: optional CSV export path
- `--json`: optional JSON export path
- `--output`: optional PNG image output path

### CLI Analysis Example

```bash
wrgd --route sample.gpx --dem output_hh.tif --csv result.csv --json result.json
```

Example output:

```text
Difficulty        : Very Easy
Difficulty Level  : 1
Evaluation Score  : 3.3
```

---

## Example Generated Outputs

When you run the CLI with `--csv`, `--json`, and `--output`, WRGD can generate the following files:

```text
output/road_statistics.csv
output/road_statistics.json
output/elevation_profile.png
```

CSV example:

```csv
distance,ascent,descent,highest_elevation,lowest_elevation,max_gradient,average_gradient
423.9,3.0,1.3,11.7,8.7,1.45,0.41
```

JSON example:

```json
{
  "distance": 423.9,
  "ascent": 3.0,
  "descent": 1.3,
  "highest_elevation": 11.7,
  "lowest_elevation": 8.7,
  "max_gradient": 1.45,
  "average_gradient": 0.41
}
```

The PNG file is an elevation profile chart created from the road segment data.

---

## Segment GeoJSON and Geo Heatmap

WRGD can export road segments as GeoJSON Features with gradient and color attributes.

```bash
python -m examples.segment_geojson
```

The output is written to:

```text
output/segments.geojson
```

Each road segment contains the following properties:

- `segment_id`
- `distance`
- `gradient`
- `color`
The `color` property is a hexadecimal RGB color derived from the road gradient.

The generated GeoJSON can be loaded into QGIS or other GIS software and the `color` attribute can be used for road gradient visualization.


## API Examples

The following examples use the current public APIs from the `wrgd` package.

### Analysis utilities

The `wrgd.analysis` package provides helpers for evaluating road routes through statistics, difficulty, and score APIs.

```python
from wrgd.analysis import calculate_difficulty, calculate_score
from wrgd.models import RoadStatistics

statistics = RoadStatistics(
    distance=1000.0,
    ascent=50.0,
    descent=20.0,
    highest_elevation=150.0,
    lowest_elevation=100.0,
    max_gradient=2.0,
    average_gradient=1.0,
)

difficulty = calculate_difficulty(statistics)
score = calculate_score(statistics)

print(difficulty.name)
print(score)
```

### RoadStatistics

`RoadSegment.statistics()` returns a `RoadStatistics` dataclass with summary values.

```python
from pathlib import Path

from wrgd.app import load_route, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.road.builder import RoadSegmentBuilder

route_file = Path("data/sample/sample.gpx")
dem_file = Path("data/raw/output_hh.tif")

coordinates = load_route(route_file)
builder_coordinates = to_builder_coordinates(coordinates)

dem_loader = DEMLoader(dem_file)
dem_loader.load()

road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)
stats = road_segment.statistics()

print(stats.distance)
print(stats.ascent)
print(stats.descent)
print(stats.highest_elevation)
print(stats.lowest_elevation)
print(stats.max_gradient)
print(stats.average_gradient)
```

### ElevationProfile

`ElevationProfile` converts a `RoadSegment` into a JSON-serializable structure.

```python
from pathlib import Path

from wrgd.app import load_route, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.profile import ElevationProfile
from wrgd.road.builder import RoadSegmentBuilder

route_file = Path("data/sample/sample.gpx")
dem_file = Path("data/raw/output_hh.tif")

coordinates = load_route(route_file)
builder_coordinates = to_builder_coordinates(coordinates)

dem_loader = DEMLoader(dem_file)
dem_loader.load()

road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)
profile = ElevationProfile(road_segment)

print(profile.to_dict())
```

### Builder

Use `RoadSegmentBuilder` together with a `DEMLoader` to build a road segment from latitude/longitude points.

```python
from pathlib import Path

from wrgd.app import load_route, to_builder_coordinates
from wrgd.io.dem_loader import DEMLoader
from wrgd.road.builder import RoadSegmentBuilder

route_file = Path("data/sample/sample.gpx")
dem_file = Path("data/raw/output_hh.tif")

coordinates = load_route(route_file)
builder_coordinates = to_builder_coordinates(coordinates)

dem_loader = DEMLoader(dem_file)
dem_loader.load()

road_segment = RoadSegmentBuilder(dem_loader).build(builder_coordinates)
print(road_segment.point_count())
print(road_segment.segment_count())
```

### Reader / Writer

Read route data from GPX or GeoJSON and write it back out.

```python
from pathlib import Path

from wrgd.io.geojson_reader import GeoJSONReader
from wrgd.io.geojson_writer import GeoJSONWriter
from wrgd.io.gpx_reader import GPXReader
from wrgd.io.gpx_writer import GPXWriter

route_gpx = GPXReader(Path("data/sample/sample.gpx")).read()
route_geojson = GeoJSONReader(Path("tests/data/sample.geojson")).read()

print(len(route_gpx))
print(len(route_geojson))

writer = GPXWriter()
writer.write(
    [
        (35.681236, 139.767125, 12.3),
        (35.682000, 139.768000, 15.8),
    ],
    Path("output/example_route.gpx"),
)

geojson_writer = GeoJSONWriter(Path("output/example_route.geojson"))
geojson_writer.write(route_geojson)
```

---

## Project Structure

```text
.
├── examples/
│   └── demo.py                 # Simple demonstration entrypoint
├── data/
│   ├── sample/                 # Sample GPX / GeoJSON route files
│   └── raw/                    # DEM data such as GeoTIFF files
├── output/                     # Generated reports and images
├── src/
│   └── wrgd/
│       ├── app.py              # Shared application helpers
│       ├── cli.py              # Command-line interface
│       ├── geometry/           # Distance and gradient calculations
│       ├── io/                 # DEM, GeoJSON, GPX, and writer utilities
│       ├── profile/            # Elevation profile analysis
│       └── road/               # RoadSegment and builder logic
└── tests/                      # Pytest test suite
```

---

## Architecture

```text
                 GeoJSON / GPX
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      GeoJSONReader          GPXReader
          │                       │
          └───────────┬───────────┘
                      ▼
                 Coordinates
                      │
                      ▼
             RoadSegmentBuilder
                      │
                      ▼
                RoadSegment
                      │
                      ▼
             ElevationProfile
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      GeoJSONWriter          GPXWriter
```

Project responsibilities are separated as follows:

| Package | Responsibility |
|----------|----------------|
| geometry | Mathematical calculations |
| io | DEM, GeoJSON, and GPX I/O |
| road | `RoadSegment` and `RoadSegmentBuilder` |
| profile | Elevation profile analysis |
| preprocessing | Data preprocessing |
| utils | Utility functions |

---

## Supported Formats

| Format | Read | Write |
|--------|:----:|:-----:|
| GeoJSON | ✅ | ✅ |
| GPX | ✅ | ✅ |
| KML | ❌ | ❌ |
| OpenStreetMap (OSM) | ❌ | ❌ |

---

## Quality Assurance

WRGD uses standard Python project tooling for validation and CI:

- Ruff
- Black
- mypy
- pytest
- pytest-cov
- GitHub Actions

The current tests are designed to validate the package behavior described above.

| utils | Utility functions |

# Project Structure

```text
world-road-gradient-database/

├── .github/
│   └── workflows/
│
├── docs/
├── data/
│
├── examples/
│   ├── __init__.py
│   └── demo.py
│
├── output/
│   └── elevation_profile.png   # 実行時に生成
│
├── src/
│   ├── geometry/
│   ├── io/
│   ├── models/
│   ├── preprocessing/
│   ├── profile/
│   ├── road/
│   ├── utils/
│   ├── app.py                  # 共通アプリケーション処理
│   └── cli.py                  # CLI
│
├── tests/
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
├── pyproject.toml
└── pytest.ini
```

---

# Installation

```bash
git clone https://github.com/bonchan0171-ops/world-road-gradient-database.git

cd world-road-gradient-database

python -m pip install -e .
```

This installs the WRGD package in editable mode so the `wrgd` command is available.

---

# Quick Start

```python
from src.io.geojson_reader import GeoJSONReader

reader = GeoJSONReader("road.geojson")

coordinates = reader.read()

print(f"Loaded {len(coordinates)} coordinates.")
```

## Road Statistics API

`RoadSegment` provides a unified API for retrieving summary statistics.

```python
stats = road_segment.statistics()

print(stats.distance)
print(stats.ascent)
print(stats.descent)
print(stats.highest_elevation)
print(stats.lowest_elevation)
print(stats.max_gradient)
print(stats.average_gradient)
```

Example output:

```text
{
    "distance": 423.9,
    "ascent": 3.0,
    "descent": 1.3,
    "highest_elevation": 11.7,
    "lowest_elevation": 8.7,
    "max_gradient": 1.45,
    "average_gradient": 0.41,
}
```

## GPX Writer Example

```python
from src.io.gpx_writer import GPXWriter

points = [
    (35.681236, 139.767125, 12.3),
    (35.682000, 139.768000, 15.8),
]

writer = GPXWriter()
writer.write(points, "route.gpx")
```

Generated GPX:

```xml
<trkpt lat="35.681236" lon="139.767125">
    <ele>12.3</ele>
</trkpt>
```

## Run Quality Checks

```bash
ruff check .
black --check .
mypy src
```

## Run Tests

```bash
pytest
```

## Run Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

---

# Development Roadmap

| Sprint   | Status                |
| -------- | --------------------- |
| Sprint 0 | ✅ Environment         |
| Sprint 1 | ✅ DEM Research        |
| Sprint 2 | ✅ DEMLoader           |
| Sprint 3 | ✅ Distance & Gradient |
| Sprint 4 | ✅ RoadSegment         |
| Sprint 5 | ✅ RoadSegmentBuilder  |
| Sprint 6 | ✅ Elevation Profile |
| Sprint 7 | ✅ OSS Quality Improvements |
| Sprint 8  | ✅ GeoJSON / GPX Reader & Writer |
| Sprint 9  | ✅ GPX I/O Completed |
| Sprint 10 | ✅ GPX Elevation Support |
| Sprint 11 | ✅ Demo Application |
| Sprint 12 | ✅ CLI & Application Refactoring |
---

# Version History

## v0.14.0

### Added

- Road Statistics API (`RoadSegment.statistics()`)
- Unified road statistics retrieval
- Updated Demo and CLI to use the Statistics API
- Added unit tests for `statistics()`

## v0.13.0

### Added

- Command Line Interface (CLI)
- Shared application utilities
- Demo application improvements
- Elevation profile visualization

## v0.12.0

### Added

- Demonstration application
- Road analysis report
- Elevation profile visualization
- RoadSegment statistics

### Improved

- Example application
- Project documentation

## v0.11.0

### Added

- GPX elevation (`<ele>`) support
- Backward-compatible GPXWriter

### Improved

- GPXWriter documentation
- README examples

## v0.8.0

* Added Ruff
* Added Black
* Added mypy
* Added pytest-cov
* Improved GitHub Actions
* Added CHANGELOG.md

## v0.7.0

* Added ElevationProfile
* Added cumulative distance calculation
* Added ascent/descent analysis
* Added CONTRIBUTING.md
* Added MIT License

## v0.6.0

* Added RoadSegmentBuilder
* Automatic elevation retrieval
* Automatic distance calculation
* Automatic gradient calculation

## v0.5.0

* Added RoadSegment
* Validation
* Statistics

## v0.4.0

* Added Haversine distance calculation
* Added gradient calculation

## v0.3.0

* Added DEMLoader
* Added elevation lookup

## v0.2.0

* DEM research

## v0.1.0

* Project initialization

---

# Development

Development rules:

* Python 3.12
* Type hints
* pytest
* docstring
* Single Responsibility Principle
* Git tag for every Sprint

---

# Future Goals

Planned features include:

- OpenStreetMap support
- KML support
- REST API
- PyPI release
- Interactive map visualization

---

# License

This project is released under the MIT License.

# Contributing

Contributions are welcome!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting issues or pull requests.


# Data

WRGD does not include DEM datasets.

Supported DEM datasets include:

- AW3D30 (GeoTIFF)
- SRTM (GeoTIFF)
- Copernicus DEM (GeoTIFF)
- FABDEM (GeoTIFF)

Please download the datasets separately before using WRGD.

# Why WRGD?

Unlike general GIS libraries,
WRGD focuses specifically on road geometry analysis.
It is designed to be lightweight, extensible, and easy to integrate into Python applications.

It provides reusable building blocks for elevation,
gradient and terrain analysis from DEM datasets.
The project aims to become a reusable foundation for road geometry analysis across multiple GIS data sources.
WRGD is designed with a modular architecture,
making it easy to add support for additional GIS
data formats such as OpenStreetMap and KML in the future.