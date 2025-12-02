import pandas as pd


def preprocess_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning and preprocessing steps used in the original notebook."""
    df = df.copy()

    # Standardise column names: strip, lower, replace spaces with underscores
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Drop rows with missing mocodes (if column present)
    if "mocodes" in df.columns:
        df = df.dropna(subset=["mocodes"])

    # Drop rows with missing victim sex (if column present)
    if "vict_sex" in df.columns:
        df = df.dropna(subset=["vict_sex"])

    # Drop unused crime code columns if present
    cols_to_drop = [c for c in ["crm_cd_2", "crm_cd_3", "crm_cd_4"] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    # Drop cross_street if present
    if "cross_street" in df.columns:
        df = df.drop(columns=["cross_street"])

    # Handle time_occ column: ensure HH:MM format and derive hour column
    if "time_occ" in df.columns:
        df["time_occ"] = df["time_occ"].astype(str).str.zfill(4)
        df["time_occ"] = df["time_occ"].str.replace(r"(\d{2})(\d{2})", r"\1:\2", regex=True)
        df["hour"] = df["time_occ"].str[:2].astype(int)

    return df
