import streamlit as st
from datetime import datetime
from components.chat import render_chat_tab, PROMPT_SISTEM
from components.market import render_market_tab
from components.calculator import render_calculator_tab
from components.portfolio import render_portfolio_tab

st.set_page_config(
    page_title="FinanceGuru AI — Smart Finance & Investment Assistant",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/style.css", "r") as fail_css:
    st.markdown(f"<style>{fail_css.read()}</style>", unsafe_allow_html=True)

def muat_sesi():
    if "sessions" not in st.session_state:
        st.session_state.sessions = {"Default": []}
    if "active_session" not in st.session_state:
        st.session_state.active_session = "Default"
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}
    if "analyze_coin" not in st.session_state:
        st.session_state.analyze_coin = None
    
    st.session_state.messages = st.session_state.sessions[st.session_state.active_session]

def ekspor_obrolan():
    pesan_sesi = st.session_state.get("sessions", {}).get(st.session_state.get("active_session", "Default"), [])
    if not pesan_sesi:
        return ""
    baris_teks = [f"FinanceGuru AI — Chat Export ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n{'='*60}\n"]
    for pesan in pesan_sesi:
        peran = "👤 You" if pesan["role"] == "user" else "💹 FinanceGuru"
        baris_teks.append(f"\n{peran}:\n{pesan['content']}\n")
    return "\n".join(baris_teks)

def hitung_statistik_pesan():
    jumlah_user = sum(1 for m in st.session_state.messages if m["role"] == "user")
    jumlah_asisten = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    return jumlah_user, jumlah_asisten

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 1rem 0 1rem 0;">
            <div style="font-size: 2.2rem; text-shadow: 0 4px 10px rgba(16,185,129,0.3);">💹</div>
            <h2 style="font-size: 1.5rem !important; font-weight: 800 !important; margin: 0 !important;
                color: #0F172A !important; letter-spacing: -0.5px;">
                FinanceGuru
            </h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        daftar_sesi = list(st.session_state.sessions.keys())
        kolom_sesi1, kolom_sesi2 = st.columns([3, 1])
        with kolom_sesi1:
            sesi_terpilih = st.selectbox("Sesi Chat", daftar_sesi,
                index=daftar_sesi.index(st.session_state.active_session),
                label_visibility="collapsed")
        with kolom_sesi2:
            if st.button("➕", width="stretch", help="Buat sesi baru"):
                nama_baru = f"Chat {len(daftar_sesi) + 1}"
                st.session_state.sessions[nama_baru] = []
                st.session_state.active_session = nama_baru
                st.session_state.messages = st.session_state.sessions[nama_baru]
                st.rerun()

        if sesi_terpilih != st.session_state.active_session:
            st.session_state.active_session = sesi_terpilih
            st.session_state.messages = st.session_state.sessions[sesi_terpilih]
            st.rerun()

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        kunci_api = st.text_input(
            "API Key", type="password", placeholder="gsk_xxxxxxxxxxxx",
            value=st.session_state.groq_api_key,
            help="Dapatkan API key gratis di https://console.groq.com/",
        )
        st.session_state.groq_api_key = kunci_api

        if not kunci_api:
            st.caption("⚠️ Dapatkan key gratis di [console.groq.com](https://console.groq.com/)")

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        model_ai = st.selectbox("Model", options=[
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
            "gemma2-9b-it", "mixtral-8x7b-32768",
        ], index=0)

        gaya_bahasa = st.selectbox("Gaya Komunikasi", options=list(PROMPT_SISTEM.keys()), index=0)

        kolom_param1, kolom_param2 = st.columns(2)
        with kolom_param1:
            suhu = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        with kolom_param2:
            maksimal_token = st.slider("Max Tokens", 256, 8192, 2048, 256)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        jumlah_tanya, jumlah_jawab = hitung_statistik_pesan()
        st.markdown(f"""
        <div class="stats-container" style="justify-content: center;">
            <div class="stat-pill">
                <span class="number">{jumlah_tanya}</span>
                <span class="label">tanya</span>
            </div>
            <div class="stat-pill">
                <span class="number">{jumlah_jawab}</span>
                <span class="label">jawab</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        kolom_aksi1, kolom_aksi2 = st.columns(2)
        with kolom_aksi1:
            if st.button("Hapus Chat", width="stretch"):
                st.session_state.sessions[st.session_state.active_session] = []
                st.session_state.messages = st.session_state.sessions[st.session_state.active_session]
                st.rerun()
        with kolom_aksi2:
            teks_ekspor = ekspor_obrolan()
            if teks_ekspor:
                st.download_button("Export .txt", data=teks_ekspor, file_name="financeguru_chat.txt",
                                 mime="text/plain", width="stretch")
            else:
                st.button("Export .txt", width="stretch", disabled=True)

        st.markdown("""
        <div class="footer-text">
            <p style="font-size: 0.75rem !important;">
                Powered by Groq & Streamlit<br>Hacktiv8 • 2026
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return model_ai, gaya_bahasa, suhu, maksimal_token

def utama():
    muat_sesi()
    model_ai, gaya_bahasa, suhu, maksimal_token = render_sidebar()

    st.markdown("""
    <div class="hero-banner">
        <h1>FinanceGuru AI</h1>
        <p class="subtitle">Asisten keuangan cerdas untuk analisis pasar, strategi investasi, dan perencanaan keuangan.</p>
        <span class="badge">Powered by Groq LLM · Real-time Streaming · Live Market Data</span>
    </div>
    """, unsafe_allow_html=True)

    tab_obrolan, tab_pasar, tab_kalkulator, tab_portofolio = st.tabs(["Chat", "Live Market", "Kalkulator", "Portfolio"])

    with tab_obrolan:
        render_chat_tab(model_ai, gaya_bahasa, suhu, maksimal_token)
    with tab_pasar:
        render_market_tab()
    with tab_kalkulator:
        render_calculator_tab()
    with tab_portofolio:
        render_portfolio_tab()

if __name__ == "__main__":
    utama()
