import pandas as pd

def ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex.")
    return df.sort_index()

def to_kwh_series(df: pd.DataFrame) -> pd.Series:
    if "kwh" not in df.columns:
        raise ValueError("Input must contain 'kwh' column.")
    s = df["kwh"].astype(float)
    s.index = pd.to_datetime(s.index, utc=True)
    return s
