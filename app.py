import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz
import time

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- SUNTIKAN CSS GOD TIER (VISUAL + ANIMASI BALIK!) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif !important;
        }
        
        /* --- EFEK BACKGROUND DOT GRID --- */
        [data-testid="stAppViewContainer"] {
            background-color: #EAE3CD;
            background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px);
            background-size: 30px 30px;
        }

        /* --- ANIMASI FADE-IN SAAT DIBUKA --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main {
            animation: fadeInUp 0.8s ease-out;
        }

        /* --- GLASSMORPHISM (EFEK KACA BURAM) --- */
        [data-testid="stForm"], [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.45) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            box-shadow: 0 8px 32px 0 rgba(129, 146, 100, 0.15) !important;
            padding: 20px !important;
            transition: all 0.3s ease-in-out !important;
        }

        /* Efek Kotak Melayang (Hover) */
        [data-testid="stForm"]:hover, [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(129, 146, 100, 0.25) !important;
        }
        
        /* Fix Tabel Biar Ga Nabrak */
        [data-testid="stDataFrame"] {
            border-radius: 15px !important;
            overflow: hidden !important;
            box-shadow: 0 8px 32px 0 rgba(129, 146, 100, 0.15) !important;
        }
        
        /* --- WARNA CUSTOM (OLIVE GREEN) --- */
        .stTextInput input:focus, .stNumberInput input:focus, input[type="password"]:focus {
            border-color: #819264 !important;
            box-shadow: 0 0 0 1px #819264 !important;
        }
        
        /* Tombol Premium */
        .stButton > button {
            background-color: #819264 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.3s ease-in-out !important;
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0px 8px 15px rgba(129, 146, 100, 0.4) !important;
            background-color: #6a7a52 !important;
            color: white !important;
        }

        /* Efek Teks Glowing untuk Judul */
        @keyframes pulseGlow {
            0% { text-shadow: 0 0 5px rgba(129,146,100,0.2); }
            50% { text-shadow: 0 0 20px rgba(129,146,100,0.8), 0 0 30px rgba(129,146,100,0.6); }
            100% { text-shadow: 0 0 5px rgba(129,146,100,0.2); }
        }
        h3.glow-title {
            animation: pulseGlow 3s infinite alternate !important;
            color: #2c3322 !important;
            text-align: center;
            font-weight: 700;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOGO & JUDUL ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("logo.png", use_container_width=True)
st.markdown("<h3 class='glow-title'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)

# --- KONFIGURASI DATA ---
MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TARGET_CUAN = 1500000

def get_safe_data(conn, sheet_name, cols):
    try:
        return conn.read(worksheet=sheet_name, usecols=cols, ttl=5).dropna(how="all")
    except Exception as e:
        st.error(f"⚠️ Google Sheets lagi sibuk. Refresh webnya. ({sheet_name})")
        return pd.DataFrame()

conn = st.connection("gsheets", type=GSheetsConnection)

df_income = get_safe_data(conn, "Pemasukan", [0, 1, 2])
df_att = get_safe_data(conn, "Absensi", [0, 1, 2, 3, 4])
df_setting = get_safe_data(conn, "Pengaturan", [0, 1])

if df_att.empty and not 'Tanggal' in df_att.columns: df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])
if df_income.empty and not 'Nominal' in df_income.columns: df_income = pd.DataFrame(columns=["Tanggal", "Keterangan", "Nominal"])

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

# --- TARGET BAR ---
pct = min((total_income / TARGET_CUAN) * 100, 100) if TARGET_CUAN > 0 else 0
is_gold = pct >= 100
bar_color = "linear-gradient(90deg, #FFD700, #F5A623)" if is_gold else "linear-gradient(90deg, #819264, #A3B18A)"

