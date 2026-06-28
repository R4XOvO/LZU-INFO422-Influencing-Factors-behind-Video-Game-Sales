# Video Game Sales Analysis

## Overview

In the current digital era, the game industry is experiencing rapid growth and has become an important part of the global cultural and entertainment sector. From casual mobile games to large-scale 3A titles on console platforms, the types, forms and target audiences of games are constantly expanding. The commercial value of the game industry has become increasingly prominent, attracting a large amount of capital inflow, and the market competition has become increasingly fierce. For game developers, publishers and investors, understanding various factors that affect game sales is crucial for formulating scientific and effective marketing strategies, enhancing product competitiveness and achieving commercial success.

This project aims to fully utilize the 2024 dataset from VGChartz, and employ advanced data mining and analysis techniques to systematically quantify the specific impact of various factors on game sales. This will provide targeted and forward-looking market strategy reference materials for all professionals in the game industry.

The mining and analysis of these video game sales data are systematic and comprehensive, covering all the factors that affect game sales and their interrelationships. They have a significant positive impact on future video game development work.

## Research Questions

1. **Platform-Genre Sales Advantage**: How do the total sales volumes of different game genres (such as Action, Shooter, etc.) vary across various game platforms (such as the PS series, X360, etc.)? Is there a specific platform-genre combination that has a sales advantage?

2. **Genre-Regional Impact**: Do different game genres (such as Role-Playing, Sports, etc.) have any impact on sales in different regions (North America, Japan, Europe, etc.)? Is there a specific genre-region combination that has a sales advantage?

3. **Brand Effect**: Does the brand effect of game developers and publishers have a significant impact on the total game sales volume and sales volume in various regions (North America, Japan, Europe, etc.)?

## Dataset

The data is sourced from the **VGChartz** platform, which is a well-known data statistics platform in the gaming industry and can provide detailed information about numerous games. This analysis uses the locally downloaded file named `vgchartz-2024.csv`.

- **Size**: 64,016 game-related records
- **Variables**: 14 columns covering:
  - Game platforms (e.g., PS3, PS4, X360)
  - Game genres (e.g., Action, Shooter)
  - Publishers and developers
  - Critic ratings (critic_score)
  - Regional sales (North America, Europe, Japan, etc.)
  - Release dates
  - Total global sales

The data comprehensively covers multi-dimensional information of various games, and the data from 2024 can promptly reflect the current dynamics and trends of the game market. Its extensive game records and rich variables are conducive to precise analysis of the key factors influencing game sales at present, providing strong data support for game industry practitioners to formulate market strategies. Meanwhile, the authority of the VGChartz platform ensures the relative accuracy and reliability of the data.

Below is a partial view of the dataset:

![Dataset Part 1](images/dataset_part1.png)
*Figure 1: Dataset preview (part 1)*

![Dataset Part 2](images/dataset_part2.png)
*Figure 2: Dataset preview (part 2)*

The dataset is available on [Kaggle](https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024).

## Methodology

This study follows the **CRISP-DM** framework and uses Python along with its scientific computing stack (pandas, numpy, seaborn, matplotlib, scipy, statsmodels, scikit-learn, XGBoost, LightGBM) throughout the process. It was iteratively completed in the Jupyter Lab environment.

### Data Preprocessing

#### 1. Data Cleaning

- The `critic_score` is filled with the median value.
- The missing values in the regional sales column are marked as 0.
- The missing values in the categorical fields are set as "Unknown".
- Abnormal values where `total_sales` is less than or equal to 0 are excluded.
- Extreme values in sales are marked using IQR > 1.5 x Q3.

#### 2. Data Reduction

- **Stratified sampling** by genre maintains the proportion of each type.
- **K-means clustering** is used to cluster based on "sales + platform" to retain the centroids.
- Average sales are calculated by **aggregating** based on "console + genre".

#### 3. Data Transformation and Discretization

- Construct `log_sales = log1p(total_sales)` to alleviate right skewness.
- Unify the string formats of publisher and developer.
- Numerical sales fields can be normalized using the z-score / min-max method.
- Continuous fields (such as `release_date`) can be discretized using equal-frequency binning.

### Exploratory Data Analysis (EDA)

#### 1. Nominal Feature Distribution

By visualizing the correlation between nominal features (console, genre, publisher) and sales volume, we initially identify the characteristic combinations that have a significant advantage in sales, and use this to select the key analysis objects for subsequent quantitative verification.

> **Example**: Create a box plot of sales data for console-genre-publishers (using seaborn) to visually identify the "high sales group" (such as the "PS4 x Action" combination).

#### 2. Numerical Feature Distribution

Analyze the basic statistical patterns of the numerical features (sales in the four regions, log_sales), and simultaneously verify whether the distribution of key variables meets the prerequisite conditions for subsequent statistical tests to ensure the validity of the analysis results.

> **Example**: Calculate the mean, median, and standard deviation of sales in the four regions (using pandas); Test the normality of log_sales (using Shapiro test from scipy) to ensure it meets the requirements for subsequent statistical tests.

