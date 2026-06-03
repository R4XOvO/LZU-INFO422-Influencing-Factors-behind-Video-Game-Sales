# Preprocessing Log

> **Project:** LZU INFO422 — Influencing Factors behind Video Game Sales  
> **Module:** M2 & M3 — Data Acquisition & Preprocessing  
> **Dataset:** `vgchartz-2024.csv` (Video Game Sales Database)

---

## 📊 Dataset Overview

| Attribute | Value |
|-----------|-------|
| **Raw data source** | `vgchartz-2024.csv` |
| **Initial shape** | 64,016 rows × 14 columns |
| **Final shape** | 17,570 rows × 11 columns |
| **Data retention rate** | 27.4% (17,570 / 64,016) |

**Initial columns:** `img`, `title`, `console`, `genre`, `publisher`, `developer`, `critic_score`, `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales`, `release_date`, `last_update`

---

## 🔄 Preprocessing Pipeline

```
Raw Data (64,016 × 14)
    │
    ▼
Step 1: Column Selection ──────► (64,016 × 10)
    │
    ▼
Step 2: Missing Value Handling ──► (64,016 × 10)
    │
    ▼
Step 3: Sales Filtering ─────────► (17,570 × 10)
    │
    ▼
Step 4: Text Normalization ──────► (17,570 × 10)
    │
    ▼
Step 5: Log Transformation ──────► (17,570 × 11) ✓ Final
```

---

## Step 1: Column Selection

**Action:** Retained only analysis-relevant columns; removed `img`, `title`, `release_date`, and `last_update`.

| Kept Columns | Removed Columns |
|--------------|-----------------|
| `console`, `genre`, `publisher`, `developer`, `critic_score` | `img` (image URLs) |
| `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales` | `title` (game names) |
| | `release_date`, `last_update` (temporal metadata) |

**Justification:**
- The `img` column contains image URLs with no analytical value for statistical modeling.
- `title` is a unique identifier per game and does not contribute to pattern discovery.
- Temporal columns (`release_date`, `last_update`) were excluded in this phase to focus on core feature engineering; they may be reintroduced in later EDA if temporal trends are investigated.

**Shape after selection:** `(64,016, 10)`

---

## Step 2: Missing Value Handling

### 2.1 Row Deletion for Critical Categorical Variables

**Action:** Removed rows where `console` or `genre` was missing.

| Metric | Value |
|--------|-------|
| Rows before deletion | 64,016 |
| Rows after deletion | 64,016 |
| Rows removed | 0 |

**Justification:** `console` and `genre` are primary categorical grouping variables essential for segmentation analysis. They are nominal categories that **cannot be reliably imputed** — any imputation would introduce artificial categories and bias downstream group comparisons. The fact that no rows were removed indicates these fields were fully populated in the raw data.

### 2.2 Median Imputation for `critic_score`

**Action:** Filled missing `critic_score` values with the median (`7.50`).

| Metric | Value |
|--------|-------|
| Missing values before | ~2,300 (≈ 3.6%) |
| Imputation method | Median imputation |
| Imputed value | `7.50` |

**Justification:**
- The critic score distribution is approximately symmetric with a bounded range (0–100), making the median a robust central tendency measure.
- Median is less sensitive to extreme values (outliers) than mean imputation, preserving the overall distribution shape.
- The proportion of missing values (~3.6%) is small enough that single imputation is acceptable without requiring multiple imputation techniques.

> **Note:** Alternative approaches considered: (1) mean imputation — rejected due to outlier sensitivity; (2) mode imputation — rejected as scores are continuous; (3) KNN imputation — deemed unnecessary given low missing rate.

---

## Step 3: Sales Filtering

**Action:** Removed records with `total_sales <= 0`.

| Metric | Value |
|--------|-------|
| Rows before filtering | 64,016 |
| Rows after filtering | 17,570 |
| Rows removed | 46,446 (72.6%) |

**Justification:**
- Zero or negative sales values are likely **data entry errors, placeholders, or unreleased games** with no commercial activity.
- These records have no analytical meaning for sales prediction and would severely distort summary statistics (mean, standard deviation) and model training.
- The high removal rate (72.6%) suggests the raw dataset contains a substantial number of incomplete or unreleased game entries. This is common in crowdsourced video game databases where unreleased or cancelled titles are catalogued.

**Impact Assessment:**
While 72.6% data loss appears significant, the retained 17,570 records represent commercially active games with valid sales data — the actual population of interest for this analysis. The removed entries were effectively "noise" for our research question.

---

## Step 4: Text Normalization

**Action:** Converted `console` and `genre` to uppercase and stripped leading/trailing whitespace.

```python
# Pseudocode of the transformation
df['console'] = df['console'].str.strip().str.upper()
df['genre']   = df['genre'].str.strip().str.upper()
```

**Examples of normalization:**

| Before | After |
|--------|-------|
| `" ps3 "` | `"PS3"` |
| `"Action"` | `"ACTION"` |
| `"Xbox 360"` | `"XBOX 360"` |

