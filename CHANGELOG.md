# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog.
This project follows Semantic Versioning.

---

## v1.0.0

### Added

- Stable 1.0.0 API definition based on the documented top-level WRGD exports
- API Stability Policy and API Freeze documentation for the 1.0.0 public API
- Purpose-based Feature Navigation with the README `Find by Goal` section
- OSM fixture-based CI execution for `network_route.py`

### Improved

- Stabilized CI execution for representative Examples without external DEM downloads
- Synchronized Example inputs, fixtures, documentation, and GitHub Actions workflows
- Clarified the distinction between the top-level Stable API and advanced Module API

### Quality

- Verified package, Example, OSM fixture, documentation, and CI integration workflows
- Prepared the v1.0.0 release candidate without promoting development-only API fields

---

## v0.30.2

### Fixed

- Fixed `curvature_statistics.py` CI failure caused by referencing the unavailable `RoadStatistics.average_radius` attribute.
- Calculated average curvature radius from finite `CurvatureResult.radius_m` values while retaining `RoadStatistics.min_radius` for the minimum radius.

---

## v0.30.1

### Fixed

- Fixed GitHub Actions examples by generating a deterministic DEM fixture during CI.
- Added `curvature_statistics.py`, `network_route.py`, and `interactive_map.py` as tracked examples.
- Synchronized `README`, `examples/README`, and the CI example list.
- Fixed `curvature_statistics.py` to use the stable `RoadStatistics.min_radius` API.

---

## v0.30.0

### Added

- Public API export review for `src/wrgd/__init__.py` and explicit top-level `__all__` documentation
- README section for the advanced module API and API stability policy
- CI workflow expansion to execute representative example scripts and build the package after test coverage
- README examples aligned with the actual `examples/` scripts and duplicate/omitted references resolved

### Improved

- Documentation consistency across README, examples, and package-public API descriptions
- Validation coverage for example execution and packaging checks in CI

### Quality

- Verified the package entrypoint and documentation remain aligned with the implemented public API
- Maintained existing Ruff, Black, mypy, and pytest checks without altering the publish workflow

---

## v0.29.0

### Added

- README and example synchronization for public usage patterns and module-level entrypoints
- Documentation updates covering API stability expectations and the available advanced integrations
- Example and workflow validation tasks for documentation correctness and release readiness

### Improved

- Consolidated README examples for quick-start, Python API, and analysis workflows
- Clarified the distinction between stable top-level APIs and lower-level module APIs
- Updated release-facing documentation to reflect actual package usage and package build validation

### Quality

- Cross-checked examples against the implemented package surface and package metadata
- Kept CI and packaging checks aligned with the current repository workflow

---

## v0.28.0

### Added

- Three-point road curvature analysis with local metre coordinate conversion
- `CurvatureResult`, `calculate_turn_angle()`, `calculate_curvature()`, and `analyze_curvature()` APIs
- Curvature statistics in `RoadStatistics`: average curvature, maximum curvature, minimum radius, and Sharp Curve count
- Optional curvature attributes for GeoJSON and GeoPackage segment output
- README documentation and Python API example for road curvature analysis

---

## v0.27.0

### Added

- GeoPackage export with the `GeoPackageWriter` API
- `--gpkg` CLI option for exporting the `road_segments` layer
- EPSG:4326 LineString geometries with longitude/latitude coordinate order
- GeoPackage attributes for distance, gradient, elevation, difficulty, score, and color
- GeoPackage Writer and CLI integration tests
- README usage examples for CLI, Python API, and QGIS

---

## v0.26.0

### Added

- `--interactive` CLI option for GIS exports
- Automatic `segments.geojson` generation in the specified output directory
- Automatic `interactive_map.html` generation with Leaflet
- Clickable Leaflet segment popups with road analysis properties
- README usage example for Interactive GIS Export
- CLI tests for interactive output paths and export calls

---

## v0.25.0

### Added

- `wrgd analyze` subcommand (backward compatible)
- `wrgd map` interactive map CLI
- Automatic Segment GeoJSON generation
- Automatic Leaflet HTML generation
- Offline standalone HTML map
- Interactive segment popup
- CLI map integration tests

