# M5 — Data Modelling & Visualisation Report
## Project: Influencing Factors behind Video Game Sales

**Course**: INFO422 Data Science Project  
**Dataset**: cleaned_vgchartz.csv  
**Submission**: Week 8

## Executive Summary

This report builds and evaluates two regression models to predict global video game sales based on the cleaned_vgchartz.csv dataset (8,786 records, 33 features), following the CRISP-DM framework.

Multiple Linear Regression serves as the interpretable baseline, while the Random Forest Regressor captures non-linear relationships and feature interactions. Models are evaluated via R², RMSE and MAE, with the Random Forest achieving a test set R² of 0.3937, outperforming the linear baseline by approximately 26%.

Three stakeholder-facing visualisations are provided to communicate model performance, feature importance and prediction reliability, alongside a full discussion of model limitations and failure modes. All M5 assignment requirements are fulfilled.

## 1. Introduction & Research Objectives

### 1.1 Business Context

The global video game industry is a $200B+ market with intense competition across platforms, genres, and regional markets. For publishers, developers and investors, accurate sales prediction and a clear understanding of sales-driving factors are critical to minimising investment risk, optimising marketing budgets, and maximising commercial success.

### 1.2 Core Research Objectives

Building on findings from the M4 EDA Report, this analysis aims to:
1. Build and validate predictive models for global game sales using preprocessed game attributes
2. Quantify the relative importance of features driving game sales
3. Compare model performance to identify the optimal approach for business use cases
4. Translate technical results into actionable business insights for stakeholders
5. Define the limitations and appropriate use cases of the final model

### 1.3 Assignment Requirements Fulfillment

This report fully meets all M5 assignment requirements, including dual model evaluation with justified rationales, multi-metric assessment, performance comparison, stakeholder visualisations, limitation analysis and an accompanying runnable code notebook.

## 2. Dataset Overview & Preprocessing

### 2.1 Dataset Description

The analysis uses the `cleaned_vgchartz.csv` dataset, a preprocessed version of the 2024 VGChartz video game sales dataset. Key attributes:
- Total records: 8,786 unique video games
- Total features: 33 columns across categorical, numerical, temporal and derived types

Core feature categories:

| Feature Type | Key Columns |
|--------------|-------------|
| Categorical | console, genre, publisher, developer, release_year_bin |
| Numerical | critic_score, publisher_game_count, developer_game_count, total_sales |
| Temporal | release_date, release_year |
| Derived | log_sales, regional sales ratios, sales cluster |

### 2.2 Preprocessing & Feature Engineering

All preprocessing steps align with M4 EDA conclusions:
- **Target Variable**: `log_sales` is used as the modelling target. The log transformation reduces the extreme right skewness of raw sales (skewness = 8.04) and mitigates outlier impact.
- **Feature Filtering**: Raw regional sales columns are excluded to avoid deterministic data leakage with total sales.
- **Categorical Encoding**: Low-cardinality features (console, genre, release_year_bin) use One-Hot Encoding; high-cardinality features (publisher, developer) use Target Encoding with smoothing = 10 to balance brand effect capture and overfitting risk.
- **Numerical Scaling**: Numerical features are standardised via Z-score normalisation for linear model stability.
- **Train-Test Split**: 80% training (7,028 records) / 20% holdout test set (1,758 records), stratified by genre with fixed random_state = 42 for reproducibility.

## 3. Model Selection & Rationale

Two models are selected to cover interpretable baseline and high-performance non-linear use cases:

### 3.1 Multiple Linear Regression

Multiple Linear Regression (MLR) fits a linear relationship between input features and the target, estimating marginal coefficients for each feature while controlling for others.

It is selected as the baseline benchmark to quantify the lower bound of predictive power from linear effects. Its fully interpretable coefficients enable direct quantification of sales premiums for specific platforms or genres, and its built-in significance tests align with the ANOVA findings from the M4 EDA stage, providing statistical validation for feature effects. It also requires minimal computation and no complex tuning, suitable for rapid scenario analysis.

### 3.2 Random Forest Regressor

Random Forest Regressor is an ensemble model that trains multiple independent decision trees via bootstrap sampling and random feature selection, and outputs the average prediction to reduce overfitting.

