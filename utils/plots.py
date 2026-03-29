import matplotlib.pyplot as plt
import seaborn as sns
from utils.variables import get_col_type
import pandas as pd


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
    df_encoded = df.copy()
    cols_to_drop = [col for col in df.columns if get_col_type(df[col]) == "Text"]
    df_encoded = df_encoded.drop(columns=cols_to_drop, errors='ignore')

    for col in df_encoded.select_dtypes(include="object").columns:
        df_encoded[col] = pd.factorize(df_encoded[col])[0]

    corr = df_encoded.corr(numeric_only=True)
    corr = corr.sort_index(axis=0).sort_index(axis=1)

    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(
        corr,
        annot=False,
        cmap=sns.diverging_palette(20, 220, as_cmap=True),
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor="white",
        square=True,
        ax=ax
    )
    plt.tight_layout()
    return fig


# Missing values bar chart
def plot_missing(df):
    count = df.notna().sum()
    ratio = df.notna().mean()

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(count.index, ratio.values, color="#2196F3")

    for bar, c in zip(bars, count.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            str(c),
            ha='center', va='bottom', fontsize=9
        )

    ax.set_ylim(0, 1.1)
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel("")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig


# Categorical value counts
def plot_categorical(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().head(10).plot(kind='bar', ax=ax)
    ax.set_title(f"Top Categories in {column}")
    return fig