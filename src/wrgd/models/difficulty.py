"""難易度評価のレベル情報を表すモデル。"""

from dataclasses import dataclass


@dataclass(slots=True)
class DifficultyLevel:
    """道路の難易度レベルを表す値オブジェクト。"""

    level: int
    name: str
    score: float
