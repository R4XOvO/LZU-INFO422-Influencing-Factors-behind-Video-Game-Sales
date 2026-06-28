# Presentation Director's Guide
## Project: Influencing Factors behind Video Game Sales
## Duration: 7 minutes + 5 minutes Q&A

---

### Slide 1: Title Slide

**Content**:
- Project title: "Influencing Factors behind Video Game Sales"
- Team name: "Group 23"
- Course: INFO422 Data Science
- Date

**Visual**: Clean title slide with a gaming icon/illustration (optional).
**Speaking Notes** (30 sec):
- "Good morning/afternoon. Today we present our analysis of the factors that drive video game sales."
- "In a $200B+ industry, understanding what makes a game succeed is critical for developers, publishers, and investors."
- "Our project uses the VGChartz 2024 dataset to quantify the relative impact of platform, genre, brand, and quality on global sales."
- "We'll walk you through our journey from data acquisition to modelling and deployment, and share actionable insights for the industry."

**Milestone Source**: M1 proposal.md

---

### Slide 2: The $200B Question — Research Objectives

**Content**: Three research questions in a clean 3-column layout with icons:
1. Platform-Genre Synergy: Do specific combinations (e.g., PS4×Sports) deliver sales premiums?
2. Regional Preferences: Do genre preferences vary across NA, Japan, and Europe?
3. Brand Effect: Does publisher/developer brand impact sales through scale and/or prestige?

**Visual**: Three-column cards with question marks/insight icons. Light background.

**Speaking Notes** (45 sec):
- "We pursued three core questions. First, do platform-genre combinations matter? For example, does a PS4 Sports game sell better than an Xbox Sports game?"
- "Second, are there regional preference patterns? We know Japanese gamers love RPGs, but how does this play out across all genres?"
- "Third, what's the role of brand? Do big publishers like EA and Ubisoft win just because they release more games, or does brand prestige itself carry a premium?"
- "These questions matter because they directly inform platform strategy, regional marketing, and partnership decisions."

**Milestone Source**: M1 proposal.md, M4 EDA Report

---

### Slide 3: Dataset & Preprocessing

**Content**: Data pipeline summary:
- **Source**: VGChartz 2024 (Kaggle)
- **Raw**: 64,016 records × 14 columns
- **Cleaned**: 8,786 records × 33 features (removed duplicates, imputed nulls, engineered features)
- **Key transformations**: log_sales target, platform-genre interaction indicators, brand scale counts

**Visual**: Flow diagram or a clean bullet list with icons showing the data pipeline.

**Speaking Notes** (40 sec):
- "We started with 64K raw VGChartz records and cleaned down to 8,786 high-quality, unique games."
- "We engineered 33 features including log_sales as our target, platform-genre interaction indicators, and brand scale counts."
- "Importantly, we removed regional sales from model inputs to avoid data leakage — we're predicting global sales from pre-release attributes."
- "All preprocessing is documented and reproducible via the M2/M3 notebook."

**Milestone Source**: M2 & M3 preprocessing.md, summary.md

---

### Slide 4: EDA Insight 1 — Platform-Genre Synergy

**Content**: Key finding: platform-genre interactions are real, concentrated in the upper quartile. Top combos: PS4×Sports (0.75M median), PS3×Fighting (0.74M), X360×Shooter (0.64M).

**Visual**: [M4/images/viz08_console_genre_heatmap.png] — heatmap of platform-genre median sales.

**Speaking Notes** (40 sec):
- "Our EDA revealed that platform-genre combinations matter. Here's a heatmap of median sales by platform and genre."
- "The hot spots: PS4 Sports, PS3 Fighting, Xbox 360 Shooter — these specific combinations command sales premiums that generic platform or genre analysis would miss."
- "The effect isn't linear — it shows up in the upper quartile. Shooter and RPG genres consistently have higher ceilings, while Sports is compressed (annualized franchises)."
- "This validates our hypothesis that the interaction term is crucial for strategic platform-genre positioning."

