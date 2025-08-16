from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest

from .base import BaseAnomalyDetector


class IsolationForestDetector(BaseAnomalyDetector):
    """Detect anomalies in energy usage using scikit-learn's IsolationForest."""

    def __init__(self, contamination: float = 0.05, random_state: int | None = None):
        self._model = IsolationForest(contamination=contamination, random_state=random_state)

    def detect(self, ts: pd.DataFrame) -> pd.DataFrame:
        if "kwh" not in ts.columns:
            raise ValueError("Input must contain 'kwh' column")
        df = ts.copy()
        self._model.fit(df[["kwh"]])
        scores = self._model.decision_function(df[["kwh"]])
        preds = self._model.predict(df[["kwh"]])
        df = df.copy()
        df["score"] = scores
        df["is_anomaly"] = preds == -1
        return df.reset_index().rename(columns={df.index.name or "index": "ts"})