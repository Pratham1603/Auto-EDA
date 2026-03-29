import pandas as pd

def dataset_statistics(df):
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    memory = df.memory_usage().sum()  # FIXED

    stats = {
        "Number of variables": df.shape[1],
        "Number of observations": df.shape[0],
        "Missing cells": missing_cells,
        "Missing cells (%)": f"{(missing_cells / total_cells) * 100:.2f}%",
        "Duplicate rows": duplicate_rows,
        "Duplicate rows (%)": f"{(duplicate_rows / len(df)) * 100:.2f}%",
        "Total size in memory": f"{memory / 1024:.2f} KiB",
        "Average record size in memory": f"{memory / len(df):.2f} B"
    }

    return stats

def classify_columns(df):
    numeric_cols = []
    categorical_cols = []
    text_cols = []

    for col in df.columns:
        series = df[col].dropna()

        if len(series) == 0:
            continue

        unique_count = series.nunique()
        total_count = len(series)
        unique_ratio = unique_count / total_count

        # -------- NUMERIC --------
        if pd.api.types.is_numeric_dtype(series):

            # Only very low unique → categorical
            if unique_count <= 5:
                categorical_cols.append(col)
            else:
                numeric_cols.append(col)

        # -------- OBJECT --------
        else:
            # FIX: better text detection
            if unique_ratio > 0.6:
                text_cols.append(col)
            else:
                categorical_cols.append(col)

    return {
        "Numeric": len(numeric_cols),
        "Categorical": len(categorical_cols),
        "Text": len(text_cols)
    }