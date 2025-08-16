from __future__ import annotations

import math
from typing import Optional, TYPE_CHECKING

import pandas as pd

from .base import BaseForecaster

if TYPE_CHECKING:
    # Only for typing; avoids import at runtime if prophet isn't installed yet.
    from prophet import Prophet


class ProphetForecaster(BaseForecaster):
    """
    Lightweight wrapper around Facebook Prophet for energy forecasting.

    Expects a DataFrame with DatetimeIndex and a 'kwh' column in `fit()`.
    `predict()` returns a Series of kWh for the requested horizon/frequency.
    """

    def __init__(self, daily_seasonality: bool = True, weekly_seasonality: bool = True):
        self._daily = daily_seasonality
        self._weekly = weekly_seasonality
        self._model: Optional["Prophet"] = None

    def fit(self, ts: pd.DataFrame) -> None:
        """
        Fit a Prophet model.
        Parameters
        ----------
        ts : pd.DataFrame
            Index must be DatetimeIndex; column must include 'kwh'.
        """
        try:
            from prophet import Prophet  # runtime import to keep optional
        except Exception as e:
            raise ImportError(
                "prophet is required for ProphetForecaster. Install with `pip install prophet`."
            ) from e

        if "kwh" not in ts.columns:
            raise ValueError("ProphetForecaster.fit expects a DataFrame column named 'kwh'.")

        if not isinstance(ts.index, pd.DatetimeIndex):
            raise ValueError("ProphetForecaster.fit expects a DatetimeIndex.")

        df = ts[["kwh"]].reset_index().rename(columns={"index": "ds", "kwh": "y"})
        df["ds"] = pd.to_datetime(df["ds"], utc=True)

        m = Prophet(
            daily_seasonality=self._daily,
            weekly_seasonality=self._weekly,
            seasonality_mode="additive",
        )
        m.fit(df)
        self._model = m

    def predict(self, horizon_hours: int = 24, freq: str = "30min") -> pd.Series:
        """
        Predict kWh for the next period.

        Returns
        -------
        pd.Series
            Series named 'kwh' indexed by timestamps for the forecast horizon.
        """
        if self._model is None:
            raise RuntimeError(
                "Prophet model is not initialised. Call `fit()` before `predict()`."
            )

        steps = int(math.ceil(horizon_hours * 60 / 30)) if freq == "30min" else int(horizon_hours)

        # Prophet needs a future frame to predict on.
        future = self._model.make_future_dataframe(
            periods=steps, freq=freq, include_history=False
        )
        fc = self._model.predict(future).set_index("ds")["yhat"]
        fc.index = pd.to_datetime(fc.index, utc=True)
        return fc.rename("kwh")
