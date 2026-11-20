# Methodology

## 1. Spatial weights
Spatial dependence requires a definition of "neighbour". For the 81 Turkish provinces the thesis uses
**queen contiguity**: provinces *i* and *j* are neighbours if they share a border or a vertex
(w<sub>ij</sub> = 1, otherwise 0). All Turkish provinces are contiguous, so no province is left without
neighbours, and queen and rook contiguity give very similar results (Gezici & Hewings, 2007).
The matrix **W** (81 × 81) is **row-standardised**, so the spatial lag Σ<sub>j</sub> w<sub>ij</sub> x<sub>j</sub>
is the average of the neighbours' values.

## 2. Global Moran's I
For a variable *x* in year *t*, with deviations from the mean *z<sub>i</sub>*:

I = (n / S<sub>0</sub>) · Σ<sub>i</sub> Σ<sub>j</sub> w<sub>ij</sub> z<sub>i</sub> z<sub>j</sub> / Σ<sub>i</sub> z<sub>i</sub>²,
with S<sub>0</sub> = Σ<sub>i</sub> Σ<sub>j</sub> w<sub>ij</sub> (= n for row-standardised W).

- H<sub>0</sub>: no spatial autocorrelation (values are randomly distributed across provinces).
- Values close to +1 → similar values cluster; close to −1 → dissimilar values are neighbours;
  E[I] = −1/(n−1) ≈ −0.0125 under H<sub>0</sub>.

**Inference by permutation.** The observed values are randomly re-assigned to provinces 9,999 times and I is
recomputed each time. The pseudo p-value is (number of permuted I ≥ observed I + 1) / (9,999 + 1); the smallest
attainable value is 0.0001 – the significance level reported in the thesis. A fixed random seed makes the
inference reproducible.

## 3. Local Moran's I (LISA)
I<sub>i</sub> = z<sub>i</sub> · Σ<sub>j</sub> w<sub>ij</sub> z<sub>j</sub> (Anselin, 1995) decomposes the global statistic by province.
Combining the sign of z<sub>i</sub> and of its spatial lag gives four types (Moran scatterplot quadrants):

| Type | Province | Neighbours | Interpretation |
|---|---|---|---|
| High-High | above mean | above mean | hot spot |
| Low-Low | below mean | below mean | cold spot |
| High-Low | above mean | below mean | spatial outlier |
| Low-High | below mean | above mean | spatial outlier |

Only provinces with a conditional-permutation pseudo p-value < 0.05 are shown on the cluster maps.
Because 81 local tests are run at once, single significant provinces should be read with caution
(multiple-testing problem); the thesis therefore focuses on larger, stable clusters.

## 4. Extensions in the 2026 reproduction
- **Robustness:** Moran's I under queen contiguity and under 5 / 8 nearest neighbours (distances between
  projected province centroids, EPSG:5254).
- **Bivariate Moran's I:** correlation between GDP per capita in province *i* and the average gender indicator of
  its neighbours – a first look at whether development and gender inequality overlap in space.

## 5. Limitations
- ESDA is descriptive: it shows spatial patterns, not causal effects.
- Results depend on the definition of W; the robustness check addresses this partly.
- Province-level averages can hide large differences within provinces (MAUP / ecological fallacy).
- Natural next steps: spatial regression models (spatial lag / spatial error) and panel models with spatial effects.
