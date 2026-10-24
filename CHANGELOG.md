# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-19

### Added
- **5-Layer FinTech AI & Market Simulation Architecture**: Enterprise system design organizing Presentation, AI Reasoning, Market Data Telemetry, Quantitative Calculation, and In-Memory Ephemeral Sessions.
- **Ultra-Low Latency Groq LPU Inference Core**: Integration with Groq Cloud supporting dynamic model selection between `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, and `mixtral-8x7b-32768`.
- **System Prompt Guardrails & Disclaimer Standard**: Built-in personas for professional wealth advisory and educational guidance, enforcing strict non-financial advice disclaimers.
- **Real-Time Crypto Market Telemetry & Sentiment Engine**: CoinGecko REST API client with intelligent tiered caching (`@st.cache_data(ttl=120)`) and Alternative.me Crypto Fear & Greed Index telemetry (`@st.cache_data(ttl=300)`).
- **Interactive Plotly 5.20+ Market Visualizations**: Rich interactive price area charts, volume sparklines, and metric cards for top cryptocurrencies.
- **Quantitative Calculation Engine**:
  - Compound Interest with periodic deposits simulator using Future Value ($FV$) annuity formulas.
  - Loan and mortgage amortization schedule calculator.
  - Dollar Cost Averaging (DCA) wealth projection model.
  - Net trading Profit/Loss calculator with fee deduction.
- **Dynamic Multi-Asset Portfolio Tracker**: Real-time valuation tracking computing holdings value against live market quotes with portfolio allocation breakdowns.
- **Vectorized D2 Architecture Topology**: Terminal Dark 5-layer system diagram compiled to `assets/architecture.svg` (51.5KB).
- **Mathematical Formula Vector Card**: 3-panel SVG card `assets/financial_formulas.svg` (15.2KB) featuring Future Value annuity, Monthly Amortization ($M$), DCA compounding, and Sharpe Ratio formulations.
- **Dashboard UI Showcase Gallery**: 4 embedded interface screenshots (`dashboard_chat.png`, `Live_Market.png`, `Kalkulator.png`, `Portofolio.png`).
- **Enterprise 9-Element README Showcase**: Comprehensive technical documentation with feature matrix, quantitative modeling breakdown, and deployment runbooks.
- **Environment & Configuration Templates**: Standardized `.env.example` and `.streamlit/secrets.toml.example` files.

### Changed
- Refactored `app.py` and `components/chat.py` to implement secure tiered API key fallback resolution: UI Session State $\rightarrow$ Streamlit Secrets $\rightarrow$ OS Environment Variables.
- Pinned core dependencies in `requirements.txt` (`streamlit>=1.32.0`, `groq>=0.9.0`, `plotly>=5.20.0`, `requests>=2.31.0`, `python-dotenv>=1.0.0`) to prevent supply chain breaks.

### Security
- **SPDX MIT License Legal Protection**: Published formal `LICENSE` file under MIT terms with copyright attribution to `Luthfi Muthathohirin` (P0).
- **Audit Secret Scan Certification**: 100% clean Gitleaks v8.30.1 scan across all 11 commits with 0 secret leaks detected (P0).
- **Hardened `.gitignore` Filter**: Expanded repository exclusion rules to 125 patterns covering `.streamlit/secrets.toml`, `.env*`, transaction exports, financial logs, and cache directories (P0).
- **Zero-Storage Financial Privacy Standard**: Enforced ephemeral in-memory processing where portfolio holdings and conversation sessions exist solely in volatile browser state (`st.session_state`) with zero server-side disk persistence.
