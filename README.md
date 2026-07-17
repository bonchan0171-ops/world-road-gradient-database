# World Road Geometry Database (WRGD)

A Python open-source library for analyzing road geometry from Digital Elevation Models (DEM).

WRGD combines DEM data with geographic coordinates to calculate:

* Elevation
* Distance
* Road gradient
* Road geometry

The project is designed as a reusable foundation for applications such as:

* 🚴 Cycling route analysis
* 🚗 Navigation systems
* 🚛 Logistics optimization
* 🗺 Geographic Information Systems (GIS)
* 🌎 Terrain analysis

---

# Features

Current features include:

* ✅ DEM (GeoTIFF) loading
* ✅ Elevation lookup by latitude and longitude
* ✅ Haversine distance calculation
* ✅ Road gradient calculation
* ✅ RoadSegment data model
* ✅ RoadSegmentBuilder
* ✅ ElevationProfile analysis
* ✅ Unit tests with pytest
* ✅ Continuous Integration with GitHub Actions

## ElevationProfile

The `ElevationProfile` class provides elevation analysis for a `RoadSegment`.

### Features

- Cumulative distance calculation
- Elevation profile
- Maximum elevation
- Minimum elevation
- Total ascent
- Total descent

# Quality Assurance

WRGD follows modern Python OSS development practices.

- ✅ Ruff (Lint)
- ✅ Black (Code Formatter)
- ✅ mypy (Static Type Checking)
- ✅ pytest (Unit Testing)
- ✅ pytest-cov (Coverage)
- ✅ GitHub Actions (Continuous Integration)

Current test coverage:

- **98%**

### Example

```python
from src.profile import ElevationProfile

profile = ElevationProfile(segment)

print(profile.max_elevation())
print(profile.total_ascent())
print(profile.cumulative_distances())
```

---

# Architecture

```text
Coordinates
      │
      ▼
RoadSegmentBuilder
      │
      ├── DEMLoader
      ├── calculate_distance()
      ├── calculate_gradient()
      ▼
RoadSegment
```

Project responsibilities are clearly separated.

| Package       | Responsibility                     |
| ------------- | ---------------------------------- |
| geometry      | Mathematical calculations          |
| io            | DEM loading                        |
| road          | RoadSegment and RoadSegmentBuilder |
| profile       | Elevation profile analysis         |
| preprocessing | Data preprocessing                 |
| utils         | Utility functions                  |


---

# API Overview

| Package | Description |
|---------|-------------|
| io | DEM loading |
| geometry | Distance and gradient calculations |
| road | RoadSegment and Builder |
| profile | Elevation profile analysis |
| preprocessing | Data preprocessing |
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
├── src/
│   ├── geometry/
│   ├── io/
│   ├── profile/
│   ├── preprocessing/
│   ├── road/
│   └── utils/
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

pip install -r requirements.txt
```

---

# Quick Start

Run quality checks

```bash
ruff check .
black --check .
mypy src
```

Run all tests

```bash
pytest
```

Run tests with coverage

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
| Sprint 8 | Planned |

---

# Version History

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

* GPX support
* GeoJSON support
* OpenStreetMap integration
* Interactive maps
* Routing engine integration
* REST API
* PyPI release
* Global road geometry database

---

# License

This project is released under the MIT License.

# Contributing

Contributions are welcome!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting issues or pull requests.
