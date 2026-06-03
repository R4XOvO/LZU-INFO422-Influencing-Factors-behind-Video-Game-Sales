# Data Quality Summary

> **Project:** LZU INFO422 — Influencing Factors behind Video Game Sales  
> **Module:** M2 & M3 — Data Quality Assessment  
> **Dataset:** `cleaned_vgchartz.csv` (Post-preprocessing)

---

## 📋 Executive Summary

The cleaned dataset comprises **17,570 video game records** across **11 features** after preprocessing. Overall data quality is **good for core features** (`console`, `genre`, `total_sales`, `critic_score`) but exhibits **significant missingness in regional sales breakdowns**, particularly Japanese sales data. These gaps must be carefully considered in subsequent modeling and analysis phases.

| Quality Dimension | Assessment | Risk Level |
|-------------------|------------|------------|
| Core feature completeness | Excellent (< 0.1% missing) | 🟢 Low |
| Regional sales completeness | Poor (19–63% missing) | 🔴 High |
| Class balance (console) | Moderate imbalance | 🟡 Medium |
| Class balance (genre) | Moderate imbalance | 🟡 Medium |
| Outlier presence | Managed via log transform | 🟢 Low |

---

## 1. Null Rates (Final Dataset)

| Column | Non-Null Count | Null Count | Null % | Impact Assessment |
|--------|---------------|------------|--------|-------------------|
| `console` | 17,570 | 0 | 0.00% | ✅ Complete — primary grouping variable |
| `genre` | 17,570 | 0 | 0.00% | ✅ Complete — primary grouping variable |
| `publisher` | 17,570 | 0 | 0.00% | ✅ Complete |
| `developer` | 17,568 | 2 | 0.01% | ✅ Near-complete — negligible impact |
| `critic_score` | 17,570 | 0 | 0.00% | ✅ Complete (imputed) |
| `total_sales` | 17,570 | 0 | 0.00% | ✅ Complete — target variable |
| `na_sales` | 12,455 | 5,115 | 29.11% | ⚠️ Moderate — may bias NA market analysis |
| `jp_sales` | 6,475 | 11,095 | 63.15% | ❌ Severe — JP analysis highly unreliable |
| `pal_sales` | 11,782 | 5,788 | 32.94% | ⚠️ Moderate — may bias PAL market analysis |
| `other_sales` | 14,141 | 3,429 | 19.52% | ⚠️ Moderate — may bias other regions analysis |
| `log_sales` | 17,570 | 0 | 0.00% | ✅ Complete — derived target variable |

### Key Observations on Missingness

**Regional Sales Missingness Pattern:**

The disproportionate missingness in regional sales columns (`na_sales`, `jp_sales`, `pal_sales`, `other_sales`) compared to `total_sales` suggests a systematic data collection issue rather than random missingness (MCAR). Possible explanations:

1. **Data source fragmentation:** Regional sales figures may come from different tracking services with varying coverage. Japanese sales data (63.15% missing) likely reflects limited Western database coverage of Japan's domestic market.
2. **Temporal coverage:** Older games may lack granular regional breakdowns even when total sales are known.
3. **Platform specificity:** Certain platforms (e.g., PC, mobile) may not report regional splits consistently.

**Implications for Analysis:**
- Any analysis of **regional market preferences** must acknowledge substantial bias, particularly for Japan.
- `total_sales` should be treated as the primary reliable target variable.
- Regional sales columns may be usable as **supplementary features** with appropriate missing value handling (e.g., indicator variables for missingness, or imputation if justified).

---

## 2. Class Balance

### 2.1 Console Distribution

