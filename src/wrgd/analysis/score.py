"""道路の評価スコアを算出する分析ユーティリティ。"""

from __future__ import annotations

from wrgd.models import RoadStatistics


def calculate_score(statistics: RoadStatistics) -> float:
    """RoadStatistics から道路の評価スコアを算出する。

    Parameters
    ----------
    statistics : RoadStatistics
        道路の統計情報。距離、累積上昇量、最大勾配を利用する。

    Returns
    -------
    float
        0.0 から 100.0 の範囲に収めた評価スコア。
    """

    distance_score: float = statistics.distance / 1000.0
    ascent_score: float = statistics.ascent / 100.0
    gradient_score: float = statistics.max_gradient / 2.0

    score: float = distance_score * 0.4 + ascent_score * 0.4 + gradient_score * 0.2

    score *= 10.0

    if score < 0.0:
        score = 0.0
    elif score > 100.0:
        score = 100.0

    return score
