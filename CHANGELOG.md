# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog.
This project follows Semantic Versioning.

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

## [Unreleased]

No unreleased changes.

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