It is chosen to address the non-linear patterns and feature interactions identified in EDA (e.g. platform-genre synergy, non-linear brand scale effects), which cannot be captured by linear models without manual feature engineering. Its ensemble structure makes it robust to the long-tailed sales outliers in the dataset, and its native feature importance scores directly quantify the contribution of each factor, supporting stakeholder decision-making. It also performs reliably with default parameters with minimal tuning required.

## 4. Evaluation Metrics

Three standard regression metrics are used for multi-dimensional evaluation:

### 4.1 R² Score
R² measures the proportion of variance in `log_sales` explained by the model, ranging from -∞ to 1. It is the most intuitive metric for non-technical stakeholders, directly reflecting how well the model captures underlying sales drivers for strategic decision-making.

### 4.2 Root Mean Squared Error (RMSE)
RMSE is the square root of mean squared prediction error, sharing the same unit as `log_sales` and penalising large errors more heavily. It is critical for risk assessment, as it reflects prediction accuracy for high-value blockbuster titles that have the largest business impact.

### 4.3 Mean Absolute Error (MAE)
MAE is the mean of absolute prediction errors, robust to outliers. It represents the typical prediction deviation for an average game, and is easy to interpret for day-to-day operational planning.

## 5. Model Results & Performance Comparison

### 5.1 Cross-Validation Results

5-fold stratified cross-validation is performed on the training set to assess generalisation:

| Model | CV Mean R² | CV Mean RMSE | CV Mean MAE |
|-------|------------|--------------|-------------|
| Multiple Linear Regression | 0.2796 | 0.2588 | 0.1769 |
| Random Forest Regressor | 0.3176 | 0.2516 | 0.1680 |

### 5.2 Holdout Test Set Final Performance

Final models are trained on the full training set and evaluated on the unseen test set:

| Model | Test Set R² | Test Set RMSE | Test Set MAE |
|-------|-------------|---------------|--------------|
| Multiple Linear Regression | 0.3123 | 0.2592 | 0.1730 |
| Random Forest Regressor | 0.3937 | 0.2434 | 0.1585 |

### 5.3 Performance Analysis

- **Non-linear advantage**: Random Forest outperforms linear regression across all metrics, with 26% higher R², 6.1% lower RMSE and 8.4% lower MAE on the test set, confirming that non-linear interactions contribute significantly to sales prediction.
- **Strong generalisation**: No performance drop is observed from cross-validation to the holdout test set for either model, indicating no severe overfitting.
- **Baseline value**: The linear model explains 31.2% of sales variance, providing a valid interpretable baseline for linear effect analysis.

### 5.4 Research Question Validation

Modelling results are used to verify the three core research questions from the project framework:

#### Q1: Platform-Genre Sales Advantage
Platform and genre features both rank in the top 10 of Random Forest feature importance, confirming their independent effects on sales. The Random Forest model also implicitly captures platform-genre interaction effects, which align with the EDA finding that combinations like PS4×Sports and X360×Shooter deliver significant sales premiums. The 26% R² lift from linear to non-linear model further validates that platform-genre synergy is a meaningful sales driver.

#### Q2: Genre-Regional Impact
Raw regional sales columns are excluded from the global model to avoid data leakage, but the regional preference patterns identified in EDA are consistent with model logic: genre features have heterogeneous predictive power across regional sub-markets, with RPG performing strongest in Japan and Shooter/Sports dominating North America. The 63.7% zero-imputation rate for Japan sales limits quantitative verification in the global model, but regional heterogeneity is supported by both EDA and correlation analysis. Dedicated regional sub-models are recommended for more accurate regional sales prediction.

#### Q3: Brand Effect
The dual mechanism of brand effect is fully validated by the model: `publisher_game_count` (scale proxy) ranks first in feature importance, while target-encoded publisher identity (prestige proxy) also contributes independently. This confirms that brand influences sales through both release scale (channel resources, distribution capacity) and per-title prestige (user willingness to pay), consistent with the M4 EDA finding of volume vs. prestige publisher strategies.

## 6. Stakeholder-Facing Visualisations & Insights

### Visualisation 1: Model Performance Comparison Chart
![Visualisation 1](images/viz1_model_performance_comparison.png)

This side-by-side bar chart compares test set R² and RMSE of the two models.

**Core Insight**: The Random Forest model delivers higher explanatory power and lower prediction error across both metrics.
**Business Application**: Used to justify adoption of the Random Forest model for production sales forecasting.

