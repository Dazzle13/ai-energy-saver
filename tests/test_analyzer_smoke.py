from pathlib import Path
import json

from ai_energy_saver.analyzer import Analyzer


def test_analyzer_smoke(tmp_path: Path):
    meter = tmp_path / "meter.csv"
    meter.write_text(
        "timestamp,kwh\n"
        "2025-08-15T20:00:00Z,0.42\n"
        "2025-08-15T20:30:00Z,0.35\n"
        "2025-08-15T21:00:00Z,0.30\n"
        "2025-08-15T21:30:00Z,0.28\n"
    )

    tariff = tmp_path / "tariff.json"
    tariff.write_text(
        json.dumps(
            [
                {"start": "23:00", "end": "07:00", "price_per_kwh": 0.08},
                {"start": "07:00", "end": "20:00", "price_per_kwh": 0.30},
                {"start": "20:00", "end": "23:00", "price_per_kwh": 0.12},
            ]
        )
    )

    an = Analyzer(meter_csv=str(meter), tariff_json=str(tariff))
    report = an.run()

    assert "summary" in report and "forecast" in report
    assert isinstance(report["summary"].get("forecast_kwh"), float)
    assert isinstance(report.get("recommendations"), list)
