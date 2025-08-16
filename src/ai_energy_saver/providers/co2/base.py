from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd

class BaseCO2Provider(ABC):
    @abstractmethod
    def intensity(self, when: pd.DatetimeIndex) -> pd.Series:
        """Return gCO2/kWh series aligned to timestamps."""
        raise NotImplementedError
