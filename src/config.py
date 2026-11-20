"""Central configuration for the analysis (paths, variables, years, settings)."""
from pathlib import Path

import os

ROOT = Path(__file__).resolve().parents[1]

# DEMO=1 runs the whole pipeline on simulated data (data/demo) and writes to figures/demo, outputs/demo.
# Without it, the pipeline expects the (private) thesis data in data/raw.
DEMO = os.environ.get("DEMO") == "1"

RAW = ROOT / "data" / ("demo" if DEMO else "raw")
PROCESSED = ROOT / "data" / ("processed_demo" if DEMO else "processed")
GEO = ROOT / "data" / "geo"
TABLES = ROOT / "outputs" / ("demo" if DEMO else "tables")
FIGURES = ROOT / "figures" / ("demo" if DEMO else "")
WATERMARK = "SIMULATED DATA – NOT THESIS RESULTS" if DEMO else None
DOCS = ROOT / "docs"

YEARS = list(range(2009, 2019))          # analysis period of the thesis
MAP_YEARS = [2009, 2018]                  # years shown on maps

# Variable codes as used in the thesis (Table 3.1)
VARIABLES = {
    "EGT_KAD": "Female educational attainment (%, 25+, at least high school)",
    "EGT_ESZ": "Gender gap in education (female minus male share, 25+)",
    "ERG_DOG": "Adolescent fertility (births <19 per 1,000 births)",
    "KIST":    "Female share of insured employment (%)",
    "KBGDO":   "GDP per capita (USD)",
}

PERMUTATIONS = 9999   # pseudo p-values; GeoDa's minimum p of 0.0001 corresponds to 9,999 permutations
ALPHA = 0.05          # significance level for LISA clusters (as in the thesis)
SEED = 12345          # fixed seed -> reproducible permutation inference

BOUNDARIES_URL = (
    "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json"
)
