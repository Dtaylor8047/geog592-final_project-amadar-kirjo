import argparse as arg
import re
import geopandas as gpd


def get_info():
    """Collect the user's file and normalization preferences."""

    filetypes = r"\.(shp|csv)$"
    methods = r"^(clip|crs|null)"

    # File input
    while True:
        path = input("Enter the path name: ").strip()
        if re.search(filetypes, path, re.IGNORECASE):
            break
        print("Incorrect file type. Please enter a .shp or .csv file.")
    # Normalization method
    while True:
        norm = input(
            "Enter normalization method: "
        ).strip().lower()
        if norm in methods:
            break
        print(f"Unsupported method. Choose from {methods}")
    # CRS input
    reproject = None
    if norm == "crs":
        while True:
            reproject = input("Enter preferred CRS: ").strip()
            try:
                reproject = int(reproject)
                if reproject > 0:
                    break
            except ValueError:
                pass
            print("Please enter a valid CRS!")
    return path, norm, reproject


def validate_info(path):
    """Check whether the supplied file exists and can be read."""
    try:
        with open(path, 'w') as f:
            data = gpd.read_file(path)
        print("File successfully loaded!")
        return data

    except Exception as error:
        print(f"Unable to read file: {error}")
        return None


def change_crs(data, crs=4326):
    """Reproject the GeoDataFrame."""
    return data.to_crs(epsg=crs)


def process_data(data, norm, reproject=None):
    """Perform the requested normalization operation."""

    if norm == "crs":
        data = change_crs(data, reproject)

    elif norm == "clip":
        print("Clip normalization selected.")
        # Add mask variable to fully implement clip here

    elif norm == "null":
        print("Null normalization selected.")
        # Add null-value handling here.

    return data

def check_continue():
    """Ask whether the user wants to continue normalizing."""

    while True:
        answer = input(
            "Would you like to continue the normalization process? (Y/N): "
        ).strip().upper()
        if answer in ("Y", "N"):
            return answer == "Y"
        print("Invalid response. Enter Y or N.")

def main():

    parser = arg.ArgumentParser(
        description="A program that smooths out the normalization process of GIS data."
    )

    args = parser.parse_args()

    while True:
        path, norm, reproject = get_info()
        data = validate_info(path)
        if data is None:
            if not check_continue():
                break
            continue
        data = process_data(data, norm, reproject)
        print("Normalization operation completed!")
        if not check_continue():
            break
    print("Normalization process complete!")


if __name__ == "__main__":
    main()