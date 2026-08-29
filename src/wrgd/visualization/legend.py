from __future__ import annotations

from .color import gradient_to_color


def build_legend() -> list[dict[str, object]]:
    """Return WRGD gradient legend."""

    ranges = [
        (-15, -10),
        (-10, -5),
        (-5, 0),
        (0, 0),
        (0, 5),
        (5, 10),
        (10, 15),
    ]

    legend = []

    for minimum, maximum in ranges:
        value = (minimum + maximum) / 2
        legend.append(
            {
                "min": float(minimum),
                "max": float(maximum),
                "color": gradient_to_color(value),
                "label": f"{minimum}~{maximum}%",
            }
        )

    return legend
