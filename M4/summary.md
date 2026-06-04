# Data Quality Summary

> **Project:** LZU INFO422 — Influencing Factors behind Video Game Sales  
> **Module:** M2 & M3 — Data Quality Assessment  
> **Dataset:** `cleaned_vgchartz.csv` (Post-preprocessing, enriched)

---

## Executive Summary

The cleaned enriched dataset comprises **8,786 video game records** across **33 features** after a full three-phase preprocessing pipeline (cleaning → reduction → transformation). Overall data quality is **excellent for core features** with only 0.25% residual missingness (limited to temporal features). Engineered features (outlier flags, clusters, normalized columns, ratios, brand proxies) are fully populated and ready for exploratory analysis and modeling.

| Quality Dimension | Assessment | Risk Level |
|-------------------|------------|------------|
| Core feature completeness | Excellent (0% missing) | Green (Low) |
| Engineered feature completeness | Excellent (0% missing) | Green (Low) |
| Temporal feature completeness | Good (0.25% missing) | Yellow (Medium) |
| Class balance (console) | Moderate imbalance | Yellow (Medium) |
| Class balance (genre) | Moderate imbalance | Yellow (Medium) |
| Outlier presence | Flagged, not removed | Green (Low) |

---

## 1. Null Rates (Final Dataset)

| Column | Non-Null Count | Null Count | Null % | Impact Assessment |
|--------|---------------|------------|--------|-------------------|
| `console` | 8,786 | 0 | 0.00% | Complete — primary grouping variable |
| `genre` | 8,786 | 0 | 0.00% | Complete — primary grouping variable |
| `publisher` | 8,786 | 0 | 0.00% | Complete (imputed: "Unknown" for missing) |
| `developer` | 8,786 | 0 | 0.00% | Complete (imputed: "Unknown" for missing) |
| `critic_score` | 8,786 | 0 | 0.00% | Complete (imputed: median 7.50) |
| `total_sales` | 8,786 | 0 | 0.00% | Complete — primary target variable |
| `na_sales` | 8,786 | 0 | 0.00% | Complete (imputed: 0 for missing) |
| `jp_sales` | 8,786 | 0 | 0.00% | Complete (imputed: 0 for missing) |
| `pal_sales` | 8,786 | 0 | 0.00% | Complete (imputed: 0 for missing) |
| `other_sales` | 8,786 | 0 | 0.00% | Complete (imputed: 0 for missing) |
| `release_date` | 8,764 | 22 | 0.25% | Negligible — 22 unparseable dates |
| `release_year` | 8,764 | 22 | 0.25% | Negligible — derived from release_date |
| `release_year_bin` | 8,764 | 22 | 0.25% | Negligible — derived from release_year |
| All outlier flags (5) | 8,786 | 0 | 0.00% | Complete |
| `sales_cluster` | 8,786 | 0 | 0.00% | Complete |
| `log_sales` | 8,786 | 0 | 0.00% | Complete — derived target variable |
| All normalized columns (6) | 8,786 | 0 | 0.00% | Complete |
| All regional ratios (4) | 8,786 | 0 | 0.00% | Complete |
| All brand proxies (2) | 8,786 | 0 | 0.00% | Complete |
| `has_regional_data` | 8,786 | 0 | 0.00% | Complete |

### Key Observations on Missingness

**Regional Sales Zero-Inflation (Post-Imputation):**

Filling original NaN values with 0 resulted in zero-inflated regional columns:

| Column | % Zero | Origin |
|--------|--------|--------|
| `na_sales` | 29.50% | Originally NaN → imputed 0 |
| `jp_sales` | 63.70% | Originally NaN → imputed 0 |
| `pal_sales` | 39.75% | Originally NaN → imputed 0 |
| `other_sales` | 42.62% | Originally NaN → imputed 0 |

This is a known consequence of conservative imputation. The `has_regional_data` flag (binary) was explicitly created to distinguish genuine zero-sales from imputed zeros. Any model using regional sales should either (a) include this flag, or (b) use `total_sales` as the primary target.

**Temporal Missingness:** 22 records (0.25%) had unparseable `release_date` values. These lack `release_year` and `release_year_bin`. This is negligible for aggregate temporal analysis.

---

## 2. Class Balance

### 2.1 Console Distribution

| Rank | Console | Count | % of Dataset |
|:----:|:--------|------:|:------------:|
| 1 | DS | 1,055 | 12.0% |
| 2 | PS2 | 1,054 | 12.0% |
| 3 | WII | 699 | 8.0% |
| 4 | X360 | 637 | 7.3% |
| 5 | PS3 | 629 | 7.2% |
| 6 | PSP | 607 | 6.9% |
| 7 | PS | 571 | 6.5% |
| 8 | PC | 492 | 5.6% |
| 9 | PS4 | 468 | 5.3% |
| 10 | XB | 413 | 4.7% |
| 11 | GBA | 407 | 4.6% |
| 12 | PSV | 317 | 3.6% |
| 13 | 3DS | 289 | 3.3% |
| 14 | GC | 261 | 3.0% |
| 15 | XONE | 262 | 3.0% |
| … | *(18 others)* | *625* | *7.1%* |

