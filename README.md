# WFM Forecasting Calculator

> **An Erlang C workforce-forecasting calculator for contact-centre planning.**

This project applies Erlang C queueing mathematics to interval volume and average-handle-time data to estimate staffing requirements, occupancy, service level, and FTE demand.

It is one of the technical precursors that informed the workforce-management engine inside Helix Prime.

## What it demonstrates

- Interval-based volume and AHT analysis
- Erlang C staffing calculations
- Shrinkage and occupancy considerations
- Variance analysis against actual demand
- Export-oriented planner outputs
- A focused operational problem solved with a transparent model

## Status

**Reference implementation / precursor project.**

The repository contains project-specific benchmark claims such as forecast variance and schedule-build time. These should be treated as historical project context rather than independently audited production evidence in this portfolio.

The broader, governed version of this operational thinking now lives in [Helix Prime](https://github.com/HatemIsmailShalaby1979/Helix-Prime).

## Run locally

    git clone https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator.git
    cd wfm-forecasting-calculator
    pip install -r requirements.txt
    streamlit run app_wfm.py

## Stack

Python · Pandas · SciPy · OpenPyXL · Streamlit

## Why it matters

This project shows the technical foundation behind the Helix direction: mathematical operational models first, governed orchestration later, and measurable outcomes throughout.

## Related work

- [Helix Prime](https://github.com/HatemIsmailShalaby1979/Helix-Prime)
- [Portfolio](https://github.com/HatemIsmailShalaby1979/HatemIsmailShalaby1979)

## License

MIT