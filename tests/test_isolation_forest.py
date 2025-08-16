import pandas as pd

from ai_energy_saver.providers.anomaly.isolation_forest import IsolationForestDetector


def test_isolation_forest_detector_outputs_columns():
    # Mostly steady usage with one spike (likely anomaly)
    idx = pd.date_range("2025-08-15T20:00:00Z", periods=20, freq="30min")
    vals = [0.3] * 10 + [2.0] + [0.3] * 9
    df = pd.DataFrame({"kwh": vals}, index=idx)

    det = IsolationForestDetector(contamination=0.1, random_state=42)
    out = det.detect(df)

    assert {"ts", "kwh", "score", "is_anomaly"}.issubset(set(out.columns))
    assert len(out) == 20
    # At least one anomaly flagged
    assert out["is_anomaly"].any()