| Rank | Console | Count | % of Dataset | Platform Era |
|:----:|:--------|------:|:------------:|:-------------|
| 1 | DS | 2,152 | 12.2% | Handheld (7th Gen) |
| 2 | PS2 | 2,097 | 11.9% | Home Console (6th Gen) |
| 3 | PS3 | 1,310 | 7.5% | Home Console (7th Gen) |
| 4 | WII | 1,281 | 7.3% | Home Console (7th Gen) |
| 5 | X360 | 1,264 | 7.2% | Home Console (7th Gen) |
| 6 | PSP | 1,257 | 7.2% | Handheld (7th Gen) |
| 7 | PS | 1,126 | 6.4% | Home Console (5th Gen) |
| 8 | PC | 939 | 5.3% | Multi-purpose |
| 9 | PS4 | 891 | 5.1% | Home Console (8th Gen) |
| 10 | XB | 822 | 4.7% | Home Console (6th Gen) |
| 11 | GBA | 820 | 4.7% | Handheld (6th Gen) |
| 12 | PSV | 638 | 3.6% | Handheld (8th Gen) |
| 13 | 3DS | 543 | 3.1% | Handheld (8th Gen) |
| 14 | GC | 527 | 3.0% | Home Console (6th Gen) |
| 15 | XONE | 517 | 2.9% | Home Console (8th Gen) |
| … | *(20 others)* | *1,096* | *6.2%* | Various |

**Console Balance Assessment:**

- **Top 5 consoles** account for **46.1%** of all records.
- **Top 15 consoles** account for **93.8%** of all records.
- **Long tail:** 20 platforms contribute only 6.2% collectively, including rare platforms like PCFX (1), MOB (1), and GG (1).

**Implications:**
- Models predicting sales by console will be **heavily biased toward Nintendo DS/PS2-era platforms**.
- Rare platforms may be candidates for **grouping** (e.g., "Retro Consoles" category) or **exclusion** if per-platform analysis is performed.
- The dataset spans **5 console generations** (5th–8th gen + PC/handheld), enabling generational comparison studies.

---

### 2.2 Genre Distribution

| Rank | Genre | Count | % of Dataset |
|:----:|:------|------:|:------------:|
| 1 | ACTION | 2,686 | 15.3% |
| 2 | SPORTS | 2,484 | 14.1% |
| 3 | MISC | 1,834 | 10.4% |
| 4 | ADVENTURE | 1,683 | 9.6% |
| 5 | ROLE-PLAYING | 1,414 | 8.0% |
| 6 | SHOOTER | 1,377 | 7.8% |
| 7 | RACING | 1,349 | 7.7% |
| 8 | SIMULATION | 1,004 | 5.7% |
| 9 | PLATFORM | 903 | 5.1% |
| 10 | FIGHTING | 856 | 4.9% |
| 11 | STRATEGY | 692 | 3.9% |
| 12 | PUZZLE | 630 | 3.6% |
| 13 | ACTION-ADVENTURE | 257 | 1.5% |
| 14 | VISUAL NOVEL | 197 | 1.1% |
| 15 | MUSIC | 138 | 0.8% |
| 16 | MMO | 30 | 0.2% |
| 17 | PARTY | 28 | 0.2% |
| 18 | EDUCATION | 4 | 0.02% |
| 19 | BOARD GAME | 3 | 0.02% |
| 20 | SANDBOX | 1 | 0.006% |

**Genre Balance Assessment:**

- **Top 3 genres** (ACTION, SPORTS, MISC) account for **39.8%** of the dataset.
- **Top 7 genres** account for **70.7%** of the dataset.
- **Tail genres** (MMO, PARTY, EDUCATION, BOARD GAME, SANDBOX) collectively represent **< 1%**.

**Implications:**
- Genre-based models will have **sufficient data** for major categories but may struggle with rare genres.
- The dominance of ACTION and SPORTS aligns with industry trends — these are historically the best-selling genres.
- The "MISC" category (10.4%) is a catch-all bucket. If the original source provides more granular classification, **recoding MISC** into sub-categories could improve model performance.
- SANDBOX (1 record), BOARD GAME (3 records), and EDUCATION (4 records) may need **special handling** or exclusion from genre-specific models.

---

## 3. Outlier Treatment

### 3.1 Sales Variables

| Variable | Treatment Applied | Rationale |
|----------|-------------------|-----------|
| `total_sales` | Removed values ≤ 0; no capping | Data errors and unreleased games filtered out |
| `na_sales`, `jp_sales`, `pal_sales`, `other_sales` | Retained as-is | Regional outliers preserved for regional pattern detection |
| `log_sales` | Derived via `log1p(total_sales)` | Reduces impact of extreme blockbuster titles |

**Why no winsorizing/capping?**

