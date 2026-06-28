# Model Card: Video Game Sales Random Forest Predictor

**Version**: 1.0 (M6 final deployment)
**Date**: 2026-06-28
**Model Type**: Random Forest Regressor (scikit-learn)

---

## Model Details

| Attribute | Value |
|-----------|-------|
| Algorithm | Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`) |
| Hyperparameters | n_estimators=100, max_depth=15, min_samples_leaf=10, random_state=42, n_jobs=-1 |
| Training data | 7,028 records (80% train split of 8,786 cleaned VGChartz 2024 records) |
| Evaluation data | 1,758 holdout test records (20% stratified by genre) |
| Primary target | `log_sales` (natural log of 1 + total_sales in millions of units) |
| Secondary target (two-stage variant) | Blockbuster segment RMSE |

---

## Intended Use

**Use case**: Sales forecasting for mainstream mid-budget video games (not blockbusters). Supports marketing budget allocation, project risk assessment, and portfolio planning for publishers and developers.

**Do NOT use for**:
- Brand-new platforms or genres with zero historical training examples.
- Titles with purely digital monetisation (subscription, F2P microtransactions) not represented in the dataset.
- Budget-allocation as the sole decision factor (use as decision support only).
- Blockbuster prediction (if accuracy > 40% R² is required) — use the two-stage variant instead.

**Out-of-scope**: Pre-release forecasting for games with no critic scores or unknown publishers/developers not present in the training data. Target encoding will use global means for unknown entities, degrading reliability.

---

## Factors

The model uses 8 input features, transformed as follows:

| Feature | Type | Encoding | Notes |
|---------|------|----------|-------|
| console | categorical (33 values) | One-Hot | Platform effects (PS4, Switch, PC, etc.) |
| genre | categorical (20 values) | One-Hot | Genre preferences (Shooter, RPG, Sports, etc.) |
| release_year_bin | categorical (5 eras) | One-Hot | Historical era (retro → modern) |
| publisher | high-cardinality (~1,000) | Target encoding (smoothing=10) | Brand scale & prestige; top driver |
| developer | high-cardinality (~2,500) | Target encoding (smoothing=10) | Brand scale & prestige; top driver |
| critic_score | numerical (0–10) | Z-score standardisation | Review quality; surprisingly weak |
| publisher_game_count | numerical | Z-score standardisation | Publisher scale proxy; top driver |
| developer_game_count | numerical | Z-score standardisation | Developer scale proxy; significant |

**Excluded**: Regional sales columns (`na_sales`, `jp_sales`, etc.) to avoid data leakage with the target `total_sales`.

---

## Metrics

### Overall Test Set Performance

| Metric | Random Forest | Two-Stage Blockbuster-Aware |
|--------|---------------|-----------------------------|
| R² Score | 0.3937 | 0.3775 |
| RMSE (log_sales units) | 0.2434 | 0.2466 |
| MAE (log_sales units) | 0.1585 | 0.1594 |

### Cross-Validation (5-fold, stratified by genre)

| Metric | Mean | Std |
|--------|------|-----|
| R² | 0.3176 | 0.041 |
| RMSE | 0.2516 | 0.009 |
| MAE | 0.1680 | 0.005 |

### Blockbuster Segment (18 test blockbusters, total_sales > 3.5M)

| Metric | Random Forest | Two-Stage | Improvement |
|--------|---------------|-----------|-------------|
| RMSE (log_sales) | 1.0845 | 1.0121 | −6.7% |

**Interpretation**: The model explains ~39% of log_sales variance, which is modest but meaningful for a prediction task with high inherent noise in entertainment markets. The two-stage variant sacrifices 1.6 percentage points of overall R² to gain 6.7% blockbuster RMSE improvement — a justified trade when blockbuster accuracy matters.

---

## Training Data Summary

| Attribute | Value |
|-----------|-------|
| Total records (cleaned) | 8,786 unique video games |
| Time period covered | Primarily pre-2019 releases; limited post-2019 |
| Geographic coverage | VGChartz (physical-sales biased; undercounts PC digital) |
| Blockbuster definition | total_sales > 3.5M units (62 training records, 0.9%) |
| Categorical coverage | 33 consoles, 20 genres, ~1,000 publishers, ~2,500 developers |
| Missing data handling | Critic scores median-imputed; genre rare categories (<1%) merged to "Other" |

**Key limitation**: Japan sales have 63.7% zero-imputation, reducing model reliability for the Japanese market.

---

## Ethical Considerations

1. **Physical-sales bias**: The dataset is VGChartz-based and focuses on physical sales. Digital-first PC titles and modern monetisation (DLC, microtransactions, subscription) are undercounted, leading to systematic bias.

2. **Publisher/developer scale bias**: The model rewards established publishers with large `publisher_game_count` values. This may disadvantage new entrants with strong titles but no track record, potentially reinforcing market concentration.

3. **Regional fairness**: Japan data quality issues (63.7% zeros) mean the model is less reliable for Japanese-published titles. Recommendations for Japan should be treated with caution.

4. **Genre representation**: Niche genres (<1% frequency) are merged into "Other", eliminating granularity for those titles.

5. **Temporal extrapolation**: Model is trained on predominantly pre-2019 data. Performance may degrade for newer platforms (PS5, Xbox Series X/S) and new monetisation models.

**Recommendations for responsible use**:
- Use the model as a decision-support tool, not the sole basis for budget decisions.
- For new market entrants or digital-first titles, supplement model forecasts with qualitative market research.
- Do not use the model to deny opportunities based solely on predicted sales.

---

## Caveats & Recommendations

### Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Blockbuster sample scarcity (0.9%) | Underestimates top-tier titles | Use two-stage variant; supplement with qualitative analysis |
| Digital sales undercount | Systematic bias for PC/indie | Treat PC forecasts as conservative estimates |
| Japan data gap (63.7% zeros) | Poorer reliability for JP market | Separate regional sub-models recommended |
| Temporal drift (pre-2019) | May not capture modern dynamics | Retrain quarterly with new data |
| High-cardinality encoding | Overfitting risk for new entities | Use conservative predictions for new publishers |

### Recommendations

1. **Operational use**: Deploy the Random Forest model for general sales forecasting. Switch to the two-stage variant when blockbuster prediction accuracy is prioritized.

2. **Retraining cadence**: Retrain models quarterly with updated VGChartz data to capture new releases and platform shifts.

3. **Feature expansion**: Add marketing spend, IP attributes, and user review sentiment to improve explanatory power (R² target > 0.45).

4. **Regional modelling**: Build separate sub-models for North America, Europe/PAL, and Japan to address regional preference heterogeneity and data quality gaps.

5. **Blockbuster data sourcing**: Actively collect more blockbuster training samples (through data partnerships or public sources) to widen the two-stage gain beyond the current 6.7% RMSE improvement.

---

## References

- Dataset: VGChartz 2024, [Kaggle](https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024)
- Course: INFO422 Data Science Project, LZU
- Project GitHub: [repository link]
- Model Card Guidelines: [Google Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

---

**Contact**: For questions about model interpretation, deployment, or updates, refer to the project repository or the course instructor.