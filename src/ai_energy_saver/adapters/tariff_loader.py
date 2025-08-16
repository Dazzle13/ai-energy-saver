from typing import Union
from pathlib import Path
import json
import pandas as pd

def load_tariff(path: Union[str, Path]) -> pd.DataFrame:
    """
    JSON list of objects:
    [
      {"start": "20:00", "end": "23:00", "price_per_kwh": 0.12},
      {"start": "23:00", "end": "07:00", "price_per_kwh": 0.08},
      {"start": "07:00", "end": "20:00", "price_per_kwh": 0.30}
    ]
    Times are daily wall-clock. Non-overlapping expected.
    """
    data = json.loads(Path(path).read_text())
    df = pd.DataFrame(data)
    for col in ("start", "end"):
        if col not in df.columns:
            raise ValueError("Tariff JSON entries must have 'start' and 'end'")
    if "price_per_kwh" not in df.columns:
        raise ValueError("Tariff JSON entries must have 'price_per_kwh'")
    return df
