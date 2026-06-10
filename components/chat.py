import streamlit as st
import time
from datetime import datetime
from groq import Groq
from utils.api_handler import ambil_harga_kripto

HARI_INI = datetime.now().strftime("%A, %d %B %Y")

PROMPT_SISTEM = {
    "Professional": f"""Kamu adalah FinanceGuru AI, asisten keuangan dan investasi profesional.
Hari ini adalah {HARI_INI}.

Cara berkomunikasi:
- Bahasa Indonesia formal-profesional, mudah dipahami
- Berikan analisis terstruktur dengan data dan angka
- Sertakan disclaimer risiko saat membahas investasi
- Gunakan istilah keuangan dengan penjelasan singkat
- Jangan berlebihan menggunakan emoji

Keahlian: Analisis teknikal & fundamental saham, forex, crypto, komoditas trading, perencanaan keuangan, manajemen portofolio & diversifikasi, produk investasi (reksadana, obligasi, deposito, ETF).

PENTING: Selalu sertakan disclaimer bahwa ini bukan financial advice resmi.""",

    "Santai & Edukasi": f"""Kamu adalah FinanceGuru AI, mentor keuangan yang ramah dan santai.
Hari ini adalah {HARI_INI}.

Gaya komunikasi:
- Bahasa Indonesia santai, friendly
- Jelaskan konsep keuangan dengan analogi sederhana
- Kasih contoh real-world yang relatable
- Buat topik finance yang rumit jadi gampang dicerna
- Boleh pakai emoji tapi jangan berlebihan

Keahlian: Edukasi investasi untuk pemula, tips menabung dan budgeting, penjelasan saham/crypto/reksadana secara sederhana, goal-based financial planning.

PENTING: Selalu ingatkan bahwa ini edukasi, bukan saran investasi resmi.""",

    "Trader Mode": f"""Lo adalah FinanceGuru AI, trader berpengalaman yang sharing insight.
Hari ini adalah {HARI_INI}.

Gaya lo:
- Bahasa gaul tapi tetap smart
- To the point, actionable
- Pake istilah trader (bullish, bearish, support, resistance)
- Passionate soal market, hemat emoji

Keahlian: Technical analysis (candlestick, indikator, chart pattern), momentum trading & swing trading, crypto market analysis, risk management & position sizing.

PENTING: SELALU kasih disclaimer bahwa ini bukan ajakan beli/jual."""
}

def dapatkan_klien_groq():
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def hasilkan_respons(klien, daftar_pesan, model, suhu, maksimal_token):
    try:
        aliran_data = klien.chat.completions.create(
            model=model, messages=daftar_pesan,
            temperature=suhu, max_tokens=maksimal_token, stream=True,
        )
        def aliran_teks():
            for potongan in aliran_data:
                if potongan.choices and potongan.choices[0].delta.content:
                    yield potongan.choices[0].delta.content
        return aliran_teks()
    except Exception as galat:
        st.error(f"❌ Terjadi kesalahan: {str(galat)}")
        return None

def hitung_pesan():
    jumlah_user = sum(1 for p in st.session_state.messages if p["role"] == "user")
    jumlah_asisten = sum(1 for p in st.session_state.messages if p["role"] == "assistant")
    return jumlah_user, jumlah_asisten

def render_chat_tab(model, gaya_bahasa, suhu, maksimal_token):
    for pesan in st.session_state.messages:
        avatar = "🧑‍💻" if pesan["role"] == "user" else "💹"
        with st.chat_message(pesan["role"], avatar=avatar):
            st.markdown(pesan["content"])

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
        kolom_saran1, kolom_saran2 = st.columns(2)
        with kolom_saran1:
            if st.button("Analisis teknikal vs fundamental saham", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Jelaskan perbedaan analisis teknikal dan fundamental dalam saham"})
                st.rerun()
            if st.button("Strategi diversifikasi portofolio 10 juta", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Buatkan strategi diversifikasi portofolio dengan budget 10 juta rupiah"})
                st.rerun()
        with kolom_saran2:
            if st.button("Cara mulai investasi crypto untuk pemula", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Bagaimana cara mulai investasi crypto untuk pemula dengan modal kecil?"})
                st.rerun()
            if st.button("Risk management dalam trading", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Apa itu risk management dalam trading dan bagaimana menerapkannya?"})
                st.rerun()

    perintah_analisis = st.session_state.analyze_coin
    if perintah_analisis:
        st.session_state.analyze_coin = None
        perintah = perintah_analisis
    elif input_pengguna := st.chat_input("Tanya tentang investasi, trading, saham, crypto, atau financial planning..."):
        perintah = input_pengguna
    else:
        perintah = None

    if perintah:
        if not st.session_state.groq_api_key:
            st.error("⚠️ Masukkan Groq API Key di sidebar terlebih dahulu!")
            st.stop()

        klien = dapatkan_klien_groq()
        if not klien:
            st.error("❌ Gagal menginisialisasi klien Groq.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": perintah})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(perintah)

        prompt_sistem = PROMPT_SISTEM[gaya_bahasa]

        harga_pasar = ambil_harga_kripto()
        if harga_pasar and isinstance(harga_pasar, list):
            konteks_harga = "\n\nData harga crypto terkini (real-time dari CoinGecko):\n"
            for koin in harga_pasar:
                nama_koin = koin.get("name", "")
                harga_koin = koin.get("current_price", 0)
                perubahan_koin = koin.get("price_change_percentage_24h", 0) or 0
                konteks_harga += f"- {nama_koin}: ${harga_koin:,.2f} ({perubahan_koin:+.2f}% 24h)\n"
            prompt_sistem += konteks_harga

        if st.session_state.portfolio:
            konteks_portofolio = "\n\nData Portfolio User Saat Ini:\n"
            for id_koin, qty in st.session_state.portfolio.items():
                konteks_portofolio += f"- {id_koin}: {qty} units\n"
            konteks_portofolio += "Berikan saran investasi atau analisis dengan mempertimbangkan aset di atas jika relevan.\n"
            prompt_sistem += konteks_portofolio

        pesan_api = [{"role": "system", "content": prompt_sistem}]
        for msg in st.session_state.messages[-20:]:
            pesan_api.append({"role": msg["role"], "content": msg["content"]})

        with st.chat_message("assistant", avatar="💹"):
            waktu_mulai = time.time()
            with st.status("Menganalisis...", expanded=False) as status:
                aliran_respons = hasilkan_respons(klien, pesan_api, model, suhu, maksimal_token)
                if aliran_respons is None:
                    status.update(label="Gagal", state="error")
                    st.stop()
                status.update(label="Menyusun jawaban...", state="running")
            teks_balasan = st.write_stream(aliran_respons)
            durasi = time.time() - waktu_mulai
            st.caption(f"Respons dalam {durasi:.1f}s")

        st.session_state.messages.append({"role": "assistant", "content": teks_balasan})

        sesi_aktif = st.session_state.active_session
        if sesi_aktif.startswith("Default") or sesi_aktif.startswith("Chat "):
            if len(st.session_state.messages) == 2:
                judul = perintah[:40].strip()
                if len(perintah) > 40:
                    judul += "..."
                st.session_state.sessions[judul] = st.session_state.sessions.pop(sesi_aktif)
                st.session_state.active_session = judul
                st.session_state.messages = st.session_state.sessions[judul]

        st.rerun()