st.markdown(f"""
<div style="padding: 20px; background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.4); box-shadow: 0 8px 32px 0 rgba(129, 146, 100, 0.15); margin-bottom: 30px;">
    <h4 style="margin: 0 0 10px 0; text-align: center; color: #2c3322;">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background-color: rgba(0,0,0,0.1); border-radius: 10px; width: 100%; height: 25px;">
        <div style="background: {bar_color}; width: {pct}%; height: 100%; border-radius: 10px; transition: width 1s ease-in-out;"></div>
    </div>
    <p style="text-align: center; margin: 10px 0 0 0; font-weight: 600; color: #2c3322; font-size: 16px;">Terkumpul: Rp {total_income:,.0f} ({pct:.1f}%)</p>
</div>
""", unsafe_allow_html=True)
if is_gold and total_income > 0: st.balloons()

# --- AMBIL PIN ---
current_pin = "2026"
if not df_setting.empty and "Parameter" in df_setting.columns:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty:
        raw_pin = str(pin_row.iloc[0]["Value"])
        current_pin = raw_pin[:-2] if raw_pin.endswith('.0') else raw_pin.strip()

# --- DETEKSI STATUS MEMBER ---
if "Jam Keluar" in df_att.columns:
    active_mask = df_att["Jam Keluar"].isna() | (df_att["Jam Keluar"] == "")
    df_active = df_att[active_mask]
    active_names = df_active["Nama"].tolist() if not df_active.empty else []
else:
    active_names = []
    
inactive_names = [m for m in MEMBERS if m not in active_names]

