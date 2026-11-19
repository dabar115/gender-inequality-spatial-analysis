"""Spatial helpers: weights, global Moran's I, local Moran's I (LISA)."""
import numpy as np
import pandas as pd
import geopandas as gpd
from libpysal.weights import Queen, Rook, KNN
from esda.moran import Moran, Moran_Local, Moran_BV

from .config import PERMUTATIONS, ALPHA, SEED

CLUSTER_LABELS = {0: "Not significant", 1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}


def build_weights(gdf: gpd.GeoDataFrame, kind: str = "queen", k: int = 5):
    """Row-standardised spatial weights. Queen contiguity is the thesis default."""
    if kind == "queen":
        w = Queen.from_dataframe(gdf, use_index=True)
    elif kind == "rook":
        w = Rook.from_dataframe(gdf, use_index=True)
    elif kind == "knn":
        # use projected centroids (EPSG:5254 / TM30) for distances
        pts = gdf.to_crs(5254).copy()
        pts["geometry"] = pts.geometry.centroid
        w = KNN.from_dataframe(pts, k=k, use_index=True)
    else:
        raise ValueError(f"unknown weights type: {kind}")
    if w.islands:
        raise ValueError(f"islands in weights matrix: {w.islands}")
    w.transform = "r"
    return w


def global_moran(y, w) -> dict:
    """Global Moran's I with permutation inference."""
    np.random.seed(SEED)
    m = Moran(np.asarray(y, dtype=float), w, permutations=PERMUTATIONS)
    return {"I": m.I, "EI": m.EI, "z_sim": m.z_sim, "p_sim": m.p_sim}


def bivariate_moran(x, y, w) -> dict:
    """Bivariate Moran's I: x at i vs. spatial lag of y around i."""
    np.random.seed(SEED)
    m = Moran_BV(np.asarray(x, float), np.asarray(y, float), w, permutations=PERMUTATIONS)
    return {"I": m.I, "z_sim": m.z_sim, "p_sim": m.p_sim}


def lisa_clusters(y, w) -> pd.DataFrame:
    """Local Moran's I and cluster labels (HH, LH, LL, HL) at the chosen alpha."""
    lm = Moran_Local(np.asarray(y, dtype=float), w, permutations=PERMUTATIONS, seed=SEED)
    sig = lm.p_sim < ALPHA
    code = np.where(sig, lm.q, 0)
    return pd.DataFrame({
        "Ii": lm.Is,
        "p_sim": lm.p_sim,
        "quadrant": lm.q,
        "cluster_code": code,
        "cluster": [CLUSTER_LABELS[c] for c in code],
    })
