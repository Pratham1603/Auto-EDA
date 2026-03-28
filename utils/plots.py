import matplotlib.pyplot as plt
import seaborn as sns

# Histogram (numeric)
def plot_histogram(df, column):
    fig, ax = plt.subplots()
    df[column].dropna().hist(ax=ax)
    ax.set_title(f"Histogram of {column}")
    return fig


# Boxplot (for outliers)
def plot_boxplot(df, column):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[column], ax=ax)
    ax.set_title(f"Boxplot of {column}")
    return fig


# Correlation heatmap
def plot_correlation(df):
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=False, ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig


# Missing values bar chart
def plot_missing(missing):
    fig, ax = plt.subplots()
    missing.plot(kind='bar', ax=ax)
    ax.set_title("Missing Values Count")
    return fig


# Categorical value counts
def plot_categorical(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().head(10).plot(kind='bar', ax=ax)
    ax.set_title(f"Top Categories in {column}")
    return fig