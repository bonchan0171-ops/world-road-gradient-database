"""道路難易度の評価を行う分析ユーティリティ。"""

from __future__ import annotations

from wrgd.models.difficulty import DifficultyLevel
from wrgd.models.road_statistics import RoadStatistics


def calculate_difficulty(statistics: RoadStatistics) -> DifficultyLevel:
    """RoadStatistics から道路の難易度レベルを算出する。

    Parameters
    ----------
    statistics : RoadStatistics
        道路の統計情報。距離、累積上昇量、最大勾配を利用する。

    Returns
    -------
    DifficultyLevel
        スコアに基づいて 5 段階で評価された難易度情報。

    Notes
    -----
    距離、累積上昇量、最大勾配を重み付きで組み合わせ、
    0.0 から 10.0 の範囲に正規化したスコアを作成する。
    その後、スコアを 5 段階に分類して返す。
    """

    distance_score = statistics.distance / 1000.0
    ascent_score = statistics.ascent / 100.0
    gradient_score = statistics.max_gradient / 2.0
    score = (distance_score * 0.4) + (ascent_score * 0.4) + (gradient_score * 0.2)

    if score < 1.0:
        level = 1
        name = "非常に易しい"
    elif score < 2.5:
        level = 2
        name = "易しい"
    elif score < 4.5:
        level = 3
        name = "普通"
    elif score < 7.0:
        level = 4
        name = "難しい"
    else:
        level = 5
        name = "非常に難しい"

    return DifficultyLevel(level=level, name=name, score=score)
