"""Global Moran's I, 2009-2018, queen contiguity (thesis Table 3.2).

Also compares the reproduced values with the values reported in the thesis.
"""
import sys
from pathlib import Path
import pandas as pd, geopandas as gpd
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import PROCESSED, TABLES, DOCS, VARIABLES, YEARS
from src.spatial import build_weights, global_moran

TABLES.mkdir(parents=True, exist_ok=True)
geo = gpd.read_file(PROCESSED / "provinces.gpkg")
panel = pd.read_csv(PROCESSED / "panel.csv")
w = build_weights(geo, "queen")

rows = []
for year in YEARS:
    d = geo[["key"]].merge(panel[panel.year == year], on="key", how="left")
    for var in VARIABLES:
        rows.append({"year": year, "variable": var, **global_moran(d[var], w)})
res = pd.DataFrame(rows)
res.to_csv(TABLES / "global_moran_long.csv", index=False)

wide = res.pivot(index="year", columns="variable", values="I").round(2)[list(VARIABLES)]
wide.to_csv(TABLES / "global_moran_queen.csv")
print(wide)

# --- validation against the thesis -----------------------------------------
ref = pd.read_csv(DOCS / "thesis_reference_moran.csv", index_col="year")
diff = (wide - ref[wide.columns]).abs()
diff.round(3).to_csv(TABLES / "validation_vs_thesis.csv")
print(f"\nmax |difference| to thesis values: {diff.values.max():.3f}")
