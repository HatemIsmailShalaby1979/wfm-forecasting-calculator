# 📞 WFM Forecasting Calculator

**Complete Workforce Management Planning Toolkit**

Built by [Hatem Shalaby](https://linkedin.com/in/hatem-shalaby-7359611a2)

## 🎯 What This Does

Professional-grade WFM calculations:
- ✅ **Erlang C Staffing** - Calculate required agents for target service level
- 📊 **Interval Planning** - 30-minute interval staffing for full day
- 📉 **Shrinkage Analysis** - Break down non-productive time
- 👥 **FTE Planning** - Account for shrinkage & absenteeism
- 💰 **Cost Modeling** - Calculate total workforce costs

## 🚀 Quick Start

```bash
cd wfm-forecasting-toolkit
pip install -r requirements.txt
streamlit run src/app_wfm.py
```

## 📊 Calculation Modes

### Mode 1: Quick Staffing
Input: Call volume, AHT, target SL  
Output: Required agents with sensitivity analysis

### Mode 2: Interval Planning
Input: 24-hour call volumes  
Output: 30-minute interval staffing plan

### Mode 3: Shrinkage Analysis
Input: Time allocations (breaks, meetings, etc.)  
Output: Total shrinkage % with breakdown

### Mode 4: FTE Planning
Input: Base agents + shrinkage + absenteeism  
Output: Total FTE needed + cost analysis

## 🧮 Formulas

**Erlang C:** [A^N / N!] × [N/(N-A)] / Σ

**Service Level:** 1 - [Pw × e^(-(N-A)×t/AHT)]

**Occupancy:** (A / N) × 100

## 📝 License

MIT License - Free to use

## 👤 Author

**Hatem Shalaby** | RTA & WFM Automation Expert
