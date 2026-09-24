# WFM Forecasting Calculator

> **Status: building attempt.** The Erlang C model runs and produces staffing,
> occupancy, service-level, and FTE estimates from interval volume and
> average-handle-time data. No figure in this repository has an external audit,
> and the project-specific benchmark claims below are historical project context
> rather than measured results. Snapshot 2026-08-29.

One of the four building attempts from May–June 2026 — the period when I left a
twenty-eight-year operations career and started building full time, alone, while
teaching myself to write software. The thinking here was later absorbed into
Helix Prime.

## What it does

Erlang C queueing mathematics applied to interval volume and average handle time.
It estimates required staffing, occupancy, service level, and FTE demand, and it
compares a plan against actual demand.

- Interval-based volume and AHT analysis
- Erlang C staffing calculation
- Shrinkage and occupancy targets
- Variance analysis against actual demand
- Export-oriented planner outputs

## What is verified, and what is not

| Item | Status |
|---|---|
| Erlang C staffing calculation on interval input | Runs locally from the supplied data. |
| Shrinkage and occupancy adjustments | Runs locally. |
| Variance analysis against actual demand | Runs locally. |
| Forecast-variance and schedule-build-time figures | Historical project context. No recorded baseline, sample, or method. Not presented as a measured result. |
| External audit | None. |

The repository contains project-specific benchmark claims such as forecast
variance and schedule-build time. Those claims predate this documentation pass and
are kept as historical project context, not as independently audited evidence. The
caveat has applied since the project was written, and it is kept deliberately.

## Run locally

    git clone https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator.git
    cd wfm-forecasting-calculator
    pip install -r requirements.txt
    streamlit run app_wfm.py

## Stack

Python · Pandas · SciPy · OpenPyXL · Streamlit

## Honest boundary

It is a calculator, not a planning system. It does not connect to a
workforce-management platform or a live volume feed, and it does not store
history. Its output depends entirely on the interval data supplied to it. It has
no user accounts and no access control.

This is not a production deployment claim. There is no external audit, no
certified data isolation, and no signed security review. No revenue has been
realised.

## The founder's story

I spent twenty-eight years in contact-centre operations and workforce management.
Forecasting, scheduling, adherence, service levels, churn. The same problems
appeared in every company I worked in, and none of the tools solved them properly.

In April 2026 I left that career and started building full time — alone, and
teaching myself to write software as I went. The first four tools were published
six weeks later, in May and June 2026. Each one took a single operational problem
and solved it properly. They were not impressive. They were correct.

Those four tools converged into one idea: **Helix Codex**, an accountable AI
operating organization. Not an autonomous agent. An organization with a
constitution, named roles with bounded authority, evidence trails, and a human at
every consequential boundary. Helix Prime is its operations core.

WFM Forecasting Calculator is one of the four building attempts. It is maintained
by one person, with no team and no funding. It has not been externally audited and
it has not made revenue. Where it is unfinished, this document says so.

## Related work

- [Helix Prime](https://github.com/HatemIsmailShalaby1979/Helix-Prime) — the operations core
- [Helix Education](https://github.com/HatemIsmailShalaby1979/Helix-Education) — event-sourced learning engine
- [Study Studio](https://github.com/HatemIsmailShalaby1979/Study-Studio) — local-first AI tutor
- [L&D Command Center](https://github.com/HatemIsmailShalaby1979/L-D-Command-Center) — desktop learning and career workstation
- [Blue Waves](https://github.com/HatemIsmailShalaby1979/Blue-Waves-) — content studio
- [LIVE Support Assistant](https://github.com/HatemIsmailShalaby1979/LIVE-Support-Assistant) — explainable support prototype
- [Full portfolio](https://github.com/HatemIsmailShalaby1979) — the front door

### The 2026 building attempts

- [RTA Command Center](https://github.com/HatemIsmailShalaby1979/RTA_command_center)
- [CX Sentiment Sentinel](https://github.com/HatemIsmailShalaby1979/cx-sentiment-sentinel)
- [Dynamic Ops Automation Engine](https://github.com/HatemIsmailShalaby1979/Dynamic-Ops-Automation-Engine)

## Author

**Hatem Ismail Shalaby** — Operations Architect · AI Systems Engineer · Founder

- GitHub: [HatemIsmailShalaby1979](https://github.com/HatemIsmailShalaby1979)
- LinkedIn: [hatem-shalaby-202902127](https://www.linkedin.com/in/hatem-shalaby-202902127/)
- Email: hatemshalaby2025@gmail.com

Based in Al Obour City, Al-Qalyubia Governorate, Egypt.

## Licence

MIT