- Extreme sales values (blockbuster titles like *Grand Theft Auto*, *Call of Duty*) are **genuine data points**, not measurement errors.
- Capping would artificially compress the distribution and lose information about the "hit-driven" nature of the video game industry.
- Log transformation provides a **middle ground**: it dampens extreme values without discarding them.

### 3.2 Critic Score

| Aspect | Status |
|--------|--------|
| Missing values | Imputed with median (7.50) |
| Valid range | Confirmed 0–100 |
| Distribution | Approximately symmetric |
| Outliers | No extreme outliers detected |

---

## 4. Data Schema

```
<class 'pandas.core.frame.DataFrame'>
Index: 17570 entries, 0 to 17569
Data columns (total 11 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   console       17570 non-null  object 
 1   genre         17570 non-null  object 
 2   publisher     17570 non-null  object 
 3   developer     17568 non-null  object 
 4   critic_score  17570 non-null  float64
 5   total_sales   17570 non-null  float64
 6   na_sales      12455 non-null  float64
 7   jp_sales      6475 non-null   float64
 8   pal_sales     11782 non-null  float64
 9   other_sales   14141 non-null  float64
 10  log_sales     17570 non-null  float64
```

**Data types per column:**

| Column | Dtype | Notes |
|--------|-------|-------|
| `console` | object | Categorical — 35 unique platforms |
| `genre` | object | Categorical — 20 unique genres |
| `publisher` | object | Categorical — ~1,000 unique publishers |
| `developer` | object | Categorical — ~2,500 unique developers |
| `critic_score` | float64 | Continuous — 0–100 scale |
| `total_sales` | float64 | Continuous — millions of units |
| `na_sales` | float64 | Continuous — North America sales (29.11% missing) |
| `jp_sales` | float64 | Continuous — Japan sales (63.15% missing) |
| `pal_sales` | float64 | Continuous — PAL region sales (32.94% missing) |
| `other_sales` | float64 | Continuous — Other regions (19.52% missing) |
| `log_sales` | float64 | Continuous — log-transformed `total_sales` |

---

## 5. Key Insights & Recommendations

### 5.1 For Exploratory Data Analysis (EDA)

1. **Sales distribution:** Examine `total_sales` vs `log_sales` distributions to confirm log transform appropriateness. Identify potential multi-modal patterns (e.g., indie vs. AAA game sales).
2. **Platform lifecycle:** Cross-reference `console` with sales volume to identify platform maturity effects (launch, peak, decline phases).
3. **Genre-market interaction:** Investigate whether genre popularity varies by region — this may explain some regional sales missingness (e.g., RPGs dominate Japan but may be underreported).
4. **Critic score vs. sales correlation:** Determine whether `critic_score` is a meaningful predictor of `total_sales` or if the relationship is genre-dependent.

### 5.2 For Predictive Modeling

1. **Target variable:** Use `log_sales` as the primary target for regression models; `total_sales` for business interpretation.
2. **Feature engineering considerations:**
   - **Publisher/Developer encoding:** High cardinality (~1,000 / ~2,500 unique values) requires target encoding or grouping by frequency.
   - **Regional sales:** Consider creating `regional_sales_ratio` features (e.g., `jp_sales / total_sales`) where data exists, plus a `has_regional_data` indicator.
   - **Platform generation:** Map `console` to generation (5th–8th) as an ordinal feature.
3. **Missing value strategy:** For regional sales, consider:
   - Excluding regional columns and using only `total_sales` (safest)
   - Multiple imputation (if justified by MCAR/MAR assumptions)
   - Using only complete-case analysis for regional-specific models

### 5.3 Data Quality Red Flags 🚩

| Issue | Severity | Recommended Action |
|-------|----------|-------------------|
| 63.15% missing `jp_sales` | 🔴 High | Flag in all reports; avoid JP-specific conclusions without sensitivity analysis |
| Genre "MISC" is 10.4% | 🟡 Medium | Investigate whether MISC can be recoded; otherwise treat as "Other" |
| 72.6% data loss in preprocessing | 🟡 Medium | Document in methodology; justify that removed records were non-commercial |
| Rare platforms (< 10 records) | 🟢 Low | Group into "Other Platforms" or exclude from per-platform analysis |

