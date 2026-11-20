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
        #check_in = input(f"Would you like to begin? (Y/N): ")
        #for check_in == 'Y':
        filetypes = r"\.(shp|csv)$"
        mthds = r"(clip|crs|null)"
        crs = r"(0|1|2|3|4|5|6|7|8|9)"
        ans_val = r"(Y|N)"
        #pop = r"(pop)"
        # File
        while True:
            path = input(f"Enter the path name: ")
            try:
                if not re.search(filetypes, path, re.IGNORECASE):
                    raise ValueError(f"Incorrect file type!")
                break
            except ValueError as error:
                print(error)
                path = input(f"Change file type or enter a different file with type {filetypes}: ")
        # Normalization
        while True:
            norm = input(f"Enter the normalization method: ")
            try:
                if not re.search(mthds, norm, re.IGNORECASE):
                    raise ValueError(f"Unknown or unsupported method!")
                break
            except ValueError as error:
                print(error)
                norm = input(f"Select from the options listed {mthds}: ")
        # Reproject
        while True:
            reproject = input(f"Enter the preferred CRS: ")
            try:
                if not re.search(crs, reproject):
                    raise ValueError(f"Invalid CRS!")
                else:
                    change_crs(reproject)
                    #check_in(f"Continue? (Y/N): ")
                break
            except ValueError as error:
                print(error)
                reproject = input(f"Please enter a valid CRS projection: ")
        # Naturalize(Wishlist function, not necessary)
        while True:
            population = input(f"Naturalize the population? (Y/N): ")
            try:
                if not re.search(ans_val, population):
                    raise ValueError(f"Invalid input!")
                break
            except ValueError as error:
                print(error)
                population = input(f"Please enter either Y or N: ")
        # Validate
        while True:
            break
        # Export

        return path, norm, reproject

    args = smoother.parse_args(get_info())

    def change_crs(crs: "4326"):
        """Function to change the crs with the default being 4326."""
        data = gpd.read_file(args.file)
        return data.to_crs(crs)

    # validate(check for missing vals), export_data functions need to be added as well!


if __name__ == "__main__":
    main()