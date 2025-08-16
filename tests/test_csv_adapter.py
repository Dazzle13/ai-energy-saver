from pathlib import Path
import pandas as pd

from ai_energy_saver.adapters.csv_adapter import load_meter


def test_load_meter_parses_and_indexes(tmp_path: Path):
    p = tmp_path / "meter.csv"
    p.write_text(
        "timestamp,kwh\n"
        "2025-08-15T20:00:00Z,0.42\n"
        "2025-08-15T20:30:00Z,0.35\n"
    )

    df = load_meter(p)
    assert list(df.columns) == ["kwh"]
    assert isinstance(df.index, pd.DatetimeIndex)
    assert len(df) == 2
    # Ensure values are floats and sorted
    assert float(df.iloc[0, 0]) == 0.42
    assert df.index.is_monotonic_increasing
