# Preprocessing Log

> **Project:** LZU INFO422 — Influencing Factors behind Video Game Sales  
> **Module:** M2 & M3 — Data Acquisition & Preprocessing  
> **Dataset:** `vgchartz-2024.csv` (Video Game Sales Database)

---

## Dataset Overview

| Attribute | Value |
|-----------|-------|
| **Raw data source** | `vgchartz-2024.csv` |
| **Initial shape** | 64,016 rows × 14 columns |
| **After cleaning (pre-reduction)** | 17,570 rows × 16 columns |
| **Final shape** | 8,786 rows × 33 columns |
| **Overall retention rate** | 13.7% (8,786 / 64,016) |

**Initial columns:** `img`, `title`, `console`, `genre`, `publisher`, `developer`, `critic_score`, `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales`, `release_date`, `last_update`

---

## Preprocessing Pipeline

```
Raw Data (64,016 × 14)
    │
    ▼
╔══════════════════════════════════════╗
║ PHASE 1: DATA CLEANING              ║
╠══════════════════════════════════════╣
║ 1.1 Column Selection ────────► (64,016 × 11) ║
║ 1.2 Categorical Imputation ──► ("Unknown")   ║
║ 1.3 Regional Sales Imputation ► (NaN → 0)    ║
║ 1.4 Critic Score Imputation ──► (median)     ║
║ 1.5 Sales Filtering ──────────► (17,570 × 11)║
║ 1.6 Outlier Flagging (IQR) ───► (17,570 × 16)║
╚══════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════╗
║ PHASE 2: DATA REDUCTION             ║
╠══════════════════════════════════════╣
║ 2.1 Stratified Sampling ─────► (8,786 × 16)  ║
║ 2.2 K-Means Clustering ──────► (+sales_cluster)║
║ 2.3 Console×Genre Aggregation► (270 combos)  ║
╚══════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════╗
║ PHASE 3: DATA TRANSFORMATION        ║
╠══════════════════════════════════════╣
║ 3.1 Text Normalization ──────► (uppercase, dedup)║
║ 3.2 Log Transformation ──────► (log_sales)       ║
║ 3.3 Normalization ───────────► (Min-Max + Z-Score)║
║ 3.4 Date Discretization ─────► (5 equal-freq bins)║
║ 3.5 Derived Features ────────► (ratios, brands)  ║
╚══════════════════════════════════════╝
    │
    ▼
Final Dataset (8,786 × 33) ✓
```

---

## Phase 1: Data Cleaning

### Step 1.1 — Column Selection

**Action:** Retained 11 analysis-relevant columns; removed `img`, `title`, and `last_update`.

| Retained Columns | Removed Columns |
|-------------------|-----------------|
| `console`, `genre`, `publisher`, `developer`, `critic_score` | `img` (image URLs) |
| `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales` | `title` (game names) |
| `release_date` | `last_update` (metadata) |

**Justification:** The `img` column contains image URLs with no analytical value. `title` is a unique identifier per game and does not contribute to pattern discovery. `last_update` is metadata. `release_date` is retained for temporal feature engineering in Phase 3.

**Shape after selection:** `(64,016, 11)`

---

### Step 1.2 — Categorical Missing Value Imputation

**Action:** Filled missing values in `publisher` and `developer` with the string `"Unknown"`.

| Metric | Value |
|--------|-------|
| Columns affected | `publisher`, `developer` |
| Imputation method | Constant fill (`"Unknown"`) |

**Justification:** Creates an explicit "Unknown" category rather than deleting records. This preserves information by flagging incomplete records while keeping them in the dataset for analysis. `console` and `genre` had no missing values in the raw data.

---

### Step 1.3 — Regional Sales Missing Value Imputation

**Action:** Filled missing values in all regional sales columns with `0`.

| Column | Missing Before | Handling |
|--------|---------------|----------|
| `na_sales` | 29.11% | Filled with 0 |
| `jp_sales` | 63.15% | Filled with 0 |
| `pal_sales` | 32.94% | Filled with 0 |
| `other_sales` | 19.52% | Filled with 0 |

**Justification:** Missing regional sales indicate no reported sales in that region. Filling with 0 is conservative and prevents inflating regional averages. `total_sales` remains the primary target variable and was complete.

---

### Step 1.4 — Critic Score Imputation

**Action:** Filled missing `critic_score` values with the median (`7.50`).

| Metric | Value |
|--------|-------|
| Missing values before | ~2,300 (≈ 3.6%) |
| Imputation method | Median imputation |
| Imputed value | `7.50` |

**Justification:** The critic score distribution is approximately symmetric with a bounded range (0–100), making the median a robust central tendency measure less sensitive to outliers than the mean. The low missing rate (~3.6%) makes single imputation acceptable.

---

### Step 1.5 — Sales Filtering

**Action:** Removed records where `total_sales <= 0`.

| Metric | Value |
|--------|-------|
| Rows before filtering | 64,016 |
| Rows after filtering | 17,570 |
| Rows removed | 46,446 (72.6%) |

