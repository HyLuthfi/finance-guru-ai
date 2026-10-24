---
name: Feature Request
about: Suggest a new financial model, market data integration, or UI capability for FinanceGuru
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## Feature Overview
A clear and concise description of the proposed capability, financial model, or visualization for FinanceGuru.

---

## Problem Statement & Use Case
What financial analysis challenge, investment planning need, or user experience limitation does this feature resolve?
*(Example: "Currently, users can only analyze crypto assets; integrating equity market indices such as the IDX Composite / IHSG would broaden applicability for Indonesian retail investors.")*

---

## Proposed Enhancement Category
Select the architectural layer directly impacted:
- [ ] AI Reasoning & Agent Prompting (New Groq models, custom analyst personas)
- [ ] Quantitative Financial Modeling (Black-Scholes, Monte Carlo, DCF Valuation, CAPM)
- [ ] Market Data & Telemetry (Equities, Forex, Commodities, Precious Metals)
- [ ] Interactive Visualizations (Technical analysis indicators, RSI, MACD, Bollinger Bands)
- [ ] Portfolio Management (Multi-currency rebalancing, tax estimation, benchmark tracking)
- [ ] Export & Reporting (Automated PDF audit reports, CSV/Excel financial statements)

---

## Technical Implementation Specification
Detail the proposed engineering approach:
- **Mathematical Formulations / Algorithms**: (e.g., *Black-Scholes European call/put pricing formula with normal CDF*)
- **Target Files / Modules**: (e.g., `components/calculator.py`, `utils/api_handler.py`)
- **New Dependencies**: (Specify Python packages required; preference is given to lightweight packages)
- **Caching & Rate Limit Strategy**: (Suggested `@st.cache_data` TTL or data refresh intervals)

---

## Regulatory & Disclaimer Impact
Does this feature require additional risk disclosures or non-financial advice disclaimers? Provide details.
