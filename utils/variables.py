import pandas as pd

def get_col_type(series):
    """Returns 'Numeric', 'Categorical', or 'Text' for a single series."""
    series_clean = series.dropna()
    unique_count = series_clean.nunique()
    total_count = len(series_clean)
    unique_ratio = unique_count / total_count if total_count > 0 else 0

    if pd.api.types.is_numeric_dtype(series):
        if unique_count <= 5:
            return "Categorical"
        else:
            return "Numeric"
    else:
        if unique_ratio > 0.6:
            return "Text"
        else:
            return "Categorical"