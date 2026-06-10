import requests
from datetime import datetime
import streamlit as st

@st.cache_data(ttl=120)
def ambil_harga_kripto():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd", 
        "order": "market_cap_desc",
        "per_page": 5, 
        "page": 1, 
        "sparkline": True,
        "ids": "bitcoin,ethereum,solana,binancecoin,ripple",
    }
    try:
        respons = requests.get(url, params=params, timeout=10)
        respons.raise_for_status()
        return respons.json()
    except requests.exceptions.RequestException as e:
        st.error("Gagal mengambil data harga kripto. Periksa koneksi internet atau coba beberapa saat lagi.")
        return []

@st.cache_data(ttl=300)
def ambil_grafik_koin(id_koin, hari=7):
    url = f"https://api.coingecko.com/api/v3/coins/{id_koin}/market_chart"
    params = {"vs_currency": "usd", "days": hari}
    try:
        respons = requests.get(url, params=params, timeout=10)
        respons.raise_for_status()
        data = respons.json().get("prices", [])
        waktu = [datetime.fromtimestamp(p[0] / 1000) for p in data]
        harga = [p[1] for p in data]
        return waktu, harga
    except requests.exceptions.RequestException:
        st.warning("Gagal mengambil grafik riwayat harga.")
        return None, None

@st.cache_data(ttl=600)
def ambil_berita_kripto():
    url = "https://api.coingecko.com/api/v3/news"
    try:
        respons = requests.get(url, timeout=10)
        respons.raise_for_status()
        return respons.json().get("data", [])[:8]
    except requests.exceptions.RequestException:
        st.warning("Gagal mengambil berita terbaru.")
        return []

@st.cache_data(ttl=300)
def ambil_fear_greed():
    url = "https://api.alternative.me/fng/?limit=1"
    try:
        respons = requests.get(url, timeout=10)
        respons.raise_for_status()
        data = respons.json()["data"][0]
        return {"nilai": int(data["value"]), "label": data["value_classification"]}
    except requests.exceptions.RequestException:
        return None

@st.cache_data(ttl=60)
def cari_koin(kueri):
    url_cari = "https://api.coingecko.com/api/v3/search"
    try:
        respons_cari = requests.get(url_cari, params={"query": kueri}, timeout=10)
        respons_cari.raise_for_status()
        koin = respons_cari.json().get("coins", [])[:3]
        if koin:
            id_koin = ",".join(c["id"] for c in koin)
            url_detail = "https://api.coingecko.com/api/v3/coins/markets"
            respons_detail = requests.get(url_detail, params={"vs_currency": "usd", "ids": id_koin}, timeout=10)
            respons_detail.raise_for_status()
            return respons_detail.json()
    except requests.exceptions.RequestException:
        st.warning("Gagal mencari koin.")
    return []

def ambil_portofolio_pasar(id_koin_list):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "ids": id_koin_list, "sparkline": False}
    try:
        respons = requests.get(url, params=params, timeout=10)
        respons.raise_for_status()
        return respons.json()
    except requests.exceptions.RequestException:
        return []
