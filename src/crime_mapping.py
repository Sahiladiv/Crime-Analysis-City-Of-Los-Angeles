import pandas as pd
import folium
from folium.plugins import HeatMap

from .crime_analysis import crime_by_area, top_locations_for_selected_areas


def create_crime_heatmap(df: pd.DataFrame) -> folium.Map:
    """Create a folium heatmap of crimes per area using area lat/lon."""
    area_df = crime_by_area(df)
    if not {"lat", "lon"}.issubset(area_df.columns):
        raise ValueError("DataFrame must contain 'lat' and 'lon' columns for mapping")

    heatmap_data = area_df[["lat", "lon", "crime_count"]].dropna()

    m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)  # LA center

    HeatMap(
        data=heatmap_data[["lat", "lon", "crime_count"]].values.tolist(),
        radius=15,
        blur=10,
        max_zoom=1,
    ).add_to(m)

    return m


def create_top_locations_map(df: pd.DataFrame, areas: list[str], top_n: int = 5) -> folium.Map:
    """Create a folium map marking top N locations for each given area by crime count."""
    top_locations = top_locations_for_selected_areas(df, areas, top_n=top_n)

    # Base map
    m = folium.Map(location=[34.0522, -118.2437], zoom_start=11)

    # Simple color palette for multiple areas
    palette = ["blue", "green", "red", "purple", "orange"]
    color_map = {}
    for idx, area in enumerate(areas):
        color_map[area] = palette[idx % len(palette)]

    for _, row in top_locations.iterrows():
        area = row["area_name"]
        lat, lon, count = row["lat"], row["lon"], row["crime_count"]
        folium.Marker(
            location=[lat, lon],
            popup=f"{area} - Crimes: {count}",
            icon=folium.Icon(color=color_map.get(area, "blue"), icon="info-sign"),
        ).add_to(m)

    return m
