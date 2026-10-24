# Contributing to FinanceGuru

Thank you for your interest in contributing to **FinanceGuru: A Sophisticated AI-Driven Financial Assistant and Market Simulation Platform Built with Streamlit**.

FinanceGuru bridges generative AI reasoning via Groq LPU with rigorous quantitative financial modeling and live market data. To preserve calculation accuracy, data privacy, and legal compliance, please review the contribution guidelines below.

---

## 🏛️ Code of Conduct & Financial Ethics

When contributing to FinanceGuru, all contributors must uphold the following core principles:

1. **Strict Non-Financial Advice Policy**: FinanceGuru is an educational and analytical platform. All prompt designs, LLM responses, and calculation outputs must reinforce that information provided does not constitute certified financial, legal, or investment advice.
2. **Mathematical & Numerical Accuracy**: All financial calculation modules (annuities, amortizations, compounding, risk metrics) must be verified against analytical benchmarks with robust edge-case handling (e.g., zero interest rates, negative returns, zero division).
3. **User Financial Privacy (Zero-Storage Policy)**: Never introduce code that persists sensitive portfolio balances, transaction histories, or user identity records to disk or unvetted external services. All session state must remain ephemeral within `st.session_state`.
4. **Credential Security**: Never commit API keys (`GROQ_API_KEY`, market tokens) or personal `.streamlit/secrets.toml` files.

---

## 🛠️ Local Development Setup

### 1. Prerequisites

- **Python 3.10+** (tested on Python 3.10, 3.11, and 3.12)
- A **Groq API Key** (obtain free access at [console.groq.com](https://console.groq.com/))
- A virtual environment tool (`venv`, `conda`, or `uv`)

### 2. Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/HyLuthfi/finance-guru-ai.git
cd finance-guru-ai

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure local environment variables
cp .env.example .env
# Edit .env and insert your GROQ_API_KEY

# Alternatively, configure Streamlit secrets:
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 5. Launch the Streamlit application
streamlit run app.py
```

---

## 📐 Implementing New Quantitative Financial Models

We welcome additions of quantitative financial tools (e.g., **Black-Scholes Options Pricing**, **Monte Carlo Portfolio Simulation**, **Discounted Cash Flow (DCF) Valuation**, or **Sortino / Treynor Ratios**):

### 1. Mathematical Standards & Validation
- Modularize functions under `components/calculator.py` or create specialized helper modules under `utils/`.
- Provide docstrings documenting formulas, variable definitions, and unit assumptions (e.g., annual vs monthly rates).
- Enforce guards against numerical exceptions:
  ```python
  def hitung_amortisasi(pokok, bunga_tahunan, tenor_tahun):
      if pokok <= 0 or tenor_tahun <= 0:
          return 0.0, []
      
      bunga_bulanan = (bunga_tahunan / 100) / 12
      total_bulan = int(tenor_tahun * 12)
      
      # Zero-division guard for 0% interest scenarios
      if bunga_bulanan == 0:
          cicilan = pokok / total_bulan
          return cicilan, [...]
      
      faktor = (1 + bunga_bulanan) ** total_bulan
      cicilan = pokok * (bunga_bulanan * faktor) / (faktor - 1)
      return cicilan, [...]
  ```

### 2. Market Data Integration
- When adding new asset classes (Indonesian Stock Exchange / IDX, US Equities, Commodities):
  - Integrate free, public endpoints via `utils/api_handler.py`.
  - Apply `@st.cache_data` decorators with reasonable time-to-live (`ttl=120` to `ttl=300`) to respect API rate limits.
  - Implement graceful fallbacks when external APIs experience rate-limiting or network downtime.

---

## 🧪 Testing & Pre-Commit Validation

Before opening a pull request, ensure that your modifications execute cleanly:

### 1. API Resolution Smoke Test
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
from components.chat import dapatkan_klien_groq
client = dapatkan_klien_groq()
print('Groq client initialized successfully:', client is not None)
"
```

### 2. Quantitative Calculation Integrity Test
```bash
python -c "
from components.calculator import hitung_bunga_majemuk
total, pokok, bunga = hitung_bunga_majemuk(10_000_000, 1_000_000, 10.0, 5)
assert total > pokok, 'Future value must exceed principal'
print(f'Compound interest test passed: Total FV = Rp {total:,.2f}')
"
```

### 3. Application Launch Test
```bash
streamlit run app.py --server.headless true
# Verify startup on http://localhost:8501 without runtime syntax errors
```

---

## 🌿 Git Workflow & Conventional Commits

1. Branch from `main` using descriptive names:
   ```bash
   git checkout -b feature/dcf-calculator
   # or
   git checkout -b fix/market-cache-ttl
   ```
2. Commit with **Conventional Commits**:
   - `feat(calc)`: New financial formula, valuation engine, or simulator
   - `feat(chat)`: Enhancements to Groq model router or prompt engineering
   - `feat(market)`: New telemetry endpoints or interactive Plotly chart types
   - `fix(formula)`: Bug fixes in financial mathematics or edge-case handling
   - `perf(cache)`: Optimizations in API call frequency or session state
   - `docs(readme)`: Updates to documentation, architectural diagrams, or runbooks
   - `chore(security)`: Dependency updates or `.gitignore` hardening
3. Maintain a clean working tree and verify that no secret files or runtime logs are tracked.

---

## 🔒 Security & Vulnerability Reporting

If you identify a security issue, API key exposure, or privacy vulnerability:
- Do **NOT** disclose the issue publicly in an open GitHub issue.
- Contact the lead maintainer directly: **Luthfi Muthathohirin** at `luthfirg2502@gmail.com`.
- Security reports receive priority triage and remediation within 24 hours.

---

## 📄 License & Attribution

By contributing to FinanceGuru, you agree that your contributions will be licensed under the project's **MIT License** with copyright attributed to **Luthfi Muthathohirin**.