def parse_time_safe(time_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%H:%M:%S", "%Y-%m-%d %H:%M"):
        try: return datetime.strptime(str(time_str), fmt)
        except: pass
    return datetime.now()

col1, col2 = st.columns(2)

# === BAGIAN KIRI: PEMASUKAN ===
with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan", placeholder="Misal: Live Saweria")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        if st.form_submit_button("Simpan Pemasukan"):
            try:
                new_row = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d %H:%M"), "Keterangan": desc, "Nominal": amount}])
                conn.update(worksheet="Pemasukan", data=pd.concat([df_income, new_row], ignore_index=True))
                st.success("Tersimpan!")
                time.sleep(1)
                st.rerun()
            except: st.error("Google Sheets sibuk. Coba lagi!")
                    
    st.markdown("**📜 Riwayat Pemasukan**")
    if not df_income.empty and len(df_income) > 0:
        st.dataframe(df_income.tail(5).iloc[::-1], use_container_width=True, hide_index=True)

# === BAGIAN KANAN: ABSENSI ===
with col2:
    st.subheader("⏱️ 2. Sistem Absen")
    if active_names: st.info(f"🔴 Sedang Live: **{', '.join(active_names)}**")
    else: st.info("⚪ Studio kosong.")
    
    mode = st.radio("Pilih Aksi:", ["Masuk Live", "Selesai Individu (Pulang Duluan)", "Tutup Studio (Selesai Semua)"])
    
    if mode == "Masuk Live":
        if inactive_names:
            with st.form("form_masuk"):
                nama = st.selectbox("Siapa yang mau absen?", inactive_names)
                pin = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Masuk Live!"):
                    if pin != current_pin: st.error("❌ PIN Salah!")
                    else:
                        try:
                            now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                            new_att = pd.DataFrame([{"Tanggal": now_str[:10], "Nama": nama, "Jam Masuk": now_str, "Jam Keluar": "", "Poin": ""}])
                            conn.update(worksheet="Absensi", data=pd.concat([df_att, new_att], ignore_index=True))
                            st.success(f"✅ {nama} masuk live!")
                            time.sleep(1)
                            st.rerun()
                        except: st.error("Gagal nyimpen, klik lagi.")
        else:
            # Pake kotak info cantik biar ga kuning polos
            st.info("Semua member sudah di dalam Live!")

    elif mode == "Selesai Individu (Pulang Duluan)":
        if active_names:
            with st.form("form_keluar_individu"):
                nama_out = st.selectbox("Siapa yang mau pulang duluan?", active_names)
                pin_out = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Hitung Poin Individu"):
                    if pin_out != current_pin: st.error("❌ PIN Salah!")
                    else:
                        try:
                            now_dt = datetime.now(tz)
                            now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                            for idx, row in df_att.iterrows():
                                if row["Nama"] == nama_out and (pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == ""):
                                    masuk_dt = parse_time_safe(row["Jam Masuk"])
                                    masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.at[idx, "Jam Keluar"] = now_str
                                    df_att.at[idx, "Poin"] = round(durasi, 1)
                            conn.update(worksheet="Absensi", data=df_att)
                            st.snow()
                            time.sleep(1)
                            st.rerun()
                        except: st.error("Gagal ngitung, klik lagi.")
        else: st.warning("Tidak ada member yang sedang live.")
        
    elif mode == "Tutup Studio (Selesai Semua)":
        if active_names:
            with st.form("form_keluar_semua"):
                st.warning("⚠️ Ini akan mengakhiri waktu untuk SEMUA member yang aktif.")
                pin_all = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Akhiri Semua & Hitung Poin"):
                    if pin_all != current_pin: st.error("❌ PIN Salah!")
                    else:
                        try:
                            now_dt = datetime.now(tz)
                            now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                            for idx, row in df_att.iterrows():
                                if pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == "":
                                    masuk_dt = parse_time_safe(row["Jam Masuk"])
                                    masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.at[idx, "Jam Keluar"] = now_str
                                    df_att.at[idx, "Poin"] = round(durasi, 1)
                            conn.update(worksheet="Absensi", data=df_att)
                            st.snow()
                            time.sleep(1)
                            st.rerun()
                        except: st.error("Gagal nutup studio, klik lagi.")
        else: st.warning("Studio sudah kosong.")

# --- STATISTIK & KALKULASI GAJI ---
st.divider()
st.subheader("📊 3. Statistik & Leaderboard")

if "Poin" in df_att.columns:
    df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
    total_points = df_att["Poin"].sum()
    points_map = df_att.groupby("Nama")["Poin"].sum().to_dict()
else:
    total_points = 0
    points_map = {}

for m in MEMBERS: 
    if m not in points_map: points_map[m] = 0.0

active_members_count = sum(1 for m in MEMBERS if points_map[m] > 0)

# Cari MVP
mvp_name = max(points_map, key=points_map.get) if points_map else MEMBERS[0]
mvp_points = points_map.get(mvp_name, 0)

c1, c2 = st.columns([1, 2])
with c1:
    st.markdown(f"### 👑 MVP Tim\n**{mvp_name}**\n*( {mvp_points} Jam Live )*\n\n🔥 Gacor parah!")

with c2:
    chart_data = pd.DataFrame(list(points_map.items()), columns=["Anggota", "Total Jam"]).set_index("Anggota")
    st.bar_chart(chart_data, color="#819264")

st.divider()

st.subheader("💼 4. Hasil Bagi Hasil Mingguan")
kas_studio = total_income * 0.30
kas_ops = total_income * 0.20
team_share = total_income * 0.50

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Pemasukan", f"Rp {total_income:,.0f}")
m2.metric("🏢 Kas Studio", f"Rp {kas_studio:,.0f}")
m3.metric("☕ Ops/Makan", f"Rp {kas_ops:,.0f}")
m4.metric("👥 Jatah Tim", f"Rp {team_share:,.0f}")

base_pool = team_share * 0.40
live_pool = team_share * 0.60
base_per_person = (base_pool / active_members_count) if active_members_count > 0 else 0
val_per_point = (live_pool / total_points) if total_points > 0 else 0

result_data = []
for m in MEMBERS:
    pts = points_map[m]
    earned_base = base_per_person if pts > 0 else 0
    earned_bonus = pts * val_per_point
    is_mvp = " 👑" if m == mvp_name and pts > 0 else ""
    result_data.append({
        "Anggota": f"{m}{is_mvp}",
        "Poin Jam": f"{pts} Jam",
        "Upah Dasar": f"Rp {earned_base:,.0f}",
        "Bonus Jam": f"Rp {earned_bonus:,.0f}",
        "TOTAL CAIR": f"Rp {(earned_base + earned_bonus):,.0f}"
    })
st.table(pd.DataFrame(result_data))

# --- SLIP GAJI ---
st.divider()
st.subheader("🖨️ Generator Slip Gaji Digital")
slip_name = st.selectbox("Cetak Struk Atas Nama:", MEMBERS)

pts_slip = points_map.get(slip_name, 0)
base_slip = base_per_person if pts_slip > 0 else 0
bonus_slip = pts_slip * val_per_point
total_slip = base_slip + bonus_slip

html_slip = f"""
<div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; border: 2px dashed #819264; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 32px rgba(129, 146, 100, 0.15);">
<h4 style="text-align: center; margin: 0 0 5px 0; color: #2c3322;">🧾 SLIP GAJI PROJECT 4/4</h4>
<p style="text-align: center; font-size: 12px; color: #6a7a52; border-bottom: 1px solid #819264; padding-bottom: 10px; margin-bottom: 15px;">Dicetak: {datetime.now(tz).strftime('%d %b %Y %H:%M')}</p>
<div style="display: flex; justify-content: space-between; margin-bottom: 5px;"><span style="font-weight: 500; color: #2c3322;">Nama:</span><span style="font-weight: 700; color: #2c3322;">{slip_name}</span></div>
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><span style="font-weight: 500; color: #2c3322;">Jam Live:</span><span style="font-weight: 700; color: #2c3322;">{pts_slip} Jam</span></div>
<div style="border-bottom: 1px dashed #819264; margin-bottom: 15px;"></div>
<div style="display: flex; justify-content: space-between; margin-bottom: 5px;"><span style="font-weight: 500; color: #2c3322;">Upah Dasar:</span><span style="color: #2c3322;">Rp {base_slip:,.0f}</span></div>
<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><span style="font-weight: 500; color: #2c3322;">Bonus (Poin):</span><span style="color: #2c3322;">Rp {bonus_slip:,.0f}</span></div>
<div style="background: rgba(129, 146, 100, 0.15); padding: 15px; border-radius: 8px;"><h3 style="text-align: center; margin: 0; color: #2c3322; font-weight: 700;">TOTAL CAIR</h3><h3 style="text-align: center; margin: 0; color: #2c3322; font-weight: 700;">Rp {total_slip:,.0f}</h3></div>
</div>
"""
st.markdown(html_slip, unsafe_allow_html=True)

# --- PANEL ADMIN ---
st.divider()
st.subheader("⚙️ Panel Admin")
with st.expander("Klik untuk Ganti PIN Harian"):
    with st.form("form_ganti_pin"):
        new_pin_input = st.text_input("PIN Baru", placeholder="Misal: 9999")
        master_pass_input = st.text_input("Password Master", type="password")
        if st.form_submit_button("Update PIN Database"):
            if master_pass_input == "ALE1508": 
                try:
                    if "Parameter" in df_setting.columns:
                        idx = df_setting.index[df_setting["Parameter"] == "PIN_STUDIO"].tolist()
                        if idx: df_setting.at[idx[0], "Value"] = new_pin_input
                        else: df_setting = pd.concat([df_setting, pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])], ignore_index=True)
                    else:
                        df_setting = pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])
                    conn.update(worksheet="Pengaturan", data=df_setting)
                    st.success(f"✅ PIN Studio diubah jadi {new_pin_input}!")
                    time.sleep(1)
                    st.rerun()
                except: st.error("Gagal nyimpen, Google sibuk. Coba bentar lagi.")
            else: st.error("❌ Password Master Salah!")
