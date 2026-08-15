import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona Waktu
tz = pytz.timezone('Asia/Jakarta')
now_time = datetime.now(tz)

st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- CSS VISUAL ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Poppins', sans-serif !important; }
        [data-testid="stAppViewContainer"] { background-color: #EAE3CD; background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px); background-size: 30px 30px; }
        
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .main { animation: fadeInUp 0.5s ease-out; }
        
        @keyframes blinker { 50% { opacity: 0.3; } }
        .on-air-badge { background-color: #ff4b4b; color: white; padding: 8px 20px; border-radius: 50px; font-weight: 700; animation: blinker 1.2s linear infinite; display: inline-block; margin-bottom: 15px; }
        .offline-badge { background-color: #6c757d; color: white; padding: 8px 20px; border-radius: 50px; font-weight: 700; display: inline-block; margin-bottom: 15px; }
        
        [data-testid="stForm"], [data-testid="stMetric"], .stDataFrame {
            background: rgba(255, 255, 255, 0.5) !important; backdrop-filter: blur(10px) !important;
            border-radius: 15px !important; border: 1px solid rgba(255, 255, 255, 0.4) !important;
            padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        
        .schedule-container { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 20px; }
        .schedule-container::-webkit-scrollbar { display: none; }
        .schedule-card { background: rgba(255,255,255,0.5); border: 1px solid rgba(129,146,100,0.3); border-radius: 12px; min-width: 120px; padding: 15px 10px; text-align: center; flex: 1; }
        .schedule-card.today { background: rgba(129,146,100,0.2); border: 2px solid #819264; transform: scale(1.05); }
        .sch-day { font-weight: 700; color: #819264; margin-bottom: 5px; font-size: 14px; text-transform: uppercase; }
        .sch-name { font-weight: 600; color: #2c3322; font-size: 13px; }
        .today .sch-day { color: #2c3322; }
        
        .stButton > button { background-color: #819264 !important; color: white !important; border-radius: 10px !important; border: none !important; font-weight: 600 !important; width: 100%; }
        h3.glow-title { color: #2c3322 !important; text-align: center; font-weight: 700; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
greeting = "Pagi" if 5 <= now_time.hour < 11 else "Siang" if 11 <= now_time.hour < 15 else "Sore" if 15 <= now_time.hour < 18 else "Malam"
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2: st.image("logo.png", use_container_width=True)
st.markdown("<h3 class='glow-title'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #6a7a52; font-weight: 600;'>Selamat {greeting}, Warga 4/4! | {now_time.strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

st.markdown("""<marquee scrollamount="7" style="background-color: #819264; color: white; padding: 8px; border-radius: 8px; font-weight: 600; font-size: 14px; margin-bottom: 20px;">🔥 INFO PROJECT 4/4: JANGAN LUPA BERSIHIN STUDIO SEBELUM BALIK -- PASTIKAN ABSEN KELUAR PAS SELESAI LIVE 🔥</marquee>""", unsafe_allow_html=True)

# --- KONFIGURASI ---
MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TARGET_CUAN = 1500000
JADWAL_STUDIO = {"Senin": "Vino & Adli", "Selasa": "Ale & Rian", "Rabu": "Owbet & Vino", "Kamis": "Adli & Rian", "Jumat": "Ale & Owbet", "Sabtu": "All Member", "Minggu": "Libur"}

conn = st.connection("gsheets", type=GSheetsConnection)

# Cara baca data yang dijamin anti nyangkut
try:
    df_income = conn.read(worksheet="Pemasukan", usecols=[0, 1, 2], ttl=10).dropna(how="all")
except:
    df_income = pd.DataFrame(columns=["Tanggal", "Keterangan", "Nominal"])
try:
    df_att = conn.read(worksheet="Absensi", usecols=[0, 1, 2, 3, 4], ttl=10).dropna(how="all")
except:
    df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])
try:
    df_setting = conn.read(worksheet="Pengaturan", usecols=[0, 1], ttl=10).dropna(how="all")
except:
    df_setting = pd.DataFrame(columns=["Parameter", "Value"])

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

# --- TARGET ---
pct = min((total_income / TARGET_CUAN) * 100, 100) if TARGET_CUAN > 0 else 0
bar_color = "#FFD700" if pct >= 100 else "#819264"
st.markdown(f"""
<div style="padding: 20px; background: rgba(255,255,255,0.5); border-radius: 15px; border: 1px solid rgba(255,255,255,0.4); margin-bottom: 20px;">
    <h4 style="margin: 0 0 10px 0; text-align: center; color: #2c3322;">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background:rgba(0,0,0,0.1); border-radius:10px; height:20px;"><div style="background:{bar_color}; width:{pct}%; height:100%; border-radius:10px;"></div></div>
    <p style="text-align: center; margin: 10px 0 0 0; font-weight: 600; color: #2c3322;">Terkumpul: Rp {total_income:,.0f} ({pct:.1f}%)</p>
</div>
""", unsafe_allow_html=True)

# --- JADWAL ---
hari_ini_idx = now_time.weekday()
html_jadwal = "<div class='schedule-container'>"
for i, day in enumerate(JADWAL_STUDIO.keys()):
    c_today = "today" if i == hari_ini_idx else ""
    html_jadwal += f"<div class='schedule-card {c_today}'><div class='sch-day'>{day}</div><div class='sch-name'>{JADWAL_STUDIO[day]}</div></div>"
html_jadwal += "</div>"
st.markdown(html_jadwal, unsafe_allow_html=True)

# --- PIN & STATUS ---
current_pin = "2026"
if not df_setting.empty and "Parameter" in df_setting.columns:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty: current_pin = str(pin_row.iloc[0]["Value"]).replace('.0','').strip()

active_names = df_att[df_att["Jam Keluar"] == ""]["Nama"].tolist() if "Jam Keluar" in df_att.columns else []
inactive_names = [m for m in MEMBERS if m not in active_names]

col1, col2 = st.columns(2)

# === KIRI: PEMASUKAN ===
with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        if st.form_submit_button("Simpan"):
            try:
                new_row = pd.DataFrame([{"Tanggal": now_time.strftime("%Y-%m-%d %H:%M"), "Keterangan": desc, "Nominal": amount}])
                conn.update(worksheet="Pemasukan", data=pd.concat([df_income, new_row], ignore_index=True))
                st.rerun()
            except: st.error("Gagal nyimpen!")
    if not df_income.empty: st.dataframe(df_income.tail(5).iloc[::-1], use_container_width=True, hide_index=True)

# === KANAN: ABSENSI ===
with col2:
    st.subheader("⏱️ 2. Sistem Absen")
    st.markdown(f"<div class='{'on-air-badge' if active_names else 'offline-badge'}'>{'🔴 ON AIR : ' + ', '.join(active_names) if active_names else '⚪ STUDIO OFFLINE'}</div>", unsafe_allow_html=True)
    
    mode = st.radio("Aksi:", ["Masuk", "Keluar Individu", "Keluar Semua"])
    
    if mode == "Masuk" and inactive_names:
        with st.form("f_masuk"):
            nama = st.selectbox("Nama", inactive_names)
            pin = st.text_input("PIN", type="password")
            if st.form_submit_button("Masuk"):
                if pin != current_pin: st.error("PIN Salah!")
                else:
                    new_att = pd.DataFrame([{"Tanggal": now_time.strftime("%Y-%m-%d"), "Nama": nama, "Jam Masuk": now_time.strftime("%H:%M:%S"), "Jam Keluar": "", "Poin": ""}])
                    conn.update(worksheet="Absensi", data=pd.concat([df_att, new_att], ignore_index=True))
                    st.rerun()
    elif mode == "Keluar Individu" and active_names:
        with st.form("f_keluar_1"):
            nama_out = st.selectbox("Nama", active_names)
            pin_out = st.text_input("PIN", type="password")
            if st.form_submit_button("Keluar"):
                if pin_out != current_pin: st.error("PIN Salah!")
                else:
                    for idx, row in df_att.iterrows():
                        if row["Nama"] == nama_out and row["Jam Keluar"] == "":
                            try:
                                masuk = datetime.strptime(str(row["Jam Masuk"]), "%H:%M:%S").replace(year=now_time.year, month=now_time.month, day=now_time.day)
                                durasi = max((now_time.replace(tzinfo=None) - masuk).total_seconds() / 3600.0, 0.01)
                            except: durasi = 0.1
                            df_att.at[idx, "Jam Keluar"] = now_time.strftime("%H:%M:%S"); df_att.at[idx, "Poin"] = round(durasi, 1)
                    conn.update(worksheet="Absensi", data=df_att); st.rerun()
    elif mode == "Keluar Semua" and active_names:
        with st.form("f_keluar_all"):
            pin_all = st.text_input("PIN", type="password")
            if st.form_submit_button("Akhiri Semua"):
                if pin_all != current_pin: st.error("PIN Salah!")
                else:
                    for idx, row in df_att.iterrows():
                        if row["Jam Keluar"] == "":
                            try:
                                masuk = datetime.strptime(str(row["Jam Masuk"]), "%H:%M:%S").replace(year=now_time.year, month=now_time.month, day=now_time.day)
                                durasi = max((now_time.replace(tzinfo=None) - masuk).total_seconds() / 3600.0, 0.01)
                            except: durasi = 0.1
                            df_att.at[idx, "Jam Keluar"] = now_time.strftime("%H:%M:%S"); df_att.at[idx, "Poin"] = round(durasi, 1)
                    conn.update(worksheet="Absensi", data=df_att); st.rerun()

# --- STATS & GAJI ---
st.divider()
st.subheader("📊 3. Kalkulasi Gaji")
if "Poin" in df_att.columns: df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
points_map = df_att.groupby("Nama")["Poin"].sum().to_dict() if not df_att.empty else {}
for m in MEMBERS: points_map.setdefault(m, 0.0)

act_count = sum(1 for m in MEMBERS if points_map[m] > 0)
val_base = (total_income * 0.5 * 0.4 / act_count) if act_count > 0 else 0
val_point = (total_income * 0.5 * 0.6 / sum(points_map.values())) if sum(points_map.values()) > 0 else 0

res = [{"Anggota": m, "Poin": f"{points_map[m]} Jam", "Dasar": f"Rp {val_base if points_map[m]>0 else 0:,.0f}", "Bonus": f"Rp {points_map[m]*val_point:,.0f}", "TOTAL": f"Rp {(val_base if points_map[m]>0 else 0) + (points_map[m]*val_point):,.0f}"} for m in MEMBERS]
st.table(pd.DataFrame(res))

# --- SLIP GAJI ---
st.divider()
st.subheader("🖨️ Struk Digital")
slip_name = st.selectbox("Nama:", MEMBERS)
s_base = val_base if points_map[slip_name] > 0 else 0
s_bonus = points_map[slip_name] * val_point
st.markdown(f"""
<div style="background: rgba(255,255,255,0.7); padding: 20px; border-radius: 15px; border: 2px dashed #819264; max-width: 400px; margin: auto;">
    <h4 style="text-align:center; color:#2c3322;">🧾 SLIP GAJI {slip_name}</h4>
    <p style="text-align:center; font-size:12px;">Total Jam: {points_map[slip_name]} Jam</p><hr style="border-top:1px dashed #819264;">
    <p>Dasar: Rp {s_base:,.0f}<br>Bonus: Rp {s_bonus:,.0f}</p>
    <h3 style="text-align:center; background:rgba(129,146,100,0.2); padding:10px; border-radius:10px;">CAIR: Rp {s_base+s_bonus:,.0f}</h3>
</div>
""", unsafe_allow_html=True)
