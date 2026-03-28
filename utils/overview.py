import pandas as pd

def get_overview(df):
    overview = {
        "Shape": df.shape,
        "Columns": df.columns.tolist(),
        "Data Types": df.dtypes,
        "Memory Usage (MB)": round(df.memory_usage(deep=True).sum() / 1e6, 2),
        "Duplicate Rows": df.duplicated().sum()
    }
    return overview