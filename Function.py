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
        path = input(f"Enter the path name: ")
        while path != re.search("[].$")
        norm = input(f"Enter the normalization method: ")

    args = smoother.parse_args(get_info())

    def to_crs(crs: "4326"):
        """Function to change the crs with the default being 4326."""
        args.file.to_crs(crs)