import pytest

from wrgd.io.dem_loader import DEMLoader


def test_load_dem():
    """DEMが正常に読み込めることを確認"""

    loader = DEMLoader("tests/data/sample_dem.tif")

    dem = loader.load()

    assert dem is not None
    assert dem.shape[0] > 0
    assert dem.shape[1] > 0


def test_get_elevation():
    """標高が取得できることを確認"""

    loader = DEMLoader("tests/data/sample_dem.tif")
    loader.load()

    elevation = loader.get_elevation(35.7700, 139.7250)

    assert isinstance(elevation, float)


def test_out_of_bounds():
    """範囲外座標ではValueErrorになることを確認"""

    loader = DEMLoader("tests/data/sample_dem.tif")
    loader.load()

    with pytest.raises(ValueError):
        loader.get_elevation(35.681236, 139.767125)
