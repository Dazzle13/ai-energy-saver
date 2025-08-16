from __future__ import annotations
import math
import pandas as pd

from .base import BaseForecaster

class ProphetForecaster(BaseForecaster):
    def __init__(self, daily_seasonality: bool = True, weekly_seasonality: bool = True):
        self._model = None
        self._daily_seasonality = daily_seasonality
        self._weekly_seasonality = weekly_seasonality

    def fit(self, ts: pd.DataFrame) -> None:
        try:
            from prophet import Prophet
        except Exception as e:
            raise ImportError("prophet is required for ProphetForecaster") from e
        df = ts.reset_index()
        df.columns = ["ds", "y"]
        m = Prophet(
            daily_seasonality=self._daily_seasonality,
            weekly_seasonality=self._weekly_seasonality,
            seasonality_mode="additive",
        )
        m.fit(df)
        self._model = m

    def predict(self, horizon_hours: int = 24, freq: str = "30min") -> pd.Series:
        steps = int(math.ceil(horizon_hours * 60 / 30)) if freq == "30min" else horizon_hours
        future = self._model.make_future_dataframe(periods=steps, freq=freq, include_history=False)
        fc = self._model.predict(future).set_index("ds")["yhat"].rename("kwh")
        return fc
