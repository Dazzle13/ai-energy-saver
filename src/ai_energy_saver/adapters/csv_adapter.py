from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_meter(path: str | Path) -> pd.DataFrame:
    """Load meter readings from a CSV file.

    Expected columns: ``timestamp`` and ``kwh``.  Timestamps are parsed and set as
    the DataFrame index in UTC order.  Returns a DataFrame with a single ``kwh``
    column indexed by ``timestamp``.
    """
    df = pd.read_csv(Path(path))
    if "timestamp" not in df.columns or "kwh" not in df.columns:
        raise ValueError("CSV must contain 'timestamp' and 'kwh' columns")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.set_index("timestamp").sort_index()
    df["kwh"] = df["kwh"].astype(float)
    return df