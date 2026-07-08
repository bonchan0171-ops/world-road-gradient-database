from src.io.dem_loader import DEMLoader


def main():

    filepath = "data/raw/output_hh.tif"

    loader = DEMLoader(filepath)

    loader.load()

    lat = 35.7700
    lon = 139.7250

    elevation = loader.get_elevation(lat, lon)

    print()
    print("===== Elevation =====")
    print(f"Latitude : {lat}")
    print(f"Longitude: {lon}")
    print(f"Elevation: {elevation:.2f} m")


if __name__ == "__main__":
    main()