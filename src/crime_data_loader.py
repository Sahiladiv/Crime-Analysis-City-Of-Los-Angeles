import pandas as pd


def load_crime_data(csv_path: str) -> pd.DataFrame:
    """Load the LA crime dataset from a CSV file."""
    df = pd.read_csv(csv_path)
    return df
