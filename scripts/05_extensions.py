"""Extensions added in the 2026 reproduction (not part of the original thesis).

1. Robustness: Global Moran's I under different weights (queen contiguity, 5 and 8 nearest neighbours).
   Rook contiguity is not used: in the boundary file some neighbouring provinces only touch at
   vertices, which leaves an island under rook (the thesis also reports queen ~ rook for Turkey).
2. Bivariate Moran's I: GDP per capita (KBGDO) vs. the spatial lag of each gender indicator.
"""
import sys
from pathlib import Path
import pandas as pd, geopandas as gpd
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import PROCESSED, TABLES, VARIABLES, MAP_YEARS
from src.spatial import build_weights, global_moran, bivariate_moran

TABLES.mkdir(parents=True, exist_ok=True)
geo = gpd.read_file(PROCESSED / "provinces.gpkg")
panel = pd.read_csv(PROCESSED / "panel.csv")
weights = {"queen": build_weights(geo, "queen"),
           "knn5": build_weights(geo, "knn", k=5),
           "knn8": build_weights(geo, "knn", k=8)}

rob = []
for year in MAP_YEARS:
    d = geo[["key"]].merge(panel[panel.year == year], on="key")
    for var in VARIABLES:
        for name, w in weights.items():
            rob.append({"year": year, "variable": var, "weights": name, **global_moran(d[var], w)})
rob = pd.DataFrame(rob)
rob.pivot_table(index=["year", "variable"], columns="weights", values="I").round(3).to_csv(
    TABLES / "robustness_weights.csv")

bv = []
for year in MAP_YEARS:
    d = geo[["key"]].merge(panel[panel.year == year], on="key")
    for var in [v for v in VARIABLES if v != "KBGDO"]:
        bv.append({"year": year, "x": "KBGDO", "y_lag": var,
                   **bivariate_moran(d["KBGDO"], d[var], weights["queen"])})
pd.DataFrame(bv).round(4).to_csv(TABLES / "bivariate_moran_gdp.csv", index=False)
print("saved robustness and bivariate tables")
