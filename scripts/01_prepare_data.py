"""Clean the provincial panel and join it to the province boundaries.

Input : data/raw/provincial_indicators.csv  (long format, see data/raw/README.md)
Output: data/processed/panel.csv, data/processed/provinces.gpkg
"""
import sys, unicodedata
from pathlib import Path
import pandas as pd
import geopandas as gpd
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import RAW, PROCESSED, GEO, YEARS, VARIABLES

# Name harmonisation between TÜİK spelling and the boundary file
ALIASES = {"afyonkarahisar": "afyon", "icel": "mersin", "k.maras": "kahramanmaras"}


def key(name: str) -> str:
    s = name.strip().lower().replace("ı", "i").replace("İ", "i")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return ALIASES.get(s, s)


PROCESSED.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(RAW / "provincial_indicators.csv")
missing_cols = {"province", "year", *VARIABLES} - set(df.columns)
if missing_cols:
    raise SystemExit(f"missing columns in raw data: {sorted(missing_cols)}")

df = df[df["year"].isin(YEARS)].copy()
df["key"] = df["province"].map(key)

geo = gpd.read_file(GEO / "tr_provinces.geojson")
geo["key"] = geo["name"].map(key)

unmatched = sorted(set(df["key"]) - set(geo["key"]))
if unmatched:
    raise SystemExit(f"province names without a geometry match: {unmatched}")

counts = df.groupby("year")["key"].nunique()
bad = counts[counts != 81]
if not bad.empty:
    raise SystemExit(f"years without 81 provinces: {bad.to_dict()}")
if df[list(VARIABLES)].isna().any().any():
    raise SystemExit("missing values found - please check the raw data")

df.to_csv(PROCESSED / "panel.csv", index=False)
geo[["key", "name", "geometry"]].sort_values("key").reset_index(drop=True).to_file(
    PROCESSED / "provinces.gpkg", driver="GPKG")
print(f"panel: {len(df)} rows, {df['year'].nunique()} years, 81 provinces")