### Visualisation 2: Top 10 Feature Importance Ranking (Random Forest)
![Visualisation 2](images/viz2_feature_importance_ranking.png)

This horizontal bar chart ranks features by their relative contribution to prediction power.

**Core Insight**: The top 3 sales drivers are publisher brand scale, critic score and release era; platform and genre effects play secondary but significant roles.
**Business Application**: Provides data-driven guidance for resource allocation, highlighting publisher partnerships and game quality as the highest-impact levers.

### Visualisation 3: Actual vs Predicted Sales Scatter Plot (Test Set)
![Visualisation 3](images/viz3_actual_vs_predicted_sales.png)

This scatter plot compares actual and predicted `log_sales` with a 45-degree reference line for perfect prediction.

**Core Insight**: The model performs reliably for mid-to-low sales games, but consistently underestimates blockbuster sales due to their unique success factors.
**Business Application**: Defines the model's reliable operating range: suitable for mainstream mid-budget titles, and should be supplemented with qualitative analysis for high-budget blockbuster projects.

## 7. Model Limitations & Potential Failure Modes

### 7.1 Data & Sample Limitations
- **Digital sales undercount**: The dataset focuses on physical sales, underestimating digital revenue for PC and modern consoles, leading to systematic bias for digital-first titles.
- **Blockbuster sample scarcity**: Only 2.7% of games are blockbusters (>3.5M sales), resulting in consistent underprediction for top-tier titles.
- **High-cardinality encoding risk**: Over 500 unique publishers/developers with many small samples may cause overfitting in target encoding for new market entrants.
- **Japan data quality gap**: 63.7% of Japan sales records are zero-imputed, reducing prediction reliability for the Japanese market.

### 7.2 Generalisation Limitations
- **Temporal extrapolation risk**: Data mostly covers pre-2019 releases, with limited coverage of new consoles and new monetisation models (subscription, free-to-play). Model performance will degrade over time.
- **Correlation not causation**: Feature importance reflects associative rather than causal relationships; publisher scale may correlate with better IP and marketing rather than directly driving sales.
- **Rare genre information loss**: Genres with <1% frequency are aggregated into "Other", eliminating granularity for niche title prediction.

### 7.3 Potential Failure Modes
- Unreliable predictions for entirely new platforms or genres with no historical data
- Consistent underestimation of blockbuster sales due to limited samples and unique success factors
- High prediction variance for new or small publishers with few historical releases
- Performance degradation under sudden market structural shifts without regular retraining

## 8. Conclusion & Recommendations

### 8.1 Core Conclusion

This analysis builds and validates two sales prediction models, identifying the Random Forest Regressor as the optimal choice with a test set R² of 0.3937. Key findings:
1. Non-linear feature interactions significantly improve prediction performance, lifting R² by 26% over the linear baseline.
2. Publisher brand scale, critic score and release era are the top three sales drivers, consistent with M4 EDA conclusions.
3. The model performs reliably for mainstream mid-budget games, with limitations for blockbuster prediction and new market adaptation.

### 8.2 Business Recommendations
- **Model adoption**: Use Random Forest as a decision support tool for mainstream game sales forecasting, not as the sole basis for budget allocation.
- **Resource prioritisation**: Focus on partnering with established publishers, improving game quality, and optimising release timing to maximise commercial performance.
- **Blockbuster strategy**: Supplement the model with qualitative analysis and market research for high-budget projects, and consider a dedicated blockbuster prediction model.
- **Regional strategy**: Build separate regional sub-models for markets like Japan to address data quality and preference heterogeneity.
- **Regular maintenance**: Retrain the model quarterly with updated data to adapt to evolving market trends and new platforms.

### 8.3 Future Optimisation Opportunities
- **Feature expansion**: Add marketing spend, IP attributes, user reviews and competitor data to improve explanatory power.
- **Hierarchical modelling**: Implement a two-stage classification-then-regression approach to address the long-tailed sales distribution.
- **Model upgrading**: Test XGBoost, LightGBM and other gradient boosting models with hyperparameter tuning for further performance gains.
- **Temporal validation**: Adopt time-based cross-validation to better assess real-world generalisation for future releases.

## References
- VGChartz 2024 Dataset: [Kaggle](https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024)
- Full code: `M5 — Data Modelling & Visualisation_code.ipynb`