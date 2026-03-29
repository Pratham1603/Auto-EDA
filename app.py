import streamlit as st
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt

from utils.overview import dataset_statistics
from utils.overview import classify_columns
from utils.variables import get_col_type 
from utils.missing import missing_analysis
from utils.plots import plot_correlation, plot_histogram, plot_boxplot, plot_categorical, plot_missing

st.set_page_config(layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 AUTO-EDA")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

page = st.sidebar.radio("Navigate", [
    "Overview",
    "Variables",
    "Interactions",
    "Correlations",
    "Missing Values",
    "Sample"
])

# ---------------- LOAD DATA ----------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ================= OVERVIEW =================
    if page == "Overview":

        st.title("Overview")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Dataset Statistics",
            "Variable Types",
            "Alerts",
            "Reproduction"
        ])

        # -------- TAB 1 --------
        with tab1:
            stats = dataset_statistics(df)
            stats_df = pd.DataFrame({
                "Metric": list(stats.keys()),
                "Value": list(stats.values())
            })
            st.subheader("Dataset Statistics")
            st.dataframe(stats_df, use_container_width=True)

        # -------- TAB 2 --------
        with tab2:
            types = classify_columns(df)
            types_df = pd.DataFrame(
                list(types.items()),
                columns=["Type", "Count"]
            )
            st.subheader("Variable Types")
            st.table(types_df)

        # -------- TAB 3 --------
        with tab3:
            alerts = []

            for col in df.columns:
                series = df[col]
                col_type = get_col_type(series)

                # Missing
                missing_count = series.isnull().sum()
                missing_pct = series.isnull().mean() * 100
                if missing_count > 0:
                    alerts.append(f"⚠️ **{col}** has {missing_count} ({missing_pct:.1f}%) missing values")

                # Zeros
                if col_type == "Numeric":
                    zero_count = (series == 0).sum()
                    zero_pct = (series == 0).mean() * 100
                    if zero_count > 0:
                        alerts.append(f"🔵 **{col}** has {zero_count} ({zero_pct:.1f}%) zeros")

                # Unique
                if series.nunique() == len(df):
                    alerts.append(f"🔴 **{col}** has unique values")

                # Uniform
                if col_type == "Numeric":
                    if series.nunique() / len(df) > 0.9:
                        alerts.append(f"🔴 **{col}** is uniformly distributed")

            # High correlation
            df_encoded = df.copy()
            cols_to_drop = [col for col in df.columns if get_col_type(df[col]) == "Text"]
            df_encoded = df_encoded.drop(columns=cols_to_drop, errors='ignore')
            for col in df_encoded.select_dtypes(include="object").columns:
                df_encoded[col] = pd.factorize(df_encoded[col])[0]
            corr = df_encoded.corr(numeric_only=True).abs()
            for i, j in itertools.combinations(corr.columns, 2):
                if corr.loc[i, j] > 0.5:
                    alerts.append(f"⚫ **{i}** is highly correlated with **{j}**")
                    alerts.append(f"⚫ **{j}** is highly correlated with **{i}**")

            if not alerts:
                st.success("No alerts found.")
            else:
                for msg in alerts:
                    st.write(msg)

        # -------- TAB 4 --------
        with tab4:
            st.link_button("GitHub Repository", "https://github.com/Pratham1603/Auto-EDA")
            st.link_button("Twitter", "https://x.com/PROSEED_AI")

    # ================= VARIABLES =================
    elif page == "Variables":

        st.title("Variables")

        col = st.selectbox("Select Column", df.columns)
        series = df[col]
        col_type = get_col_type(series)

        st.subheader(col)
        st.caption(f"Type: **{col_type}**")

        distinct = series.nunique()
        distinct_pct = series.nunique() / len(df) * 100
        missing = series.isnull().sum()
        missing_pct = series.isnull().mean() * 100
        mem_str = f"{series.memory_usage(deep=True) / 1024:.1f} KiB"

        if col_type == "Numeric":
            left_stats = {
                "Distinct": distinct,
                "Distinct (%)": f"{distinct_pct:.1f}%",
                "Missing": missing,
                "Missing (%)": f"{missing_pct:.1f}%",
                "Infinite": 0,
                "Infinite (%)": "0.0%",
                "Mean": round(series.mean(), 2),
            }
            right_stats = {
                "Minimum": series.min(),
                "Maximum": series.max(),
                "Zeros": int((series == 0).sum()),
                "Zeros (%)": f"{(series == 0).mean() * 100:.1f}%",
                "Negative": int((series < 0).sum()),
                "Negative (%)": f"{(series < 0).mean() * 100:.1f}%",
                "Memory size": mem_str,
            }
        else:
            left_stats = {
                "Distinct": distinct,
                "Distinct (%)": f"{distinct_pct:.1f}%",
                "Missing": missing,
                "Missing (%)": f"{missing_pct:.1f}%",
                "Memory size": mem_str,
            }
            right_stats = {}

        col1, col2, col3 = st.columns([2, 2, 2])

        def render_table(stats_dict):
            rows_html = ""
            for k, v in stats_dict.items():
                rows_html += f"""
                <tr>
                    <td style='padding:6px 12px; font-weight:600;'>{k}</td>
                    <td style='padding:6px 12px;'>{v}</td>
                </tr>"""
            st.markdown(f"""
            <table style='width:100%; border-collapse:collapse; font-size:14px;'>
                <tbody>{rows_html}</tbody>
            </table>""", unsafe_allow_html=True)

        with col1:
            render_table(left_stats)

        with col2:
            if right_stats:
                render_table(right_stats)

        with col3:
            if col_type == "Numeric":
                st.pyplot(plot_histogram(df, col))
            elif col_type == "Categorical":
                st.pyplot(plot_categorical(df, col))
            elif col_type == "Text":
                from wordcloud import WordCloud
                text = " ".join(series.dropna().astype(str).tolist())
                wc = WordCloud(width=400, height=300, background_color="white").generate(text)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)

    # ================= INTERACTIONS =================
    elif page == "Interactions":

        st.title("Interactions")

        cols = [c for c in df.columns if get_col_type(df[c]) == "Numeric"]

        c1, c2 = st.columns(2)
        with c1:
            col1 = st.selectbox("Column 1", cols, key="int_col1")
        with c2:
            col2 = st.selectbox("Column 2", cols, key="int_col2")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(df[col1], df[col2], alpha=0.5, s=15, color="#4C72B0")
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        plt.tight_layout()

        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.pyplot(fig)

    # ================= CORRELATIONS =================
    elif page == "Correlations":

        st.title("Correlation Heatmap")

        view = st.radio("", ["Heatmap", "Table"], horizontal=True)

        if view == "Heatmap":
            st.pyplot(plot_correlation(df), use_container_width=True)
        else:
            df_encoded = df.copy()
            cols_to_drop = [col for col in df.columns if get_col_type(df[col]) == "Text"]
            df_encoded = df_encoded.drop(columns=cols_to_drop, errors='ignore')
            for col in df_encoded.select_dtypes(include="object").columns:
                df_encoded[col] = pd.factorize(df_encoded[col])[0]
            corr = df_encoded.corr(numeric_only=True).round(3)
            corr = corr.sort_index(axis=0).sort_index(axis=1)
            st.dataframe(corr, use_container_width=True)

    # ================= MISSING =================
    elif page == "Missing Values":

        missing, percent = missing_analysis(df)

        view = st.radio("", ["Count", "Matrix", "Heatmap"], horizontal=True)

        if view == "Count":
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("Missing Count")
                st.dataframe(missing)
            with col2:
                st.subheader("Missing %")
                st.dataframe(percent)
            st.pyplot(plot_missing(df))

        elif view == "Matrix":
            import missingno as msno
            fig, ax = plt.subplots(figsize=(10, 5))
            msno.matrix(df, ax=ax, sparkline=False)
            plt.tight_layout()
            st.pyplot(fig)

        elif view == "Heatmap":
            import missingno as msno
            fig, ax = plt.subplots(figsize=(10, 5))
            msno.heatmap(df, ax=ax)
            plt.tight_layout()
            st.pyplot(fig)

    # ================= SAMPLE =================
    elif page == "Sample":

        st.subheader("Head")
        st.dataframe(df.head())

        st.subheader("Tail")
        st.dataframe(df.tail())

        st.subheader("Random Sample")
        st.dataframe(df.sample(min(5, len(df))))

else:
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1>📊 AUTO-EDA</h1>
        <p style='font-size:18px;'>An automated exploratory data analysis tool.</p>
        <br>
        <p>Upload a CSV file from the sidebar to get started.</p>
        <br>
        <br>
        <p>Made with ❤️ by Pratham Harer</p>
        <p>Inspired by the ydata-profiling library</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
