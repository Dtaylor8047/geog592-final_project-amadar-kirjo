## Imports 
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely import wkt

### Make CSV to Geodataframe

filename = "censusdata.csv"

CSV_GDF = pd.read_csv('filename')