**Justification:**
- Prevents duplicate categories caused by inconsistent capitalization (e.g., `"Action"` vs `"ACTION"`).
- Removes accidental whitespace that would create spurious distinct categories (e.g., `" PS3"` vs `"PS3"` treated as different consoles).
- Ensures clean, consistent grouping for downstream categorical analysis and visualization.

**Result:** After normalization, `console` consolidated into **35 distinct platforms** and `genre` into **19 distinct genres**.

---

## Step 5: Target Variable Transformation

**Action:** Created `log_sales = log1p(total_sales)`.

```python
# Pseudocode
df['log_sales'] = np.log1p(df['total_sales'])
```

**Why log transformation?**

Video game sales follow a **highly right-skewed distribution** — a small number of blockbuster titles dominate total sales while the majority sell modestly. Log transformation addresses this in three ways:

1. **Reduces skewness:** Compresses the long right tail, making the distribution more symmetric and suitable for parametric models (linear regression, ANOVA).
2. **Stabilizes variance:** Homogenizes variance across the range of values, satisfying homoscedasticity assumptions.
3. **Improves visualization:** Enables clearer pattern detection in scatter plots and box plots.

**Why `log1p` instead of `log`?**

- `log1p(x) = ln(1 + x)` handles potential zero values gracefully (though Step 3 already removed zero sales).
- Provides numerical stability and ensures the function is defined for all non-negative inputs.

---

## 📈 Preprocessing Summary

| Stage | Rows | Columns | Key Operation |
|-------|------|---------|---------------|
| Raw data | 64,016 | 14 | — |
| After column selection | 64,016 | 10 | Removed metadata columns |
| After missing value handling | 64,016 | 10 | Imputed `critic_score` with median |
| After sales filtering | 17,570 | 10 | Removed `total_sales <= 0` |
| After text normalization | 17,570 | 10 | Uppercase + strip whitespace |
| **Final dataset** | **17,570** | **11** | Added `log_sales` |

**Final dataset columns:**
`console`, `genre`, `publisher`, `developer`, `critic_score`, `total_sales`, `na_sales`, `jp_sales`, `pal_sales`, `other_sales`, `log_sales`

---

## ⚠️ Limitations & Considerations

1. **High data loss (72.6%):** While justified by filtering invalid sales records, this reduces sample diversity. Results may not generalize to games with very low sales or unreleased titles.
2. **Single imputation for `critic_score`:** Median imputation does not account for uncertainty in missing values. Future work could explore multiple imputation (MICE) if critic score becomes a central predictor.
3. **No temporal analysis:** `release_date` was excluded in this phase. Sales trends over time (e.g., platform lifecycle effects) are not captured in the current dataset.
4. **Regional sales missingness:** `jp_sales` has 63.15% missing values (see `summary.md`). These were retained as-is, which may bias regional comparison analyses.

---

## 🔗 Related Files

- `summary.md` — Data quality summary and class balance analysis
- `cleaned_vgchartz.csv` — Final cleaned dataset
- `INFO422-DS Project-group-23-Data Acquisition & Preprocessing.ipynb` — Full preprocessing code
# Preprocessing Log

**Raw data loaded from:** `vgchartz-2024.csv`

**Initial shape:** 64016 rows, 14 columns

**Initial columns:** img, title, console, genre, publisher, developer, critic_score, total_sales, na_sales, jp_sales, pal_sales, other_sales, release_date, last_update

## Step 1: Column selection

**Action:** Kept only analysis-relevant columns; removed `img` and other metadata.

**Justification:** The `img` column contains image URLs and is not useful for statistical analysis. Other possible metadata columns were excluded for clarity.

**Shape after selection:** (64016, 10)

## Step 2: Row deletion based on missing values

**Action:** Removed rows where `console` or `genre` was missing.

**Rows before:** 64016

**Rows after:** 64016

**Justification:** `console` and `genre` are primary categorical grouping variables. They cannot be reliably imputed; removing these rows avoids introducing false categories.

**Action:** Filled missing `critic_score` values with the median (7.50).

**Justification:** The critic score distribution is approximately symmetric, so the median is a robust imputation less affected by outliers.

## Step 3: Sales filtering

**Action:** Removed records with `total_sales <= 0`.

**Rows before:** 64016

**Rows after:** 17570

**Justification:** Zero or negative sales values are likely data errors or placeholders; they have no analytical meaning and would distort summary statistics.

## Step 4: Text normalization

**Action:** Converted `console` and `genre` to uppercase and removed leading/trailing whitespace.

**Justification:** Prevents duplicate categories caused by inconsistent capitalisation or accidental spaces, ensuring clean grouping.

## Step 5: Target variable transformation

**Action:** Created `log_sales = log1p(total_sales)`.

**Justification:** The logarithm reduces the skewness of the sales distribution, making it more suitable for linear models and visualizations. `log1p` is used for numerical stability (though no zero sales remain).

**Final dataset shape:** (17570, 11)

