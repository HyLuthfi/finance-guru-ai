---
name: Bug Report
about: Report a financial calculation anomaly, Groq API issue, or Streamlit error in FinanceGuru
title: "[BUG] "
labels: bug
assignees: ''
---

## Description
A clear and concise description of the bug encountered in the FinanceGuru assistant or calculation modules.

---

## Sub-System Affected
Please select the component where the issue occurred:
- [ ] Groq AI Chat & Inference (`components/chat.py`)
- [ ] Market Telemetry & CoinGecko API (`components/market.py` / `utils/api_handler.py`)
- [ ] Fear & Greed Sentiment Index (`components/market.py`)
- [ ] Compound Interest Calculator (`components/calculator.py`)
- [ ] Loan Amortization Schedule (`components/calculator.py`)
- [ ] DCA Wealth Simulator (`components/calculator.py`)
- [ ] Portfolio Tracker & Valuation (`components/portfolio.py`)
- [ ] Plotly Chart Rendering & Layout
- [ ] Streamlit Session State & History Persistence

---

## Financial Calculation Anomaly (If Applicable)
If the bug relates to numerical or mathematical inaccuracy:
- **Input Parameters**: (e.g., *Principal: Rp 10.000.000, Interest: 12%, Tenor: 5 Years*)
- **Expected Mathematical Output**: (e.g., *Expected FV = Rp ...*)
- **Actual App Output**: (e.g., *Received FV = Rp ...*)
- **Formula or Method Under Scrutiny**: (e.g., *Monthly compounding vs continuous compounding*)

---

## Steps to Reproduce
1. Launch app with `streamlit run app.py`
2. Navigate to Tab: `...`
3. Enter inputs or query: `...`
4. Observe error or unexpected calculation: `...`

---

## Expected vs Actual Behavior
- **Expected Behavior**: What you expected to occur.
- **Actual Behavior**: What actually happened (include error traceback if available).

---

## Environment & Configuration
- **Operating System**: (e.g., Windows 11 / Ubuntu 22.04 / macOS)
- **Python Version**: (e.g., 3.10.12 / 3.11.8)
- **Streamlit Version**: (e.g., `1.32.0`)
- **Groq Library Version**: (e.g., `0.9.0`)
- **API Key Configuration Method**: [ ] UI Input / [ ] Streamlit Secrets / [ ] `.env` file

---

## Logs & Stack Trace
```text
Paste terminal output or Streamlit traceback here (ensure all API keys and personal credentials are redacted).
```