**Milestone Source**: M4/M4_EDA_Report.md, M4/images/viz08_console_genre_heatmap.png

---

### Slide 5: EDA Insight 2 — Regional Market Clusters

**Content**: Key finding: three distinct regional clusters with different genre preferences.
- North America: Shooter, Sports, Action dominate (na_ratio > 40%).
- Japan: RPG, Visual Novel, Fighting dominate (jp_ratio > 35%).
- Europe/PAL: Racing, Platform, Sports elevated.

**Visual**: [M4/images/viz09_regional_preference_patterns.png] — stacked bar chart of regional genre preferences.

**Speaking Notes** (40 sec):
- "Regional patterns are stark. Here's how genre preferences split across North America, Japan, and Europe."
- "North America: Shooter and Sports dominate. Japan: RPG and Visual Novel — a very different cultural landscape. Europe/PAL leans toward Racing and Platform."
- "This has practical implications: a generic RPG might fail in NA but succeed in Japan, while a generic Shooter might struggle in Japan but thrive in NA."
- "We limited regional modelling due to Japan data quality issues (63.7% zeros), but the EDA patterns are clear."

**Milestone Source**: M4/M4_EDA_Report.md, M4/images/viz09_regional_preference_patterns.png

---

### Slide 6: EDA Insight 3 — Brand Scale vs Prestige

**Content**: Key finding: brand operates through two mechanisms — scale (volume) and prestige (per-title premium). Blockbuster tier (Cluster 1): 2.7% of games, median 3.58M sales. Top publishers by scale: EA, Ubisoft, Konami.

**Visual**: [M4/images/viz10_kmeans_clusters.png] — K-Means sales cluster visualization showing the blockbuster tier.

**Speaking Notes** (40 sec):
- "What about brand? We found that brand affects sales through two channels: scale and prestige."
- "Scale — publisher game count — is the single biggest feature in our models. Big publishers have distribution and marketing advantages."
- "But there's also prestige. Even after controlling for scale, certain publishers (Nintendo, Rockstar) command a per-title premium."
- "The K-Means clustering revealed a blockbuster tier: only 2.7% of games, but they account for a disproportionate share of revenue."
- "This long-tail is a key modelling challenge — which leads us to the next section."

**Milestone Source**: M4/M4_EDA_Report.md, M4/images/viz10_kmeans_clusters.png

---

### Slide 7: Modelling Approach

**Content**: Three models evaluated.
1. **Multiple Linear Regression** — interpretable baseline, quantifies linear effects.
2. **Random Forest Regressor** — captures non-linear interactions, our production model (R² = 0.39).
3. **Two-Stage Blockbuster-Aware** — hybrid blend that reduces blockbuster RMSE by 6.7%.

**Visual**: Simple diagram showing the two-stage architecture: global RF → classifier → blend with blockbuster regressor.

**Speaking Notes** (45 sec):
- "We built three models. Linear regression provides an interpretable baseline — we can see exactly how much each feature contributes in linear terms."
- "Random Forest captures non-linear interactions and achieves R² = 0.39, a 26% lift over the linear baseline."
- "Critically, the Random Forest confirmed that platform-genre synergy matters — the non-linear gain validates the EDA insight."
- "We also added a two-stage blockbuster-aware model that uses a classifier to flag likely blockbusters and blends their predictions toward a dedicated regressor. This reduces blockbuster error by 6.7%, addressing the long-tail underestimation we identified."

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md, M5 images

---

### Slide 8: Results — Model Comparison

**Content**: Performance table (R², RMSE, MAE) for all three models on holdout test set. RF wins overall; two-stage wins on blockbuster segment.

| Model | R² | RMSE | MAE |
|-------|-----|------|-----|
| Linear Regression | 0.31 | 0.259 | 0.173 |
| Random Forest | **0.39** | **0.243** | **0.158** |
| Two-Stage RF | 0.38 | 0.247 | 0.159 |

