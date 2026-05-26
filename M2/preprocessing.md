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

