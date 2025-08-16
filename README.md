
# `ai-energy-saver` ⚡

*A pluggable Python library for forecasting energy use, detecting anomalies, and suggesting cost/CO₂-saving shifts based on tariff data.*

---

## 🔹 Why this library?

Household and small-scale IoT devices generate a lot of energy data, but most tools are locked into closed dashboards or require vendor-specific hardware. `ai-energy-saver` is:

* **Pluggable** → works with any time-series (CSV, smart plug export, smart meter API).
* **Action-oriented** → not just dashboards, but concrete suggestions like *“Run washer at 21:00 → save £0.42 and 0.18kg CO₂”*.
* **Lightweight & transparent** → runs locally, no cloud lock-in, explainable outputs.
* **Open source** → designed for developers, researchers, and civic tech projects.

---

## 🔹 Key Features

* 📈 **Forecasting** – predict 24h energy usage with seasonality (Prophet/ARIMA).
* 💸 **Tariff-aware scheduling** – find cheapest/greenest windows for appliances.
* 🔎 **Anomaly detection** – identify standby drain and unusual consumption spikes.
* 🌍 **CO₂ insights** – estimate carbon savings alongside cost.
* 🛠 **Pluggable adapters** – start with CSV, extend to APIs (Octopus, Home Assistant).
* 📦 **Library + CLI** – import in Python or run quick analyses from the terminal.

---

## 🔹 Quickstart

### Installation

```bash
pip install ai-energy-saver
```

### Example (Python)

```python
from ai_energy_saver import Analyzer

analyzer = Analyzer(meter_csv="examples/sample_meter.csv", 
                    tariff_json="examples/sample_tariff.json")

report = analyzer.run()

print(report["summary"])
# => {'forecast_kwh': 9.8, 'top_saving': 'Shift washer to 21:00 → save £0.42'}
```

### Example (CLI)

```bash
ai-energy-saver analyze \
  --meter examples/sample_meter.csv \
  --tariff examples/sample_tariff.json \
  --out report.json
```

---

## 🔹 Sample Output

```json
{
  "date": "2025-08-16",
  "forecast_kwh": 9.8,
  "top_actions": [
    {"action":"Shift washing machine 20:00→22:00","saving_gbp":0.42,"saving_co2_kg":0.18}
  ],
  "anomalies":[
    {"period":"02:00–04:00","excess_watts":28,"confidence":0.83}
  ]
}
```

---

## 🔹 Roadmap

* ✅ v0.1: CSV/JSON input, forecasting, tariff optimisation, CLI
* 🔜 v0.2: CO₂ intensity lookup, anomaly detection refinements
* 🔜 v0.3: API adapters (For Energy Companies, Home Assistant)
* 🔜 v0.4: Web demo + visualisation

---

## 🔹 Contributing

Contributions are welcome!

* Fork and PR
* Add test cases in `/tests`
* Follow style guide in `CONTRIBUTING.md`

---

## 🔹 License

MIT License © 2025 Your Name

---

## 🔹 Citation / Recognition

If you use this library in research or projects, please cite:

```
@software{ai_energy_saver,
  author = {Your Name},
  title = {ai-energy-saver: Open-Source AI for Household Energy Forecasting and Savings},
  year = {2025},
  url = {https://github.com/YOURNAME/ai-energy-saver}
}
```

---

## 🔹 Why it matters

This project shows how **AI can help everyday users reduce bills and cut emissions** by making smart energy optimisation accessible through a simple, pluggable library. It is lightweight enough for job seekers, researchers, and civic tech projects to adopt, yet scalable for integration into IoT systems and sustainability platforms.