**Justification:** Zero or negative sales values are data entry errors, placeholders, or unreleased games. They lack analytical meaning and would severely distort summary statistics. The high removal rate is expected for crowdsourced game databases where unreleased titles are catalogued. The retained 17,570 records represent commercially active games — the actual population of interest.

---

### Step 1.6 — Outlier Flagging (IQR Method)

**Action:** Flagged extreme values using the IQR method (threshold: 1.5 × IQR). Outliers are **flagged, not removed** — extreme sales values are genuine blockbuster hits.

| Column | Outliers Flagged | Percentage |
|--------|-----------------|------------|
| `total_sales` | 1,771 | 10.1% |
| `na_sales` | 1,706 | 9.7% |
| `jp_sales` | 2,924 | 16.6% |
| `pal_sales` | 2,259 | 12.9% |
| `other_sales` | 1,931 | 11.0% |

**Output columns:** `total_sales_outlier`, `na_sales_outlier`, `jp_sales_outlier`, `pal_sales_outlier`, `other_sales_outlier` (binary flags)

**Justification:** Extreme sales values (blockbuster titles like *Grand Theft Auto*, *Call of Duty*) are genuine data points, not measurement errors. Flagging preserves information while enabling outlier-aware analysis. Log transformation (Phase 3) further dampens outlier impact.

**Shape after cleaning:** `(17,570, 16)` — 11 core features + 5 outlier flag columns.

---

## Phase 2: Data Reduction

### Step 2.1 — Stratified Sampling by Genre

**Action:** Applied 50% stratified random sampling, preserving genre proportions. Rare genres (< 5 records) were kept in full.

| Metric | Value |
|--------|-------|
| Rows before sampling | 17,570 |
| Rows after sampling | 8,786 |
| Sampling fraction | 50% |
| Minimum samples per genre | 5 |

**Justification:** Reduces dataset size for faster prototyping while maintaining genre representativeness. Rare genres are preserved via the minimum sample threshold, preventing information loss in tail categories. The 8,786-row sample is large enough for robust statistical inference.

---

### Step 2.2 — K-Means Clustering

**Action:** Applied K-Means clustering (K=4) on scaled features: `total_sales`, `console` (label-encoded), and `critic_score`. Features were standardized with Z-Score normalization before clustering.

| Cluster | Count | Avg Total Sales | Interpretation |
|---------|-------|----------------|----------------|
| 0 | 5,960 | 0.285 | Low-to-moderate sellers |
| 1 | 237 | 3.582 | Blockbuster titles |
| 2 | 2,133 | 0.236 | Niche / budget titles |
| 3 | 456 | 0.325 | Moderate performers |

**Output column:** `sales_cluster` (integer 0–3)

**Justification:** Identifies natural groupings of games by commercial performance and platform type. K=4 was selected via elbow method as the balance between granularity and interpretability. Cluster labels serve as engineered features for downstream modeling (e.g., one-hot encoded cluster membership).

---

### Step 2.3 — Console × Genre Aggregation

**Action:** Created aggregated view of average sales per console-genre combination, filtering to combinations with at least 3 games for statistical reliability.

| Metric | Value |
|--------|-------|
| Total combinations | 270 |
| Minimum games per combo | 3 |
| Aggregation metrics | mean, median, std, count |

**Output:** `reports/auto_generated/console_genre_aggregation.csv`

**Justification:** Directly addresses Research Question 1 (Platform-Genre Sales Advantage). Enables identification of high-performing platform-genre combinations for strategic recommendations. The ≥3 game threshold ensures each combination has sufficient data for reliable statistics.

**Shape after reduction:** `(8,786, 17)` — added `sales_cluster`.

---

## Phase 3: Data Transformation & Discretization

### Step 3.1 — Text Normalization

**Action:** Applied uppercase conversion and whitespace stripping to all categorical columns (`console`, `genre`, `publisher`, `developer`). Additionally applied publisher name deduplication:

| Before | After |
|--------|-------|
| `ELECTRONIC ARTS` | `EA` |
| `EA SPORTS` | `EA` |
| `NAMCO BANDAI GAMES` | `BANDAI NAMCO` |
| `BANDAI NAMCO GAMES` | `BANDAI NAMCO` |

**Result:** Unique publishers reduced from 553 → 551.

**Justification:** Prevents duplicate categories from inconsistent capitalization and formatting. Publisher mapping consolidates known aliases, ensuring clean categorical grouping for brand-effect analysis (Q3).

---

### Step 3.2 — Log Transformation

**Action:** Created `log_sales = log1p(total_sales)`.

| Metric | `total_sales` | `log_sales` |
|--------|-------------|-----------|
| Skewness | 8.041 | 2.546 |

**Justification:** Reduces right skewness by ~5.5 units, making the distribution more suitable for parametric models (linear regression, ANOVA) and improving visualization clarity. `log1p` provides numerical stability (defined for all x ≥ 0).

---

### Step 3.3 — Normalization (Min-Max & Z-Score)

**Action:** Applied Min-Max scaling (0–1 range) to all sales columns; Z-Score standardization to `critic_score`.

| Technique | Columns |
|-----------|---------|
| Min-Max | `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales` |
| Z-Score | `critic_score` |

