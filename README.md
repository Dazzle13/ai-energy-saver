# ai-energy-saver

*A pluggable Python library for forecasting household energy use, detecting anomalies, and suggesting tariff/CO₂-aware shifts.*

## Why
Most energy tools are locked to vendor dashboards. **ai-energy-saver** is:
- **Pluggable**: works with CSVs, smart plug exports, or adapters.
- **Action-oriented**: produces concrete suggestions (e.g., “Run washer at 21:00 → save £0.42 / 0.18 kg CO₂”).
- **Privacy-first**: local by default; optional, consented data contribution.
- **Open**: clean interfaces so anyone can extend providers and adapters.

## Features
- 📈 Forecast next 24h (Prophet/ARIMA default providers)
- 💸 Tariff-aware scheduling (find cheapest/greenest windows)
- 🔎 Standby & anomaly detection (IsolationForest + heuristics)
- 🌍 Optional CO₂ estimates via intensity tables
- 🧩 Provider system to swap forecasting/anomaly engines
- 🛠 CLI & Python API
- 🌍 Global-ready: works with any time-of-use tariff and currency. You can pass a `currency` code (e.g., USD/EUR/INR) and provide your own tariff JSON; the optimisation logic is geography-agnostic.


## Install
```bash
pip install ai-energy-saver
````

## Quickstart (CLI)

```bash
ai-energy-saver analyze \
  --meter examples/sample_meter.csv \
  --tariff examples/sample_tariff.json \
  --out report.json
```

## Quickstart (Python)

```python
from ai_energy_saver import Analyzer

an = Analyzer(meter_csv="examples/sample_meter.csv",
              tariff_json="examples/sample_tariff.json")
report = an.run()
print(report["summary"])  
# {'forecast_kwh': 9.8, 'top_saving': 'Shift washer to 21:00 → save £0.42'}
```

## Configuration

* See `config.yaml.example` and `ARCHITECTURE.md`.
* Providers can be switched via config or env:

```yaml
providers:
  forecast: "ai_energy_saver.providers.forecast.prophet_forecaster:ProphetForecaster"
  optimize: "ai_energy_saver.providers.optimize.tariff_window:TariffWindowOptimizer"
  anomaly:  "ai_energy_saver.providers.anomaly.isolation_forest:IsolationForestDetector"
  co2:      "ai_energy_saver.providers.co2.static_intensity:StaticCO2Provider"
```

## Extending

* Implement a provider interface (see `providers/*/base.py`).
* Add adapters for new data sources (e.g., Home Assistant, Octopus Energy).
* See `CONTRIBUTING.md` for guidelines.

## Privacy

* Analysis is local by default. Optional, anonymised data contribution is described in `PRIVACY.md`.

## Docs

* `ARCHITECTURE.md` – components & data flow
* `MODEL_CARD.md` – assumptions, limits, responsible AI
* `SECURITY.md` – reporting vulnerabilities
* `CONTRIBUTING.md` – how to develop and extend

## Authors

* Deep Swaroop Sachan ([@deep12650](https://github.com/deep12650))
* Karan Srinivas ([@justkarnaa](https://github.com/justkarnaa))

## License

MIT © Deep Swaroop Sachan, Karan Srinivas & contributors
