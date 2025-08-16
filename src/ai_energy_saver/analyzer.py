from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from .adapters.csv_adapter import load_meter
from .adapters.tariff_loader import load_tariff
from .core.features import ensure_datetime_index, to_kwh_series
from .providers.forecast.prophet_forecaster import ProphetForecaster
from .providers.optimize.tariff_window import TariffWindowOptimizer
from .providers.anomaly.isolation_forest import IsolationForestDetector


class Analyzer:
    """
    High-level convenience orchestrator for one-shot analysis.
    Expect meter CSV with columns: timestamp,kwh (UTC or local).
    Tariff JSON: [{"start":"HH:MM","end":"HH:MM","price_per_kwh":0.12}, ...]
    """

    def __init__(self, meter_csv: str, tariff_json: str):
        self.meter_csv = Path(meter_csv)
        self.tariff_json = Path(tariff_json)

    def run(self) -> Dict[str, Any]:
        # Load inputs
        ts = load_meter(self.meter_csv)                  # DataFrame with index=Timestamp, column 'kwh'
        ts = ensure_datetime_index(ts)
        kwh = to_kwh_series(ts)

        tariff = load_tariff(self.tariff_json)           # DataFrame with start,end,price_per_kwh (time only)

        # Forecast
        forecaster = ProphetForecaster()
        forecaster.fit(kwh.to_frame("kwh"))
        forecast = forecaster.predict(horizon_hours=24, freq="30min")  # Series of kWh per slot

        # Optimise (simple default cycle)
        optimizer = TariffWindowOptimizer()
        cycles = [{"name": "washer", "kwh": 1.2, "duration_h": 2, "latest_start": "23:00"}]
        recommendations = optimizer.schedule(forecast, tariff, cycles)

        # Anomalies
        detector = IsolationForestDetector()
        anomalies = detector.detect(kwh.to_frame("kwh"))

        # Simple summary
        total_kwh_forecast = float(forecast.sum())
        top_actions = [
            {
                "action": r["explanation"],
                "saving_gbp": round(r["saving_gbp"], 2),
            }
            for r in recommendations
        ]

        return {
            "summary": {
                "forecast_kwh": round(total_kwh_forecast, 3),
                "top_actions": top_actions[:3],
            },
            "forecast": forecast.reset_index().rename(columns={"index": "ts", 0: "kwh"}).to_dict(orient="records"),
            "anomalies": anomalies.to_dict(orient="records"),
            "recommendations": recommendations,
        }
