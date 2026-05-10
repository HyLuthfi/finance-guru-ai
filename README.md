# FinanceGuru AI

A comprehensive, AI-powered financial dashboard and investment assistant built with Streamlit and the Groq API. Designed for high-performance market analysis, strategic financial planning, and intelligent portfolio tracking.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-00C7B7?style=for-the-badge&logo=groq&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## Overview

FinanceGuru AI is a sophisticated financial platform that combines live market data, interactive charting, financial calculators, and Large Language Models (LLMs) to provide actionable investment insights. Moving beyond standard chat interfaces, the platform features context-aware AI that natively understands real-time asset prices and user portfolio compositions.

### Core Objectives
- **Market Intelligence**: Provide real-time data on cryptocurrencies, including pricing, market capitalization, volume, and sentiment analysis (Fear & Greed Index).
- **Financial Simulation**: Offer robust calculators for compound interest, Dollar Cost Averaging (DCA), and trading profit/loss estimation.
- **Portfolio Management**: Enable users to track crypto assets and receive personalized, data-driven AI recommendations based on their holdings.

## Key Features

### 1. Intelligent AI Assistant
- **Multi-Session State**: Create, seamlessly switch between, and export multiple chat sessions.
- **Contextual Awareness**: The AI dynamically integrates real-time market data and the user's specific portfolio holdings into its system prompt.
- **Persona Customization**: Three distinct communication modes: Professional, Educational, and Trader.
- **LLM Flexibility**: Supports leading models via Groq (Llama 3.3 70B, Llama 3.1 8B, Gemma 2 9B, Mixtral 8x7B).

### 2. Live Market Dashboard
- **Market Overviews**: Tracks top assets with real-time pricing and 24-hour fluctuations.
- **Interactive Price Charts**: Utilizes `plotly.graph_objects` to render historical price trends across customizable timeframes (1D, 7D, 30D, 90D).
- **Global Sentiment**: Integrates the real-time Crypto Fear & Greed Index.
- **News Feed**: Aggregates the latest headlines and articles from major crypto news outlets.
- **1-Click AI Analysis**: Dedicated buttons to instantly dispatch comprehensive analytical prompts to the AI for specific assets.

### 3. Financial Calculator Suite
- **Compound Interest Simulator**: Projects long-term wealth growth incorporating initial capital, annual returns, and monthly contributions.
- **DCA Simulator**: Evaluates the effectiveness of recurring investments over specified durations.
- **Profit/Loss Calculator**: Computes net trading outcomes, factoring in variable transaction fees.

### 4. Portfolio Tracker
- **Live Valuation**: Calculates real-time total portfolio value using CoinGecko market data.
- **Allocation Breakdown**: Displays detailed holding quantities, current valuations, and percentage allocations.

## Architecture & Integrations

The platform relies on several external APIs and libraries to deliver real-time functionality:
- **Groq API**: High-speed LLM inference.
- **CoinGecko API v3**: Supplies `/coins/markets`, `/search`, `/market_chart`, and `/news` endpoints.
- **Alternative.me API**: Provides the Fear & Greed Index.
- **Plotly**: Renders advanced, interactive financial charts.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- A valid Groq API Key (available at [console.groq.com](https://console.groq.com/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/financeguru-ai.git
   cd financeguru-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure `streamlit`, `groq`, `requests`, and `plotly` are included in your requirements list)*

3. Launch the application:
   ```bash
   streamlit run app.py
   ```

### Application Setup
1. Access the local server (typically `http://localhost:8501`).
2. Input your **Groq API Key** in the sidebar configuration panel.
3. Begin exploring the market data, configuring your portfolio, or chatting with the AI.

## Project Structure

```text
financeguru-ai/
├── app.py                  # Core Streamlit application logic
├── requirements.txt        # Python dependency manifest
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration (Light Theme)
├── .gitignore
└── README.md
```

## Disclaimer

This application is designed strictly for **educational and informational purposes**. The AI-generated insights, calculations, and market data do not constitute formal financial advice, investment recommendations, or trading signals. Always conduct independent research (DYOR) and consult with a certified financial advisor before making investment decisions.

---

**Author**: Hacktiv8 Final Project — LLM-Based Tools and API Integration
