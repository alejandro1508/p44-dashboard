import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- KODE VISUAL V10: LOGO DYNAMIC SHRINK ---
st.markdown("""
    <style>
        /* Background & Font */
        [data-testid="stAppViewContainer"] {
            background-color: #EAE3CD;
            background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px);
            background-size: 30px 30px;
        }
        
        /* Navbar yang nempel di atas */
        .sticky-nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            background: rgba(234, 227, 205, 0.9);
            backdrop-filter: blur(10px);
            padding: 15px 0;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        /* Logo gede pas di atas */
        .logo-img {
            height: 80px; 
            transition: all 0.3s ease;
        }
        
        /* Saat discroll, dia jadi kecil */
        .scrolled .logo-img {
            height: 40px;
        }
        .scrolled .sticky-nav {
            padding: 5px 0;
        }

        /* Glassmorphism umum */
        [data-testid="stForm"], [data-testid="stMetric"], .stDataFrame {
            background: rgba(255, 255, 255, 0.4) !important;
            backdrop-filter: blur(10px);
            border-radius: 15px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }
        
        /* Kasih jarak atas biar ga nabrak navbar */
        .block-container { padding-top: 100px !important; }
    </style>
    
    <div id="nav" class="sticky-nav">
        <img src="https://raw.githubusercontent.com/alejandro1508/p44-dashboard/main/logo.png" class="logo-img">
    </div>
    
    <script>
        window.onscroll = function() {
            var nav = document.getElementById("nav");
            if (window.pageYOffset > 50) {
                nav.classList.add("scrolled");
            } else {
                nav.classList.remove("scrolled");
            }
        };
    </script>
""", unsafe_allow_html=True)

# --- KONFIGURASI UTAMA ---
MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TARGET_CUAN = 1500000

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df_income = conn.read(worksheet="Pemasukan", usecols=[0, 1, 2], ttl=0).dropna(how="all")
df_att = conn.read(worksheet="Absensi", usecols=[0, 1, 2, 3, 4], ttl=0).dropna(how="all")
df_setting = conn.read(worksheet="Pengaturan", usecols=[0, 1], ttl=0).dropna(how="all")

# ... (Sisa fungsi logika aplikasi lu sama persis kayak V9 sebelumnya) ...
# PENTING: Paste sisa kode logika (mulai dari hitungan income, form absen, dst) di bawah sini ya!
