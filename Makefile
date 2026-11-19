all:
	python scripts/00_download_boundaries.py
	python scripts/01_prepare_data.py
	python scripts/02_distribution_maps.py
	python scripts/03_global_moran.py
	python scripts/04_lisa_clusters.py
	python scripts/05_extensions.py
