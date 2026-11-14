## Imports 
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely import wkt
import sys

### Make CSV to Geodataframe

## Read CSV
def csv_to_df(csv_path, lat_col=None, lon_col=None, geometry_col=None, crs="EPSG:4326"):

 # Read CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Makes a point geometry for Longitude and latitude (doesnt work if there is no lat and long though but should be fine for census)
    if lat_col and lon_col:
        if lat_col not in df.columns or lon_col not in df.columns:
            raise ValueError(f"Missing latitude/longitude columns: {lat_col}, {lon_col}")

        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
            crs=crs
        )

        return gdf

    raise ValueError("Latitude and longitude columns must be provided.")


## Test 

test_gdf = csv_to_df(
    r"C:\Users\Jakcr\OneDrive\Documents\Dev\GEOG592\geog592-amadar-kirjo\Function\test.csv",
    lat_col="Latitude",
    lon_col="Longitude"
)

print(test_gdf.head())