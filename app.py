import streamlit as st
from groq import Groq
from datetime import datetime
import requests
import time
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="FinanceGuru AI — Smart Finance & Investment Assistant",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS Setup
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    *, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

    .stApp { background: #f8fafb; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e8ecf0;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label,
    section[data-testid="stSidebar"] .stMarkdown span { color: #64748b !important; }

    /* Hero */
    .hero-banner {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
        border-radius: 18px; padding: 1.8rem 2.2rem; margin-bottom: 1rem;
        position: relative; overflow: hidden;
        box-shadow: 0 4px 24px rgba(16,185,129,0.15);
    }
    .hero-banner::before {
        content: ''; position: absolute; top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 {
        color: #fff !important; font-size: 1.7rem !important; font-weight: 800 !important;
        margin: 0 0 0.3rem 0 !important; position: relative; z-index: 1;
    }
    .hero-banner .subtitle {
        color: rgba(255,255,255,0.88) !important; font-size: 0.88rem !important;
        margin: 0 !important; position: relative; z-index: 1; line-height: 1.5;
    }
    .hero-banner .badge {
        display: inline-block; background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.2); border-radius: 50px;
        padding: 0.2rem 0.7rem; font-size: 0.7rem; color: #fff;
        margin-top: 0.5rem; position: relative; z-index: 1;
    }

    /* Market Cards */
    .market-card {
        background: #fff; border: 1px solid #e8ecf0;
        border-radius: 14px; padding: 1rem 1.2rem;
        transition: all 0.25s ease;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .market-card:hover { border-color: #10b981; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16,185,129,0.1); }
    .market-card .coin-name { color: #94a3b8; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .market-card .coin-price { color: #1e293b; font-size: 1.1rem; font-weight: 700; font-family: 'JetBrains Mono', monospace !important; margin: 0.15rem 0; }
    .market-card .coin-change { font-size: 0.78rem; font-weight: 600; font-family: 'JetBrains Mono', monospace !important; }
    .market-card .up { color: #059669; }
    .market-card .down { color: #dc2626; }

    /* Chat */
    .stChatMessage {
        background: #ffffff !important;
        border: 1px solid #e8ecf0 !important;
        border-left: 3px solid #10b981 !important;
        border-radius: 4px 14px 14px 4px !important;
        padding: 1.1rem 1.3rem !important; margin-bottom: 0.5rem !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    .stChatMessage:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important; }
    .stChatMessage p, .stChatMessage li, .stChatMessage span { color: #334155 !important; line-height: 1.75 !important; }
    .stChatMessage h1,.stChatMessage h2,.stChatMessage h3,.stChatMessage h4 { color: #059669 !important; }
    .stChatMessage strong { color: #047857 !important; }
    .stChatMessage code {
        background: #f0fdf4 !important; color: #059669 !important;
        border-radius: 4px !important; padding: 2px 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Chat Input */
    .stChatInput > div { border: none !important; }
    .stChatInput textarea {
        background: #fff !important; color: #1e293b !important;
        border: 1px solid #e2e8f0 !important; border-radius: 14px !important;
        padding: 0.9rem 1.2rem !important;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.04) !important;
    }
    .stChatInput textarea:focus { border-color: #10b981 !important; box-shadow: 0 0 0 3px rgba(16,185,129,0.1) !important; }
    .stChatInput button { background: #10b981 !important; border-radius: 12px !important; }

    /* Form */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: #fff !important; border: 1px solid #e2e8f0 !important;
        color: #1e293b !important; border-radius: 10px !important;
    }
    .stSlider > div > div > div > div { background: #10b981 !important; }
    .stSlider label, .stSelectbox label, .stTextInput label { color: #475569 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: #f1f5f9; border-radius: 12px; padding: 4px; border: 1px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px; color: #94a3b8; font-weight: 500; font-size: 0.85rem;
        padding: 0.5rem 1.2rem; border: none !important;
    }
    .stTabs [aria-selected="true"] { background: #fff !important; color: #059669 !important; font-weight: 600; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Buttons */
    .stButton > button {
        background: #10b981 !important;
        color: #fff !important; border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(16,185,129,0.18) !important;
    }
    .stButton > button:hover { background: #059669 !important; transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(16,185,129,0.22) !important; }

    /* Download button */
    .stDownloadButton > button {
        background: #f1f5f9 !important; color: #475569 !important;
        border: 1px solid #e2e8f0 !important; border-radius: 10px !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover { background: #e2e8f0 !important; color: #1e293b !important; }

    /* Stats */
    .stats-container { display: flex; gap: 0.5rem; margin-top: 0.8rem; flex-wrap: wrap; }
    .stat-pill {
        background: #f0fdf4; border: 1px solid #d1fae5;
        border-radius: 8px; padding: 0.3rem 0.7rem;
        display: inline-flex; align-items: center; gap: 0.35rem;
    }
    .stat-pill .number { color: #059669; font-weight: 700; font-size: 0.88rem; font-family: 'JetBrains Mono', monospace !important; }
    .stat-pill .label { color: #6b7280; font-size: 0.72rem; }

    .custom-divider { height: 1px; background: #e8ecf0; margin: 0.8rem 0; }

    /* Welcome */
    .welcome-container { text-align: center; padding: 2rem 2rem; }
    .welcome-container .emoji { font-size: 3rem; margin-bottom: 0.6rem; display: block; animation: pulse 2.5s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.06); } }
    .welcome-container h2 { color: #1e293b !important; font-size: 1.3rem !important; font-weight: 700 !important; margin-bottom: 0.3rem !important; }
    .welcome-container p { color: #64748b !important; font-size: 0.88rem !important; line-height: 1.6 !important; }

    .footer-text { text-align: center; font-size: 0.7rem; margin-top: 2rem; padding: 1rem; }
    #MainMenu, header, footer { visibility: hidden; }
    .stDeployButton, div[data-testid="stDecoration"], div[data-testid="stToolbar"] { display: none !important; }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# System Prompts
TODAY = datetime.now().strftime("%A, %d %B %Y")

SYSTEM_PROMPTS = {
    "Professional": f"""Kamu adalah FinanceGuru AI, asisten keuangan dan investasi profesional.
Hari ini adalah {TODAY}.

Cara berkomunikasi:
- Bahasa Indonesia formal-profesional, mudah dipahami
- Berikan analisis terstruktur dengan data dan angka
- Sertakan disclaimer risiko saat membahas investasi
- Gunakan istilah keuangan dengan penjelasan singkat
- Jangan berlebihan menggunakan emoji

Keahlian: Analisis teknikal & fundamental saham, forex, crypto, komoditas trading, perencanaan keuangan, manajemen portofolio & diversifikasi, produk investasi (reksadana, obligasi, deposito, ETF).

PENTING: Selalu sertakan disclaimer bahwa ini bukan financial advice resmi.""",

    "Santai & Edukasi": f"""Kamu adalah FinanceGuru AI, mentor keuangan yang ramah dan santai.
Hari ini adalah {TODAY}.

Gaya komunikasi:
- Bahasa Indonesia santai, friendly
- Jelaskan konsep keuangan dengan analogi sederhana
- Kasih contoh real-world yang relatable
- Buat topik finance yang rumit jadi gampang dicerna
- Boleh pakai emoji tapi jangan berlebihan

Keahlian: Edukasi investasi untuk pemula, tips menabung dan budgeting, penjelasan saham/crypto/reksadana secara sederhana, goal-based financial planning.

PENTING: Selalu ingatkan bahwa ini edukasi, bukan saran investasi resmi.""",

    "Trader Mode": f"""Lo adalah FinanceGuru AI, trader berpengalaman yang sharing insight.
Hari ini adalah {TODAY}.

Gaya lo:
- Bahasa gaul tapi tetap smart
- To the point, actionable
- Pake istilah trader (bullish, bearish, support, resistance)
- Passionate soal market, hemat emoji

Keahlian: Technical analysis (candlestick, indikator, chart pattern), momentum trading & swing trading, crypto market analysis, risk management & position sizing.

PENTING: SELALU kasih disclaimer bahwa ini bukan ajakan beli/jual."""
}


# Helper Functions
def get_groq_client():
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def generate_response(client, messages, model, temperature, max_tokens):
    """Generate streaming response, yielding text strings."""
    try:
        stream = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=max_tokens, stream=True,
        )
        def text_stream():
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        return text_stream()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def count_messages():
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
    assistant_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    return user_msgs, assistant_msgs


@st.cache_data(ttl=120)
def fetch_crypto_prices():
    """Fetch crypto prices with market cap & volume from CoinGecko."""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd", "order": "market_cap_desc",
            "per_page": 5, "page": 1, "sparkline": True,
            "ids": "bitcoin,ethereum,solana,binancecoin,ripple",
        }
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None


@st.cache_data(ttl=300)
def fetch_coin_chart(coin_id, days=7):
    """Fetch historical price data for Plotly charting."""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        resp = requests.get(url, params={"vs_currency": "usd", "days": days}, timeout=8)
        if resp.status_code == 200:
            data = resp.json().get("prices", [])
            timestamps = [datetime.fromtimestamp(p[0] / 1000) for p in data]
            prices = [p[1] for p in data]
            return timestamps, prices
    except:
        pass
    return None, None


def build_price_chart(timestamps, prices, coin_name, change_pct=0):
    """Build interactive Plotly chart."""
    color = "#059669" if change_pct >= 0 else "#dc2626"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps, y=prices, mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy", fillcolor=f"rgba({'5,150,105' if change_pct >= 0 else '220,38,38'},0.06)",
        hovertemplate="$%{y:,.2f}<extra></extra>"
    ))
    fig.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=False, color="#94a3b8", tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", showline=False, color="#94a3b8",
                   tickfont=dict(size=10), tickprefix="$"),
        hovermode="x unified",
    )
    return fig


@st.cache_data(ttl=600)
def fetch_crypto_news():
    """Fetch latest crypto news from CoinGecko."""
    try:
        url = "https://api.coingecko.com/api/v3/news"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("data", [])[:8]
    except:
        pass
    return None


def calculate_portfolio(holdings, market_data):
    """Calculate total portfolio value from holdings + live prices."""
    total = 0.0
    details = []
    price_map = {}
    if market_data and isinstance(market_data, list):
        for c in market_data:
            price_map[c["id"]] = c
    for coin_id, qty in holdings.items():
        if coin_id in price_map:
            p = price_map[coin_id]["current_price"]
            val = p * qty
            total += val
            details.append({"id": coin_id, "name": price_map[coin_id]["name"],
                           "symbol": price_map[coin_id]["symbol"].upper(),
                           "qty": qty, "price": p, "value": val})
    return total, details


@st.cache_data(ttl=300)
def fetch_fear_greed():
    """Fetch Crypto Fear & Greed Index."""
    try:
        resp = requests.get("https://api.alternative.me/fng/?limit=1", timeout=5)
        if resp.status_code == 200:
            data = resp.json()["data"][0]
            return {"value": int(data["value"]), "label": data["value_classification"]}
    except:
        pass
    return None


def export_chat():
    """Export chat history as downloadable text."""
    msgs = st.session_state.get("sessions", {}).get(st.session_state.get("active_session", "Default"), [])
    if not msgs:
        return ""
    lines = [f"FinanceGuru AI — Chat Export ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n{'='*60}\n"]
    for msg in msgs:
        role = "👤 You" if msg["role"] == "user" else "💹 FinanceGuru"
        lines.append(f"\n{role}:\n{msg['content']}\n")
    return "\n".join(lines)


@st.cache_data(ttl=60)
def search_coin(query):
    """Search for a specific coin on CoinGecko."""
    try:
        url = "https://api.coingecko.com/api/v3/search"
        resp = requests.get(url, params={"query": query}, timeout=5)
        if resp.status_code == 200:
            coins = resp.json().get("coins", [])[:3]
            if coins:
                ids = ",".join(c["id"] for c in coins)
                detail = requests.get(
                    "https://api.coingecko.com/api/v3/coins/markets",
                    params={"vs_currency": "usd", "ids": ids}, timeout=5
                )
                if detail.status_code == 200:
                    return detail.json()
    except:
        pass
    return None

# Session State & Multi-Session Support
if "sessions" not in st.session_state:
    st.session_state.sessions = {"Default": []}
if "active_session" not in st.session_state:
    st.session_state.active_session = "Default"
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}  # {coin_id: quantity}
if "analyze_coin" not in st.session_state:
    st.session_state.analyze_coin = None
# Alias for backward compat
st.session_state.messages = st.session_state.sessions[st.session_state.active_session]


# Sidebar Setup
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.4rem;">💹</div>
        <h2 style="font-size: 1.3rem !important; font-weight: 800 !important; margin: 0 !important;
            color: #059669 !important;">
            FinanceGuru AI
        </h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Multi-Session Chat ──
    session_names = list(st.session_state.sessions.keys())
    nc1, nc2 = st.columns([3, 1])
    with nc1:
        selected = st.selectbox("Sesi Chat", session_names,
            index=session_names.index(st.session_state.active_session),
            label_visibility="collapsed")
    with nc2:
        if st.button("➕", use_container_width=True, help="Buat sesi baru"):
            new_name = f"Chat {len(session_names) + 1}"
            st.session_state.sessions[new_name] = []
            st.session_state.active_session = new_name
            st.session_state.messages = st.session_state.sessions[new_name]
            st.rerun()

    if selected != st.session_state.active_session:
        st.session_state.active_session = selected
        st.session_state.messages = st.session_state.sessions[selected]
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    api_key_input = st.text_input(
        "API Key", type="password", placeholder="gsk_xxxxxxxxxxxx",
        value=st.session_state.groq_api_key,
        help="Dapatkan API key gratis di https://console.groq.com/",
    )
    st.session_state.groq_api_key = api_key_input

    if not api_key_input:
        st.caption("⚠️ Dapatkan key gratis di [console.groq.com](https://console.groq.com/)")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    model = st.selectbox("Model", options=[
        "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
        "gemma2-9b-it", "mixtral-8x7b-32768",
    ], index=0)

    language_style = st.selectbox("Gaya Komunikasi", options=list(SYSTEM_PROMPTS.keys()), index=0)

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    with col2:
        max_tokens = st.slider("Max Tokens", 256, 8192, 2048, 256)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Stats
    user_count, assistant_count = count_messages()
    st.markdown(f"""
    <div class="stats-container" style="justify-content: center;">
        <div class="stat-pill">
            <span class="number">{user_count}</span>
            <span class="label">tanya</span>
        </div>
        <div class="stat-pill">
            <span class="number">{assistant_count}</span>
            <span class="label">jawab</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Action buttons
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        if st.button("Hapus Chat", use_container_width=True):
            st.session_state.sessions[st.session_state.active_session] = []
            st.session_state.messages = st.session_state.sessions[st.session_state.active_session]
            st.rerun()
    with bcol2:
        chat_export = export_chat()
        if chat_export:
            st.download_button("Export .txt", data=chat_export, file_name="financeguru_chat.txt",
                             mime="text/plain", use_container_width=True)
        else:
            st.button("Export .txt", use_container_width=True, disabled=True)

    st.markdown("""
    <div class="footer-text">
        <p style="color: #94a3b8 !important; font-size: 0.68rem !important;">
            Powered by Groq & Streamlit<br>Hacktiv8 • 2026
        </p>
    </div>
    """, unsafe_allow_html=True)


# Main UI Components

# Hero
st.markdown("""
<div class="hero-banner">
    <h1>FinanceGuru AI</h1>
    <p class="subtitle">Asisten keuangan cerdas untuk analisis pasar, strategi investasi, dan perencanaan keuangan.</p>
    <span class="badge">Powered by Groq LLM · Real-time Streaming · Live Market Data</span>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_chat, tab_market, tab_calc, tab_portfolio = st.tabs(["Chat", "Live Market", "Kalkulator", "Portfolio"])

# ── TAB: CHAT ──
with tab_chat:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "💹"):
            st.markdown(message["content"])

    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-container">
            <span class="emoji">📈</span>
            <h2>Selamat Datang di FinanceGuru AI</h2>
            <p>Asisten keuangan berbasis AI yang siap membantu kamu memahami pasar,<br>
            merencanakan investasi, dan membuat keputusan finansial yang lebih cerdas.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        scol1, scol2 = st.columns(2)
        with scol1:
            if st.button("Analisis teknikal vs fundamental saham", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Jelaskan perbedaan analisis teknikal dan fundamental dalam saham"})
                st.rerun()
            if st.button("Strategi diversifikasi portofolio 10 juta", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Buatkan strategi diversifikasi portofolio dengan budget 10 juta rupiah"})
                st.rerun()
        with scol2:
            if st.button("Cara mulai investasi crypto untuk pemula", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Bagaimana cara mulai investasi crypto untuk pemula dengan modal kecil?"})
                st.rerun()
            if st.button("Risk management dalam trading", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Apa itu risk management dalam trading dan bagaimana menerapkannya?"})
                st.rerun()

# ── TAB: LIVE MARKET ──
with tab_market:
    # Fear & Greed Index
    fg = fetch_fear_greed()
    if fg:
        fg_val = fg["value"]
        fg_color = "#dc2626" if fg_val < 25 else "#f59e0b" if fg_val < 50 else "#10b981" if fg_val < 75 else "#059669"
        st.markdown(f"""
        <div style="background: #fff; border: 1px solid #e8ecf0; border-radius: 14px; padding: 1rem 1.5rem;
             margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
            <div style="font-size: 2rem; font-weight: 800; color: {fg_color}; font-family: 'JetBrains Mono', monospace;">{fg_val}</div>
            <div>
                <div style="color: #1e293b; font-weight: 600; font-size: 0.9rem;">Fear & Greed Index</div>
                <div style="color: {fg_color}; font-size: 0.8rem; font-weight: 500;">{fg['label']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Live Crypto Market")
    st.caption(f"Data dari CoinGecko API • Auto-refresh 2 menit • {datetime.now().strftime('%H:%M:%S')}")

    market_data = fetch_crypto_prices()

    if market_data and isinstance(market_data, list):
        cols = st.columns(len(market_data))
        for i, coin in enumerate(market_data):
            price = coin.get("current_price", 0)
            change = coin.get("price_change_percentage_24h", 0) or 0
            mcap = coin.get("market_cap", 0)
            vol = coin.get("total_volume", 0)
            symbol = coin.get("symbol", "").upper()
            name = coin.get("name", "")
            change_class = "up" if change >= 0 else "down"
            arrow = "▲" if change >= 0 else "▼"
            sparkline = coin.get("sparkline_in_7d", {}).get("price", [])

            if mcap >= 1e12: mcap_str = f"${mcap/1e12:.1f}T"
            elif mcap >= 1e9: mcap_str = f"${mcap/1e9:.1f}B"
            else: mcap_str = f"${mcap/1e6:.0f}M"

            with cols[i]:
                st.markdown(f"""
                <div class="market-card">
                    <div class="coin-name">{symbol} · {name}</div>
                    <div class="coin-price">${price:,.2f}</div>
                    <div class="coin-change {change_class}">{arrow} {change:+.2f}%</div>
                    <div style="margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px solid #f1f5f9;">
                        <div style="color: #94a3b8; font-size: 0.65rem;">MCap: {mcap_str}</div>
                        <div style="color: #94a3b8; font-size: 0.65rem;">Vol: ${vol/1e6:.0f}M</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # AI Analyze button
        st.markdown("")
        analyze_cols = st.columns(len(market_data))
        for i, coin in enumerate(market_data):
            with analyze_cols[i]:
                if st.button(f"Analisis {coin['symbol'].upper()}", key=f"ai_{coin['id']}", use_container_width=True):
                    prompt = f"Berikan analisis mendalam tentang {coin['name']} ({coin['symbol'].upper()}) saat ini. Harga: ${coin['current_price']:,.2f}, perubahan 24h: {coin.get('price_change_percentage_24h', 0) or 0:+.2f}%, market cap: ${coin.get('market_cap',0):,.0f}. Bagaimana outlook-nya?"
                    st.session_state.analyze_coin = prompt
                    st.rerun()

        # Interactive Price Chart
        st.markdown("---")
        st.markdown("#### Price Chart")
        ch1, ch2 = st.columns([3, 1])
        with ch1:
            chart_coin = st.selectbox("Coin", [c["id"] for c in market_data],
                format_func=lambda x: next((c["name"] for c in market_data if c["id"] == x), x),
                key="chart_coin", label_visibility="collapsed")
        with ch2:
            chart_tf = st.selectbox("Timeframe", [1, 7, 30, 90],
                format_func=lambda x: {1:"24H",7:"7D",30:"30D",90:"90D"}[x],
                index=1, key="chart_tf", label_visibility="collapsed")

        ts, ps = fetch_coin_chart(chart_coin, chart_tf)
        if ts and ps:
            sel_coin = next((c for c in market_data if c["id"] == chart_coin), {})
            ch_pct = sel_coin.get("price_change_percentage_24h", 0) or 0
            fig = build_price_chart(ts, ps, chart_coin, ch_pct)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.caption("Chart tidak tersedia saat ini.")

        st.markdown("")
        if st.button("Refresh", use_container_width=False):
            st.cache_data.clear()
            st.rerun()
    else:
        st.info("Tidak bisa mengambil data market. Coba refresh.")
        if st.button("Coba Lagi"):
            st.cache_data.clear()
            st.rerun()

    st.caption("Data harga untuk referensi saja. Bukan saran investasi.")

    # Coin Search
    st.markdown("---")
    st.markdown("#### Cari Coin")
    search_q = st.text_input("Nama coin", key="coin_search", label_visibility="collapsed", placeholder="Cari coin... (contoh: cardano, dogecoin)")
    if search_q:
        results = search_coin(search_q)
        if results:
            scols = st.columns(len(results))
            for i, coin in enumerate(results):
                price = coin.get("current_price", 0)
                change = coin.get("price_change_percentage_24h", 0) or 0
                mcap = coin.get("market_cap", 0)
                sym = coin.get("symbol", "").upper()
                name = coin.get("name", "")
                ch_cls = "up" if change >= 0 else "down"
                arrow = "\u25b2" if change >= 0 else "\u25bc"
                mc = f"${mcap/1e9:.1f}B" if mcap >= 1e9 else f"${mcap/1e6:.0f}M"
                with scols[i]:
                    st.markdown(f"""
                    <div class="market-card">
                        <div class="coin-name">{sym} \u00b7 {name}</div>
                        <div class="coin-price">${price:,.4f}</div>
                        <div class="coin-change {ch_cls}">{arrow} {change:+.2f}%</div>
                        <div style="margin-top:0.4rem;padding-top:0.4rem;border-top:1px solid #f1f5f9;">
                            <div style="color:#94a3b8;font-size:0.65rem;">MCap: {mc}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("Tidak ditemukan. Coba nama lain.")

    # News Feed
    st.markdown("---")
    st.markdown("#### Crypto News")
    news = fetch_crypto_news()
    if news:
        for article in news[:6]:
            title = article.get("title", "")
            desc = article.get("description", "")[:120]
            url = article.get("url", "#")
            source = article.get("news_site", "")
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e8ecf0;border-radius:10px;padding:0.8rem 1rem;
                 margin-bottom:0.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                <a href="{url}" target="_blank" style="color:#1e293b;font-weight:600;font-size:0.85rem;
                   text-decoration:none;">{title}</a>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:0.2rem;">{source} · {desc}...</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Berita tidak tersedia saat ini.")

# ── TAB: FINANCIAL CALCULATOR ──
with tab_calc:
    calc_type = st.selectbox("Pilih Kalkulator", [
        "Compound Interest", "DCA Simulator", "Profit / Loss"
    ])

    st.markdown("")

    if calc_type == "Compound Interest":
        st.markdown("#### Kalkulator Compound Interest")
        st.caption("Hitung pertumbuhan investasi dengan bunga majemuk")
        c1, c2 = st.columns(2)
        with c1:
            ci_principal = st.number_input("Modal Awal (Rp)", min_value=0, value=10_000_000, step=1_000_000, format="%d")
            ci_rate = st.number_input("Return Tahunan (%)", min_value=0.0, value=12.0, step=0.5)
        with c2:
            ci_years = st.number_input("Durasi (tahun)", min_value=1, value=10, step=1)
            ci_monthly = st.number_input("Tambahan Bulanan (Rp)", min_value=0, value=1_000_000, step=100_000, format="%d")

        if st.button("Hitung", use_container_width=True):
            monthly_rate = ci_rate / 100 / 12
            months = ci_years * 12
            total = ci_principal
            for _ in range(months):
                total = total * (1 + monthly_rate) + ci_monthly
            total_invested = ci_principal + (ci_monthly * months)
            profit = total - total_invested

            r1, r2, r3 = st.columns(3)
            r1.metric("Nilai Akhir", f"Rp {total:,.0f}")
            r2.metric("Total Investasi", f"Rp {total_invested:,.0f}")
            r3.metric("Keuntungan", f"Rp {profit:,.0f}", f"+{(profit/total_invested*100):.1f}%")

    elif calc_type == "DCA Simulator":
        st.markdown("#### DCA (Dollar Cost Averaging) Simulator")
        st.caption("Simulasi strategi investasi berkala")
        c1, c2 = st.columns(2)
        with c1:
            dca_amount = st.number_input("Investasi per Bulan (Rp)", min_value=0, value=500_000, step=100_000, format="%d")
            dca_months = st.number_input("Durasi (bulan)", min_value=1, value=24, step=1)
        with c2:
            dca_avg_return = st.number_input("Estimasi Return Bulanan (%)", min_value=-50.0, value=1.5, step=0.5)

        if st.button("Simulasi", use_container_width=True):
            monthly_rate = dca_avg_return / 100
            total_value = 0
            for m in range(dca_months):
                total_value = (total_value + dca_amount) * (1 + monthly_rate)
            total_invested = dca_amount * dca_months
            dca_profit = total_value - total_invested

            r1, r2, r3 = st.columns(3)
            r1.metric("Nilai Portfolio", f"Rp {total_value:,.0f}")
            r2.metric("Total Investasi", f"Rp {total_invested:,.0f}")
            r3.metric("Profit/Loss", f"Rp {dca_profit:,.0f}",
                      f"+{(dca_profit/total_invested*100):.1f}%" if dca_profit >= 0 else f"{(dca_profit/total_invested*100):.1f}%")

    elif calc_type == "Profit / Loss":
        st.markdown("#### Kalkulator Profit / Loss")
        st.caption("Hitung keuntungan atau kerugian trading")
        c1, c2 = st.columns(2)
        with c1:
            pl_buy = st.number_input("Harga Beli", min_value=0.0, value=50000.0, step=1000.0)
            pl_qty = st.number_input("Jumlah Unit", min_value=0.0, value=10.0, step=1.0)
        with c2:
            pl_sell = st.number_input("Harga Jual", min_value=0.0, value=65000.0, step=1000.0)
            pl_fee = st.number_input("Fee Transaksi (%)", min_value=0.0, value=0.15, step=0.05)

        if st.button("Hitung", use_container_width=True, key="calc_pl"):
            cost = pl_buy * pl_qty
            revenue = pl_sell * pl_qty
            fee_total = (cost + revenue) * (pl_fee / 100)
            net_pl = revenue - cost - fee_total
            pct = (net_pl / cost * 100) if cost > 0 else 0

            r1, r2, r3 = st.columns(3)
            r1.metric("Net P/L", f"Rp {net_pl:,.0f}", f"{pct:+.2f}%")
            r2.metric("Total Cost", f"Rp {cost:,.0f}")
            r3.metric("Fee", f"Rp {fee_total:,.0f}")


# ── TAB: PORTFOLIO TRACKER ──
with tab_portfolio:
    st.markdown("#### Portfolio Tracker")
    st.caption("Tambah aset crypto dan lihat valuasi real-time")

    coin_options = {"bitcoin": "Bitcoin (BTC)", "ethereum": "Ethereum (ETH)",
                    "solana": "Solana (SOL)", "binancecoin": "BNB",
                    "ripple": "XRP", "cardano": "Cardano (ADA)",
                    "dogecoin": "Dogecoin (DOGE)", "polkadot": "Polkadot (DOT)"}

    pc1, pc2, pc3 = st.columns([2, 1, 1])
    with pc1:
        add_coin = st.selectbox("Coin", options=list(coin_options.keys()),
                                format_func=lambda x: coin_options[x], label_visibility="collapsed")
    with pc2:
        add_qty = st.number_input("Qty", min_value=0.0, value=0.1, step=0.01, label_visibility="collapsed")
    with pc3:
        if st.button("Tambah", use_container_width=True, key="add_pf"):
            if add_qty > 0:
                st.session_state.portfolio[add_coin] = st.session_state.portfolio.get(add_coin, 0) + add_qty
                st.rerun()

    if st.session_state.portfolio:
        try:
            pf_ids = ",".join(st.session_state.portfolio.keys())
            pf_resp = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                params={"vs_currency": "usd", "ids": pf_ids, "sparkline": False}, timeout=5)
            pf_data = pf_resp.json() if pf_resp.status_code == 200 else []
        except:
            pf_data = []

        total_val, details = calculate_portfolio(st.session_state.portfolio, pf_data)

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e8ecf0;border-radius:14px;padding:1.2rem 1.5rem;
             margin:1rem 0;box-shadow:0 1px 4px rgba(0,0,0,0.04);text-align:center;">
            <div style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;">Total Portfolio Value</div>
            <div style="color:#1e293b;font-size:2rem;font-weight:800;font-family:'JetBrains Mono',monospace;">
                ${total_val:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        det_cols = st.columns(len(details)) if details else []
        for i, d in enumerate(details):
            pct_alloc = (d["value"] / total_val * 100) if total_val > 0 else 0
            with det_cols[i]:
                st.markdown(f"""
                <div class="market-card">
                    <div class="coin-name">{d['symbol']} · {d['name']}</div>
                    <div style="color:#64748b;font-size:0.75rem;">{d['qty']:.4f} units</div>
                    <div class="coin-price">${d['value']:,.2f}</div>
                    <div style="color:#059669;font-size:0.72rem;font-weight:600;">{pct_alloc:.1f}% alokasi</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        rm_cols = st.columns(len(details)) if details else []
        for i, d in enumerate(details):
            with rm_cols[i]:
                if st.button(f"Hapus {d['symbol']}", key=f"rm_{d['id']}", use_container_width=True):
                    del st.session_state.portfolio[d["id"]]
                    st.rerun()
    else:
        st.markdown("""
        <div class="welcome-container">
            <h2>Portfolio kosong</h2>
            <p>Tambahkan coin di atas untuk mulai tracking portfolio kamu.</p>
        </div>
        """, unsafe_allow_html=True)


# Chat Input & AI Generation
# Handle AI analyze from market tab
analyze_prompt = st.session_state.analyze_coin
if analyze_prompt:
    st.session_state.analyze_coin = None
    prompt = analyze_prompt
elif user_input := st.chat_input("Tanya tentang investasi, trading, saham, crypto, atau financial planning..."):
    prompt = user_input
else:
    prompt = None

if prompt:
    if not st.session_state.groq_api_key:
        st.error("⚠️ Masukkan Groq API Key di sidebar terlebih dahulu!")
        st.stop()

    client = get_groq_client()
    if not client:
        st.error("❌ Gagal menginisialisasi Groq client.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with tab_chat:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        system_prompt = SYSTEM_PROMPTS[language_style]

        # Inject live market data into context if available
        prices = fetch_crypto_prices()
        if prices and isinstance(prices, list):
            price_context = "\n\nData harga crypto terkini (real-time dari CoinGecko):\n"
            for coin in prices:
                name = coin.get("name", "")
                p = coin.get("current_price", 0)
                ch = coin.get("price_change_percentage_24h", 0) or 0
                price_context += f"- {name}: ${p:,.2f} ({ch:+.2f}% 24h)\n"
            system_prompt += price_context

        # Inject portfolio data if available
        if st.session_state.portfolio:
            pf_context = "\n\nData Portfolio User Saat Ini:\n"
            for coin_id, qty in st.session_state.portfolio.items():
                pf_context += f"- {coin_id}: {qty} units\n"
            pf_context += "Berikan saran investasi atau analisis dengan mempertimbangkan aset di atas jika relevan.\n"
            system_prompt += pf_context

        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages[-20:]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

        with st.chat_message("assistant", avatar="💹"):
            start_time = time.time()
            with st.status("Menganalisis...", expanded=False) as status:
                stream = generate_response(client, api_messages, model, temperature, max_tokens)
                if stream is None:
                    status.update(label="Gagal", state="error")
                    st.stop()
                status.update(label="Menyusun jawaban...", state="running")
            response_text = st.write_stream(stream)
            elapsed = time.time() - start_time
            st.caption(f"Respons dalam {elapsed:.1f}s")

    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Auto-title session if first message
    active = st.session_state.active_session
    if active.startswith("Default") or active.startswith("Chat "):
        if len(st.session_state.messages) == 2:  # 1 user + 1 assistant
            title = prompt[:40].strip()
            if len(prompt) > 40:
                title += "..."
            st.session_state.sessions[title] = st.session_state.sessions.pop(active)
            st.session_state.active_session = title
            st.session_state.messages = st.session_state.sessions[title]

    st.rerun()
