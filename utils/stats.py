def basic_stats(df):
    return df.describe()

def skewness(df):
    return df.skew(numeric_only=True)