import streamlit as st

def render_calculator_tab():
    jenis_kalkulator = st.selectbox("Pilih Kalkulator", [
        "Compound Interest", "DCA Simulator", "Profit / Loss"
    ])

    st.markdown("")

    if jenis_kalkulator == "Compound Interest":
        st.markdown("#### Kalkulator Compound Interest")
        st.caption("Hitung pertumbuhan investasi dengan bunga majemuk")
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            modal_awal = st.number_input("Modal Awal (Rp)", min_value=0, value=10_000_000, step=1_000_000, format="%d")
            bunga_tahunan = st.number_input("Return Tahunan (%)", min_value=0.0, value=12.0, step=0.5)
        with kolom2:
            durasi_tahun = st.number_input("Durasi (tahun)", min_value=1, value=10, step=1)
            tambahan_bulanan = st.number_input("Tambahan Bulanan (Rp)", min_value=0, value=1_000_000, step=100_000, format="%d")

        if st.button("Hitung", use_container_width=True):
            bunga_bulanan = bunga_tahunan / 100 / 12
            total_bulan = durasi_tahun * 12
            total_akhir = modal_awal
            for _ in range(total_bulan):
                total_akhir = total_akhir * (1 + bunga_bulanan) + tambahan_bulanan
            total_investasi = modal_awal + (tambahan_bulanan * total_bulan)
            keuntungan = total_akhir - total_investasi

            baris1, baris2, baris3 = st.columns(3)
            baris1.metric("Nilai Akhir", f"Rp {total_akhir:,.0f}")
            baris2.metric("Total Investasi", f"Rp {total_investasi:,.0f}")
            baris3.metric("Keuntungan", f"Rp {keuntungan:,.0f}", f"+{(keuntungan/total_investasi*100):.1f}%")

    elif jenis_kalkulator == "DCA Simulator":
        st.markdown("#### DCA (Dollar Cost Averaging) Simulator")
        st.caption("Simulasi strategi investasi berkala")
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            nominal_dca = st.number_input("Investasi per Bulan (Rp)", min_value=0, value=500_000, step=100_000, format="%d")
            durasi_bulan = st.number_input("Durasi (bulan)", min_value=1, value=24, step=1)
        with kolom2:
            estimasi_bunga = st.number_input("Estimasi Return Bulanan (%)", min_value=-50.0, value=1.5, step=0.5)

        if st.button("Simulasi", use_container_width=True):
            bunga_bulanan = estimasi_bunga / 100
            total_nilai = 0
            for _ in range(durasi_bulan):
                total_nilai = (total_nilai + nominal_dca) * (1 + bunga_bulanan)
            total_investasi = nominal_dca * durasi_bulan
            profit_dca = total_nilai - total_investasi

            baris1, baris2, baris3 = st.columns(3)
            baris1.metric("Nilai Portfolio", f"Rp {total_nilai:,.0f}")
            baris2.metric("Total Investasi", f"Rp {total_investasi:,.0f}")
            persentase = (profit_dca/total_investasi*100) if total_investasi > 0 else 0
            baris3.metric("Profit/Loss", f"Rp {profit_dca:,.0f}", f"{persentase:+.1f}%")

    elif jenis_kalkulator == "Profit / Loss":
        st.markdown("#### Kalkulator Profit / Loss")
        st.caption("Hitung keuntungan atau kerugian trading")
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            harga_beli = st.number_input("Harga Beli", min_value=0.0, value=50000.0, step=1000.0)
            jumlah_unit = st.number_input("Jumlah Unit", min_value=0.0, value=10.0, step=1.0)
        with kolom2:
            harga_jual = st.number_input("Harga Jual", min_value=0.0, value=65000.0, step=1000.0)
            biaya_transaksi = st.number_input("Fee Transaksi (%)", min_value=0.0, value=0.15, step=0.05)

        if st.button("Hitung", use_container_width=True, key="calc_pl"):
            total_beli = harga_beli * jumlah_unit
            total_jual = harga_jual * jumlah_unit
            total_biaya = (total_beli + total_jual) * (biaya_transaksi / 100)
            keuntungan_bersih = total_jual - total_beli - total_biaya
            persentase = (keuntungan_bersih / total_beli * 100) if total_beli > 0 else 0

            baris1, baris2, baris3 = st.columns(3)
            baris1.metric("Net P/L", f"Rp {keuntungan_bersih:,.0f}", f"{persentase:+.2f}%")
            baris2.metric("Total Cost", f"Rp {total_beli:,.0f}")
            baris3.metric("Fee", f"Rp {total_biaya:,.0f}")
