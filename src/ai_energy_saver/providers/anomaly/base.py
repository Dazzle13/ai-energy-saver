from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class BaseAnomalyDetector(ABC):
    @abstractmethod
    def detect(self, ts: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame with columns: ts, kwh, score, is_anomaly (bool)."""
        raise NotImplementedError
