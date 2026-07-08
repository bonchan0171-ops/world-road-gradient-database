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

    def get_elevation(self, lat, lon):
        """
        緯度・経度から標高を取得
        """
        row, col = self.dataset.index(lon, lat)

        return self.dem[row, col]