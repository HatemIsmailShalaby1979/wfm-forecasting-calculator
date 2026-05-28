# WFM Forecasting Engine
> Erlang C-powered FTE demand forecasting system that delivers sub-8% variance against actual staffing requirements, replacing manual spreadsheet forecasting for contact center operations.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---
## Executive Summary
Contact center staffing operated on manual interval-based forecasting, producing variance rates of 18–25% against actual demand — a direct driver of SLA breaches and overstaffing costs. This engine applies the Erlang C queuing model to historical volume and AHT data, generating statistically grounded FTE requirements per interval. Deployed forecasts consistently achieve <8% variance, reducing schedule build time from 6 hours to under 40 minutes per cycle.

---
## Business Impact
| Metric | Baseline | Post-Deployment | Delta |
|---|---|---|---|
| Forecast Variance | 18–25% | <8% | ↓ 17 pts avg |
| Weekly Schedule Build Time | ~6 hrs manual | ~40 min | ↓ 89% |
| SLA Achievement Rate | 71% | 88% | ↑ 17 pts |
| Overstaffing Cost Exposure | High (untracked)| Quantified/Bounded | Controlled |

---
## Architecture Overview
```mermaid
flowchart LR
    A[("Raw Volume Data\nCSV / DB Extract")] --> B["Data Ingestion Layer\npandas pipeline"]
    B --> C["Interval Normalizer\n30-min bucketing"]
    C --> D["AHT Aggregator\nRolling avg per skill"]
    D --> E[["Erlang C Core\nP(wait), Intensity,\nAgent occupancy"]]
    E --> F["Variance Engine\nActual vs Forecast\ndelta scoring"]
    F --> G["FTE Output Layer\nInterval staffing matrix"]
    G --> H[("Schedule Export\n.xlsx / API feed")]
    style E fill:#1a1a2e,color:#e0e0ff,stroke:#7b7bff
Tech Stack JustificationComponentTechnologyRationaleForecasting CorePython / Erlang CErlang C is the industry standard queuing model for contact center staffing; validated against Poisson arrival assumptions present in our dataData ManipulationPandasVectorized interval aggregation at scale; native CSV/SQL/Excel I/O avoids middleware overheadStatistical LayerSciPyUsed for confidence interval computation and distribution fitting on AHT dataSchedule ExportOpenPyXLDirect .xlsx generation for planner consumption without format conversion lossOrchestrationCronLightweight; no orchestration framework justified at current pipeline complexity
Deployment
Prerequisites
Python 3.11+

Input data: 30-min interval volume + AHT by skill/queue
Local Setup
git clone [https://github.com/ThommyShelby79/wfm-forecasting-engine.git](https://github.com/ThommyShelby79/wfm-forecasting-engine.git)
cd wfm-forecasting-engine
pip install -r requirements.txt
cp config/.env.example config/.env
Run
# Batch forecast from CSV
python src/data_pipeline.py --input data/sample_intervals.csv --output output/fte_schedule.xlsx

# Variance report against actuals
python src/variance_engine.py --forecast output/fte_schedule.xlsx --actuals data/actuals.csv
Author
Hatem Shalaby — Operations Architect & Automation Engineer
LinkedIn · Portfolio · Email
