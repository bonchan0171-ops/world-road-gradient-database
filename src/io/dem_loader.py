import rasterio


class DEMLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataset = None
        self.dem = None

    def load(self):
        """DEMを読み込む"""
        self.dataset = rasterio.open(self.filepath)
        self.dem = self.dataset.read(1)

        print("===== DEM Information =====")
        print(f"File      : {self.filepath}")
        print(f"Width     : {self.dataset.width}")
        print(f"Height    : {self.dataset.height}")
        print(f"CRS       : {self.dataset.crs}")
        print(f"Resolution: {self.dataset.res}")
        print(f"NoData    : {self.dataset.nodata}")
        print(f"Bounds    : {self.dataset.bounds}")
        print(f"Minimum Elevation : {self.dem.min()}")
        print(f"Maximum Elevation : {self.dem.max()}")

        return self.dem

    def get_elevation(self, lat: float, lon: float) -> float:
        """
        緯度・経度から標高を取得する

        Parameters
        ----------
        lat : float
            緯度
        lon : float
            経度

        Returns
        -------
        float
            標高（m）
        """

        # DEMが読み込まれていることを確認
        if self.dataset is None or self.dem is None:
            raise RuntimeError("DEM is not loaded.")

        # mypyに「ここから先はNoneではない」と伝える
        assert self.dataset is not None
        assert self.dem is not None

        row, col = self.dataset.index(lon, lat)

        # DEM範囲外チェック
        if row < 0 or row >= self.dataset.height:
            raise ValueError(f"Latitude {lat} is outside the DEM coverage.")

        if col < 0 or col >= self.dataset.width:
            raise ValueError(f"Longitude {lon} is outside the DEM coverage.")

        return float(self.dem[row, col])