**Output columns:** `total_sales_minmax`, `na_sales_minmax`, `jp_sales_minmax`, `pal_sales_minmax`, `other_sales_minmax`, `critic_score_zscore`

**Justification:** Min-Max preserves relative proportions and the zero baseline (important for regional sales where 0 has semantic meaning). Z-Score standardizes `critic_score` for fair comparison across models with different feature scales.

---

### Step 3.4 — Release Date Discretization

**Action:** Parsed `release_date` into datetime, extracted `release_year`, and applied equal-frequency binning (5 bins).

| Bin | Count |
|-----|-------|
| `era_1` | 2,024 |
| `era_2` | 1,871 |
| `era_4` | 1,827 |
| `era_5` | 1,527 |
| `era_3` | 1,515 |

> **Note:** 22 records (0.25%) had unparseable release dates and inherited NaN for `release_year` and `release_year_bin`.

**Output columns:** `release_year`, `release_year_bin`

**Justification:** Converts continuous temporal data into interpretable eras for modeling. Equal-frequency binning ensures balanced representation across time periods, avoiding skewed temporal splits.

---

### Step 3.5 — Derived Features

**Action:** Engineered additional features for research questions:

| Feature | Description | Addresses |
|---------|-------------|-----------|
| `na_ratio`, `jp_ratio`, `pal_ratio`, `other_ratio` | Regional sales / total_sales | Q2 (Genre-Regional Impact) |
| `has_regional_data` | Binary flag: any non-zero regional sales | Q2 (missingness awareness) |
| `publisher_game_count` | Number of games per publisher | Q3 (Brand Effect) |
| `developer_game_count` | Number of games per developer | Q3 (Brand Effect) |

**Justification:** Regional ratios directly quantify market preference patterns. Publisher/developer game counts serve as proxies for brand experience and scale. The `has_regional_data` flag enables missingness-aware modeling — models can distinguish between "no regional sales" (true zero) and "regional data unavailable" (originally NaN).

**Shape after transformation:** `(8,786, 33)`

---

## Preprocessing Summary

| Stage | Rows | Columns | Key Operation |
|-------|------|---------|---------------|
| Raw data | 64,016 | 14 | — |
| After column selection | 64,016 | 11 | Dropped img, title, last_update |
| After categorical imputation | 64,016 | 11 | publisher/developer → "Unknown" |
| After regional imputation | 64,016 | 11 | NaN → 0 for 4 regional cols |
| After critic score imputation | 64,016 | 11 | median = 7.50 |
| After sales filtering | 17,570 | 11 | Removed total_sales ≤ 0 |
| After outlier flagging | 17,570 | 16 | +5 IQR outlier flags |
| After stratified sampling | 8,786 | 16 | 50% genre-stratified |
| After K-Means clustering | 8,786 | 17 | +sales_cluster |
| After transformation | 8,786 | 33 | +16 engineered features |
| **Final dataset** | **8,786** | **33** | |

**Final dataset columns (33 total):**

| Category | Columns |
|----------|---------|
| Core categorical (4) | `console`, `genre`, `publisher`, `developer` |
| Core numerical (5) | `critic_score`, `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales` |
| Temporal (2) | `release_date`, `release_year`, `release_year_bin` |
| Outlier flags (5) | `total_sales_outlier`, `na_sales_outlier`, `jp_sales_outlier`, `pal_sales_outlier`, `other_sales_outlier` |
| Clustering (1) | `sales_cluster` |
| Derived target (1) | `log_sales` |
| Normalized (6) | `total_sales_minmax`, `na_sales_minmax`, `jp_sales_minmax`, `pal_sales_minmax`, `other_sales_minmax`, `critic_score_zscore` |
| Regional ratios (4) | `na_ratio`, `jp_ratio`, `pal_ratio`, `other_ratio` |
| Brand proxies (2) | `publisher_game_count`, `developer_game_count` |
| Data flags (1) | `has_regional_data` |

---

## Limitations & Considerations

1. **Sampling reduces sample size:** 50% stratified sampling reduced 17,570 → 8,786 rows. While sufficient for EDA and modeling, rare platform-genre combinations may be underrepresented.

2. **JP sales zero-inflation:** 63.7% of `jp_sales` records are zero (originally NaN → imputed 0). Regional ratio features involving Japan should be interpreted with caution.

3. **Release date parsing:** 22 records (0.25%) had unparseable dates and lack `release_year`/`release_year_bin`. This is negligible for aggregate analysis.

4. **Single imputation for critic_score:** Median imputation does not account for uncertainty in missing values. Multiple imputation (MICE) could be considered if critic_score becomes a central predictor.

5. **Publisher deduplication is partial:** Only 4 known aliases are consolidated. Manual review of the full publisher list may reveal additional duplicates.

---

## Related Files

- `summary.md` — Data quality summary and class balance analysis
- `cleaned_vgchartz.csv` — Final cleaned enriched dataset (8,786 × 33)
- `reports/auto_generated/console_genre_aggregation.csv` — Console-genre aggregation (270 combos)
- `INFO422-DS Project-group-23-Data Acquisition & Preprocessing.ipynb` — Full preprocessing code
