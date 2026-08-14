import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

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
            font-weight: 600 !important;
        }
        
        h3 { color: #2c3322 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- LOGO & JUDUL ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("logo.png", use_container_width=True)
st.markdown("<h3 style='margin-bottom: 20px;'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)

# --- KONFIGURASI DATA ---
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
    <h4 style="color:#2c3322; margin-bottom:10px;">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background:#ddd; border-radius:10px; height:20px; width:100%;">
        <div style="background:#819264; height:100%; width:{pct}%; border-radius:10px;"></div>
    </div>
    <p style="margin-top:10px; font-weight:600;">Terkumpul: Rp {total_income:,.0f} ({pct:.1f}%)</p>
</div>
""", unsafe_allow_html=True)

# --- LOGIKA APLIKASI ---
# Ambil PIN
current_pin = "2026"
if not df_setting.empty and "Parameter" in df_setting.columns:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty:
        raw_pin = str(pin_row.iloc[0]["Value"])
        current_pin = raw_pin[:-2] if raw_pin.endswith('.0') else raw_pin.strip()

active_mask = df_att["Jam Keluar"].isna() | (df_att["Jam Keluar"] == "")
df_active = df_att[active_mask]
active_names = df_active["Nama"].tolist() if not df_active.empty else []

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan", placeholder="Misal: Live Saweria / Komisi TikTok")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        if st.form_submit_button("Simpan Pemasukan"):
            new_row = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d %H:%M"), "Keterangan": desc, "Nominal": amount}])
            conn.update(worksheet="Pemasukan", data=pd.concat([df_income, new_row], ignore_index=True))
            st.rerun()
    if not df_income.empty:
        st.dataframe(df_income.tail(5).iloc[::-1], use_container_width=True, hide_index=True)

with col2:
    st.subheader("⏱️ 2. Absen Otomatis")
    if active_names: st.info(f"🔴 Sedang Live: {', '.join(active_names)}")
    else: st.info("⚪ Studio kosong.")
    
    mode = st.radio("Mode:", ["Masuk", "Selesai"], horizontal=True)
    with st.form("absensi"):
        nama = st.selectbox("Nama", MEMBERS)
        pin = st.text_input("PIN Studio", type="password")
        if st.form_submit_button("Submit"):
            if pin != current_pin: st.error("PIN Salah!")
            elif mode == "Masuk":
                new_att = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d"), "Nama": nama, "Jam Masuk": datetime.now(tz).strftime("%H:%M:%S"), "Jam Keluar": "", "Poin": ""}])
                conn.update(worksheet="Absensi", data=pd.concat([df_att, new_att], ignore_index=True))
                st.rerun()
            else:
                # Logic Keluar (Sederhana)
                st.success("Live selesai!")
                st.rerun()

# --- STATISTIK ---
st.divider()
st.subheader("📊 3. Statistik")
df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
points_map = df_att.groupby("Nama")["Poin"].sum().to_dict()
st.bar_chart(pd.Series(points_map))

# --- SLIP GAJI ---
st.divider()
st.subheader("🖨️ Generator Slip Gaji Digital")
slip_name = st.selectbox("Nama:", MEMBERS)
total_pts = points_map.get(slip_name, 0)
total_earned = ((total_income * 0.5 * 0.4) / len(MEMBERS)) + (total_pts * (total_income * 0.5 * 0.6 / total_points if total_points > 0 else 0))

st.markdown(f"""
<div style="background: rgba(255,255,255,0.7); padding: 20px; border-radius: 15px; border: 2px dashed #819264; max-width: 400px; margin: auto;">
    <h4>🧾 SLIP GAJI {slip_name.upper()}</h4>
    <p>Total Jam: {total_pts} Jam</p>
    <hr>
    <h3>TOTAL: Rp {total_earned:,.0f}</h3>
</div>
""", unsafe_allow_html=True)
