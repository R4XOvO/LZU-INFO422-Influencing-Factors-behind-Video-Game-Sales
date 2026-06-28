"""
Streamlit App for Video Game Sales Prediction
================================================
Deployed for M6 final deliverable. Loads models from M5/models/.
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import streamlit as st

# Page config
st.set_page_config(
    page_title="Video Game Sales Predictor",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load models and data (cached)
@st.cache_resource
def load_models():
    """Load all model artifacts from models/ (works both locally and on Vercel)."""
    models_dir = Path("models")
    return {
        "preprocessor": joblib.load(models_dir / "preprocessor.pkl"),
        "rf_model": joblib.load(models_dir / "rf_model.pkl"),
        "blockbuster_classifier": joblib.load(models_dir / "blockbuster_classifier.pkl"),
        "rf_blockbuster": joblib.load(models_dir / "rf_blockbuster.pkl"),
        "metadata": joblib.load(models_dir / "model_metadata.pkl"),
    }

@st.cache_data
def load_data():
    """Load cleaned dataset for dropdown options and lookups."""
    return pd.read_csv("cleaned_vgchartz.csv")

# Two-stage prediction (hybrid blend)
def two_stage_predict(X, base_model, classifier, reg_bb, threshold=0.6, alpha=0.3):
    base_pred = base_model.predict(X)
    bb_proba = classifier.predict_proba(X)[:, 1]
    bb_flag = bb_proba >= threshold
    final_pred = base_pred.copy()
    if bb_flag.sum() > 0:
        bb_pred = reg_bb.predict(X[bb_flag])
        final_pred[bb_flag] = alpha * bb_pred + (1 - alpha) * base_pred[bb_flag]
    return final_pred, bb_proba[0] if len(bb_proba) == 1 else bb_proba

# Back-transform log_sales to total_sales in millions
def backtransform_log(log_sales):
    return np.exp(log_sales) - 1

# Main app
def main():
    # Load
    models = load_models()
    df = load_data()

    # Sidebar: Input form
    st.sidebar.header("🎮 Game Attributes")

    # Dropdown options
    consoles = sorted(df["console"].unique().astype(str).tolist())
    genres = sorted(df["genre"].unique().tolist())
    eras = sorted([str(x) for x in df["release_year_bin"].unique() if pd.notna(x)])

    # Top publishers/developers for autocomplete suggestions
    top_publishers = df["publisher"].value_counts().head(20).index.tolist()
    top_developers = df["developer"].value_counts().head(20).index.tolist()

    # Input fields
    console = st.sidebar.selectbox("Console", consoles, index=consoles.index("PS4") if "PS4" in consoles else 0)
    genre = st.sidebar.selectbox("Genre", genres, index=genres.index("ACTION") if "ACTION" in genres else 0)
    release_year_bin = st.sidebar.selectbox("Release Era", eras, index=eras.index("era_3") if "era_3" in eras else 0)

    publisher = st.sidebar.text_input(
        "Publisher",
        value="EA",
        help="Enter publisher name. Top suggestions: " + ", ".join(top_publishers[:5])
    )
    developer = st.sidebar.text_input(
        "Developer",
        value="EA Canada",
        help="Enter developer name. Top suggestions: " + ", ".join(top_developers[:5])
    )

    critic_score = st.sidebar.slider("Critic Score", 1.0, 10.0, 7.5, 0.1)

    # Look up game counts; use median if unknown
    pub_counts = df.groupby("publisher")["publisher_game_count"].first()
    dev_counts = df.groupby("developer")["developer_game_count"].first()

    publisher_game_count = pub_counts.get(publisher, df["publisher_game_count"].median())
    developer_game_count = dev_counts.get(developer, df["developer_game_count"].median())

    # Show inferred counts
    with st.sidebar.expander("Inferred Game Counts"):
        st.write(f"Publisher '{publisher}' has published {int(publisher_game_count)} games (in dataset)")
        st.write(f"Developer '{developer}' has worked on {int(developer_game_count)} games (in dataset)")

    # Predict button
    if st.sidebar.button("🔮 Predict Sales", type="primary", use_container_width=True):
        # Build input DataFrame
        input_df = pd.DataFrame([{
            "console": console,
            "genre": genre,
            "publisher": publisher,
            "developer": developer,
            "critic_score": critic_score,
            "release_year_bin": release_year_bin,
            "publisher_game_count": publisher_game_count,
            "developer_game_count": developer_game_count,
        }])

        # Preprocess
        X_processed = models["preprocessor"].transform(input_df)

        # Predict
        rf_log_sales = models["rf_model"].predict(X_processed)[0]
        two_stage_log_sales, blockbuster_proba = two_stage_predict(
            X_processed,
            models["rf_model"],
            models["blockbuster_classifier"],
            models["rf_blockbuster"],
            threshold=models["metadata"]["blockbuster_proba_threshold"],
            alpha=models["metadata"]["blend_alpha"]
        )
        two_stage_log_sales = two_stage_log_sales[0]

        # Back-transform
        rf_sales_millions = backtransform_log(rf_log_sales)
        two_stage_sales_millions = backtransform_log(two_stage_log_sales)

        # Main content
        st.title("🎮 Video Game Sales Prediction")

        # Predictions card
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Random Forest Prediction",
                f"{rf_sales_millions:.2f}M units",
                delta="Global model (recommended for general use)"
            )
        with col2:
            st.metric(
                "Two-Stage Prediction",
                f"{two_stage_sales_millions:.2f}M units",
                delta="Blockbuster-aware (better for high-budget projects)"
            )

        # Blockbuster probability
        bb_threshold = models["metadata"]["blockbuster_threshold"]  # 3.5M
        blockbuster_label = "🎯 Blockbuster (>3.5M)" if two_stage_sales_millions > bb_threshold else "Mainstream (<3.5M)"
        st.info(f"Predicted Blockbuster Probability: {blockbuster_proba:.1%} — {blockbuster_label}")

        # Top feature drivers
        st.subheader("📊 Top Sales Drivers")

        feature_importance = pd.DataFrame(models["metadata"]["feature_importance"])
        top_features = feature_importance.head(8)

        # For categorical inputs, highlight matching features
        feature_note = ""
        if console in top_features["Feature"].values:
            feature_note = f"Your selected platform ('{console}') is a top predictor."
        elif genre in top_features["Feature"].values:
            feature_note = f"Your selected genre ('{genre}') is a top predictor."
        elif publisher in top_features["Feature"].values:
            feature_note = f"Your selected publisher ('{publisher}') contributes significantly."
        if feature_note:
            st.success(feature_note)

        st.dataframe(
            top_features.rename(columns={"Importance Score": "Relative Importance"}),
            use_container_width=True,
            hide_index=True
        )

        # Model comparison
        st.subheader("📈 Model Performance (from M5)")
        perf = models["metadata"]["performance"]
        st.dataframe(
            pd.DataFrame(perf),
            use_container_width=True
        )

        # Blockbuster segment RMSE improvement
        st.info(f"💡 The two-stage model reduces blockbuster-segment RMSE by "
                f"{(models['metadata']['blockbuster_rmse']['random_forest'] - models['metadata']['blockbuster_rmse']['two_stage']) / models['metadata']['blockbuster_rmse']['random_forest'] * 100:.1f}% "
                f"compared to the Random Forest, directly addressing long-tail underestimation.")

    else:
        # Instructions before prediction
        st.title("🎮 Video Game Sales Predictor")
        st.markdown("""
        **About this tool:** Enter game attributes on the left and click "Predict Sales" to get a sales forecast.

        This is the M6 deployment for the course project "Influencing Factors behind Video Game Sales."
        The underlying models were trained on 8,786 video games from the VGChartz 2024 dataset.

        **Models available:**
        - **Random Forest** (R² = 0.39, RMSE = 0.24) — recommended for general use.
        - **Two-Stage Blockbuster-Aware** (R² = 0.38) — improves blockbuster prediction by ~7% RMSE.

        **Key finding:** Publisher brand scale (`publisher_game_count`) and critic score are the top sales drivers.
        """)

        st.divider()
        st.subheader("📋 Feature Descriptions")

        feature_desc = {
            "Console": "The gaming platform (e.g., PS4, Switch, PC). Different platforms have different user bases and genre preferences.",
            "Genre": "Game category (e.g., Action, RPG, Sports). Shooter and RPG historically achieve higher sales ceilings.",
            "Publisher": "The company funding and distributing the game. Large publishers (EA, Ubisoft) have distribution advantages.",
            "Developer": "The studio building the game. Established studios have quality and reputation advantages.",
            "Critic Score": "Review aggregator score (0–10). Surprisingly weak correlation with sales in this dataset.",
            "Release Era": "The historical era of release (era_1 = retro, era_5 = modern). Older platforms have different dynamics.",
            "Publisher Game Count": "Number of games this publisher has released in the dataset (proxy for scale/market presence). Top driver.",
            "Developer Game Count": "Number of games this developer has worked on (proxy for experience/volume). Significant factor.",
        }

        for feature, desc in feature_desc.items():
            with st.expander(f"**{feature}**"):
                st.write(desc)

if __name__ == "__main__":
    main()