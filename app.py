import streamlit as st
from streamlit_folium import st_folium
from pathlib import Path

from src.crime_data_loader import load_crime_data
from src.crime_preprocessing import preprocess_crime_data
from src.crime_analysis import (
    dataset_shape,
    list_columns,
    null_counts,
    unique_counts,
    top_crime_types_by_area,
)
from src.crime_visualization import plot_crimes_by_area_bar, plot_time_area_heatmap
from src.crime_mapping import create_crime_heatmap, create_top_locations_map

DATA_PATH = Path("Crime_Data_from_2020_to_Present.csv")

st.set_page_config(page_title="LA Crime Analysis Dashboard", layout="wide")
st.title("🚔 Crime Analysis – City of Los Angeles")


@st.cache_data(show_spinner=True)
def load_and_preprocess(path: Path):
    df = load_crime_data(str(path))
    df = preprocess_crime_data(df)
    return df


if not DATA_PATH.exists():
    st.error(f"Data file not found at {DATA_PATH.resolve()}. Please place the CSV in the project root.")
    st.stop()

df = load_and_preprocess(DATA_PATH)

# Sidebar filters
st.sidebar.header("Filters")
if "area_name" in df.columns:
    all_areas = sorted(df["area_name"].dropna().unique().tolist())
    default_areas = [a for a in all_areas if a in ["Central", "77th Street", "Pacific"]]
    selected_areas = st.sidebar.multiselect(
        "Select Areas", options=all_areas, default=default_areas or all_areas[:3]
    )
    if selected_areas:
        df_filtered = df[df["area_name"].isin(selected_areas)]
    else:
        df_filtered = df
else:
    selected_areas = []
    df_filtered = df

tab_overview, tab_time_area, tab_maps = st.tabs(["Overview", "Time vs Area", "Maps"])

with tab_overview:
    st.subheader("Dataset Snapshot")
    st.write("Shape (rows, columns):", dataset_shape(df_filtered))
    st.write("Columns:", list_columns(df_filtered))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Missing values per column**")
        st.dataframe(null_counts(df_filtered))
    with col2:
        st.markdown("**Unique values per column**")
        st.dataframe(unique_counts(df_filtered))

    st.subheader("Raw Data (first 500 rows)")
    st.dataframe(df_filtered.head(500))

with tab_time_area:
    if "area_name" in df_filtered.columns and "hour" in df_filtered.columns:
        st.subheader("Crime Count by Time and Area")
        fig = plot_time_area_heatmap(df_filtered)
        st.pyplot(fig)

    if "area_name" in df_filtered.columns and "crm_cd_desc" in df_filtered.columns and selected_areas:
        st.subheader("Top 3 Crime Types per Selected Area")
        top_crimes = top_crime_types_by_area(df_filtered, selected_areas, top_n=3)
        st.dataframe(top_crimes)

    st.subheader("Total Crimes by Area")
    if "area_name" in df_filtered.columns:
        fig_bar = plot_crimes_by_area_bar(df_filtered)
        st.pyplot(fig_bar)

with tab_maps:
    st.subheader("Crime Heatmap (by Area)")
    try:
        heatmap_map = create_crime_heatmap(df_filtered)
        st_folium(heatmap_map, width=800, height=500)
    except Exception as e:
        st.info(f"Heatmap not available: {e}")

    if selected_areas:
        st.subheader(f"Top Locations for Selected Areas: {', '.join(selected_areas)}")
        try:
            loc_map = create_top_locations_map(df_filtered, selected_areas, top_n=5)
            st_folium(loc_map, width=800, height=500)
        except Exception as e:
            st.info(f"Location markers not available: {e}")
