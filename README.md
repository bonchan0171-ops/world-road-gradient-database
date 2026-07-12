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
* ✅ Unit tests with pytest

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

| Module   | Responsibility            |
| -------- | ------------------------- |
| geometry | Mathematical calculations |
| io       | DEM access                |
| road     | Road domain model         |
| builder  | Object construction       |

---

# Project Structure

```text
world-road-gradient-database/

├── docs/
├── data/
├── src/
│   ├── geometry/
│   ├── io/
│   ├── preprocessing/
│   ├── road/
│   └── utils/
│
├── tests/
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# Installation

```bash
git clone https://github.com/<your-github-account>/world-road-gradient-database.git

cd world-road-gradient-database

pip install -r requirements.txt
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run only Builder tests

```bash
pytest tests/test_builder.py -v
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
| Sprint 6 | 🚧 Elevation Profile  |
| Sprint 7 | Planned               |
| Sprint 8 | Planned               |

---

# Version History

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
* Elevation profile generation
* Visualization
* Routing engine integration
* Global road geometry database

---

# License

This project is released under the MIT License.
