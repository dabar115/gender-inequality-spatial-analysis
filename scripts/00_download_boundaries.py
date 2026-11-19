"""Download Turkish province boundaries (81 provinces) as GeoJSON.

Source: github.com/cihadturhan/tr-geojson (not redistributed in this repo).
"""
import sys, urllib.request
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.config import GEO, BOUNDARIES_URL

GEO.mkdir(parents=True, exist_ok=True)
out = GEO / "tr_provinces.geojson"
urllib.request.urlretrieve(BOUNDARIES_URL, out)
print(f"saved {out}")
