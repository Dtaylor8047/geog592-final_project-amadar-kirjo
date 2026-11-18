## Imports 
import geopandas as gpd
import pandas as pd
import numpy as np
import argparse as arg
import re

def main():
    smoother = arg.ArgumentParser(
        "A program that smoothes out the normalization process of GIS data."
    )
    smoother.add_argument("--file", type = str, help="Name of the preferred file.")
    smoother.add_argument("--mthd", type=str, help="Preferred method of normalizing data.")

    def get_info():
        """Receiving the File path and the normalization method."""
        # Finish working on while loop
        # I want the loop to check for file types to see if they are correct
        filetypes = r"\.(shp|geojson|csv)$"
        mthds = r"(clip|crs|null)"
        crs = r"(0-9)"
        while True:
            path = input(f"Enter the path name: ")
            try:
                if not re.search(filetypes, path, re.IGNORECASE):
                    raise ValueError(f"Incorrect file type!")
                break
            except ValueError as error:
                print(error)
                path = input(f"Change file type or enter a different file with type {filetypes}: ")
        while True:
            norm = input(f"Enter the normalization method: ")
            try:
                if not re.search(mthds, norm, re.IGNORECASE):
                    raise ValueError(f"Unknown or unsupported method!")
                break
            except ValueError as error:
                print(error)
                norm = input(f"Select from the options listed {mthds}: ")
        while True:
            reproject = input(f"Enter the preferred CRS: ")
            try:
                if not re.search(crs, reproject):
                    raise ValueError(f"Invalid CRS!")
                break
            except ValueError as error:
                print(error)
                reproject = input(f"Please enter a valid CRS projection: ")
        return path, norm, reproject

    args = smoother.parse_args(get_info())

    def to_crs(crs: "4326"):
        """Function to change the crs with the default being 4326."""
        args.file.to_crs(crs)

    # Naturalize, reproject, validate, export_data functions need to be added as well!


if __name__ == "__main__":
    main()