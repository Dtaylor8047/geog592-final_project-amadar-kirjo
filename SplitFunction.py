import argparse as arg
import re
import pandas as pd
import geopandas as gpd
from pathlib import Path


def get_info():
    """Collect the user's file and normalization preferences."""
    methods = ("clip", "crs", "null")
    # File input
    while True:
        path = input("Enter the path name: ").strip()
        if path.lower().endswith((".shp", ".csv")):
            break
        print("Incorrect file type. Please enter a .shp or .csv file.")
    # Normalization
    while True:
        norm = input(
            "Enter normalization method: "
        ).strip().lower()
        if norm in methods:
            break
        print(f"Unsupported method. Choose from {methods}")
    # CRS
    reproject = None
    if norm == "crs":
        while True:
            reproject = input("Enter preferred CRS (EPSG): ").strip()
            try:
                reproject = int(reproject)
                if reproject > 0:
                    break
            except ValueError:
                pass
            print("Please enter a valid CRS!")
    return path, norm, reproject


def validate_info(path):
    """Validate and load the user's GIS dataset."""
    path = Path(path)
    #file exists?
    if not path.exists():
        print("File does not exist. Check the file path.")
        return None
    try:
        #load shp
        if path.suffix.lower() == ".shp":
            data = gpd.read_file(path, driver="ESRI Shapefile")
        #load csv
        elif path.suffix.lower() == ".csv":
            data = pd.read_csv(path)
            data = csv_to_geodataframe(data)
        else:
            print("Unsupported file type.")
            return None
        print("File successfully loaded!")
        return data
    except Exception as error:
        print(f"Unable to read file: {error}")
        return None

def csv_to_geodataframe(data):
    """Convert CSV coordinates into a GeoDataFrame."""
    data = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(
            data["Longitude"],
            data["Latitude"]
        ),
        crs="EPSG:4326"
    )
    return data

def change_crs(data, crs=4326):
    """Reproject the GeoDataFrame."""
    return data.to_crs(epsg=crs)

def clip_data(data):
    """Clip the input GeoDataFrame using a boundary shapefile."""
    while True:
        boundary_path = input(
            "Enter the path to the boundary shapefile: "
        ).strip()
        if boundary_path.lower().endswith(".shp"):
            break
        print("Invalid file type. Please enter a .shp file.")
    try:
        boundary = gpd.read_file(boundary_path)
        # Ensure same CRS
        if data.crs != boundary.crs:
            boundary = boundary.to_crs(data.crs)
        # clipping 
        clipped_data = gpd.clip(data, boundary)
        print("Clipping operation completed successfully!")
        return clipped_data
    except Exception as error:
        print(f"Unable to clip dataset: {error}")
        return None

def handle_nulls(data):
    """Allow the user to drop null values or replace them with 0."""
    while True:
        choice = input(
            "How would you like to handle null values? "
            "(drop/zero): "
        ).strip().lower()
        if choice == "drop":
            data = data.dropna()
            print("Rows containing null values have been dropped.")
            break
        elif choice == "zero":
            data = data.fillna(0)
            print("Null values have been replaced with 0.")
            break
        else:
            print("Invalid choice. Please enter 'drop' or 'zero'.")
    return data


def process_data(data, norm, reproject=None):
    """Perform the requested normalization operation."""
    if norm == "crs":
        data = change_crs(data, reproject)
    elif norm == "clip":
        print("Clip normalization selected.")
        data = clip_data(data)
    elif norm == "null":
        print("Null normalization selected.")
        data = handle_nulls(data)
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

    smoother = arg.ArgumentParser(
        description="A program that smooths out the normalization process of GIS data."
    )

    args = smoother.parse_args()
    while True:
        path, norm, reproject = get_info()
        data = validate_info(path)
        if data is None:
            print("Normalization could not be completed.")
        else:
            data = process_data(data, norm, reproject)
            print("Normalization operation completed!")
        if not check_continue():
            break
    print("Normalization process complete!")


if __name__ == "__main__":
    main()