**Console Balance Assessment:**

- **Top 5 consoles** account for **46.5%** of records.
- **Top 15 consoles** account for **92.9%**.
- **33 unique platforms** total (2 fewer than pre-sampling due to sampling from rare platforms).
- Distribution shape largely preserved from the unsampled dataset.

**Implications:** Models predicting sales by console will be biased toward Nintendo DS/PS2-era platforms. Rare platforms (< 10 records) may need grouping or exclusion in per-platform analyses.

---

### 2.2 Genre Distribution

| Rank | Genre | Count | % of Dataset |
|:----:|:------|------:|:------------:|
| 1 | ACTION | 1,343 | 15.3% |
| 2 | SPORTS | 1,242 | 14.1% |
| 3 | MISC | 917 | 10.4% |
| 4 | ADVENTURE | 841 | 9.6% |
| 5 | ROLE-PLAYING | 707 | 8.0% |
| 6 | SHOOTER | 688 | 7.8% |
| 7 | RACING | 674 | 7.7% |
| 8 | SIMULATION | 502 | 5.7% |
| 9 | PLATFORM | 451 | 5.1% |
| 10 | FIGHTING | 428 | 4.9% |
| 11 | STRATEGY | 346 | 3.9% |
| 12 | PUZZLE | 315 | 3.6% |
| 13 | ACTION-ADVENTURE | 128 | 1.5% |
| 14 | VISUAL NOVEL | 98 | 1.1% |
| 15 | MUSIC | 69 | 0.8% |
| 16 | MMO | 15 | 0.2% |
| 17 | PARTY | 14 | 0.2% |
| 18 | EDUCATION | 2 | 0.02% |
| 19 | BOARD GAME | 2 | 0.02% |
| 20 | SANDBOX | 1 | 0.01% |

**Genre Balance Assessment:**

- **Top 3 genres** (ACTION, SPORTS, MISC) account for **39.8%** of the dataset.
- **Top 7 genres** account for **70.7%**.
- **Tail genres** (MMO, PARTY, EDUCATION, BOARD GAME, SANDBOX) collectively represent **< 1%**.
- Distribution nearly identical to the unsampled dataset — stratified sampling was effective.

**Implications:** Genre-based analyses have sufficient data for major categories but rare genres will produce unreliable statistics. SANDBOX (1 record), BOARD GAME (2), EDUCATION (2) should be excluded or grouped into an "Other" category for per-genre models.

---

### 2.3 K-Means Cluster Distribution

| Cluster | Count | % of Dataset | Avg Total Sales | Interpretation |
|:-------:|------:|:------------:|:---------------:|:---------------|
| 0 | 5,960 | 67.8% | 0.285 | Low-to-moderate sellers |
| 2 | 2,133 | 24.3% | 0.236 | Niche / budget titles |
| 3 | 456 | 5.2% | 0.325 | Moderate performers |
| 1 | 237 | 2.7% | 3.582 | Blockbuster titles |

**Implication:** The target variable (`total_sales`) is **extremely imbalanced** across clusters. 92.1% of games fall into low-sales clusters (0 + 2) while only 2.7% are blockbusters. This heavy-tailed distribution is characteristic of the "hit-driven" video game industry and motivates the log transformation for modeling.

---

## 3. Outlier Treatment

### 3.1 Sales Variables

| Variable | Treatment Applied | Rationale |
|----------|-------------------|-----------|
| `total_sales` | IQR flagging; no removal | Blockbusters are genuine data, not errors |
| `na_sales` | IQR flagging; no removal | Flagged 1,706 (9.7%) outliers |
| `jp_sales` | IQR flagging; no removal | Flagged 2,924 (16.6%) outliers |
| `pal_sales` | IQR flagging; no removal | Flagged 2,259 (12.9%) outliers |
| `other_sales` | IQR flagging; no removal | Flagged 1,931 (11.0%) outliers |
| `log_sales` | Derived via `log1p` | Reduces impact of extreme blockbuster titles |

**Why no winsorizing/capping?** Extreme sales values are genuine data points (e.g., *Grand Theft Auto*, *Wii Sports*). Capping would artificially compress the distribution and lose information about the hit-driven nature of the industry. Log transformation provides a middle ground — dampening extremes without discarding them. Outlier flags enable outlier-aware modeling when needed.

### 3.2 Critic Score

| Aspect | Status |
|--------|--------|
| Missing values | Imputed with median (7.50) |
| Valid range | Confirmed 1.4–10.0 |
| Distribution | Approximately symmetric |
| Z-Score range | Standardized (mean=0, std=1) available via `critic_score_zscore` |

---

## 4. Data Schema

