import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils.api_handler import ambil_harga_kripto, ambil_grafik_koin, ambil_berita_kripto, ambil_fear_greed, cari_koin

def buat_grafik_harga(waktu, harga, id_koin, perubahan_persen=0):
    warna = "#059669" if perubahan_persen >= 0 else "#dc2626"
    warna_isi = "rgba(5,150,105,0.06)" if perubahan_persen >= 0 else "rgba(220,38,38,0.06)"
    
    figur = go.Figure()
    figur.add_trace(go.Scatter(
        x=waktu, y=harga, mode="lines",
        line=dict(color=warna, width=2),
        fill="tozeroy", fillcolor=warna_isi,
        hovertemplate="$%{y:,.2f}<extra></extra>"
    ))
    figur.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=False, color="#94a3b8", tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", showline=False, color="#94a3b8",
                   tickfont=dict(size=10), tickprefix="$"),
        hovermode="x unified",
    )
    return figur

def render_market_tab():
    indeks_fg = ambil_fear_greed()
    if indeks_fg:
        nilai = indeks_fg["nilai"]
        warna_fg = "#EF4444" if nilai < 25 else "#F59E0B" if nilai < 50 else "#10B981" if nilai < 75 else "#059669"
        st.markdown(f"""
        <div class="glass-card fg-index-card">
            <div class="fg-value" style="color: {warna_fg};">{nilai}</div>
            <div>
                <div class="fg-title">Fear & Greed Index</div>
                <div class="fg-label" style="color: {warna_fg};">{indeks_fg['label']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Live Crypto Market")
    st.caption(f"Data dari CoinGecko API • Auto-refresh 2 menit • {datetime.now().strftime('%H:%M:%S')}")

    data_pasar = ambil_harga_kripto()

    if data_pasar:
        kolom = st.columns(len(data_pasar))
        for i, koin in enumerate(data_pasar):
            harga = koin.get("current_price", 0)
            perubahan = koin.get("price_change_percentage_24h", 0) or 0
            kapitalisasi = koin.get("market_cap", 0)
            volume = koin.get("total_volume", 0)
            simbol = koin.get("symbol", "").upper()
            nama = koin.get("name", "")
            kelas_perubahan = "up" if perubahan >= 0 else "down"
            arah = "▲" if perubahan >= 0 else "▼"

            if kapitalisasi >= 1e12: kapitalisasi_str = f"${kapitalisasi/1e12:.1f}T"
            elif kapitalisasi >= 1e9: kapitalisasi_str = f"${kapitalisasi/1e9:.1f}B"
            else: kapitalisasi_str = f"${kapitalisasi/1e6:.0f}M"

            with kolom[i]:
                st.markdown(f"""
                <div class="market-card">
                    <div class="coin-name">{simbol} · {nama}</div>
                    <div class="coin-price">${harga:,.2f}</div>
                    <div class="coin-change {kelas_perubahan}">{arah} {perubahan:+.2f}%</div>
                    <div class="divider">
                        <div class="meta-text">MCap: {kapitalisasi_str}</div>
                        <div class="meta-text">Vol: ${volume/1e6:.0f}M</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        kolom_analisis = st.columns(len(data_pasar))
        for i, koin in enumerate(data_pasar):
            with kolom_analisis[i]:
                if st.button(f"Analisis {koin['symbol'].upper()}", key=f"ai_{koin['id']}", width="stretch"):
                    prompt = f"Berikan analisis mendalam tentang {koin['name']} ({koin['symbol'].upper()}) saat ini. Harga: ${koin['current_price']:,.2f}, perubahan 24h: {koin.get('price_change_percentage_24h', 0) or 0:+.2f}%, market cap: ${koin.get('market_cap',0):,.0f}. Bagaimana outlook-nya?"
                    st.session_state.analyze_coin = prompt
                    st.rerun()

        st.markdown("---")
        st.markdown("#### Price Chart")
        kolom_chart1, kolom_chart2 = st.columns([3, 1])
        with kolom_chart1:
            pilihan_koin = st.selectbox("Coin", [c["id"] for c in data_pasar],
                format_func=lambda x: next((c["name"] for c in data_pasar if c["id"] == x), x),
                key="chart_coin", label_visibility="collapsed")
        with kolom_chart2:
            pilihan_waktu = st.selectbox("Timeframe", [1, 7, 30, 90],
                format_func=lambda x: {1:"24H",7:"7D",30:"30D",90:"90D"}[x],
                index=1, key="chart_tf", label_visibility="collapsed")

        waktu_grafik, harga_grafik = ambil_grafik_koin(pilihan_koin, pilihan_waktu)
        if waktu_grafik and harga_grafik:
            koin_terpilih = next((c for c in data_pasar if c["id"] == pilihan_koin), {})
            persentase_perubahan = koin_terpilih.get("price_change_percentage_24h", 0) or 0
            figur = buat_grafik_harga(waktu_grafik, harga_grafik, pilihan_koin, persentase_perubahan)
            st.plotly_chart(figur, width="stretch", config={"displayModeBar": False})
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

    st.markdown("---")
    st.markdown("#### Cari Coin")
    kueri_cari = st.text_input("Nama coin", key="coin_search", label_visibility="collapsed", placeholder="Cari coin... (contoh: cardano, dogecoin)")
    if kueri_cari:
        hasil = cari_koin(kueri_cari)
        if hasil:
            kolom_hasil = st.columns(len(hasil))
            for i, koin in enumerate(hasil):
                harga = koin.get("current_price", 0)
                perubahan = koin.get("price_change_percentage_24h", 0) or 0
                kapitalisasi = koin.get("market_cap", 0)
                simbol = koin.get("symbol", "").upper()
                nama = koin.get("name", "")
                kelas_perubahan = "up" if perubahan >= 0 else "down"
                arah = "▲" if perubahan >= 0 else "▼"
                kapitalisasi_str = f"${kapitalisasi/1e9:.1f}B" if kapitalisasi >= 1e9 else f"${kapitalisasi/1e6:.0f}M"
                with kolom_hasil[i]:
                    st.markdown(f"""
                    <div class="market-card">
                        <div class="coin-name">{simbol} · {nama}</div>
                        <div class="coin-price">${harga:,.4f}</div>
                        <div class="coin-change {kelas_perubahan}">{arah} {perubahan:+.2f}%</div>
                        <div class="divider">
                            <div class="meta-text">MCap: {kapitalisasi_str}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("Tidak ditemukan. Coba nama lain.")

    st.markdown("---")
    st.markdown("#### Crypto News")
    berita = ambil_berita_kripto()
    if berita:
        for artikel in berita[:6]:
            judul = artikel.get("title", "")
            deskripsi = artikel.get("description", "")[:120]
            tautan = artikel.get("url", "#")
            sumber = artikel.get("news_site", "")
            st.markdown(f"""
            <div class="glass-card" style="padding:1rem;">
                <a href="{tautan}" target="_blank" class="news-title">{judul}</a>
                <div class="meta-text" style="margin-top:0.4rem;">{sumber} · {deskripsi}...</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Berita tidak tersedia saat ini.")
