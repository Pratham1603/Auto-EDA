def missing_analysis(df):
    missing = df.isnull().sum()
    percent = (missing / len(df)) * 100

    return missing, percent