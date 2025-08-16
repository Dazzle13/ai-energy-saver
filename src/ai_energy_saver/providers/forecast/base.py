from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class BaseForecaster(ABC):
    @abstractmethod
    def fit(self, ts: pd.DataFrame) -> None:
        """ts: index datetime, column 'kwh'."""
        raise NotImplementedError

    @abstractmethod
    def predict(self, horizon_hours: int = 24, freq: str = "30min") -> pd.Series:
        """Return forecasted kWh per interval as a Series indexed by timestamp."""
        raise NotImplementedError
