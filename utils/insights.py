def generate_insights(df):
    insights = []

    # Missing values
    missing_percent = (df.isnull().sum() / len(df)) * 100
    for col, val in missing_percent.items():
        if val > 30:
            insights.append(f"{col} has high missing values ({val:.2f}%)")

    # Skewness
    skew = df.skew(numeric_only=True)
    for col, val in skew.items():
        if abs(val) > 1:
            insights.append(f"{col} is highly skewed")

    # Correlation
    corr = df.corr(numeric_only=True)
    for col in corr.columns:
        for idx in corr.index:
            if col != idx and abs(corr.loc[col, idx]) > 0.8:
                insights.append(f"High correlation between {col} and {idx}")

    return list(set(insights))