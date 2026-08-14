import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

# Konfigurasi Halaman (Logo di Tab Browser)
st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif !important;
        }
    </style>
""", unsafe_allow_html=True)

# Nampilin Logo di Tengah Atas
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("logo.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Dashboard Revenue & Absensi</h1>", unsafe_allow_html=True)
st.divider()

MEMBERS = ["Ale", "Vino", "Adli", "Owbet", "Rian"]

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df_income = conn.read(worksheet="Pemasukan", usecols=[0, 1, 2]).dropna(how="all")
df_att = conn.read(worksheet="Absensi", usecols=[0, 1, 2, 3]).dropna(how="all")

col1, col2 = st.columns(2)

# --- FORM PEMASUKAN ---
with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan", placeholder="Misal: Live Saweria")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        submit_inc = st.form_submit_button("Simpan Pemasukan")
        
        if submit_inc and amount > 0:
            now = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
            new_income = pd.DataFrame([{"Tanggal": now, "Keterangan": desc, "Nominal": amount}])
            updated_income = pd.concat([df_income, new_income], ignore_index=True)
            conn.update(worksheet="Pemasukan", data=updated_income)
            st.success("Tersimpan!")
            st.rerun()

# --- FORM ABSENSI ---
with col2:
    st.subheader("⏱️ 2. Input Jam Live")
    
    # Notif Waktu Otomatis
    now_display = datetime.now(tz).strftime("%d %b %Y, %H:%M WIB")
    st.info(f"🕒 Waktu otomatis terkunci pada: **{now_display}**")
    
    with st.form("form_att"):
        name = st.selectbox("Nama Anggota", MEMBERS)
        hours = st.selectbox("Durasi / Poin", [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0], index=3)
        session = st.text_input("Keterangan Sesi", placeholder="Misal: Live Kamis Malam")
        submit_att = st.form_submit_button("Simpan Absensi")
        
        if submit_att:
            now_submit = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
            new_att = pd.DataFrame([{"Tanggal": now_submit, "Nama": name, "Sesi": session, "Poin": hours}])
            updated_att = pd.concat([df_att, new_att], ignore_index=True)
            conn.update(worksheet="Absensi", data=updated_att)
            st.success("Tersimpan!")
            st.rerun()

st.divider()

# --- KALKULASI 30-50-20 ---
st.subheader("📊 3. Hasil Bagi Hasil Mingguan")
try:
    total_income = df_income["Nominal"].astype(float).sum() if not df_income.empty else 0
except:
    total_income = 0

kas_studio = total_income * 0.30
kas_ops = total_income * 0.20
team_share = total_income * 0.50

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Pemasukan", f"Rp {total_income:,.0f}")
m2.metric("🏢 Kas Studio (30%)", f"Rp {kas_studio:,.0f}")
m3.metric("☕ Ops/Makan (20%)", f"Rp {kas_ops:,.0f}")
m4.metric("👥 Jatah Tim (50%)", f"Rp {team_share:,.0f}")

points_map = {m: 0.0 for m in MEMBERS}
total_points = 0

if not df_att.empty:
    for _, row in df_att.iterrows():
        n = str(row["Nama"])
        pts = float(row["Poin"])
        if n in points_map:
            points_map[n] += pts
            total_points += pts

base_pool = team_share * 0.40
base_per_person = (base_pool / len(MEMBERS)) if total_income > 0 else 0
live_pool = team_share * 0.60
val_per_point = (live_pool / total_points) if total_points > 0 else 0

result_data = []
for m in MEMBERS:
    pts = points_map[m]
    total_earned = base_per_person + (pts * val_per_point)
    result_data.append({
        "Anggota": m,
        "Poin Jam": f"{pts} Jam",
        "Tugas Dasar": f"Rp {base_per_person:,.0f}",
        "Uang Poin Live": f"Rp {pts * val_per_point:,.0f}",
        "TOTAL CAIR": f"Rp {total_earned:,.0f}"
    })

st.table(pd.DataFrame(result_data))