#### 3. Key Visualizations

Through multi-dimensional visual charts, the interrelationships among different data dimensions (such as platform and type, type and region, publisher and sales volume) can be presented intuitively, enabling rapid exploration of potential sales patterns.

> **Example**: Draw graphs showing the relationships between various data, such as:
> - The sales heatmap of console x genre (displaying the average sales)
> - The stacked bar chart of genre x region (showing the sales proportion of each region)
> - The bar chart of the top 20 publishers' sales
>
> These visualizations present the data correlations in an intuitive way.

### Correlation Analysis

#### 1. Nominal vs Nominal

Use the **chi-square test** to determine whether platform and genre are independent; a significant result indicates an association.

> **Example**: A p-value < 0.001 for "PS4 x Action" suggests that this specific combination occurs more often than random chance and is worth prioritizing in release planning.

#### 2. Nominal vs Numerical

Apply **ANOVA** to examine the interaction effect of platform and genre on sales; significance quantifies the combined impact.

> **Example**: If the ANOVA F-test for "platform x genre" on log-sales yields p < 0.01, we can conclude that pairing PS4 with Action titles reliably boosts average global sales.

#### 3. Numerical vs Numerical

Calculate **correlation coefficients** and **variance inflation factors** for regional sales. In case of high correlation or multicollinearity, retain only total sales as the target variable in modeling.

> **Example**: Pearson r > 0.75 between NA and PAL sales indicates overlapping demand, so we enter only `total_sales` into the random forest to avoid over-weighting the same signal twice.

### Model Assistance and Verification

To cross-validate the findings for Q1 (platform x genre), Q2 (regional preferences) and Q3 (brand effect), we proceed as follows:

- **Random Forest regression** takes platform, genre, publisher and developer (one-hot encoded) as inputs and `total_sales` as the target; feature importances quantify the relative contributions for Q1 and Q3.

- **XGBoost regression** further captures non-linear brand-region interactions; ranking consistency with RF confirms the robustness of Q3.

- For Q2, a single **melt operation** converts the four regional columns into a categorical "region" field, allowing the same importance comparison.

- **Five-fold CV** plus **bootstrap resampling** are applied; if R^2 >= 0.6 and Kendall's tau >= 0.8 for the top-10 features, the model is deemed stable and the statistical/visual insights are translated into reliable business priorities.

## Tech Stack

- **Language**: Python
- **Environment**: Jupyter Lab
- **Core Libraries**:
  - `pandas` - data manipulation and analysis
  - `numpy` - numerical computing
  - `seaborn` / `matplotlib` - data visualization
  - `scipy` / `statsmodels` - statistical testing and modeling
  - `scikit-learn` - machine learning (Random Forest, preprocessing, cross-validation)
  - `XGBoost` / `LightGBM` - gradient boosting regression

## Team Members

| Name | Role | Responsibilities |
|------|------|------------------|
| Zuo Fengyuan | Project Leader & Final Integrator | Lead full-cycle project management, including timeline planning, task coordination and risk control; integrate all team outputs, standardize document format and conduct final quality review; organize team meetings and submit the complete project package. |
| Yang Tianxiao | Data Engineer & Preprocessing Specialist | Manage dataset acquisition, verification and version control; complete data cleaning, transformation and reduction as planned; draft dataset description and ethical compliance statement. |
| Bu Fanzhou | Data Analyst & Visualization Lead | Conduct exploratory data analysis and descriptive statistics; perform statistical hypothesis testing and correlation analysis; design and create all data visualizations, summarize EDA findings. |
| Zhong Rui | Machine Learning Engineer | Build and optimize Random Forest and XGBoost regression models; implement cross-validation and evaluate model performance; quantitatively verify the three core research questions. |
| Gong Zijie | Domain Research & Presentation Lead | Draft industry background, research questions and preliminary hypotheses; translate technical findings into actionable business recommendations; prepare presentation materials and final conclusion section. |

## Expected Final Deliverables

### 1. Comprehensive Report

- **Main Idea**: A comprehensive overview of the impact of different factors on video game sales discovered by mining the dataset.
- **Data Description**: A detailed description of the composition of the elements in the dataset.
- **Methodology and Tools**: A complete and detailed introduction to all the methodologies and tools used in data mining and analysis.
- **Analysis Results and Visualizations**: Combined with a visual model, explain how each factor (e.g., Console, Genre, Region) affects video game sales and how video game sales change with different aspects.
- **Insights and Recommendations**: All the mining and analysis results are combined with predictive models to make recommendations for the development of marketing strategies for game development companies.

### 2. Presentation

- **Introduction**: An overview of the project goal and the reason why the topic of video game sales is important.
- **Methodology**: A brief explanation to the methodology and tools we used during the project.
- **Research Questions**: An introduction to the key questions addressed in the project.
- **Key Findings**: Show significant results from analysis of video game sales sets.
- **Conclusion**: Summarize all the results and make predictions for video game developments.

## References

- [Video Game Sales 2024 - Kaggle Dataset](https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024)
