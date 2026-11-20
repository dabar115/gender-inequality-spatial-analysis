"""LISA cluster maps (HH, LL, LH, HL) at p < 0.05 for 2009 and 2018 (thesis Fig. 3.3-3.7)."""
import sys
from pathlib import Path
import pandas as pd, geopandas as gpd, matplotlib.pyplot as plt
from matplotlib.patches import Patch
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import WATERMARK, PROCESSED, TABLES, FIGURES, VARIABLES, MAP_YEARS
from src.spatial import build_weights, lisa_clusters

COLORS = {"High-High": "#d7191c", "Low-Low": "#2c7bb6", "Low-High": "#abd9e9",
          "High-Low": "#fdae61", "Not significant": "#eeeeee"}

FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)
geo = gpd.read_file(PROCESSED / "provinces.gpkg")
panel = pd.read_csv(PROCESSED / "panel.csv")
w = build_weights(geo, "queen")

all_rows = []
for var in VARIABLES:
    fig, axes = plt.subplots(1, len(MAP_YEARS), figsize=(14, 4))
    for ax, year in zip(axes, MAP_YEARS):
        d = geo.merge(panel[panel.year == year][["key", var]], on="key")
        lisa = lisa_clusters(d[var], w)
        d = pd.concat([d, lisa], axis=1)
        d.plot(color=d["cluster"].map(COLORS), edgecolor="white", linewidth=0.3, ax=ax)
        ax.set_title(f"{var} – {year}", fontsize=10)
        ax.set_axis_off()
        all_rows.append(d.drop(columns="geometry").assign(variable=var, year=year))
    handles = [Patch(color=c, label=l) for l, c in COLORS.items()]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=8, frameon=False)
    fig.suptitle(f"LISA clusters (queen, p < 0.05): {VARIABLES[var]}" + (f"  [{WATERMARK}]" if WATERMARK else ""), fontsize=11, color="black")
    if WATERMARK:
        fig.text(0.5, 0.5, WATERMARK, ha="center", va="center", fontsize=22, color="red", alpha=0.35, zorder=10, rotation=10)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(FIGURES / f"lisa_{var}.png", dpi=150)
    plt.close(fig)

out = pd.concat(all_rows)[["variable", "year", "name", "Ii", "p_sim", "cluster"]]
out.to_csv(TABLES / "lisa_clusters.csv", index=False)
summary = out.groupby(["variable", "year", "cluster"]).size().unstack(fill_value=0)
summary.to_csv(TABLES / "lisa_cluster_counts.csv")
print(summary)
