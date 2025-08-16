# Model Card

## Overview
Forecast household energy use and recommend tariff-aware shifts.  
Default models are lightweight (Prophet/ARIMA) and designed for local use.

## Intended Use
- Personal or research use for basic forecasting and optimisation.
- Education and prototyping for energy analytics.

## Out-of-Scope
- Billing-grade accuracy, utility settlement, or safety-critical control.

## Training Data
- Default providers do not require central training.
- Optional private providers may use aggregated, anonymised contributor features (see `PRIVACY.md`).

## Metrics & Evaluation
- **Forecast**: MAE/MAPE on rolling backtests.
- **Optimisation**: cost/CO₂ deltas vs naïve schedule.
- **Anomaly**: precision/recall on synthetic and tagged events.

## Ethical Considerations
- Privacy by default; explicit consent for any data contribution.
- Transparent recommendations; show tariff rows and assumptions.

## Limitations
- Sparse or irregular data reduces accuracy.
- Seasonality changes (holidays, renovations) may degrade forecasts.

## Update Policy
- Semantic versioning.
- Changelogs document model/provider changes.
