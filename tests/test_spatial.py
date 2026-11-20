"""Sanity checks for the spatial statistics on a regular grid (no real data needed)."""
import sys
from pathlib import Path
import numpy as np
import geopandas as gpd
from shapely.geometry import box
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.spatial import build_weights, global_moran, lisa_clusters, CLUSTER_LABELS


def grid(n=10):
    return gpd.GeoDataFrame(geometry=[box(i, j, i + 1, j + 1) for i in range(n) for j in range(n)])


def test_queen_weights_row_standardised():
    w = build_weights(grid(), "queen")
    assert w.n == 100
    assert np.allclose([sum(v) for v in w.weights.values()], 1.0)


def test_gradient_gives_strong_positive_autocorrelation():
    g = grid()
    y = g.geometry.centroid.x.values            # smooth west-east gradient
    res = global_moran(y, build_weights(g, "queen"))
    assert res["I"] > 0.7 and res["p_sim"] < 0.01


def test_random_noise_close_to_expectation():
    g = grid()
    y = np.random.default_rng(0).normal(size=len(g))
    res = global_moran(y, build_weights(g, "queen"))
    assert abs(res["I"] - res["EI"]) < 0.15 and res["p_sim"] > 0.01


def test_lisa_labels_valid_and_gradient_has_hh_and_ll():
    g = grid()
    y = g.geometry.centroid.x.values
    out = lisa_clusters(y, build_weights(g, "queen"))
    assert set(out["cluster"]) <= set(CLUSTER_LABELS.values())
    assert {"High-High", "Low-Low"} <= set(out["cluster"])