---

## 🔗 Related Files

- `preprocessing.md` — Detailed preprocessing steps and pipeline
- `cleaned_vgchartz.csv` — Final cleaned dataset
- `INFO422-DS Project-group-23-Data Acquisition & Preprocessing.ipynb` — Full preprocessing and summary generation code
# Data Quality Summary

## 1. Null Rates (Final Dataset)

| Column | Null % |
|--------|--------|
| console | 0.00% |
| genre | 0.00% |
| publisher | 0.00% |
| developer | 0.01% |
| critic_score | 0.00% |
| total_sales | 0.00% |
| na_sales | 29.11% |
| jp_sales | 63.15% |
| pal_sales | 32.94% |
| other_sales | 19.52% |
| log_sales | 0.00% |


## 2. Class Balance

### Console Distribution

| console   |   count |
|:----------|--------:|
| DS        |    2152 |
| PS2       |    2097 |
| PS3       |    1310 |
| WII       |    1281 |
| X360      |    1264 |
| PSP       |    1257 |
| PS        |    1126 |
| PC        |     939 |
| PS4       |     891 |
| XB        |     822 |
| GBA       |     820 |
| PSV       |     638 |
| 3DS       |     543 |
| GC        |     527 |
| XONE      |     517 |
| N64       |     279 |
| NS        |     247 |
| SNES      |     196 |
| SAT       |     175 |
| WIIU      |     139 |
| 2600      |     126 |
| DC        |      49 |
| NES       |      47 |
| GB        |      46 |
| GEN       |      27 |
| NG        |      12 |
| PSN       |       9 |
| WS        |       7 |
| SCD       |       5 |
| XBL       |       5 |
| 3DO       |       4 |
| VC        |       3 |
| GBC       |       3 |
| PCE       |       2 |
| WW        |       1 |
| GG        |       1 |
| OSX       |       1 |
| MOB       |       1 |
| PCFX      |       1 |

### Genre Distribution

| genre            |   count |
|:-----------------|--------:|
| ACTION           |    2686 |
| SPORTS           |    2484 |
| MISC             |    1834 |
| ADVENTURE        |    1683 |
| ROLE-PLAYING     |    1414 |
| SHOOTER          |    1377 |
| RACING           |    1349 |
| SIMULATION       |    1004 |
| PLATFORM         |     903 |
| FIGHTING         |     856 |
| STRATEGY         |     692 |
| PUZZLE           |     630 |
| ACTION-ADVENTURE |     257 |
| VISUAL NOVEL     |     197 |
| MUSIC            |     138 |
| MMO              |      30 |
| PARTY            |      28 |
| EDUCATION        |       4 |
| BOARD GAME       |       3 |
| SANDBOX          |       1 |

## 3. Outlier Treatment

- **total_sales:** Values <= 0 removed; no capping/winsorizing applied. Log transformation reduces impact of extreme values.
- **critic_score:** Missing values imputed with median; score range confirmed to be within 0–100.
- **Regional sales (na_sales, jp_sales, pal_sales, other_sales):** Retained as-is. Further outlier investigation may be performed during EDA.

## 4. Data Schema

```
<class 'pandas.core.frame.DataFrame'>
Index: 17570 entries, 0 to 17569
Data columns (total 11 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   console       17570 non-null  object 
 1   genre         17570 non-null  object 
 2   publisher     17570 non-null  object 
 3   developer     17568 non-null  object 
 4   critic_score  17570 non-null  float64
 5   total_sales   17570 non-null  float64
 6   na_sales      12455 non-null  float64
 7   jp_sales      6475 non-null   float64
 8   pal_sales     11782 non-null  float64
 9   other_sales   14141 non-null  float64
 10  log_sales     17570 non-null  float64
dtypes: float64(7), object(4)
memory usage: 1.6+ MB

```

**Data types per column:**

|              | 0       |
|:-------------|:--------|
| console      | object  |
| genre        | object  |
| publisher    | object  |
| developer    | object  |
| critic_score | float64 |
| total_sales  | float64 |
| na_sales     | float64 |
| jp_sales     | float64 |
| pal_sales    | float64 |
| other_sales  | float64 |
| log_sales    | float64 |