**Visual**: [M5/images/viz1_model_performance_comparison.png] — bar chart comparing R² and RMSE across models.

**Speaking Notes** (35 sec):
- "Here's the performance comparison. Random Forest wins across all metrics — R² of 0.39, RMSE of 0.24."
- "The two-stage model trades 1.6 percentage points of overall R² to gain a 6.7% improvement in blockbuster RMSE — it's a specialized tool for when that segment matters."
- "Strong generalisation: we saw no performance drop from cross-validation to the holdout test set, meaning the models aren't overfitting."

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md, M5/images/viz1_model_performance_comparison.png

---

### Slide 9: Results — What Drives Sales

**Content**: Top 10 feature importance (Random Forest). Top 3: `developer` (0.616), `critic_score` (0.122), `developer_game_count` (0.083). Platform and genre effects are secondary but significant.

**Visual**: [M5/images/viz2_feature_importance_ranking.png] — horizontal bar chart of feature importance.

**Speaking Notes** (40 sec):
- "What actually drives sales? Here are the top 10 features from the Random Forest model."
- "Number one: developer (target-encoded), capturing both scale and prestige. Critic score is second — surprising given its weak correlation, but it matters non-linearly."
- "Developer game count, publisher, and platform effects follow. Console and genre are significant but not dominant."
- "The takeaway: for stakeholders, partner with established developers and publishers — scale matters more than platform or genre choice."

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md, M5/images/viz2_feature_importance_ranking.png

---

### Slide 10: Results — Prediction Reliability

**Content**: Actual vs Predicted scatter plot. The model performs reliably for mid-to-low sales but underestimates blockbusters. Residual plot shows fan-out at high values.

**Visual**: [M5/images/viz3_actual_vs_predicted_sales.png] — side-by-side scatter of RF vs two-stage, plus [M5/images/viz0_residuals_two_stage.png] for residuals.

**Speaking Notes** (40 sec):
- "Here's actual vs predicted sales. The model is reliable for mainstream and budget titles — points hug the diagonal."
- "But for blockusters, we see systematic underestimation. This is the long-tail problem."
- "The two-stage model, shown on the right, pulls some of those upper-tail points toward the line, reducing blockbuster error."
- "The residual plot (bottom) confirms that prediction uncertainty grows with sales magnitude — use the model with wider confidence intervals for high-budget projects."

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md, M5/images/viz3_actual_vs_predicted_sales.png, M5/images/viz0_residuals_two_stage.png

---

### Slide 11: Live Demo / App Preview

**Content**: Screenshots of the Streamlit app. Input form (console, genre, publisher, developer, critic score, release era). Output: predicted sales, blockbuster probability, top feature drivers.

**Visual**: Screenshots of the Streamlit app UI. Can include: (1) sidebar input form, (2) prediction result card, (3) feature importance table.

**Speaking Notes** (50 sec):
- "Let me show you the working deployment. This is a Streamlit app we built for M6."
- "You enter game attributes here: console, genre, publisher, developer, critic score, and release era."
- "Click predict, and you get two forecasts: the Random Forest prediction (recommended for general use) and the two-stage prediction (better for blockbusters)."
- "You also see the blockbuster probability and the top feature drivers for your specific game."
- "This tool is now available for stakeholder decision support."

**Milestone Source**: M6 app.py, deployment demonstration

---

### Slide 12: Recommendations & Limitations

**Content**: 4-5 actionable recommendations + key caveats.

**Recommendations**:
1. **Partner with established publishers** (scale is the top driver).
2. **Prioritise game quality** (critic score matters non-linearly).
3. **Use platform-genre strategy** (PS4×Sports, X360×Shooter premiums).
4. **Target regions by genre** (NA: Shooter/Sports, Japan: RPG).
5. **Use the model as decision support** — not the sole basis for budget decisions.

