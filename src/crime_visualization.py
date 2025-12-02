import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .crime_analysis import crime_by_area, time_area_counts


def plot_crimes_by_area_bar(df: pd.DataFrame):
    """Horizontal bar chart of total crimes by area."""
    area_df = crime_by_area(df)
    sorted_df = area_df.sort_values("crime_count", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(sorted_df["area_name"], sorted_df["crime_count"])
    ax.set_xlabel("Number of Crimes")
    ax.set_ylabel("Area Name")
    ax.set_title("Total Crimes by Area")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def plot_time_area_heatmap(df: pd.DataFrame):
    """Heatmap of crime count by hour (x) and area (y)."""
    tac = time_area_counts(df)
    heatmap_data = tac.pivot(index="area_name", columns="hour", values="crime_count").fillna(0)

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
    ax.set_title("Crime Count by Time and Area")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Area Name")
    fig.tight_layout()
    return fig
