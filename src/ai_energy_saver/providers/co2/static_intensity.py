from __future__ import annotations
import pandas as pd

from .base import BaseCO2Provider

class StaticCO2Provider(BaseCO2Provider):
    def __init__(self, g_per_kwh: float = 180.0):
        self.value = float(g_per_kwh)

    def intensity(self, when: pd.DatetimeIndex) -> pd.Series:
        return pd.Series([self.value] * len(when), index=when, name="g_per_kwh")
