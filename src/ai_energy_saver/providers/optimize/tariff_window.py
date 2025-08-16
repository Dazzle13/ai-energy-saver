from __future__ import annotations

from datetime import time
from typing import Dict, List

import pandas as pd

from .base import BaseOptimizer


def _parse_hhmm(hhmm: str) -> time:
    h, m = map(int, hhmm.split(":"))
    return time(hour=h, minute=m)

def _price_for_timestamp(tariff_df: pd.DataFrame, ts: pd.Timestamp) -> float:
    # Map wall-clock time to price bucket
    tt = ts.tz_convert("UTC").time() if ts.tzinfo else ts.time()
    for _, row in tariff_df.iterrows():
        start = _parse_hhmm(str(row["start"]))
        end = _parse_hhmm(str(row["end"]))
        price = float(row["price_per_kwh"])
        if start <= end:
            if start <= tt < end:
                return price
        else:
            # Wraps midnight
            if tt >= start or tt < end:
                return price
    # fallback
    return float(tariff_df.iloc[0]["price_per_kwh"])

def _cost_of_series_kwh(forecast_kwh: pd.Series, tariff_df: pd.DataFrame) -> float:
    return float(sum(float(k) * _price_for_timestamp(tariff_df, ts) for ts, k in forecast_kwh.items()))

class TariffWindowOptimizer(BaseOptimizer):
    """
    Greedy window search: for each cycle, slide a fixed-duration window over the next 24h
    using forecast_kwh timestamps; compute cost using tariff; choose lowest-cost start.
    """

    def schedule(self, forecast_kwh: pd.Series, tariff: pd.DataFrame, cycles: List[Dict]) -> List[Dict]:
        recs: List[Dict] = []

        slot_minutes = int((forecast_kwh.index[1] - forecast_kwh.index[0]).total_seconds() / 60)
        slots_per_hour = max(1, 60 // slot_minutes)

        baseline_cost = _cost_of_series_kwh(forecast_kwh, tariff)

        for c in cycles:
            name = c.get("name", "cycle")
            duration_h = float(c.get("duration_h", 2))
            kwh_total = float(c.get("kwh", 1.0))
            slots_needed = int(duration_h * slots_per_hour)
            if slots_needed <= 0 or slots_needed > len(forecast_kwh):
                continue

            # Assume uniform kWh during cycle
            kwh_per_slot = kwh_total / slots_needed

            best_start_idx = None
            best_cost = float("inf")

            for i in range(0, len(forecast_kwh) - slots_needed + 1):
                window_index = forecast_kwh.index[i : i + slots_needed]
                # Cost of running cycle in this window
                window_cost = sum(_price_for_timestamp(tariff, ts) * kwh_per_slot for ts in window_index)
                if window_cost < best_cost:
                    best_cost = window_cost
                    best_start_idx = i

            if best_start_idx is None:
                continue

            start_ts = forecast_kwh.index[best_start_idx]
            end_ts = forecast_kwh.index[best_start_idx + slots_needed - 1]

            # Naive "run now" cost estimation: use first available window
            now_window_index = forecast_kwh.index[:slots_needed]
            now_cost = sum(_price_for_timestamp(tariff, ts) * kwh_per_slot for ts in now_window_index)

            saving = max(0.0, now_cost - best_cost)

            recs.append(
                {
                    "name": name,
                    "start": start_ts.isoformat(),
                    "end": end_ts.isoformat(),
                    "saving_gbp": float(round(saving, 4)),
                    "explanation": f"Shift {name} to {start_ts.strftime('%H:%M')}–{end_ts.strftime('%H:%M')} to save £{saving:.2f}",
                }
            )

        return recs
