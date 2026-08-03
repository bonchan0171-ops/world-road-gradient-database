"""統計計算ユーティリティ。"""

from __future__ import annotations

from wrgd.geometry.gradient import calculate_gradient
from wrgd.models.road_statistics import RoadStatistics
from wrgd.profile.elevation_profile import ElevationProfile


def calculate_statistics(profile: ElevationProfile) -> RoadStatistics:
    """ElevationProfile から RoadStatistics を計算する。

    Parameters
    ----------
    profile : ElevationProfile
        標高プロファイルを保持するオブジェクト。

    Returns
    -------
    RoadStatistics
        距離、累積上昇量、累積下降量、最高標高、最低標高、
        最大勾配、平均勾配を格納した統計情報。

    Notes
    -----
    `profile.get_distances()` と `profile.get_elevations()` を利用して、
    累積距離と標高系列から必要な統計量を算出する。
    """

    distances = list(profile.get_distances())
    elevations = list(profile.get_elevations())

    if len(distances) < 2 or len(elevations) < 2:
        raise ValueError("At least two profile points are required.")

    total_distance = float(distances[-1])
    ascent = 0.0
    descent = 0.0
    gradients: list[float] = []

    for previous_elevation, current_elevation in zip(
        elevations[:-1],
        elevations[1:],
    ):
        if current_elevation > previous_elevation:
            ascent += current_elevation - previous_elevation
        elif current_elevation < previous_elevation:
            descent += previous_elevation - current_elevation

    for previous_distance, current_distance in zip(
        distances[:-1],
        distances[1:],
    ):
        distance_delta = current_distance - previous_distance

        if distance_delta <= 0:
            raise ValueError("Distance values must increase monotonically.")

    for (
        previous_distance,
        current_distance,
        previous_elevation,
        current_elevation,
    ) in zip(
        distances[:-1],
        distances[1:],
        elevations[:-1],
        elevations[1:],
    ):
        distance_delta = current_distance - previous_distance
        gradient = calculate_gradient(
            previous_elevation,
            current_elevation,
            distance_delta,
        )
        gradients.append(gradient)

    max_gradient = max(gradients, default=0.0)
    average_gradient = sum(gradients) / len(gradients) if gradients else 0.0

    return RoadStatistics(
        distance=total_distance,
        ascent=ascent,
        descent=descent,
        highest_elevation=float(max(elevations)),
        lowest_elevation=float(min(elevations)),
        max_gradient=max_gradient,
        average_gradient=average_gradient,
    )
