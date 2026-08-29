from wrgd.visualization.legend import build_legend


def test_build_legend():
    legend = build_legend()

    assert len(legend) == 7

    first = legend[0]
    assert first["min"] == -15.0
    assert first["max"] == -10.0

    for item in legend:
        assert item["color"].startswith("#")
        assert len(item["color"]) == 7
        assert "%" in item["label"]
