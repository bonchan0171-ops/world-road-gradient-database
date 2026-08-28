"""Color conversion utilities for road gradient visualization."""

MIN_GRADIENT = -15.0
MAX_GRADIENT = 15.0


def _interpolate_channel(start: int, end: int, ratio: float) -> int:
    """Linearly interpolate an RGB channel value."""
    return round(start + (end - start) * ratio)


def gradient_to_color(gradient: float) -> str:
    """Convert a road gradient percentage to a hexadecimal color.

    The color scale is:

    - -15% or less: blue (#0000FF)
    -   0%: green (#00FF00)
    - +15% or more: red (#FF0000)

    Values outside the range are clipped to the range -15% to +15%.
    """
    gradient = max(MIN_GRADIENT, min(MAX_GRADIENT, gradient))

    if gradient <= 0.0:
        ratio = (gradient - MIN_GRADIENT) / (0.0 - MIN_GRADIENT)

        red = _interpolate_channel(0, 0, ratio)
        green = _interpolate_channel(0, 255, ratio)
        blue = _interpolate_channel(255, 0, ratio)
    else:
        ratio = gradient / MAX_GRADIENT

        red = _interpolate_channel(0, 255, ratio)
        green = _interpolate_channel(255, 0, ratio)
        blue = _interpolate_channel(0, 0, ratio)

    return f"#{red:02X}{green:02X}{blue:02X}"
