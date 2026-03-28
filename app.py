import streamlit as st
import pandas as pd

from utils.overview import get_overview
from utils.missing import missing_analysis
from utils.stats import basic_stats, skewness
from utils.plots import (
    plot_histogram,
    plot_correlation,
    plot_missing,
    plot_boxplot,
    plot_categorical
)
from utils.insights import generate_insights

st.set_page_config(page_title="Mini EDA Profiler", layout="wide")

st.title("📊 Mini EDA Profiler")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Tabs for better UI
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Overview",
        "📊 Analysis",
        "📉 Correlation",
        "🧠 Insights"
    ])

    # ------------------ TAB 1: OVERVIEW ------------------
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Overview")
        overview = get_overview(df)
        for key, value in overview.items():
            st.write(f"**{key}:** {value}")

        st.subheader("Missing Values")
        missing, percent = missing_analysis(df)

        st.dataframe(pd.DataFrame({
            "Missing Count": missing,
            "Percentage (%)": percent
        }))

        st.pyplot(plot_missing(missing))

    # ------------------ TAB 2: ANALYSIS ------------------
    with tab2:
        st.subheader("Statistical Summary")
        st.dataframe(basic_stats(df))

        st.subheader("Skewness")
        st.write(skewness(df))

        st.subheader("Column Analysis")
        column = st.selectbox("Select Column", df.columns)

        if pd.api.types.is_numeric_dtype(df[column]):
            st.pyplot(plot_histogram(df, column))
            st.pyplot(plot_boxplot(df, column))
        else:
            st.pyplot(plot_categorical(df, column))

    # ------------------ TAB 3: CORRELATION ------------------
    with tab3:
        st.subheader("Correlation Heatmap")
        st.pyplot(plot_correlation(df))

    # ------------------ TAB 4: INSIGHTS ------------------
    with tab4:
        st.subheader("Insights")
        insights = generate_insights(df)

        if insights:
            for insight in insights:
                st.write("•", insight)
        else:
            st.write("No major insights detected.")