```
<class 'pandas.core.frame.DataFrame'>
Index: 8786 entries, 0 to 8785
Data columns (total 33 columns):
 #   Column                  Non-Null Count  Dtype
---  ------                  --------------  -----
 0   console                 8786 non-null   object
 1   genre                   8786 non-null   object
 2   publisher               8786 non-null   object
 3   developer               8786 non-null   object
 4   critic_score            8786 non-null   float64
 5   total_sales             8786 non-null   float64
 6   na_sales                8786 non-null   float64
 7   jp_sales                8786 non-null   float64
 8   pal_sales               8786 non-null   float64
 9   other_sales             8786 non-null   float64
10   release_date            8764 non-null   object
11   total_sales_outlier     8786 non-null   int64
12   na_sales_outlier        8786 non-null   int64
13   jp_sales_outlier        8786 non-null   int64
14   pal_sales_outlier       8786 non-null   int64
15   other_sales_outlier     8786 non-null   int64
16   sales_cluster           8786 non-null   int32
17   log_sales               8786 non-null   float64
18   total_sales_minmax      8786 non-null   float64
19   na_sales_minmax         8786 non-null   float64
20   jp_sales_minmax         8786 non-null   float64
21   pal_sales_minmax        8786 non-null   float64
22   other_sales_minmax      8786 non-null   float64
23   critic_score_zscore     8786 non-null   float64
24   release_year            8764 non-null   float64
25   release_year_bin        8764 non-null   category
26   na_ratio                8786 non-null   float64
27   jp_ratio                8786 non-null   float64
28   pal_ratio               8786 non-null   float64
29   other_ratio             8786 non-null   float64
30   has_regional_data       8786 non-null   int64
31   publisher_game_count    8786 non-null   int64
32   developer_game_count    8786 non-null   int64
```

**Data types per column:**

| Column | Dtype | Notes |
|--------|-------|-------|
| `console` | object | Categorical — 33 unique platforms |
| `genre` | object | Categorical — 20 unique genres |
| `publisher` | object | Categorical — 551 unique publishers (after dedup) |
| `developer` | object | Categorical — ~2,500 unique developers |
| `critic_score` | float64 | Continuous — 1.4–10.0 scale |
| `total_sales` | float64 | Continuous — millions of units (0.01–16.15) |
| Regional sales (4) | float64 | Continuous — zero-inflated, in millions |
| `release_date` | object | Datetime string — 0.25% unparseable |
| Outlier flags (5) | int64 | Binary — 0 or 1 |
| `sales_cluster` | int32 | Categorical — 0, 1, 2, 3 |
| `log_sales` | float64 | Continuous — ln(1 + total_sales), range 0.01–2.84 |
| Normalized sales (5) | float64 | Continuous — Min-Max scaled, range [0, 1] |
| `critic_score_zscore` | float64 | Continuous — Z-Score standardized |
| `release_year` | float64 | Ordinal — year extracted from release_date |
| `release_year_bin` | category | Ordinal — 5 equal-frequency bins (era_1 to era_5) |
| Regional ratios (4) | float64 | Continuous — proportion, range [0, 1] |
| `has_regional_data` | int64 | Binary — 1 if any regional sales > 0 |
| Brand proxies (2) | int64 | Discrete — game count per publisher/developer |

---

## 5. Key Insights & Recommendations

### 5.1 For Exploratory Data Analysis (M4)

1. **Sales distribution:** Examine `total_sales` vs `log_sales` distributions. The skewness reduction (8.04 → 2.55) confirms log transform is warranted but further normalization may be needed.
2. **Platform lifecycle:** Cross-reference `release_year_bin` with sales volume to identify platform maturity effects.
3. **Genre-market interaction:** Use `na_ratio`/`jp_ratio`/`pal_ratio`/`other_ratio` to investigate regional genre preferences.
4. **Cluster characterization:** Profile each K-Means cluster by console, genre, and publisher to validate interpretability.

### 5.2 For Predictive Modeling (M5–M6)

1. **Target variable:** Use `log_sales` for regression; `total_sales` for business interpretation.
2. **Feature sets by research question:**
   - Q1 (Platform-Genre): console, genre, sales_cluster, normalized columns
   - Q2 (Regional): genre, regional ratios, has_regional_data
   - Q3 (Brand): publisher, developer, publisher_game_count, developer_game_count
3. **Outlier-aware modeling:** Include `total_sales_outlier` as a feature or use it for stratified evaluation.
4. **High cardinality:** Publisher (551) and developer (~2,500) require target encoding or frequency-based grouping.

### 5.3 Data Quality Red Flags

| Issue | Severity | Recommended Action |
|-------|----------|-------------------|
| ~64% zero `jp_sales` | High (Red) | Flag in all Japan-related conclusions; use `has_regional_data` |
| Genre "MISC" is 10.4% | Medium (Yellow) | Investigate recoding; treat as "Other" if necessary |
| 72.6% data loss in cleaning | Medium (Yellow) | Document: removed records were non-commercial |
| Rare platforms (< 10 records) | Low (Green) | Group into "Other Platforms" |
| 0.25% missing temporal data | Low (Green) | Exclude 22 records in temporal analyses |

---

## Related Files

- `preprocessing.md` — Detailed preprocessing pipeline (3 phases, 14 sub-steps)
- `cleaned_vgchartz.csv` — Final cleaned enriched dataset (8,786 × 33)
- `reports/auto_generated/console_genre_aggregation.csv` — Console-genre aggregation (270 combos)
- `INFO422-DS Project-group-23-Data Acquisition & Preprocessing.ipynb` — Full preprocessing and summary generation code
