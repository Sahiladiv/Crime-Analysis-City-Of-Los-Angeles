import pandas as pd


def dataset_shape(df: pd.DataFrame) -> tuple[int, int]:
    """Return (rows, columns)."""
    return df.shape


def list_columns(df: pd.DataFrame) -> list[str]:
    return list(df.columns)


def null_counts(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()


def unique_counts(df: pd.DataFrame) -> pd.Series:
    return df.nunique()


def crime_by_area(df: pd.DataFrame) -> pd.DataFrame:
    """Total crimes per area, merged with a representative lat/lon for that area if present."""
    if "area_name" not in df.columns:
        raise ValueError("DataFrame must contain an 'area_name' column")

    crime_by_area_df = df.groupby("area_name").size().reset_index(name="crime_count")

    # Attach one lat/lon pair per area if available
    latlon_cols = [c for c in ["lat", "lon"] if c in df.columns]
    if len(latlon_cols) == 2:
        location_data = df[["area_name", "lat", "lon"]].drop_duplicates()
        crime_by_area_df = crime_by_area_df.merge(location_data, on="area_name", how="left")

    return crime_by_area_df


def time_area_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Crime counts grouped by area and hour (requires 'area_name' and 'hour')."""
    if "area_name" not in df.columns or "hour" not in df.columns:
        raise ValueError("DataFrame must contain 'area_name' and 'hour' columns")
    return df.groupby(["area_name", "hour"]).size().reset_index(name="crime_count")


def top_locations_for_area(df: pd.DataFrame, area_name: str, top_n: int = 5) -> pd.DataFrame:
    """Top N locations (lat, lon) within a given area by crime count."""
    required_cols = {"area_name", "lat", "lon"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns {required_cols}")

    area_df = df[df["area_name"] == area_name]
    top_locations = (
        area_df.groupby(["lat", "lon"])
        .size()
        .reset_index(name="crime_count")
        .nlargest(top_n, "crime_count")
    )
    return top_locations


def top_locations_for_selected_areas(df: pd.DataFrame, areas: list[str], top_n: int = 5) -> pd.DataFrame:
    """Top N locations per selected area."""
    required_cols = {"area_name", "lat", "lon"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns {required_cols}")

    filtered = df[df["area_name"].isin(areas)]
    grouped = (
        filtered.groupby(["area_name", "lat", "lon"])
        .size()
        .reset_index(name="crime_count")
    )

    top_rows = (
        grouped.sort_values(["area_name", "crime_count"], ascending=[True, False])
        .groupby("area_name")
        .head(top_n)
        .reset_index(drop=True)
    )
    return top_rows


def top_crime_types_by_area(df: pd.DataFrame, areas: list[str], top_n: int = 3) -> pd.DataFrame:
    """Top N crime descriptions per selected area."""
    if "area_name" not in df.columns or "crm_cd_desc" not in df.columns:
        raise ValueError("DataFrame must contain 'area_name' and 'crm_cd_desc'")

    filtered = df[df["area_name"].isin(areas)]
    grouped = (
        filtered.groupby(["area_name", "crm_cd_desc"])
        .size()
        .reset_index(name="crime_count")
    )
    sorted_grouped = grouped.sort_values(
        ["area_name", "crime_count"], ascending=[True, False]
    )
    top_crimes = (
        sorted_grouped.groupby("area_name")
        .head(top_n)
        .reset_index(drop=True)
    )
    return top_crimes
