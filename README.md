<img src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,100:059669&height=120&section=header" width="100%">

<div align="center">
  
# 💹 FINANCE GURU AI

<a href="https://github.com/HyLuthfi"><img src="https://readme-typing-svg.demolab.com?font=Outfit&weight=800&size=22&pause=1000&color=10B981&center=true&vCenter=true&width=800&lines=Intelligent+Financial+Assistant;Live+Crypto+Market+%26+Charts;Advanced+Financial+Calculators;Dynamic+Portfolio+Tracker" alt="Typing SVG" /></a>

  <p align="center">
    <a href="https://finance-guru-ai.streamlit.app/"><img src="https://img.shields.io/badge/LAUNCH_LIVE_APP-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo"></a>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Groq-00C7B7?style=for-the-badge&logo=groq&logoColor=white" alt="Groq">
    <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  </p>

  <p align="center">
    Asisten keuangan cerdas dan platform dasbor analitik untuk mengoptimalkan perencanaan investasi dan pemantauan pasar kripto. Menggunakan integrasi <b>Groq LLM</b> untuk insight cerdas dengan antarmuka <i>Premium Glassmorphism Dashboard</i>.
  </p>
</div>

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## ✨ Fitur Utama

<table align="center" width="100%">
  <tr>
    <td width="50%" valign="top">
      <b>Intelligent LLM Assistant</b><br/>
      Integrasi Groq API dengan Multi-Session State, Context-Aware AI (mampu membaca isi portofolio), dan Persona Customization.
    </td>
    <td width="50%" valign="top">
      <b>Live Market Dashboard</b><br/>
      Pemantauan aset kripto <i>real-time</i> dengan visualisasi interaktif via Plotly dan metrik Global Sentiment (Fear & Greed Index).
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>Financial Simulator Suite</b><br/>
      Kalkulator presisi tinggi untuk komputasi <i>Compound Interest</i>, Simulasi DCA (Dollar Cost Averaging), dan estimasi Profit/Loss.
    </td>
    <td width="50%" valign="top">
      <b>Dynamic Portfolio Tracker</b><br/>
      Manajemen alokasi aset kripto secara dinamis dengan pembaruan valuasi <i>real-time</i> berbasis integrasi CoinGecko API.
    </td>
  </tr>
</table>

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## 📸 Antarmuka Sistem (Premium Dashboard)

<table align="center" width="100%">
  <tr>
    <td width="50%" align="center">
      <b>Intelligent Chat Assistant</b><br/>
      <img src="img/dashboard_chat.png" width="100%">
    </td>
    <td width="50%" align="center">
      <b>Live Crypto Market & Charts</b><br/>
      <img src="img/Live_Market.png" width="100%">
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle">
      <b>Financial Calculators</b><br/>
      <img src="img/Kalkulator.png" width="100%">
    </td>
    <td width="50%" align="center" valign="middle">
      <b>Portfolio Tracking</b><br/>
      <img src="img/Portofolio.png" width="100%">
    </td>
  </tr>
</table>

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## 🧮 Arsitektur Sistem & Integrasi

Sistem mengeksekusi pengambilan data asinkron dan integrasi AI secara terstruktur pada tingkat *backend*:

**Integrasi Eksternal (API Metrics):**

- **Groq API (LLM)** - Pemrosesan analitik teks berkecepatan tinggi menggunakan model canggih (Llama 3.3/Gemma 2).
- **CoinGecko API** - Pengambilan data pasar absolut (harga, volume, kapitalisasi, historis).
- **Alternative.me** - Penyedia data indeks sentimen pasar global.

**Implementasi Arsitektur:**

1. **Context-Aware Prompting:** Menggabungkan data pasar aktual dan status kepemilikan portofolio pengguna langsung ke dalam injeksi <i>system prompt</i> untuk menghasilkan analisis AI yang sangat spesifik.
2. **Modular View-Controller:** Menggunakan arsitektur <i>decoupled</i> memisahkan komponen antarmuka (<code>components/</code>), penanganan komunikasi eksternal (<code>utils/api_handler.py</code>), dan injeksi estetika CSS kustom (<code>assets/style.css</code>).

<p align="center"><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"></p>

## 🚀 Panduan Instalasi & Eksekusi

Aplikasi ini menggunakan Streamlit dan sangat mudah dikonfigurasi untuk berjalan di <i>Localhost</i>.

### Tahap Persiapan & Eksekusi

1. **Clone Repositori**
   ```bash
   git clone https://github.com/HyLuthfi/finance-guru-ai.git
   cd finance-guru-ai
   ```
2. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Server Streamlit**
   ```bash
   streamlit run app.py
   ```
4. **Setup Kunci API (API Key)**
   - Buka browser di `http://localhost:8501`.
   - Dapatkan API Key secara gratis di [console.groq.com](https://console.groq.com).
   - Masukkan kunci tersebut ke dalam bilah samping (<i>sidebar</i>) konfigurasi aplikasi untuk mengaktifkan fitur analisis AI.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,100:059669&height=120&section=footer" width="100%"/>
</p>
