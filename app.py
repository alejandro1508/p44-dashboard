import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# Zona waktu Indonesia (WIB)
tz = pytz.timezone('Asia/Jakarta')

# Konfigurasi Halaman & Font Poppins
st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")
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
        
        /* Efek Tombol Interaktif (Ngangkat pas disentuh) */
        .stButton > button {
            transition: all 0.3s ease-in-out !important;
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0px 8px 15px rgba(129, 146, 100, 0.4) !important;
        }

        /* Efek Teks Glowing (Lampu Neon) untuk Judul */
        @keyframes pulseGlow {
            0% { text-shadow: 0 0 5px rgba(129,146,100,0.2); }
            50% { text-shadow: 0 0 20px rgba(129,146,100,0.8), 0 0 30px rgba(129,146,100,0.6); }
            100% { text-shadow: 0 0 5px rgba(129,146,100,0.2); }
        }
        h3 {
            animation: pulseGlow 3s infinite alternate !important;
        }
    </style>
""", unsafe_allow_html=True)

# Logo
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.image("logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; font-weight: 700; margin-bottom: 20px;'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)
st.divider()

# DAFTAR NAMA ANGGOTA PROJECT 4/4
MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]

# Koneksi ke Google Sheets (ttl=0 biar data selalu real-time)
conn = st.connection("gsheets", type=GSheetsConnection)
df_income = conn.read(worksheet="Pemasukan", usecols=[0, 1, 2], ttl=0).dropna(how="all")
df_att = conn.read(worksheet="Absensi", usecols=[0, 1, 2, 3, 4], ttl=0).dropna(how="all")

# Baca sheet Pengaturan buat PIN
try:
    df_setting = conn.read(worksheet="Pengaturan", usecols=[0, 1], ttl=0).dropna(how="all")
except:
    st.error("⚠️ Sheet 'Pengaturan' belum dibuat di Google Sheets! Tolong buat dulu sesuai instruksi.")
    st.stop()

if df_att.empty:
    df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])

# Ambil PIN harian dari database
current_pin = "2026" # Default fallback PIN
if not df_setting.empty and "Parameter" in df_setting.columns:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty:
        raw_pin = str(pin_row.iloc[0]["Value"])
        # Antisipasi kalau Google Sheets ngebaca angka jadi float (misal 2026.0)
        if raw_pin.endswith('.0'):
            current_pin = raw_pin[:-2]
        else:
            current_pin = raw_pin.strip()

# Deteksi siapa yang sedang live
active_mask = df_att["Jam Keluar"].isna() | (df_att["Jam Keluar"] == "")
df_active = df_att[active_mask]
active_names = df_active["Nama"].tolist() if not df_active.empty else []

col1, col2 = st.columns(2)

# --- 1. FORM PEMASUKAN & HISTORY ---
with col1:
    st.subheader("💰 1. Input Pemasukan")
    with st.form("form_income"):
        desc = st.text_input("Keterangan", placeholder="Misal: Live Saweria / Komisi TikTok")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=50000)
        submit_inc = st.form_submit_button("Simpan Pemasukan")
        
        if submit_inc and amount > 0:
            now = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
            new_income = pd.DataFrame([{"Tanggal": now, "Keterangan": desc, "Nominal": amount}])
            updated_income = pd.concat([df_income, new_income], ignore_index=True)
            conn.update(worksheet="Pemasukan", data=updated_income)
            st.balloons() 
            st.success("Cuan berhasil dicatat!")
            st.rerun()
            
    # Tabel History Pemasukan Terakhir
    st.markdown("**📜 5 Riwayat Pemasukan Terakhir**")
    if not df_income.empty:
        df_history = df_income.tail(5).iloc[::-1].copy()
        df_history["Nominal"] = pd.to_numeric(df_history["Nominal"], errors='coerce').fillna(0).apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.caption("Belum ada data pemasukan tercatat.")

# --- 2. FORM ABSENSI OTOMATIS (PAKAI PIN) ---
with col2:
    st.subheader("⏱️ 2. Absen Otomatis")
    
    if active_names:
        st.info(f"🔴 Sedang Live: **{', '.join(active_names)}**")
    else:
        st.info("⚪ Studio sedang kosong (Belum ada Live).")
        
    action = st.radio("Pilih Mode:", ["Absen Masuk", "Akhiri Live (Semua)"], horizontal=True)
    
    if action == "Absen Masuk":
        with st.form("form_masuk"):
            available_members = [m for m in MEMBERS if m not in active_names]
            if available_members:
                name_in = st.selectbox("Siapa yang mau absen?", available_members)
                pin_in = st.text_input("PIN Studio Hari Ini", type="password", placeholder="Lihat di Papan Tulis")
                submit_in = st.form_submit_button("Mulai Jam Live")
                
                if submit_in:
                    if pin_in != current_pin:
                        st.error("❌ PIN Salah! Cek lagi di papan tulis.")
                    else:
                        now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                        new_att = pd.DataFrame([{"Tanggal": now_str[:10], "Nama": name_in, "Jam Masuk": now_str, "Jam Keluar": "", "Poin": ""}])
                        updated_att = pd.concat([df_att, new_att], ignore_index=True)
                        conn.update(worksheet="Absensi", data=updated_att)
                        st.success(f"✅ {name_in} resmi masuk live!")
                        st.rerun()
            else:
                st.write("Semua tim sudah berada di dalam Live!")
                st.form_submit_button("Mulai Jam Live", disabled=True)
                
    else:
        with st.form("form_keluar"):
            st.warning("⚠️ Perhatian: Ini akan menghentikan waktu & menghitung poin otomatis untuk SEMUA orang yang sedang live.")
            pin_out = st.text_input("PIN Studio Hari Ini", type="password", placeholder="Wajib pakai PIN")
            submit_out = st.form_submit_button("Selesai & Hitung Poin!")
            
            if submit_out:
                if pin_out != current_pin:
                    st.error("❌ PIN Salah!")
                elif active_names:
                    now_dt = datetime.now(tz)
                    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                    
                    for idx, row in df_att.iterrows():
                        if pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == "":
                            try:
                                masuk_dt = datetime.strptime(str(row["Jam Masuk"]), "%Y-%m-%d %H:%M:%S")
                            except:
                                continue
                            masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                            
                            diff_hours = (now_dt - masuk_dt).total_seconds() / 3600.0
                            poin = round(diff_hours, 1) 
                            
                            df_att.at[idx, "Jam Keluar"] = now_str
                            df_att.at[idx, "Poin"] = poin
                            
                    conn.update(worksheet="Absensi", data=df_att)
                    st.snow() 
                    st.success("✅ Live selesai! Poin otomatis dihitung.")
                    st.rerun()
                else:
                    st.error("Tidak ada orang yang sedang live.")

st.divider()

# --- 3. STATISTIK & GRAFIK ---
st.subheader("📊 3. Statistik & Leaderboard")

df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
total_points = df_att["Poin"].sum()
points_map = df_att.groupby("Nama")["Poin"].sum().to_dict()

for m in MEMBERS:
    if m not in points_map:
        points_map[m] = 0.0

mvp_name = max(points_map, key=points_map.get) if points_map else MEMBERS[0]
mvp_points = points_map.get(mvp_name, 0)

c1, c2 = st.columns([1, 2])
with c1:
    st.markdown(f"### 👑 MVP Tim\n**{mvp_name}**\n*( {mvp_points} Jam Live )*\n\n🔥 Gacor parah!")

with c2:
    chart_data = pd.DataFrame(list(points_map.items()), columns=["Anggota", "Total Jam"]).set_index("Anggota")
    st.bar_chart(chart_data, color="#819264")

st.divider()

# --- 4. KALKULASI BAGI HASIL ---
st.subheader("💼 4. Hasil Bagi Hasil Mingguan")

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

kas_studio = total_income * 0.30
kas_ops = total_income * 0.20
team_share = total_income * 0.50

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Pemasukan", f"Rp {total_income:,.0f}")
m2.metric("🏢 Kas Studio (30%)", f"Rp {kas_studio:,.0f}")
m3.metric("☕ Ops/Makan (20%)", f"Rp {kas_ops:,.0f}")
m4.metric("👥 Jatah Tim (50%)", f"Rp {team_share:,.0f}")

base_pool = team_share * 0.40
base_per_person = (base_pool / len(MEMBERS)) if total_income > 0 else 0
live_pool = team_share * 0.60
val_per_point = (live_pool / total_points) if total_points > 0 else 0

result_data = []
for m in MEMBERS:
    pts = points_map[m]
    total_earned = base_per_person + (pts * val_per_point)
    is_mvp = " 👑" if m == mvp_name and pts > 0 else ""
    result_data.append({
        "Anggota": f"{m}{is_mvp}",
        "Poin Jam": f"{pts} Jam",
        "Tugas Dasar": f"Rp {base_per_person:,.0f}",
        "Uang Poin Live": f"Rp {pts * val_per_point:,.0f}",
        "TOTAL CAIR": f"Rp {total_earned:,.0f}"
    })

st.table(pd.DataFrame(result_data))

st.divider()

# --- 5. PANEL ADMIN ---
st.subheader("⚙️ Panel Admin")
with st.expander("Ganti PIN Studio Harian"):
    with st.form("form_ganti_pin"):
        new_pin_input = st.text_input("Masukkan PIN Studio Baru", placeholder="Contoh: 9999")
        master_pass_input = st.text_input("Password Master", type="password", placeholder="Masukkan Password Admin")
        submit_new_pin = st.form_submit_button("Update PIN")
        
        if submit_new_pin:
            if master_pass_input == "ALE1508": 
                if "Parameter" in df_setting.columns:
                    idx = df_setting.index[df_setting["Parameter"] == "PIN_STUDIO"].tolist()
                    if idx:
                        df_setting.at[idx[0], "Value"] = new_pin_input
                    else:
                        new_row = pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])
                        df_setting = pd.concat([df_setting, new_row], ignore_index=True)
                    
                    conn.update(worksheet="Pengaturan", data=df_setting)
                    st.success(f"✅ PIN Studio berhasil diubah jadi {new_pin_input}!")
                    st.rerun()
            else:
                st.error("❌ Password Master Salah!")
