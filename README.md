<div align="center">

# WFM Forecasting Calculator


<!-- badges:start -->

[![CI](https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator/actions/workflows/Python%20package/badge.svg)](https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator/actions)
![licence](https://img.shields.io/badge/licence-MIT-blue)
[![last commit](https://img.shields.io/github/last-commit/HatemIsmailShalaby1979/wfm-forecasting-calculator)](https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator/commits/main)
![status](https://img.shields.io/badge/ci-success-brightgreen?label=success%20(2026-10-05))

*Measured 2026-10-06 — CI **success**; head `04e84dc` (2026-10-05); Python.*

<!-- No static test or coverage count is shown here: a frozen
     number decays silently. Run the suite for a current figure;
     the CI badge above is the live status. -->
<!-- badges:end -->

**A precursor to Helix Prime — the Erlang C engine that became its WFM module.**

![Status](https://img.shields.io/badge/status-learning--exercise-yellow)
![Type](https://img.shields.io/badge/type-precursor-blue)
![Licence](https://img.shields.io/badge/licence-MIT-blue)
![Python](https://img.shields.io/badge/python-3.12-3776ab)

</div>

## One-line identity

A May–June 2026 learning exercise: a standalone Erlang C workforce-management calculator. Its forecasting maths is the original sketch of what became Helix Prime's `engines/wfm/` module.

> [!NOTE]
> **Operating principle.** The maths is the point. `shared_utils/erlang_c.py` implements the five standard WFM calculations as pure static methods, and its own self-test passes. The Streamlit UI on top of it does not start from a clean install — that is a packaging gap, not a maths gap.

One of four small tools built during the May–June 2026 period, before Helix Prime existed. The Erlang C mathematics here is the same approach that later became Helix Prime's WFM engine (`engines/wfm/`). This repository is the original sketch; Helix Prime is the system.

## What works today

**The Erlang C engine. This is real, and it is the reason to look at this repository.** `shared_utils/erlang_c.py` implements the five standard workforce-management calculations as pure static methods on `ErlangCCalculator`:

| Method | What it returns |
|---|---|
| `erlang_c(agents, traffic_intensity)` | Probability that an arriving contact has to wait |
| `service_level(agents, traffic_intensity, target_answer_time, aht)` | Percentage answered within the target |
| `average_speed_of_answer(agents, traffic_intensity, aht)` | Mean wait, in seconds |
| `occupancy(traffic_intensity, agents)` | Agent utilisation, as a percentage |
| `required_agents(volume, aht, interval, target_sl, target_answer_time)` | The staffing figure that meets a service-level target, with the achieved SL, occupancy, and ASA beside it |

The repository ships its own self-test inside the module. **Measured on 2026-09-27, run against the code as committed:**

```text
Running Erlang C Tests...
✅ Test 1 Passed: Erlang C = 0.5299
✅ Test 2 Passed: Service Level = 86.70%
✅ Test 3 Passed: ASA = 10.09 seconds
✅ Test 4 Passed: Occupancy = 70.83%
✅ Test 5 Passed: Required 14 agents

✅ ALL ERLANG C TESTS PASSED
```

Those are the engine's own assertions, not a summary. The maths checks out at the boundary cases too: `erlang_c(10, 8.5) = 0.5299` sits correctly between 0 and 1, and `occupancy(8.5, 12) = 70.83%` is the expected `traffic ÷ agents`.

**The Streamlit app is substantial.** `app_wfm.py` is 416 lines and covers four modes — a quick staffing calculator, an interval staffing plan, a shrinkage calculator, and an FTE requirement calculator with a monthly cost projection. `src/data_pipeline.py` and `src/variance_engine.py` handle batch input and plan-vs-actual variance, exporting to Excel. `data/sample_intervals.csv` and `data/actuals.csv` are small illustrative inputs so the app has something to load.

## What does not work

- **`requirements.txt` contains one line: `streamlit==1.31.0`.** `app_wfm.py` imports `pandas`, `plotly.graph_objects`, and `numpy` as well. A reader who follows the documented install gets an `ImportError` on first run. This is the single most useful thing to fix in this repository.
- **`SciPy` is not used.** Earlier revisions listed the stack as "Python · Pandas · SciPy · OpenPyXL · Streamlit". SciPy is imported by no file in the repository (zero matches). OpenPyXL is used, but only via pandas' `to_excel(engine=...)` in the two `src/` scripts.
- **There is no test suite.** `test_erlang_c()` is a print-and-assert function living inside the library module rather than under a test runner. It works, but nothing collects it, and it prints checkmarks instead of reporting pass/fail to a harness.
- **It is a calculator, not a planning system.** No workforce-management platform integration, no live volume feed, no history, no persistence, no user accounts, no access control.

## Repository hygiene

Tracked files that should be removed rather than described:

- `__pycache__/erlang_c.cpython-314.pyc` — a compiled artefact committed by accident.
- `output/fte_schedule.xlsx` and `output/variance_report.xlsx` — generated output, committed.
- Five `.txt` duplicates of the source files (`wfm-forecasting-toolkitREADME.md.txt`, `...requirements.txt.txt`, `...srcapp_wfm.py.txt`, `...srcerlang_c.py.txt`, `...examplessample_hourly_volumes.csv.xlsx`). These are upload-interface artefacts, not content.

## Run it

The engine alone needs nothing but the standard library and a `sys.path` entry:

```bash
git clone https://github.com/HatemIsmailShalaby1979/wfm-forecasting-calculator.git
cd wfm-forecasting-calculator
python -c "
import sys; sys.path.insert(0, '.')
from shared_utils.erlang_c import ErlangCCalculator as E
print(E.erlang_c(10, 8.5))
print(E.required_agents(100, 180, 30, 0.8, 20))
"
```

For the Streamlit app, install what the code actually imports rather than what `requirements.txt` says:

```bash
pip install streamlit pandas plotly numpy openpyxl
streamlit run app_wfm.py
```

The second argument to `required_agents` is an average handling time in **seconds**, not minutes — the app converts before calling it, and a caller who passes minutes gets a quietly wrong answer rather than an error.

> [!WARNING]
> **Honest boundary.** This is a learning exercise. It is not a deployed service, and it does not connect to any workforce-management platform or live volume feed. Its output depends entirely on the interval data supplied to it. It has no authentication and no access control. No revenue was realised. There is no external audit, no certified data isolation, and no signed security review.
>
> Earlier revisions of this file carried benchmark claims about forecast variance and schedule-build time. No baseline, sample, or method was recorded for either, so neither is repeated here.

## Related work

- [Helix Prime](https://github.com/HatemIsmailShalaby1979/Helix-Prime) — the operations core; `engines/wfm/` is where this maths ended up
- [Helix Education](https://github.com/HatemIsmailShalaby1979/Helix-Education) — event-sourced learning engine
- [Study Studio](https://github.com/HatemIsmailShalaby1979/Study-Studio) — local-first AI tutor
- [L&D Command Center](https://github.com/HatemIsmailShalaby1979/L-D-Command-Center) — desktop learning and career workstation
- [Blue Waves](https://github.com/HatemIsmailShalaby1979/Blue-Waves-) — content studio
- [Full portfolio](https://github.com/HatemIsmailShalaby1979) — how this fits the wider work

### The other 2026 building attempts

- [RTA Command Center](https://github.com/HatemIsmailShalaby1979/RTA_command_center)
- [CX Sentiment Sentinel](https://github.com/HatemIsmailShalaby1979/cx-sentiment-sentinel) — the repository name overpromises; the code is a KPI-decay risk scorer
- [Dynamic Ops Automation Engine](https://github.com/HatemIsmailShalaby1979/Dynamic-Ops-Automation-Engine)

## Author

Built by Hatem Ismail Shalaby, Contact Centre Operations & AI Implementation Lead | WFM & CX Transformation. Background: https://github.com/HatemIsmailShalaby1979

## Licence

MIT
