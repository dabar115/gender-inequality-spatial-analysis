"""Generate a SIMULATED provincial panel so the workflow can be run without the private thesis data.

The values are artificial: a west-east gradient plus random noise, loosely calibrated to plausible
ranges. They are only meant to demonstrate the pipeline and must not be interpreted as results.
Usage:  DEMO=1 python scripts/demo_generate_synthetic_data.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import DEMO, RAW, GEO, YEARS

if not DEMO:
    raise SystemExit("run with DEMO=1 so simulated data is never mixed with real data")

RAW.mkdir(parents=True, exist_ok=True)
g = gpd.read_file(GEO / "tr_provinces.geojson").to_crs(5254)
east = g.geometry.centroid.x.values
east = (east - east.min()) / (east.max() - east.min())      # 0 = west, 1 = east

rng = np.random.default_rng(2026)
rows = []
for t, year in enumerate(YEARS):
    for name, e in zip(g["name"], east):
        rows.append({
            "province": name, "year": year,
            "EGT_KAD": 38 + 0.8 * t - 22 * e + rng.normal(0, 4),
            "EGT_ESZ": 8 - 0.2 * t + 6 * e + rng.normal(0, 2),
            "ERG_DOG": 70 - 2.0 * t + 50 * e + rng.normal(0, 12),
            "KIST": 30 + 0.5 * t - 15 * e + rng.normal(0, 5),
            "KBGDO": 11000 + 150 * t - 7000 * e + rng.normal(0, 1500),
        })
pd.DataFrame(rows).round(3).to_csv(RAW / "provincial_indicators.csv", index=False)
print(f"simulated panel written to {RAW / 'provincial_indicators.csv'}")
