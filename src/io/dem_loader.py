import rasterio


class DEMLoader:
    """DEM（GeoTIFF）を読み込むクラス"""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self):
        """DEMファイルを読み込む"""

        with rasterio.open(self.filepath) as dataset:

            print("===== DEM Information =====")
            print(f"File      : {self.filepath}")
            print(f"Width     : {dataset.width}")
            print(f"Height    : {dataset.height}")
            print(f"CRS       : {dataset.crs}")
            print(f"Resolution: {dataset.res}")
            print(f"NoData    : {dataset.nodata}")

            dem = dataset.read(1)

            print(f"Minimum Elevation : {dem.min()}")
            print(f"Maximum Elevation : {dem.max()}")

            return dem