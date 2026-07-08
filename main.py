from src.io.dem_loader import DEMLoader


def main():

    filepath = "data/raw/output_hh.tif"

    loader = DEMLoader(filepath)

    dem = loader.load()

    print(dem)


if __name__ == "__main__":
    main()