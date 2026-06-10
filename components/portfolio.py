import streamlit as st
from utils.api_handler import ambil_portofolio_pasar

def hitung_portofolio(holdings, data_pasar):
    total = 0.0
    detail = []
    peta_harga = {}
    if data_pasar and isinstance(data_pasar, list):
        for koin in data_pasar:
            peta_harga[koin["id"]] = koin
            
    for id_koin, kuantitas in holdings.items():
        if id_koin in peta_harga:
            harga = peta_harga[id_koin]["current_price"]
            nilai = harga * kuantitas
            total += nilai
            detail.append({
                "id": id_koin, 
                "nama": peta_harga[id_koin]["name"],
                "simbol": peta_harga[id_koin]["symbol"].upper(),
                "kuantitas": kuantitas, 
                "harga": harga, 
                "nilai": nilai
            })
    return total, detail

def render_portfolio_tab():
    st.markdown("#### Portfolio Tracker")
    st.caption("Tambah aset crypto dan lihat valuasi real-time")

    pilihan_koin = {
        "bitcoin": "Bitcoin (BTC)", "ethereum": "Ethereum (ETH)",
        "solana": "Solana (SOL)", "binancecoin": "BNB",
        "ripple": "XRP", "cardano": "Cardano (ADA)",
        "dogecoin": "Dogecoin (DOGE)", "polkadot": "Polkadot (DOT)"
    }

    kolom1, kolom2, kolom3 = st.columns([2, 1, 1])
    with kolom1:
        tambah_koin = st.selectbox("Coin", options=list(pilihan_koin.keys()),
                                format_func=lambda x: pilihan_koin[x], label_visibility="collapsed")
    with kolom2:
        tambah_kuantitas = st.number_input("Qty", min_value=0.0, value=0.1, step=0.01, label_visibility="collapsed")
    with kolom3:
        if st.button("Tambah", use_container_width=True, key="add_pf"):
            if tambah_kuantitas > 0:
                st.session_state.portfolio[tambah_koin] = st.session_state.portfolio.get(tambah_koin, 0) + tambah_kuantitas
                st.rerun()

    if st.session_state.portfolio:
        id_koin_str = ",".join(st.session_state.portfolio.keys())
        data_portofolio = ambil_portofolio_pasar(id_koin_str)
        
        total_nilai, detail_portofolio = hitung_portofolio(st.session_state.portfolio, data_portofolio)

        st.markdown(f"""
        <div class="glass-card portfolio-total-card">
            <div class="pf-label">Total Portfolio Value</div>
            <div class="pf-value">${total_nilai:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        kolom_detail = st.columns(len(detail_portofolio)) if detail_portofolio else []
        for i, item in enumerate(detail_portofolio):
            alokasi_persen = (item["nilai"] / total_nilai * 100) if total_nilai > 0 else 0
            with kolom_detail[i]:
                st.markdown(f"""
                <div class="market-card">
                    <div class="coin-name">{item['simbol']} · {item['nama']}</div>
                    <div class="meta-text" style="margin-bottom:0.2rem;">{item['kuantitas']:.4f} units</div>
                    <div class="coin-price">${item['nilai']:,.2f}</div>
                    <div style="color:#10B981;font-size:0.75rem;font-weight:600;">{alokasi_persen:.1f}% alokasi</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        kolom_hapus = st.columns(len(detail_portofolio)) if detail_portofolio else []
        for i, item in enumerate(detail_portofolio):
            with kolom_hapus[i]:
                if st.button(f"Hapus {item['simbol']}", key=f"rm_{item['id']}", use_container_width=True):
                    del st.session_state.portfolio[item["id"]]
                    st.rerun()
    else:
        st.markdown("""
        <div class="welcome-container">
            <h2>Portfolio kosong</h2>
            <p>Tambahkan coin di atas untuk mulai tracking portfolio kamu.</p>
        </div>
        """, unsafe_allow_html=True)