**Limitations**:
- Digital sales undercount (PC bias).
- Blockbuster sample scarcity (only 62 training blockbusters).
- Japan data quality gap (63.7% zeros).
- Temporal extrapolation risk (pre-2019 data).

**Visual**: Simple two-column layout (left: recommendations, right: limitations) with icons.

**Speaking Notes** (45 sec):
- "Our recommendations for stakeholders: partner with established publishers — scale matters more than you might think. Invest in game quality — critic score correlates with sales."
- "Use platform-genre strategy and target regions by genre. And use the model as decision support, not a crystal ball."
- "Caveats: the dataset is physical-sales biased, undercounting PC digital titles. We have limited blockbuster data, and Japan sales are noisy. The model needs quarterly retraining to stay current."

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md (Section 8), M6 model_card.md

---

### Slide 13: Conclusion & Q&A

**Content**: One-sentence takeaway per research question.
- Q1 (Platform-Genre): Synergy is real and concentrated in upper-quartile premiums.
- Q2 (Regional): Distinct clusters exist; tailor marketing by region.
- Q3 (Brand): Brand drives sales through both scale and prestige; scale dominates.

**Closing**: "Thank you. We're happy to take questions about our methodology, results, or the deployed app."

**Visual**: Summary bullets with checkmarks or icon. Clean, minimal.

**Speaking Notes** (30 sec):
- "To close: platform-genre synergy is real and concentrates in upper-quartile premiums. Regional markets have distinct patterns — tailor accordingly. Brand operates through scale and prestige, with scale being the dominant factor."
- "The Random Forest model (R² = 0.39) and our two-stage variant are now available for stakeholder use."
- "Thank you. Questions?"

**Milestone Source**: M5/M5 — Data Modelling & Visualisation Report.md (Section 8)

---

## Visual Asset Mapping Table

| Slide | Visual | Source File | Status |
|-------|--------|-------------|--------|
| 1 | Title slide | N/A (design) | Create |
| 2 | Research questions cards | N/A (design) | Create |
| 3 | Data pipeline diagram | N/A (design) | Create |
| 4 | Platform-Genre Heatmap | M4/images/viz08_console_genre_heatmap.png | Reuse |
| 5 | Regional Preferences | M4/images/viz09_regional_preference_patterns.png | Reuse |
| 6 | K-Means Clusters | M4/images/viz10_kmeans_clusters.png | Reuse |
| 7 | Two-Stage Architecture Diagram | N/A (diagram) | Create |
| 8 | Model Comparison Bar Chart | M5/images/viz1_model_performance_comparison.png | Reuse |
| 9 | Feature Importance Ranking | M5/images/viz2_feature_importance_ranking.png | Reuse |
| 10 | Actual vs Predicted + Residuals | M5/images/viz3_actual_vs_predicted_sales.png + viz0_residuals_two_stage.png | Reuse |
| 11 | Streamlit App Screenshots | N/A (screenshots) | Capture from running app |
| 12 | Recommendations & Limitations | N/A (text layout) | Create |
| 13 | Summary Bullets | N/A (text layout) | Create |

---

## Speaking Notes Script (Quick Reference)

**Slide 1 (30s)**: Intro — $200B market, three questions, VGChartz dataset, end-to-end journey.
**Slide 2 (45s)**: Q1 platform-genre, Q2 regional, Q3 brand scale/prestige. Why they matter.
**Slide 3 (40s)**: 64K → 8,786 cleaned, 33 features, log_sales target, no leakage.
**Slide 4 (40s)**: Platform-genre heatmap, hot spots, upper-quartile effect, validates hypothesis.
**Slide 5 (40s)**: Regional clusters, NA=Shooter/Sports, Japan=RPG/VN, Europe=Racing/Platform.
**Slide 6 (40s)**: Brand scale vs prestige, K-Means blockbuster tier (2.7%, median 3.58M), long-tail challenge.
**Slide 7 (45s)**: MLR baseline, RF production (R²=0.39), two-stage blockbuster-aware (-6.7% blockbuster RMSE).
**Slide 8 (35s)**: Performance table, RF wins, two-stage trade-off (small overall R² cost, blockbuster gain).
**Slide 9 (40s)**: Top 10 features, developer #1, critic #2, scale > platform/genre.
**Slide 10 (40s)**: Actual vs predicted, reliable for mid-budget, blockbuster underestimation, two-stage helps.
**Slide 11 (50s)**: Streamlit demo, input form, predictions, blockbuster probability, feature drivers.
**Slide 12 (45s)**: 5 recommendations + 4 limitations. Use as decision support, not sole basis.
**Slide 13 (30s)**: One-sentence answer per Q, closing, invite questions.