---

## v0.24.1

### Added
- Interactive Leaflet map export
- Embedded GeoJSON for offline HTML viewing
- Gradient legend
- Segment popup (distance & gradient)

## v0.24.0

---

# Changelog

## v0.23.0 (2026-08-27)

### Added

- Geo Heatmap support for segment-based GeoJSON export
- `gradient_to_color()` utility for hexadecimal RGB color generation
- Automatic `color` property in `GeoJSONWriter.write_segments()`
- New visualization package (`wrgd.visualization`)
- Example: `examples/segment_geojson.py`
- GeoJSON color export unit tests

### Improved

- Updated README with Geo Heatmap documentation
- Updated examples documentation for Segment GeoJSON

### Quality

- Ruff / Black / mypy passed
- pytest: 78 passed


---

## v0.22.0

### Added

- CLI now displays road difficulty and evaluation score
- CSV export includes difficulty level, difficulty name, and score
- JSON export includes difficulty object and evaluation score
- GeoJSON Writer supports Feature properties
- GeoJSON Writer supports segment-by-segment Feature export

### Improved

- GitHub Actions updated for Node.js 24 compatibility
- Test coverage maintained at 95%
- Total test suite expanded to 71 passing tests

---

## v0.21.0

### Added

- Difficulty model (`DifficultyLevel`)
- Road statistics model (`RoadStatistics`)
- Analysis package (`wrgd.analysis`)
- Unit tests for difficulty and score calculation

### Improved

- Type safety with mypy
- Analysis API documentation
- Overall project quality and test coverage

---

## v0.20.0

### Added

- Road statistics analysis API (`calculate_statistics`)
- Difficulty evaluation API (`calculate_difficulty`)
- Road evaluation score API (`calculate_score`)
- CLI support for CSV and JSON export
- Elevation profile PNG export

### Improved

- API documentation and usage examples
- CLI usability and output options

---

## v0.19.0

### Added

- PyPI Trusted Publishing workflow
- GitHub Release automated publishing
- Python API examples
- CONTRIBUTING, SECURITY and CODE_OF_CONDUCT documentation

### Improved

- Packaging and release workflow
- Project documentation

---

## v0.18.0 - Sprint 17

### Added

- CLI CSV export support via `--csv`
- CLI JSON export support via `--json`
- Optional statistics file output while preserving the existing console report display

### Changed

- Updated CLI to support saving analysis statistics to CSV and JSON files without changing the existing screen output flow

---

## v0.17.0

### Added

- CLI-enabled road analysis execution
- Public API entrypoint cleanup for package usage
- README onboarding updates for Installation, Quick Start, and Python API
- Improved CLI user-facing error handling
- CLI input information display

### Changed

- Migrated the codebase to the `src/wrgd` package structure
- Updated tests to align with the new package layout

---

## v0.20.0 - Sprint 20

### Added

- README onboarding improvements for first-time users
- Beginner-friendly Quick Start and installation guidance
- New example scripts aligned with the README workflow
- API usage examples for `RoadStatistics`, `ElevationProfile`, `RoadSegmentBuilder`, and reader/writer classes

### Changed

- Reorganized `examples/` to provide clearer entrypoints for Quick Start, Python API, and CLI export workflows
- Expanded README and API documentation sections to improve consistency across usage examples

---

## v0.21.0 - Sprint 21

### Added

- Analysis API utilities for `calculate_statistics`, `calculate_difficulty`, and `calculate_score`
- Road evaluation helpers for statistics, difficulty, and score analysis

### Changed

- Updated analysis documentation and examples to reflect the new scoring workflow

---

## [Unreleased] - Sprint 31

### Added

- `RoadNetwork`, `NetworkNode`, and `NetworkEdge` models
- OSM XML Reader for road network input
- DEM-based `NetworkNode` elevation assignment
- `NetworkEdge` gradient calculation from node elevations
- CLI `--network` option
- Dijkstra shortest path via `shortest_path()`
- `NetworkPath` and `shortest_route()` API
- `RoadStatistics` generation from `NetworkPath`
- Difficulty / Score API integration tests for NetworkPath statistics

