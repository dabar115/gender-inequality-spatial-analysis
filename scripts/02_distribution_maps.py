"""Quantile maps of each indicator for 2009 and 2018 (thesis Fig. 3.2)."""
import sys
from pathlib import Path
import pandas as pd, geopandas as gpd, matplotlib.pyplot as plt
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import WATERMARK, PROCESSED, FIGURES, VARIABLES, MAP_YEARS

FIGURES.mkdir(parents=True, exist_ok=True)
geo = gpd.read_file(PROCESSED / "provinces.gpkg")
panel = pd.read_csv(PROCESSED / "panel.csv")

fig, axes = plt.subplots(len(VARIABLES), len(MAP_YEARS), figsize=(12, 3.2 * len(VARIABLES)))
for r, (var, label) in enumerate(VARIABLES.items()):
    for c, year in enumerate(MAP_YEARS):
        g = geo.merge(panel[panel.year == year][["key", var]], on="key")
        ax = axes[r, c]
        g.plot(column=var, scheme="Quantiles", k=5, cmap="YlGnBu", edgecolor="white",
               linewidth=0.3, legend=(c == 1), legend_kwds={"fontsize": 7, "loc": "lower left"}, ax=ax)
        ax.set_title(f"{var} – {year}", fontsize=10)
        ax.set_axis_off()
fig.suptitle("Spatial distribution of indicators (quantiles)" + (f"  [{WATERMARK}]" if WATERMARK else ""), fontsize=13)
if WATERMARK:
    fig.text(0.5, 0.5, WATERMARK, ha="center", va="center", fontsize=28, color="red", alpha=0.35, zorder=10, rotation=20)
fig.tight_layout()
fig.savefig(FIGURES / "distribution_maps_2009_2018.png", dpi=150)
print("saved distribution maps")
