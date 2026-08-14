import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- CSS STABLE & PREMIUM ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Poppins', sans-serif !important; }
        
        [data-testid="stAppViewContainer"] {
            background-color: #EAE3CD;
            background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px);
            background-size: 30px 30px;
        }

        /* Glassmorphism Containers */
        [data-testid="stForm"], [data-testid="stMetric"], [data-testid="stDataFrame"], .stTable > div {
            background: rgba(255, 255, 255, 0.5) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            padding: 20px !important;
        }
        
        .stButton > button {
            background-color: #819264 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }
        
        h3 { color: #2c3322 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER LOGO STATIC (PALING STABIL) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)

# --- KONFIGURASI ---
MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TARGET_CUAN = 1500000

conn = st.connection("gsheets", type=GSheetsConnection)
df_income = conn.read(worksheet="Pemasukan", usecols=[0, 1, 2], ttl=0).dropna(how="all")
df_att = conn.read(worksheet="Absensi", usecols=[0, 1, 2, 3, 4], ttl=0).dropna(how="all")
df_setting = conn.read(worksheet="Pengaturan", usecols=[0, 1], ttl=0).dropna(how="all")

if df_att.empty:
    df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

# --- TARGET BAR ---
pct = min((total_income / TARGET_CUAN) * 100, 100)
st.markdown(f"""
<div style="background: rgba(255,255,255,0.5); padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center;">
    <h4 style="color:#2c3322;">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background:#ddd; border-radius:10px; height:20px; width:100%;">
        <div style="background:#819264; height:100%; width:{pct}%; border-radius:10px;"></div>
    </div>
    <p>Terkumpul: Rp {total_income:,.0f}</p>
</div>
""", unsafe_allow_html=True)

# --- LOGIKA ABSEN & PEMASUKAN ---
# (Sisa logika aplikasi lu taruh di sini ya, sama persis kayak sebelumnya)
# Lu tinggal copas bagian logika yang tadi lu punya di bawah sini
