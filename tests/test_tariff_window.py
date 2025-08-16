import pandas as pd

from ai_energy_saver.providers.optimize.tariff_window import TariffWindowOptimizer


def test_tariff_window_optimizer_basic():
    # Build simple forecast: 30-min slots, next 4 slots
    idx = pd.date_range("2025-08-15T20:00:00Z", periods=4, freq="30min")
    forecast = pd.Series([0.3, 0.3, 0.3, 0.3], index=idx, name="kwh")

    # Tariff JSON-equivalent DataFrame
    tariff = pd.DataFrame(
        [
            {"start": "23:00", "end": "07:00", "price_per_kwh": 0.08},
            {"start": "07:00", "end": "20:00", "price_per_kwh": 0.30},
            {"start": "20:00", "end": "23:00", "price_per_kwh": 0.12},
        ]
    )

    opt = TariffWindowOptimizer()
    recs = opt.schedule(
        forecast_kwh=forecast,
        tariff=tariff,
        cycles=[{"name": "washer", "kwh": 1.2, "duration_h": 1}],
    )

    assert isinstance(recs, list)
    assert recs, "expected at least one recommendation"
    r0 = recs[0]
    for key in ["name", "start", "end", "saving_gbp", "explanation"]:
        assert key in r0
