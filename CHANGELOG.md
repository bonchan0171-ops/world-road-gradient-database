# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog.
This project follows Semantic Versioning.

---

## [Unreleased]

No unreleased changes.

---

## [v0.10.0] - 2026-07-22

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