from wrgd.io.dem_loader import DEMLoader


def main():
    filepath = "data/raw/output_hh.tif"

    loader = DEMLoader(filepath)
    loader.load()

    # DEM内の座標
    lat = 35.681236
    lon = 139.767125

    try:
        elevation = loader.get_elevation(lat, lon)

        print()
        print("===== Elevation =====")
        print(f"Latitude : {lat}")
        print(f"Longitude: {lon}")
        print(f"Elevation: {elevation:.2f} m")

    except ValueError as e:
        print()
        print("ERROR")
        print(e)


if __name__ == "__main__":
    main()