---

## Transition Cues

- **Intro → Data pipeline**: "Before diving into what we found, let me briefly show you the data foundation."
- **EDA → Modelling**: "Armed with these EDA insights, we built predictive models to quantify these effects."
- **Model results → App demo**: "Let me show you how stakeholders can actually use these models."
- **Demo → Recommendations**: "Based on everything we've seen, here are our recommendations for the industry."
- **Recommendations → Conclusion**: "To wrap up, let me answer our three research questions one last time."

---

## Q&A Anticipation

| Question | Suggested Response |
|----------|---------------------|
| **Why does critic score have low correlation but feature importance is high?** | "Critic score shows low linear correlation (Pearson r ≈ 0.05) but the Random Forest captures non-linear interactions — games with very high scores (9–10) do behave differently. It's not the top driver, but it matters in the tails." |
| **How well does the model predict for new publishers/developers?** | "Target encoding uses global means for unknown entities, so predictions for completely new publishers are conservative. We recommend supplementing model forecasts with qualitative market research for new entrants." |
| **Can this model predict sales for games not yet released?** | "Yes, if you have a critic score and know the publisher/developer track record. The model is designed for pre-release decision support. For unreleased titles without critic scores, use the median (7.5) as a conservative estimate." |
| **Why is the Japan data so sparse?** | "VGChartz has incomplete Japan coverage, leading to 63.7% zero-imputation. We chose to keep the data for global modelling but excluded regional sales as features to avoid leakage. For Japan-specific insights, we recommend dedicated regional sub-models with higher-quality data." |
| **What's the single most actionable insight for a new game studio?** | "Partner with an established publisher. Publisher game count is the top feature — scale gives you distribution, marketing, and platform access. Critic score is second, so invest in quality." |

---

## Timeline Check

| Time | Slide |
|------|-------|
| 0:00-0:30 | Title |
| 0:30-1:15 | Research Questions |
| 1:15-1:55 | Dataset & Preprocessing |
| 1:55-2:35 | EDA: Platform-Genre |
| 2:35-3:15 | EDA: Regional |
| 3:15-3:55 | EDA: Brand & Blockbuster |
| 3:55-4:40 | Modelling Approach |
| 4:40-5:15 | Model Comparison |
| 5:15-5:55 | Feature Importance |
| 5:55-6:35 | Prediction Reliability |
| 6:35-7:25 | Demo / App Preview |
| 7:25-8:10 | Recommendations & Limitations |
| 8:10-8:40 | Conclusion & Q&A |

**Total speaking time**: ~7:00 (slightly under to leave buffer for transitions).

---

## File Structure Reference

The presentation draws from these files:

- Milestone 1: `proposal.md`
- Milestone 2 & 3: `M2 & M3/preprocessing.md`, `M2 & M3/summary.md`
- Milestone 4: `M4/M4_EDA_Report.md`, `M4/images/*.png`
- Milestone 5: `M5/M5 — Data Modelling & Visualisation Report.md`, `M5/images/*.png`
- Milestone 6: `app.py`, `model_card.md`, `final_report.md` (if synthesized)

All figures referenced exist in their respective `images/` folders.