### Sprint 32

#### Added

- `RoadNetwork.path_coordinates()` for continuous NetworkPath coordinates
- NetworkPath to GeoJSON LineString integration using `GeoJSONWriter.write()`
- Network Route GeoJSON CLI with `--start-node` and `--end-node`
- Network Route mode error handling and GeoJSON properties for `node_ids`,
  `edge_ids`, and `distance_m`
- GeoJSON integration tests and CLI tests

---

## v0.14.0

### Added

- Road Statistics API (`RoadSegment.statistics()`)
- Unified road statistics retrieval
- Added unit test for `statistics()`

### Changed

- Updated Demo application to use the Statistics API
- Updated CLI to use the Statistics API

---

## [v0.13.0] - 2026-07-26

### Added

- Command Line Interface (CLI)
- Shared application utilities (`src/app.py`)
- Elevation profile visualization
- Demo application improvements

### Improved

- Refactored demo and CLI to share common logic
- Improved project structure and maintainability

### Quality

- 42 pytest tests passed
- Ruff passed
- Black passed
- mypy passed

---

## [v0.12.0] - 2026-07-26

### Added

- Demo application (`examples/demo.py`)
- Road analysis report
- Elevation profile visualization
- PNG export (`output/elevation_profile.png`)

### Improved

- README updated with demo instructions
- Demo screenshots and usage examples

### Quality

- 42 pytest tests passed
- Ruff passed
- Black passed
- mypy passed

---

## [v0.11.0] - 2026-07-22

### Added

- GPX elevation (`<ele>`) output support
- Backward-compatible GPXWriter
- Unit tests for GPX elevation support
- Validation for invalid point formats

### Improved

- README updated with GPX elevation examples

### Quality

- 42 pytest tests passed
- Ruff passed
- Black passed
- mypy passed

---

## [v0.10.0] - 2026-07-22
...

### Added

- GPXWriter implementation
- GPX 1.1 export support
- GPXWriter unit tests

### Improved

- README updated
- Architecture diagram updated
- Supported formats table added

### Quality

- 39 pytest tests passed
- Ruff passed
- Black passed
- mypy passed

### Known Issues

- When using NumPy 2.5.x, a `DeprecationWarning` may be emitted by the Rasterio dependency when loading DEM files.
- This warning originates from Rasterio, not WRGD, and does not affect functionality.

---

## [v0.9.0] - 2026-07-20

### Added

- GeoJSONReader
- GeoJSONWriter
- GPXReader
- GeoJSON unit tests
- GPX unit tests

### Improved

- README
- API Overview

---

## [v0.8.0] - 2026-07-17

### Added

- Ruff
- Black
- mypy
- pytest-cov
- CHANGELOG.md

### CI

- Improved GitHub Actions

### Documentation

- README improvements

---

## [v0.7.0] - 2026-07-13

### Added

- ElevationProfile class
- Cumulative distance calculation
- Elevation profile generation
- Maximum / Minimum elevation
- Total ascent / descent

### CI

- GitHub Actions for automatic pytest execution

### Documentation

- README improvements
- LICENSE (MIT)
- CONTRIBUTING.md

---

## [v0.6.0] - 2026-07-12

### Added

- RoadSegmentBuilder
- Automatic DEM elevation lookup
- Automatic distance calculation
- Automatic gradient calculation

---

## [v0.5.0] - Sprint 4

### Added

- RoadSegment class
- Distance summary
- Average gradient
- Validation checks

---

## [v0.4.0] - Sprint 3

### Added

- calculate_distance()
- calculate_gradient()

---

## [v0.3.0] - Sprint 2

### Added

- DEMLoader
- GeoTIFF support
- Elevation lookup
- Out-of-range validation

---

## [v0.2.0] - Sprint 1

### Added

- DEM dataset research
- Dataset comparison

---

## [v0.1.0] - Sprint 0

### Added

- Repository creation
- Development environment
- pytest setup