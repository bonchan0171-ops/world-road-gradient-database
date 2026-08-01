"""Tests for ElevationProfile."""

import json
from pathlib import Path

import pytest

from wrgd.profile import ElevationProfile
from wrgd.road.segment import RoadSegment


def create_segment() -> RoadSegment:
    """Create a sample RoadSegment for testing."""
    return RoadSegment(
        coordinates=[
            (35.0, 139.0),
            (35.1, 139.1),
            (35.2, 139.2),
            (35.3, 139.3),
        ],
        elevations=[100.0, 120.0, 110.0, 140.0],
        distances=[100.0, 100.0, 100.0],
        gradients=[20.0, -10.0, 30.0],
    )


def test_cumulative_distances() -> None:
    """Test cumulative distance calculation."""
    profile = ElevationProfile(create_segment())

    assert profile.cumulative_distances() == [
        0.0,
        100.0,
        200.0,
        300.0,
    ]


def test_max_elevation() -> None:
    """Test maximum elevation."""
    profile = ElevationProfile(create_segment())

    assert profile.max_elevation() == 140.0


def test_min_elevation() -> None:
    """Test minimum elevation."""
    profile = ElevationProfile(create_segment())

    assert profile.min_elevation() == 100.0


def test_total_ascent() -> None:
    """Test total ascent."""
    profile = ElevationProfile(create_segment())

    assert profile.total_ascent() == 50.0


def test_total_descent() -> None:
    """Test total descent."""
    profile = ElevationProfile(create_segment())

    assert profile.total_descent() == 10.0


def test_get_distances() -> None:
    """Return cumulative distance data through the public accessor."""
    profile = ElevationProfile(create_segment())
    distances = profile.get_distances()

    assert isinstance(distances, tuple)
    assert distances == (0.0, 100.0, 200.0, 300.0)

    with pytest.raises(AttributeError):
        distances.append(400.0)


def test_get_elevations() -> None:
    """Return elevation data through the public accessor."""
    profile = ElevationProfile(create_segment())
    elevations = profile.get_elevations()

    assert isinstance(elevations, tuple)
    assert elevations == (100.0, 120.0, 110.0, 140.0)

    with pytest.raises(AttributeError):
        elevations.append(150.0)


def test_to_dict_returns_json_serializable_data() -> None:
    """Return a JSON-serializable dictionary for external consumption."""
    profile = ElevationProfile(create_segment())

    data = profile.to_dict()

    assert data == {
        "distances": [0.0, 100.0, 200.0, 300.0],
        "elevations": [100.0, 120.0, 110.0, 140.0],
    }
    assert json.loads(json.dumps(data)) == data


def test_save_image(tmp_path: Path) -> None:
    """Elevation profile image should be saved by the profile class."""
    profile = ElevationProfile(create_segment())
    output = tmp_path / "profile.png"

    profile.save_image(output)

    assert output.exists()


def test_save_image_accepts_title_and_dpi(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """save_image should accept optional title and dpi settings."""
    profile = ElevationProfile(create_segment())
    output = tmp_path / "profile.png"
    title_calls: list[str] = []
    save_kwargs: dict[str, object] = {}

    def fake_title(value: str) -> None:
        title_calls.append(value)

    def fake_savefig(path: Path, dpi: int) -> None:
        save_kwargs["path"] = path
        save_kwargs["dpi"] = dpi

    monkeypatch.setattr("wrgd.profile.elevation_profile.plt.title", fake_title)
    monkeypatch.setattr("wrgd.profile.elevation_profile.plt.savefig", fake_savefig)

    profile.save_image(output, title="Custom Profile", dpi=72)

    assert title_calls == ["Custom Profile"]
    assert save_kwargs["path"] == output
    assert save_kwargs["dpi"] == 72
