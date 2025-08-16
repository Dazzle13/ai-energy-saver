from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

class BaseOptimizer(ABC):
    @abstractmethod
    def schedule(self, forecast_kwh: pd.Series, tariff: pd.DataFrame, cycles: List[Dict]) -> List[Dict]:
        """Return list of recommended cycles with start/end and savings."""
        raise NotImplementedError
