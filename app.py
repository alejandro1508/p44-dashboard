import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz
import time

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')
now_time = datetime.now(tz)

st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- CSS GOD TIER + ANIMASI + RESPONSIVE MOBILE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"]  { font-family: 'Poppins', sans-serif !important; }
        .block-container { padding-left: 15px !important; padding-right: 15px !important; max-width: 100% !important; overflow-x: hidden !important;}
        
        [data-testid="stAppViewContainer"] {
            background-color: #EAE3CD;
            background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px);
            background-size: 30px 30px;
        }

        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        .main { animation: fadeInUp 0.8s ease-out; }

        @keyframes blinker { 50% { opacity: 0.3; } }
        .on-air-badge {
            background-color: #ff4b4b; color: white; padding: 8px 20px; 
            border-radius: 50px; font-weight: 700; font-size: 16px;
            animation: blinker 1.2s linear infinite; display: inline-block; margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.5);
        }
        .offline-badge {
            background-color: #6c757d; color: white; padding: 8px 20px; 
            border-radius: 50px; font-weight: 700; font-size: 16px; display: inline-block; margin-bottom: 15px;
        }

        [data-testid="stForm"], [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.45) !important; backdrop-filter: blur(10px) !important;
            border-radius: 15px !important; border: 1px solid rgba(255, 255, 255, 0.4) !important;
            box-shadow: 0 8px 32px 0 rgba(129, 146, 100, 0.15) !important;
            padding: 20px !important; transition: all 0.3s ease-in-out !important; width: 100% !important; box-sizing: border-box !important;
        }
        [data-testid="stForm"]:hover, [data-testid="stMetric"]:hover { transform: translateY(-5px); }
        
        .stButton > button {
            background-color: #819264 !important; color: white !important;
            border-radius: 10px !important; border: none !important;
            font-weight: 600 !important; transition: all 0.3s ease-in-out !important; width: 100%;
        }
        .stButton > button:hover { transform: translateY(-3px) scale(1.02) !important; background-color: #6a7a52 !important; }

        @keyframes pulseGlow { 0% { text-shadow: 0 0 5px rgba(129,146,100,0.2); } 50% { text-shadow: 0 0 20px rgba(129,146,100,0.8); } 100% { text-shadow: 0 0 5px rgba(129,146,100,0.2); } }
        h3.glow-title { animation: pulseGlow 3s infinite alternate !important; color: #2c3322 !important; text-align: center; font-weight: 700; margin-bottom: 5px; }

        .table-responsive-wrapper {
            width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 15px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05); margin: 25px 0; background-color: white;
        }
        .premium-table { width: 100%; min-width: 500px; border-collapse: collapse; font-size: 14px; text-align: left; }
        .premium-table thead tr { background-color: #819264; color: #ffffff; text-align: left; font-weight: bold; }
        .premium-table th, .premium-table td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; }
        .premium-table tbody tr { transition: all 0.2s ease-in; background-color: rgba(255, 255, 255, 0.8); }
        .premium-table tbody tr:hover { background-color: rgba(129, 146, 100, 0.1); }
        .premium-table tbody tr:last-of-type { border-bottom: 2px solid #819264; }
        .col-cair { font-weight: 700; color: #2c3322; }
    </style>
""", unsafe_allow_html=True)

hour = now_time.hour
if 5 <= hour < 11: greeting = "Pagi"
elif 11 <= hour < 15: greeting = "Siang"
elif 15 <= hour < 18: greeting = "Sore"
else: greeting = "Malam"

col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2: st.image("logo.png", use_container_width=True)
st.markdown("<h3 class='glow-title'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #6a7a52; font-weight: 600; margin-bottom: 15px;'>Selamat {greeting}, Warga 4/4! ☕ | {now_time.strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

st.markdown("<marquee scrollamount='7' style='background-color: #819264; color: white; padding: 10px; border-radius: 8px; font-weight: 600; font-size: 14px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(129,146,100,0.3);'>🔥 INFO PROJECT 4/4: JANGAN LUPA BERSIHIN STUDIO SEBELUM BALIK -- PASTIKAN ABSEN KELUAR PAS SELESAI LIVE -- GAS TARGET MINGGU INI! 🔥</marquee>", unsafe_allow_html=True)

MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TARGET_CUAN = 1500000

def get_safe_data(conn, sheet_name, cols):
    try: return conn.read(worksheet=sheet_name, usecols=cols, ttl=5).dropna(how="all")
    except Exception: return pd.DataFrame()

conn = st.connection("gsheets", type=GSheetsConnection)

df_income = get_safe_data(conn, "Pemasukan", [0, 1, 2])
df_att = get_safe_data(conn, "Absensi", [0, 1, 2, 3, 4])
df_setting = get_safe_data(conn, "Pengaturan", [0, 1])

if df_att.empty and not 'Tanggal' in df_att.columns: df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])
if df_income.empty and not 'Nominal' in df_income.columns: df_income = pd.DataFrame(columns=["Tanggal", "Keterangan", "Nominal"])

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

pct = min((total_income / TARGET_CUAN) * 100, 100) if TARGET_CUAN > 0 else 0
is_gold = pct >= 100
bar_color = "linear-gradient(90deg, #FFD700, #F5A623)" if is_gold else "linear-gradient(90deg, #819264, #A3B18A)"

st.markdown(f"""
<div style="padding: 20px; background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.4); box-shadow: 0 8px 32px 0 rgba(129, 146, 100, 0.15); margin-bottom: 30px;">
    <h4 style="margin: 0 0 10px 0; text-align: center; color: #2c3322;">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background-color: rgba(0,0,0,0.1); border-radius: 10px; width: 100%; height: 25px;">
        <div style="background: {bar_color}; width: {pct}%; height: 100%; border-radius: 10px; transition: width 1.5s ease-in-out;"></div>
    </div>
    <p style="text-align: center; margin: 10px 0 0 0; font-weight: 600; color: #2c3322; font-size: 16px;">Terkumpul: Rp {total_income:,.0f} ({pct:.1f}%)</p>
</div>
""", unsafe_allow_html=True)

current_pin = "2026"
if not df_setting.empty and "Parameter" in df_setting.columns:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty: current_pin = str(pin_row.iloc[0]["Value"]).replace('.0','').strip()

if "Jam Keluar" in df_att.columns:
    active_mask = df_att["Jam Keluar"].isna() | (df_att["Jam Keluar"] == "")
    active_names = df_att[active_mask]["Nama"].tolist() if not df_att[active_mask].empty else []
else: active_names = []
inactive_names = [m for m in MEMBERS if m not in active_names]

def parse_time_safe(time_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%H:%M:%S", "%Y-%m-%d %H:%M"):
        try: return datetime.strptime(str(time_str), fmt)
        except: pass
    return datetime.now()

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan", placeholder="Misal: Live Saweria")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        if st.form_submit_button("Simpan Pemasukan"):
            success = False
            try:
                new_row = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d %H:%M"), "Keterangan": desc, "Nominal": amount}])
                conn.update(worksheet="Pemasukan", data=pd.concat([df_income, new_row], ignore_index=True))
                success = True
            except Exception as e: st.error(f"Gagal simpan! Error sistem: {e}")
            if success:
                st.cache_data.clear()
                st.rerun()
                    
    st.markdown("**📜 Riwayat Pemasukan**")
    if not df_income.empty and len(df_income) > 0:
        st.markdown("<div style='overflow-x:auto;'>", unsafe_allow_html=True)
        st.dataframe(df_income.tail(5).iloc[::-1], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("⏱️ 2. Sistem Absen")
    if active_names: st.markdown(f"<div class='on-air-badge'>🔴 ON AIR : {', '.join(active_names)}</div>", unsafe_allow_html=True)
    else: st.markdown("<div class='offline-badge'>⚪ STUDIO OFFLINE</div>", unsafe_allow_html=True)
    
    mode = st.radio("Pilih Aksi:", ["Masuk Live", "Selesai Individu (Pulang Duluan)", "Tutup Studio (Selesai Semua)"])
    
    if mode == "Masuk Live":
        if inactive_names:
            with st.form("form_masuk"):
                nama = st.selectbox("Siapa yang mau absen?", inactive_names)
                pin = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Masuk Live!"):
                    if pin != current_pin: st.error("❌ PIN Salah!")
                    else:
                        success = False
                        try:
                            now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                            new_att = pd.DataFrame([{"Tanggal": now_str[:10], "Nama": nama, "Jam Masuk": now_str, "Jam Keluar": "", "Poin": ""}])
                            conn.update(worksheet="Absensi", data=pd.concat([df_att, new_att], ignore_index=True))
                            success = True
                        except Exception as e: st.error(f"Gagal absen: {e}")
                        
                        if success:
                            st.cache_data.clear()
                            st.rerun()
        else: st.info("Semua member sudah di dalam Live!")

    elif mode == "Selesai Individu (Pulang Duluan)":
        if active_names:
            with st.form("form_keluar_individu"):
                nama_out = st.selectbox("Siapa yang mau pulang?", active_names)
                pin_out = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Hitung Poin Individu"):
                    if pin_out != current_pin: st.error("❌ PIN Salah!")
                    else:
                        success = False
                        try:
                            now_dt = datetime.now(tz); now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                            for idx, row in df_att.iterrows():
                                if row["Nama"] == nama_out and (pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == ""):
                                    masuk_dt = parse_time_safe(row["Jam Masuk"])
                                    masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.loc[idx, "Jam Keluar"] = now_str
                                    df_att.loc[idx, "Poin"] = round(durasi, 1)
                            conn.update(worksheet="Absensi", data=df_att)
                            success = True
                        except Exception as e: st.error(f"Gagal ngitung: {e}")
                        
                        if success:
                            st.cache_data.clear()
                            st.snow()
                            st.rerun()
        else: st.warning("Tidak ada member yang sedang live.")
        
    elif mode == "Tutup Studio (Selesai Semua)":
        if active_names:
            with st.form("form_keluar_semua"):
                st.warning("⚠️ Ini akan mengakhiri waktu untuk SEMUA member yang aktif.")
                pin_all = st.text_input("PIN Studio", type="password")
                if st.form_submit_button("Akhiri Semua & Hitung Poin"):
                    if pin_all != current_pin: st.error("❌ PIN Salah!")
                    else:
                        success = False
                        try:
                            now_dt = datetime.now(tz); now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                            for idx, row in df_att.iterrows():
                                if pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == "":
                                    masuk_dt = parse_time_safe(row["Jam Masuk"])
                                    masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.loc[idx, "Jam Keluar"] = now_str
                                    df_att.loc[idx, "Poin"] = round(durasi, 1)
                            conn.update(worksheet="Absensi", data=df_att)
                            success = True
                        except Exception as e: st.error(f"Gagal nutup: {e}")
                        
                        if success:
                            st.cache_data.clear()
                            st.snow()
                            st.rerun()
        else: st.warning("Studio sudah kosong.")

st.divider()
st.subheader("📊 3. Statistik & Leaderboard")

if "Poin" in df_att.columns: df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
total_points = df_att["Poin"].sum() if "Poin" in df_att.columns else 0
points_map = df_att.groupby("Nama")["Poin"].sum().to_dict() if "Poin" in df_att.columns else {}
for m in MEMBERS: points_map.setdefault(m, 0.0)

active_members_count = sum(1 for m in MEMBERS if points_map[m] > 0)
mvp_name = max(points_map, key=points_map.get) if points_map else MEMBERS[0]
mvp_points = points_map.get(mvp_name, 0)

c1, c2 = st.columns([1, 2])
with c1: st.markdown(f"### 👑 MVP Tim\n**{mvp_name}**\n*( {mvp_points} Jam Live )*\n\n🔥 Gacor parah!")
with c2: st.bar_chart(pd.DataFrame(list(points_map.items()), columns=["Anggota", "Total Jam"]).set_index("Anggota"), color="#819264")

st.divider()
st.subheader("💼 4. Hasil Bagi Hasil Mingguan")
kas_studio = total_income * 0.30; kas_ops = total_income * 0.20; team_share = total_income * 0.50

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Pemasukan", f"Rp {total_income:,.0f}"); m2.metric("🏢 Kas Studio", f"Rp {kas_studio:,.0f}")
m3.metric("☕ Ops/Makan", f"Rp {kas_ops:,.0f}"); m4.metric("👥 Jatah Tim", f"Rp {team_share:,.0f}")

base_pool = team_share * 0.40; live_pool = team_share * 0.60
base_per_person = (base_pool / active_members_count) if active_members_count > 0 else 0
val_per_point = (live_pool / total_points) if total_points > 0 else 0

table_html = "<div class='table-responsive-wrapper'><table class='premium-table'><thead><tr><th>Anggota</th><th>Poin Jam</th><th>Upah Dasar</th><th>Bonus Jam</th><th>TOTAL CAIR</th></tr></thead><tbody>"
for m in MEMBERS:
    pts = points_map[m]
    earned_base = base_per_person if pts > 0 else 0
    earned_bonus = pts * val_per_point
    is_mvp = " 👑" if m == mvp_name and pts > 0 else ""
    table_html += f"<tr><td><strong>{m}{is_mvp}</strong></td><td>{pts} Jam</td><td>Rp {earned_base:,.0f}</td><td>Rp {earned_bonus:,.0f}</td><td class='col-cair'>Rp {(earned_base + earned_bonus):,.0f}</td></tr>"
table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

st.divider()
st.subheader("🖨️ Generator Slip Gaji Digital")
slip_name = st.selectbox("Cetak Struk Atas Nama:", MEMBERS)
pts_slip = points_map.get(slip_name, 0)
base_slip = base_per_person if pts_slip > 0 else 0
bonus_slip = pts_slip * val_per_point
html_slip = f"<div style='background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; border: 2px dashed #819264; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 32px rgba(129, 146, 100, 0.15);'><h4 style='text-align: center; margin: 0 0 5px 0; color: #2c3322;'>🧾 SLIP GAJI PROJECT 4/4</h4><p style='text-align: center; font-size: 12px; color: #6a7a52; border-bottom: 1px solid #819264; padding-bottom: 10px; margin-bottom: 15px;'>Dicetak: {datetime.now(tz).strftime('%d %b %Y %H:%M')}</p><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: 500; color: #2c3322;'>Nama:</span><span style='font-weight: 700; color: #2c3322;'>{slip_name}</span></div><div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: 500; color: #2c3322;'>Jam Live:</span><span style='font-weight: 700; color: #2c3322;'>{pts_slip} Jam</span></div><div style='border-bottom: 1px dashed #819264; margin-bottom: 15px;'></div><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: 500; color: #2c3322;'>Upah Dasar:</span><span style='color: #2c3322;'>Rp {base_slip:,.0f}</span></div><div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: 500; color: #2c3322;'>Bonus (Poin):</span><span style='color: #2c3322;'>Rp {bonus_slip:,.0f}</span></div><div style='background: rgba(129, 146, 100, 0.15); padding: 15px; border-radius: 8px;'><h3 style='text-align: center; margin: 0; color: #2c3322; font-weight: 700;'>TOTAL CAIR</h3><h3 style='text-align: center; margin: 0; color: #2c3322; font-weight: 700;'>Rp {(base_slip + bonus_slip):,.0f}</h3></div></div>"
st.markdown(html_slip, unsafe_allow_html=True)

st.divider()
st.subheader("⚙️ Panel Admin")
with st.expander("Klik untuk Ganti PIN Harian"):
    with st.form("form_ganti_pin"):
        new_pin_input = st.text_input("PIN Baru", placeholder="Misal: 9999")
        master_pass_input = st.text_input("Password Master", type="password")
        if st.form_submit_button("Update PIN Database"):
            if master_pass_input == "ALE1508": 
                success = False
                try:
                    if "Parameter" in df_setting.columns:
                        idx = df_setting.index[df_setting["Parameter"] == "PIN_STUDIO"].tolist()
                        if idx: df_setting.at[idx[0], "Value"] = new_pin_input
                        else: df_setting = pd.concat([df_setting, pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])], ignore_index=True)
                    else: df_setting = pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])
                    conn.update(worksheet="Pengaturan", data=df_setting)
                    success = True
                except Exception as e: st.error(f"Gagal nyimpen: {e}")
                
                if success:
                    st.success(f"✅ PIN Studio diubah jadi {new_pin_input}!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
            else: st.error("❌ Password Master Salah!")
