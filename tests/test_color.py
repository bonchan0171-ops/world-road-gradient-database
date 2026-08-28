from wrgd.visualization.color import gradient_to_color


def test_gradient_to_color_boundaries() -> None:
    assert gradient_to_color(-20.0) == "#0000FF"
    assert gradient_to_color(-15.0) == "#0000FF"
    assert gradient_to_color(0.0) == "#00FF00"
    assert gradient_to_color(15.0) == "#FF0000"
    assert gradient_to_color(20.0) == "#FF0000"


def test_gradient_to_color_intermediate_values() -> None:
    assert gradient_to_color(-7.5) == "#008080"
    assert gradient_to_color(7.5) == "#808000"


def test_gradient_to_color_returns_hex_color() -> None:
    for gradient in (-15.0, -5.0, 0.0, 5.0, 15.0):
        color = gradient_to_color(gradient)

        assert color.startswith("#")
        assert len(color) == 7
        int(color[1:], 16)
