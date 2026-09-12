"""Road curvature calculation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, degrees, hypot, isfinite, radians
from typing import Literal, Sequence

from wrgd.geometry.distance import EARTH_RADIUS

Coordinate = tuple[float, float]
TurnDirection = Literal["left", "right", "straight"]

_DEFAULT_MIN_TURN_ANGLE_DEG = 45.0
_DEFAULT_MAX_RADIUS_M = 100.0
_COLLINEAR_RELATIVE_TOLERANCE = 1e-12


@dataclass(frozen=True, slots=True)
class CurvatureResult:
    """Curvature analysis result for one consecutive three-point window."""

    segment_index: int
    turn_angle_deg: float
    radius_m: float
    curvature_per_m: float
    turn_direction: TurnDirection
    is_sharp_curve: bool


def _to_local_meters(
    point: Coordinate,
    origin: Coordinate,
) -> Coordinate:
    """Convert a coordinate to a local east/north metre coordinate."""
    latitude, longitude = point
    origin_latitude, origin_longitude = origin
    meters_per_degree = EARTH_RADIUS * radians(1.0)

    return (
        (longitude - origin_longitude)
        * cos(radians(origin_latitude))
        * meters_per_degree,
        (latitude - origin_latitude) * meters_per_degree,
    )


def _local_vectors(
    point1: Coordinate,
    point2: Coordinate,
    point3: Coordinate,
) -> tuple[Coordinate, Coordinate, Coordinate, float]:
    """Return local vectors and their signed cross product."""
    local_point1 = _to_local_meters(point1, point2)
    local_point2 = (0.0, 0.0)
    local_point3 = _to_local_meters(point3, point2)
    vector01 = (
        local_point2[0] - local_point1[0],
        local_point2[1] - local_point1[1],
    )
    vector12 = (
        local_point3[0] - local_point2[0],
        local_point3[1] - local_point2[1],
    )
    vector02 = (
        local_point3[0] - local_point1[0],
        local_point3[1] - local_point1[1],
    )
    cross = vector01[0] * vector12[1] - vector01[1] * vector12[0]

    return vector01, vector12, vector02, cross


def _validate_thresholds(
    min_turn_angle_deg: float,
    max_radius_m: float,
) -> None:
    """Validate Sharp Curve thresholds."""
    if not 0.0 <= min_turn_angle_deg <= 180.0:
        raise ValueError("min_turn_angle_deg must be between 0 and 180.")
    if not isfinite(max_radius_m) or max_radius_m < 0.0:
        raise ValueError("max_radius_m must be a finite non-negative value.")


def _validate_vectors(vector01: Coordinate, vector12: Coordinate) -> None:
    """Reject duplicate consecutive coordinates."""
    if hypot(*vector01) == 0.0 or hypot(*vector12) == 0.0:
        raise ValueError("Consecutive coordinates must be distinct.")


def calculate_turn_angle(
    point1: Coordinate,
    point2: Coordinate,
    point3: Coordinate,
) -> float:
    """Calculate the absolute turn angle at the middle point in degrees."""
    vector01, vector12, _, _ = _local_vectors(point1, point2, point3)
    _validate_vectors(vector01, vector12)

    cross = vector01[0] * vector12[1] - vector01[1] * vector12[0]
    dot = vector01[0] * vector12[0] + vector01[1] * vector12[1]

    return degrees(atan2(abs(cross), dot))


def calculate_curvature(
    point1: Coordinate,
    point2: Coordinate,
    point3: Coordinate,
    *,
    segment_index: int = 0,
    min_turn_angle_deg: float = _DEFAULT_MIN_TURN_ANGLE_DEG,
    max_radius_m: float = _DEFAULT_MAX_RADIUS_M,
) -> CurvatureResult:
    """Calculate curvature and turn metadata for three consecutive points."""
    _validate_thresholds(min_turn_angle_deg, max_radius_m)
    vector01, vector12, vector02, cross = _local_vectors(point1, point2, point3)
    _validate_vectors(vector01, vector12)

    length01 = hypot(*vector01)
    length12 = hypot(*vector12)
    length02 = hypot(*vector02)
    dot = vector01[0] * vector12[0] + vector01[1] * vector12[1]
    turn_angle_deg = degrees(atan2(abs(cross), dot))

    if abs(cross) <= _COLLINEAR_RELATIVE_TOLERANCE * length01 * length12:
        radius_m = float("inf")
        curvature_per_m = 0.0
        turn_direction: TurnDirection = "straight"
    else:
        radius_m = (length01 * length12 * length02) / (2.0 * abs(cross))
        curvature_per_m = 1.0 / radius_m
        turn_direction = "left" if cross > 0.0 else "right"

    is_sharp_curve = turn_angle_deg >= min_turn_angle_deg and radius_m <= max_radius_m

    return CurvatureResult(
        segment_index=segment_index,
        turn_angle_deg=turn_angle_deg,
        radius_m=radius_m,
        curvature_per_m=curvature_per_m,
        turn_direction=turn_direction,
        is_sharp_curve=is_sharp_curve,
    )


def analyze_curvature(
    coordinates: Sequence[Coordinate],
    min_turn_angle_deg: float = _DEFAULT_MIN_TURN_ANGLE_DEG,
    max_radius_m: float = _DEFAULT_MAX_RADIUS_M,
) -> list[CurvatureResult]:
    """Analyze every consecutive three-point window in a coordinate sequence."""
    _validate_thresholds(min_turn_angle_deg, max_radius_m)

    return [
        calculate_curvature(
            coordinates[index],
            coordinates[index + 1],
            coordinates[index + 2],
            segment_index=index,
            min_turn_angle_deg=min_turn_angle_deg,
            max_radius_m=max_radius_m,
        )
        for index in range(max(0, len(coordinates) - 2))
    ]
