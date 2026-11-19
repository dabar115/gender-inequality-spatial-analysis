# Gender Inequality and Economic Development in Turkey
### A Provincial-Level Exploratory Spatial Data Analysis (2009–2018)

This repository reproduces the empirical part of my master's thesis at **Bursa Uludağ University (M.Sc. Economics, 2021)**:
*"Cinsiyet Eşitsizliği ve Ekonomik Kalkınma: Türkiye'de İller Düzeyinde Mekânsal Veri Analizi"*.

📄 **Published thesis:** [ProQuest Dissertations & Theses](https://www.proquest.com/openview/fcc8907c51e90d992a96ea3fc87c7e4d/1?pq-origsite=gscholar&cbl=2026366&diss=y)

> **Note on provenance.** The original analysis in 2021 was carried out in **GeoDa**. In 2026 I rebuilt the full
> workflow in **Python (PySAL / esda)** so that it is scripted, version-controlled and reproducible.
> The script `03_global_moran.py` compares the reproduced Moran's I values with the values reported in the thesis
> (`docs/thesis_reference_moran.csv`) and writes the differences to `outputs/tables/validation_vs_thesis.csv`.

---

## Research question
Do indicators of gender inequality and economic development cluster in space across Turkey's 81 provinces –
and did these spatial patterns change between 2009 and 2018?

## Data (81 provinces × 2009–2018)
| Code | Indicator | Source |
|---|---|---|
| `EGT_KAD` | Women 25+ with at least upper-secondary education (%) | TÜİK |
| `EGT_ESZ` | Gender gap in education (female – male share, 25+) | TÜİK |
| `ERG_DOG` | Adolescent fertility (births < 19 per 1,000 births) | TÜİK |
| `KIST` | Women's share of insured employment (%) | SGK |
| `KBGDO` | GDP per capita (USD) | TÜİK |

The indicator selection follows the UNDP Gender Inequality Index (health, education, labour market) as far as data
is available at province level.

### Data availability
This repository publishes the **methodology and code only**. The province-level dataset used in the thesis is kept
private and is **not** part of the repository (`data/` is excluded via `.gitignore`). The expected input format is
documented in `data/raw/README.md`, so the workflow can be run with the same variables from the original sources
(TÜİK, SGK). Aggregate results are reported in the published thesis.

## Methods
1. **Spatial weights** – queen contiguity, row-standardised (Turkish provinces are all contiguous; see Gezici & Hewings 2007).
2. **Global Moran's I** – spatial autocorrelation per indicator and year, permutation inference (9,999 permutations, fixed seed).
3. **Local Moran's I (LISA)** – High-High, Low-Low, High-Low and Low-High clusters at p < 0.05.
4. **Extensions added in 2026** (not in the original thesis):
   - robustness of Moran's I to the choice of weights (queen vs. 5 / 8 nearest neighbours),
   - bivariate Moran's I between GDP per capita and the spatial lag of each gender indicator.

## Main findings of the thesis
- All indicators show **significant positive spatial autocorrelation in every year** (Moran's I between 0.33 and 0.68, p = 0.0001).
- Spatial dependence **increased** from 2009 to 2018 for all indicators except female education → regional divergence.
- LISA maps show a persistent **west–east divide**: High-High clusters of income and female education in the west,
  Low-Low clusters in the east and south-east; the education gender gap forms a High-High cluster in the south-east.

## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# place data/raw/provincial_indicators.csv (format: data/raw/README.md)
make            # or run scripts/00 … 05 in order
```

## Repository structure
```
├── data/            raw/ (not committed) · geo/ (downloaded boundaries) · processed/
├── docs/            thesis_reference_moran.csv – values reported in the thesis (Table 3.2)
├── figures/         distribution maps and LISA cluster maps
├── outputs/tables/  Moran's I tables, LISA cluster lists, validation, extensions
├── scripts/         00_download … 05_extensions (run in order)
└── src/             config.py · spatial.py (weights, Moran's I, LISA)
```

---

## Kurzfassung (Deutsch)
Das Repository reproduziert den empirischen Teil meiner Masterarbeit (Uludağ-Universität, 2021) zu
**Geschlechterungleichheit und wirtschaftlicher Entwicklung in den 81 Provinzen der Türkei (2009–2018)**.
Veröffentlicht wird nur die Methodik (Code); der Datensatz bleibt privat. Die ursprüngliche Analyse wurde in GeoDa durchgeführt; 2026 habe ich sie in Python (PySAL/esda) vollständig
skriptbasiert und reproduzierbar nachgebaut und die Ergebnisse mit den Werten der Arbeit abgeglichen.
Methoden: räumliche Gewichtungsmatrix (Queen), globales Moran's I mit Permutationstest, LISA-Cluster (p < 0,05),
dazu als Erweiterung Robustheitstests verschiedener Gewichtungen und bivariates Moran's I.
Zentrales Ergebnis: deutliche, über die Zeit zunehmende räumliche Abhängigkeit und ein stabiles West-Ost-Gefälle.

## Thesis
[Full text on ProQuest](https://www.proquest.com/openview/fcc8907c51e90d992a96ea3fc87c7e4d/1?pq-origsite=gscholar&cbl=2026366&diss=y)

## Author
**Danis Baran** – M.Sc. Economics (Uludağ University), M.Sc. Economics student at Heinrich Heine University Düsseldorf
· [LinkedIn](https://linkedin.com/in/danisbaran) · [GitHub](https://github.com/dabar115)

## References (selection)
Anselin, L. (1995). Local indicators of spatial association – LISA. *Geographical Analysis*, 27(2).
Gezici, F. & Hewings, G. (2007). Spatial analysis of regional inequalities in Turkey. *European Planning Studies*, 15(3).
Le Gallo, J. & Ertur, C. (2003). Exploratory spatial data analysis of the distribution of regional per capita GDP in Europe. *Papers in Regional Science*, 82.
