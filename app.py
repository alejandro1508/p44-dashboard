import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz
import time
import random

tz = pytz.timezone('Asia/Jakarta')
now_time = datetime.now(tz)

st.set_page_config(page_title="Dashboard Project 4/4", page_icon="logo.png", layout="wide")

# --- FITUR STUDIO MODE (DARK THEME TOGGLE) ---
col_mode1, col_mode2 = st.columns([8, 2])
with col_mode2:
    dark_mode = st.toggle("🌙 Studio Mode", value=False)

# --- CSS GOD TIER + DYNAMIC THEME ---
if dark_mode:
    bg_color = "#121212"; text_color = "#E0E0E0"; card_bg = "rgba(30, 30, 30, 0.7)"
    border_color = "rgba(212, 175, 55, 0.4)"; table_bg = "#1E1E1E"; table_hover = "#2C2C2C"
    title_color = "#D4AF37"; sec_text = "#A3B18A"; btn_bg = "#D4AF37"; btn_hover = "#B8960B"
else:
    bg_color = "#EAE3CD"; text_color = "#2c3322"; card_bg = "rgba(255, 255, 255, 0.45)"
    border_color = "rgba(255, 255, 255, 0.4)"; table_bg = "rgba(255, 255, 255, 0.8)"; table_hover = "rgba(129, 146, 100, 0.1)"
    title_color = "#2c3322"; sec_text = "#6a7a52"; btn_bg = "#819264"; btn_hover = "#6a7a52"

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  {{ font-family: 'Poppins', sans-serif !important; color: {text_color} !important; }}
        .block-container {{ padding-left: 15px !important; padding-right: 15px !important; max-width: 100% !important; overflow-x: hidden !important; }}
        
        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color};
            background-image: radial-gradient(rgba(129, 146, 100, 0.2) 2px, transparent 2px);
            background-size: 30px 30px;
            transition: background-color 0.5s ease;
        }}
        
        h1, h2, h3, h4, p, span {{ color: {text_color} !important; transition: color 0.5s ease; }}
        
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .main {{ animation: fadeInUp 0.8s ease-out; }}
        @keyframes blinker {{ 50% {{ opacity: 0.3; }} }}
        
        .on-air-badge {{ background-color: #ff4b4b; color: white !important; padding: 8px 20px; border-radius: 50px; font-weight: 700; font-size: 16px; animation: blinker 1.2s linear infinite; display: inline-block; margin-bottom: 15px; box-shadow: 0 0 15px rgba(255, 75, 75, 0.5); }}
        .offline-badge {{ background-color: #6c757d; color: white !important; padding: 8px 20px; border-radius: 50px; font-weight: 700; font-size: 16px; display: inline-block; margin-bottom: 15px; }}
        
        [data-testid="stForm"], [data-testid="stMetric"] {{
            background: {card_bg} !important; backdrop-filter: blur(10px) !important;
            border-radius: 15px !important; border: 1px solid {border_color} !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15) !important;
            padding: 20px !important; transition: all 0.3s ease-in-out !important; width: 100% !important; box-sizing: border-box !important;
        }}
        [data-testid="stForm"]:hover, [data-testid="stMetric"]:hover {{ transform: translateY(-5px); }}
        
        .stButton > button {{
            background-color: {btn_bg} !important; color: #ffffff !important;
            border-radius: 10px !important; border: none !important;
            font-weight: 600 !important; transition: all 0.3s ease-in-out !important; width: 100%;
        }}
        .stButton > button:hover {{ transform: translateY(-3px) scale(1.02) !important; background-color: {btn_hover} !important; }}
        
        @keyframes pulseGlow {{ 0% {{ text-shadow: 0 0 5px {title_color}; }} 50% {{ text-shadow: 0 0 20px {title_color}; }} 100% {{ text-shadow: 0 0 5px {title_color}; }} }}
        h3.glow-title {{ animation: pulseGlow 3s infinite alternate !important; color: {title_color} !important; text-align: center; font-weight: 700; margin-bottom: 5px; }}
        
        .table-responsive-wrapper {{ width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.05); margin: 25px 0; background-color: transparent; }}
        .premium-table {{ width: 100%; min-width: 500px; border-collapse: collapse; font-size: 14px; text-align: left; background-color: {table_bg}; color: {text_color}; }}
        .premium-table thead tr {{ background-color: {btn_bg}; color: #ffffff; text-align: left; font-weight: bold; }}
        .premium-table th, .premium-table td {{ padding: 12px 15px; border-bottom: 1px solid {border_color}; color: {text_color}; }}
        .premium-table tbody tr {{ transition: all 0.2s ease-in; }}
        .premium-table tbody tr:hover {{ background-color: {table_hover}; }}
        .col-cair {{ font-weight: 700; }}
        
        /* Rank Colors */
        .rank-mythic {{ color: #FF00FF; font-weight: 900; text-shadow: 0 0 5px rgba(255,0,255,0.5); }}
        .rank-legend {{ color: #FFD700; font-weight: 800; }}
        .rank-epic {{ color: #00FF00; font-weight: 700; }}
    </style>
""", unsafe_allow_html=True)

hour = now_time.hour
greeting = "Pagi" if 5 <= hour < 11 else "Siang" if 11 <= hour < 15 else "Sore" if 15 <= hour < 18 else "Malam"

col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2: st.image("logo.png", use_container_width=True)
st.markdown("<h3 class='glow-title'>DASHBOARD REVENUE & ABSENSI</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sec_text}; font-weight: 600; margin-bottom: 15px;'>Selamat {greeting}, Warga 4/4! ☕ | {now_time.strftime('%d %B %Y')}</p>", unsafe_allow_html=True)
st.markdown(f"<marquee scrollamount='7' style='background-color: {btn_bg}; color: white; padding: 10px; border-radius: 8px; font-weight: 600; font-size: 14px; margin-bottom: 25px;'>🔥 INFO PROJECT 4/4: JANGAN LUPA BERSIHIN STUDIO -- PASTIKAN ABSEN KELUAR PAS SELESAI LIVE -- GAS TARGET MINGGU INI! 🔥</marquee>", unsafe_allow_html=True)

MEMBERS = ["Ale", "Adli", "Rian", "Vino", "Owbet"]
TAMU_VIP = ["Fauzi", "Hakim", "Rayhan", "Rusdi", "Naufal"]
TARGET_CUAN = 1500000
TARGET_POIN_VIP = 7

# --- SISTEM PANGKAT ---
def get_rank(hours):
    if hours >= 9: return "<span class='rank-mythic'>🐉 Mythical Glory</span>"
    elif hours >= 5: return "<span class='rank-legend'>🦁 Legend</span>"
    elif hours >= 1: return "<span class='rank-epic'>🦏 Epic</span>"
    elif hours > 0: return "🗡️ Elite"
    else: return "🗿 Warrior"

def get_safe_data(conn, sheet_name, cols):
    try: return conn.read(worksheet=sheet_name, usecols=cols, ttl=5).dropna(how="all")
    except Exception: return pd.DataFrame()

conn = st.connection("gsheets", type=GSheetsConnection)

df_income = get_safe_data(conn, "Pemasukan", [0, 1, 2])
df_att = get_safe_data(conn, "Absensi", [0, 1, 2, 3, 4])
df_setting = get_safe_data(conn, "Pengaturan", [0, 1])
df_expense = get_safe_data(conn, "Pengeluaran", [0, 1, 2, 3])
df_tamu = get_safe_data(conn, "Tamu", [0, 1, 2, 3])

if df_att.empty and not 'Tanggal' in df_att.columns: df_att = pd.DataFrame(columns=["Tanggal", "Nama", "Jam Masuk", "Jam Keluar", "Poin"])
else: df_att = df_att.astype(str).replace(['nan', 'NaN', '<NA>'], '')

if df_setting.empty and not 'Parameter' in df_setting.columns: df_setting = pd.DataFrame(columns=["Parameter", "Value"])
else: df_setting = df_setting.astype(str).replace(['nan', 'NaN', '<NA>'], '')

if df_tamu.empty and not 'Aksi' in df_tamu.columns: df_tamu = pd.DataFrame(columns=["Tanggal", "Nama", "Aksi", "Reward"])
else: df_tamu = df_tamu.astype(str).replace(['nan', 'NaN', '<NA>'], '')

if df_income.empty and not 'Nominal' in df_income.columns: df_income = pd.DataFrame(columns=["Tanggal", "Keterangan", "Nominal"])
if df_expense.empty and not 'Nominal' in df_expense.columns: df_expense = pd.DataFrame(columns=["Tanggal", "Kategori", "Keterangan", "Nominal"])

# BACA SALDO ENDAPAN
saldo_kas_lalu = 0
saldo_ops_lalu = 0
if not df_setting.empty:
    kas_row = df_setting[df_setting["Parameter"] == "SALDO_KAS"]
    if not kas_row.empty: saldo_kas_lalu = float(kas_row.iloc[0]["Value"])
    ops_row = df_setting[df_setting["Parameter"] == "SALDO_OPS"]
    if not ops_row.empty: saldo_ops_lalu = float(ops_row.iloc[0]["Value"])

total_income = pd.to_numeric(df_income["Nominal"], errors='coerce').fillna(0).sum() if not df_income.empty else 0

if not df_expense.empty: df_expense["Nominal"] = pd.to_numeric(df_expense["Nominal"], errors='coerce').fillna(0)
total_out_kas = df_expense[df_expense["Kategori"] == "Kas Studio"]["Nominal"].sum() if not df_expense.empty else 0
total_out_ops = df_expense[df_expense["Kategori"] == "Ops/Makan"]["Nominal"].sum() if not df_expense.empty else 0
total_out_gaji = df_expense[df_expense["Kategori"] == "Gaji/Jatah Tim"]["Nominal"].sum() if not df_expense.empty else 0

pct = min((total_income / TARGET_CUAN) * 100, 100) if TARGET_CUAN > 0 else 0
is_gold = pct >= 100
bar_color = "linear-gradient(90deg, #FFD700, #F5A623)" if is_gold else f"linear-gradient(90deg, {btn_bg}, {btn_hover})"

st.markdown(f"""
<div style="padding: 20px; background: {card_bg}; backdrop-filter: blur(10px); border-radius: 15px; border: 1px solid {border_color}; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15); margin-bottom: 30px;">
    <h4 style="margin: 0 0 10px 0; text-align: center; color: {text_color};">🎯 TARGET MINGGUAN: Rp {TARGET_CUAN:,.0f}</h4>
    <div style="background-color: rgba(128,128,128,0.2); border-radius: 10px; width: 100%; height: 25px;">
        <div style="background: {bar_color}; width: {pct}%; height: 100%; border-radius: 10px; transition: width 1.5s ease-in-out;"></div>
    </div>
    <p style="text-align: center; margin: 10px 0 0 0; font-weight: 600; color: {text_color}; font-size: 16px;">Terkumpul: Rp {total_income:,.0f} ({pct:.1f}%)</p>
</div>
""", unsafe_allow_html=True)

current_pin = "2026"
if not df_setting.empty:
    pin_row = df_setting[df_setting["Parameter"] == "PIN_STUDIO"]
    if not pin_row.empty: current_pin = str(pin_row.iloc[0]["Value"]).replace('.0','').strip()

if "Jam Keluar" in df_att.columns:
    active_mask = (df_att["Jam Keluar"] == "") | (df_att["Jam Keluar"].isna()) | (df_att["Jam Keluar"] == "None")
    active_names = df_att[active_mask]["Nama"].tolist() if not df_att[active_mask].empty else []
else: active_names = []
inactive_names = [m for m in MEMBERS if m not in active_names]

def parse_time_safe(time_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%H:%M:%S", "%Y-%m-%d %H:%M"):
        try: return datetime.strptime(str(time_str), fmt)
        except: pass
    return datetime.now()

poin_tamu = {}
for t in TAMU_VIP:
    if not df_tamu.empty:
        jml_hadir = len(df_tamu[(df_tamu["Nama"] == t) & (df_tamu["Aksi"] == "Hadir")])
        jml_gacha = len(df_tamu[(df_tamu["Nama"] == t) & (df_tamu["Aksi"] == "Gacha")])
        poin_tamu[t] = jml_hadir - (jml_gacha * TARGET_POIN_VIP)
    else: poin_tamu[t] = 0

col1, col2 = st.columns(2)

with col1:
    tab1, tab2 = st.tabs(["💰 Pemasukan", "💸 Kas Keluar"])
    with tab1:
        with st.form("form_income"):
            desc = st.text_input("Sumber Uang (Live Saweria, dll)")
            amount = st.number_input("Nominal Masuk (Rp)", min_value=0, step=50000)
            if st.form_submit_button("Simpan Pemasukan"):
                success = False
                try:
                    new_row = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d %H:%M"), "Keterangan": desc, "Nominal": amount}])
                    conn.update(worksheet="Pemasukan", data=pd.concat([df_income, new_row], ignore_index=True))
                    success = True
                except Exception as e: st.error(f"Error: {e}")
                if success: st.cache_data.clear(); st.rerun()
        st.markdown(f"**📜 Histori Pemasukan**")
        if not df_income.empty: st.dataframe(df_income.tail(3).iloc[::-1], use_container_width=True, hide_index=True)

    with tab2:
        with st.form("form_expense"):
            cat_exp = st.selectbox("Ambil dari Dompet Mana?", ["Kas Studio", "Ops/Makan", "Gaji/Jatah Tim"])
            desc_exp = st.text_input("Keterangan (Misal: Bayar Gaji Rian)")
            amount_exp = st.number_input("Nominal Ditarik (Rp)", min_value=0, step=10000)
            if st.form_submit_button("Tarik Uang"):
                success = False
                try:
                    new_row = pd.DataFrame([{"Tanggal": datetime.now(tz).strftime("%Y-%m-%d %H:%M"), "Kategori": cat_exp, "Keterangan": desc_exp, "Nominal": amount_exp}])
                    conn.update(worksheet="Pengeluaran", data=pd.concat([df_expense, new_row], ignore_index=True))
                    success = True
                except Exception as e: st.error(f"Error: {e}")
                if success: st.cache_data.clear(); st.rerun()
        st.markdown(f"**📉 Histori Uang Keluar**")
        if not df_expense.empty: st.dataframe(df_expense.tail(3).iloc[::-1], use_container_width=True, hide_index=True)

with col2:
    st.subheader("⏱️ 2. Sistem Absen Tim Inti")
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
                        if success: st.cache_data.clear(); st.rerun()
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
                                if row["Nama"] == nama_out and (row["Jam Keluar"] == "" or pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == "None"):
                                    masuk_dt = parse_time_safe(row["Jam Masuk"]); masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.loc[idx, "Jam Keluar"] = now_str; df_att.loc[idx, "Poin"] = str(round(durasi, 1))
                            conn.update(worksheet="Absensi", data=df_att)
                            success = True
                        except Exception as e: st.error(f"Gagal ngitung: {e}")
                        if success: st.cache_data.clear(); st.snow(); time.sleep(0.5); st.rerun()
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
                                if row["Jam Keluar"] == "" or pd.isna(row["Jam Keluar"]) or row["Jam Keluar"] == "None":
                                    masuk_dt = parse_time_safe(row["Jam Masuk"]); masuk_dt = tz.localize(masuk_dt) if masuk_dt.tzinfo is None else masuk_dt
                                    durasi = max((now_dt - masuk_dt).total_seconds() / 3600.0, 0.01)
                                    df_att.loc[idx, "Jam Keluar"] = now_str; df_att.loc[idx, "Poin"] = str(round(durasi, 1))
                            conn.update(worksheet="Absensi", data=df_att)
                            success = True
                        except Exception as e: st.error(f"Gagal nutup: {e}")
                        if success: st.cache_data.clear(); st.snow(); time.sleep(0.5); st.rerun()
        else: st.warning("Studio sudah kosong.")

st.divider()
st.markdown("<h3 class='glow-title' style='margin-bottom:20px;'>🎟️ ARENA VIP WARGA (LOYALTY PROGRAM)</h3>", unsafe_allow_html=True)
if "gacha_prize" in st.session_state:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #FFD700, #F5A623); padding:40px 20px; border-radius:20px; text-align:center; color:#2c3322; animation: pulseGlow 2s infinite alternate; margin-bottom:20px; box-shadow: 0 10px 40px rgba(212, 175, 55, 0.4); border: 2px solid #fff;'>
        <h1 style='margin:0; font-size: 36px;'>🎉 SELAMAT BANG {st.session_state.gacha_winner}! 🎉</h1>
        <p style='font-size:18px; margin:10px 0; font-weight: 500;'>Rezeki anak nongkrong, lu berhak claim:</p>
        <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; display: inline-block;'>
            <h1 style='margin:0; font-weight:800; color:#fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-size: 42px;'>🚬 {st.session_state.gacha_prize}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Tutup Banner & Lanjut Nongkrong ☕", use_container_width=True):
        del st.session_state["gacha_prize"]; del st.session_state["gacha_winner"]; st.rerun()
else:
    st.markdown("<div style='background: rgba(255,255,255,0.1); padding:25px; border-radius:20px; border:2px solid #D4AF37; box-shadow: 0 8px 32px 0 rgba(212, 175, 55, 0.2);'>", unsafe_allow_html=True)
    vip_c1, vip_c2 = st.columns([1, 1])
    with vip_c1:
        tamu_dipilih = st.selectbox("Pilih Nama Warga VIP:", TAMU_VIP)
        poin_sekarang = poin_tamu.get(tamu_dipilih, 0)
        pct_tamu = min((poin_sekarang / TARGET_POIN_VIP) * 100, 100)
        warna_bar = "#FFD700" if poin_sekarang >= TARGET_POIN_VIP else btn_bg
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:15px; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px;">
            <p style="margin:0; font-weight:600; color:{text_color}; font-size: 16px;">Progress Kedatangan: {poin_sekarang} / {TARGET_POIN_VIP} Hari</p>
            <div style="background:rgba(255,255,255,0.1); border-radius:10px; height:20px; margin-top:10px;">
                <div style="background:{warna_bar}; width:{pct_tamu}%; height:100%; border-radius:10px; transition: width 0.5s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with vip_c2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        if st.button("Absen Nongkrong ☕", use_container_width=True):
            cek_hari_ini = now_time.strftime("%Y-%m-%d")
            if not df_tamu.empty and len(df_tamu[(df_tamu["Nama"] == tamu_dipilih) & (df_tamu["Aksi"] == "Hadir") & (df_tamu["Tanggal"].str.startswith(cek_hari_ini))]) > 0:
                st.warning("Udah absen hari ini, Bang! Besok balik lagi ya.")
            else:
                try:
                    new_row = pd.DataFrame([{"Tanggal": now_time.strftime("%Y-%m-%d %H:%M"), "Nama": tamu_dipilih, "Aksi": "Hadir", "Reward": "-"}])
                    conn.update(worksheet="Tamu", data=pd.concat([df_tamu, new_row], ignore_index=True))
                    st.cache_data.clear(); st.success(f"Mantap, {tamu_dipilih}! Poin berhasil masuk."); time.sleep(1); st.rerun()
                except: st.error("Gagal nyimpen data.")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if poin_sekarang >= TARGET_POIN_VIP:
            st.markdown("""<style>.btn-gacha > button { background: linear-gradient(45deg, #FFD700, #F5A623) !important; color: #2c3322 !important; border: 2px solid #2c3322 !important; font-size: 18px !important; animation: pulseGlow 1.5s infinite alternate; }</style>""", unsafe_allow_html=True)
            st.markdown("<div class='btn-gacha'>", unsafe_allow_html=True)
            if st.button("🎰 SPIN GACHA SEKARANG!", use_container_width=True):
                hadiah_normal = ["Aroma Mile", "Camel Intense Blue", "Camel Option Purple", "Evo Diplomat", "Twizz Purple", "Aroma Bold", "Win Click Berry"]
                hadiah_jackpot = ["Sampoerna Mild (Jackpot!)", "LA Purple (Jackpot!)", "Dunhill Fine Cut Mild (Jackpot!)"]
                dapet_hadiah = random.choices(hadiah_normal + hadiah_jackpot, weights=[12.8]*7 + [3.3]*3, k=1)[0]
                try:
                    new_row = pd.DataFrame([{"Tanggal": now_time.strftime("%Y-%m-%d %H:%M"), "Nama": tamu_dipilih, "Aksi": "Gacha", "Reward": dapet_hadiah}])
                    conn.update(worksheet="Tamu", data=pd.concat([df_tamu, new_row], ignore_index=True))
                    st.cache_data.clear(); st.session_state["gacha_winner"] = tamu_dipilih; st.session_state["gacha_prize"] = dapet_hadiah
                    st.balloons(); time.sleep(0.5); st.rerun()
                except: st.error("Sistem Gacha sibuk!")
            st.markdown("</div>", unsafe_allow_html=True)
        else: st.button("🎰 SPIN GACHA SEKARANG!", disabled=True, use_container_width=True, help="Penuhi dulu bar poinnya!")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.subheader("📊 3. Statistik & Keuangan Studio")

if "Poin" in df_att.columns: df_att["Poin"] = pd.to_numeric(df_att["Poin"], errors='coerce').fillna(0)
total_points = df_att["Poin"].sum() if "Poin" in df_att.columns else 0
points_map = df_att.groupby("Nama")["Poin"].sum().to_dict() if "Poin" in df_att.columns else {}
for m in MEMBERS: points_map.setdefault(m, 0.0)

active_members_count = sum(1 for m in MEMBERS if points_map[m] > 0)
mvp_name = max(points_map, key=points_map.get) if points_map else MEMBERS[0]
mvp_points = points_map.get(mvp_name, 0)

c1, c2 = st.columns([1, 2])
with c1: 
    st.markdown(f"### 👑 MVP Tim\n**{mvp_name}**\n*( {mvp_points:.1f} Jam Live )*\n\n🔥 Rank: {get_rank(mvp_points)}", unsafe_allow_html=True)
with c2: st.bar_chart(pd.DataFrame(list(points_map.items()), columns=["Anggota", "Total Jam"]).set_index("Anggota"), color=btn_bg)

st.divider()
st.subheader("💼 4. Brankas & Bagi Hasil Mingguan")
kas_studio_minggu_ini = total_income * 0.30; kas_ops_minggu_ini = total_income * 0.20; team_share = total_income * 0.50

sisa_kas_final = kas_studio_minggu_ini + saldo_kas_lalu - total_out_kas
sisa_ops_final = kas_ops_minggu_ini + saldo_ops_lalu - total_out_ops
sisa_gaji = team_share - total_out_gaji

# --- LOGIKA TAMPILAN METRIC DIPERBAIKI ---
# Kalau ada saldo endapan, tampilin di judul kotaknya, biar pengeluaran (minus) tetep nongol warna merah di bawahnya.
lbl_kas = f"🏢 Sisa Kas (+Endapan Rp {saldo_kas_lalu:,.0f})" if saldo_kas_lalu > 0 else "🏢 Sisa Kas Studio"
lbl_ops = f"☕ Sisa Ops (+Endapan Rp {saldo_ops_lalu:,.0f})" if saldo_ops_lalu > 0 else "☕ Sisa Ops/Makan"

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Pemasukan (Minggu Ini)", f"Rp {total_income:,.0f}")
m2.metric(lbl_kas, f"Rp {sisa_kas_final:,.0f}", f"-Rp {total_out_kas:,.0f}" if total_out_kas > 0 else "")
m3.metric(lbl_ops, f"Rp {sisa_ops_final:,.0f}", f"-Rp {total_out_ops:,.0f}" if total_out_ops > 0 else "")
m4.metric("👥 Sisa Jatah Tim", f"Rp {sisa_gaji:,.0f}", f"-Rp {total_out_gaji:,.0f}" if total_out_gaji > 0 else "")

base_pool = team_share * 0.40; live_pool = team_share * 0.60
base_per_person = (base_pool / active_members_count) if active_members_count > 0 else 0
val_per_point = (live_pool / total_points) if total_points > 0 else 0

table_html = f"<div class='table-responsive-wrapper'><table class='premium-table'><thead><tr><th>Anggota</th><th>Pangkat (Rank)</th><th>Poin Jam</th><th>Upah Dasar</th><th>Bonus Jam</th><th>TOTAL HAK CAIR</th></tr></thead><tbody>"
for m in MEMBERS:
    pts = points_map[m]
    earned_base = base_per_person if pts > 0 else 0
    earned_bonus = pts * val_per_point
    is_mvp = " 👑" if m == mvp_name and pts > 0 else ""
    table_html += f"<tr><td><strong>{m}{is_mvp}</strong></td><td>{get_rank(pts)}</td><td>{pts:.1f} Jam</td><td>Rp {earned_base:,.0f}</td><td>Rp {earned_bonus:,.0f}</td><td class='col-cair'>Rp {(earned_base + earned_bonus):,.0f}</td></tr>"
table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

st.divider()
st.subheader("🖨️ Generator Slip Gaji Digital")
slip_name = st.selectbox("Cetak Struk Atas Nama:", MEMBERS)
pts_slip = points_map.get(slip_name, 0)
base_slip = base_per_person if pts_slip > 0 else 0
bonus_slip = pts_slip * val_per_point
html_slip = f"<div style='background: {card_bg}; backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; border: 2px dashed {btn_bg}; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);'><h4 style='text-align: center; margin: 0 0 5px 0; color: {text_color};'>🧾 SLIP GAJI PROJECT 4/4</h4><p style='text-align: center; font-size: 12px; color: {sec_text}; border-bottom: 1px solid {btn_bg}; padding-bottom: 10px; margin-bottom: 15px;'>Dicetak: {datetime.now(tz).strftime('%d %b %Y %H:%M')}</p><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: 500; color: {text_color};'>Nama:</span><span style='font-weight: 700; color: {text_color};'>{slip_name}</span></div><div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: 500; color: {text_color};'>Jam Live:</span><span style='font-weight: 700; color: {text_color};'>{pts_slip:.1f} Jam</span></div><div style='border-bottom: 1px dashed {btn_bg}; margin-bottom: 15px;'></div><div style='display: flex; justify-content: space-between; margin-bottom: 5px;'><span style='font-weight: 500; color: {text_color};'>Upah Dasar:</span><span style='color: {text_color};'>Rp {base_slip:,.0f}</span></div><div style='display: flex; justify-content: space-between; margin-bottom: 15px;'><span style='font-weight: 500; color: {text_color};'>Bonus (Poin):</span><span style='color: {text_color};'>Rp {bonus_slip:,.0f}</span></div><div style='background: rgba(129, 146, 100, 0.15); padding: 15px; border-radius: 8px;'><h3 style='text-align: center; margin: 0; color: {text_color}; font-weight: 700;'>TOTAL HAK CAIR</h3><h3 style='text-align: center; margin: 0; color: {text_color}; font-weight: 700;'>Rp {(base_slip + bonus_slip):,.0f}</h3></div></div>"
st.markdown(html_slip, unsafe_allow_html=True)

st.divider()
st.subheader("⚙️ Panel Admin & Tutup Buku")
adm1, adm2 = st.columns(2)
with adm1:
    with st.expander("Ganti PIN Harian"):
        with st.form("form_ganti_pin"):
            new_pin_input = st.text_input("PIN Baru", placeholder="Misal: 9999")
            master_pass_input = st.text_input("Password Master", type="password")
            if st.form_submit_button("Update PIN"):
                if master_pass_input == "ALE1508": 
                    try:
                        df_set = df_setting.copy()
                        idx = df_set.index[df_set["Parameter"] == "PIN_STUDIO"].tolist()
                        if idx: df_set.at[idx[0], "Value"] = new_pin_input
                        else: df_set = pd.concat([df_set, pd.DataFrame([{"Parameter": "PIN_STUDIO", "Value": new_pin_input}])], ignore_index=True)
                        conn.update(worksheet="Pengaturan", data=df_set); st.cache_data.clear(); st.success("PIN Diubah!"); time.sleep(1); st.rerun()
                    except: st.error("Gagal nyimpen.")
                else: st.error("❌ Password Master Salah!")

with adm2:
    with st.expander("🚨 TUTUP BUKU MINGGUAN (PAYROLL)"):
        st.warning("⚠️ AWAS! Ini akan ngereset semua data Pemasukan, Pengeluaran, dan Jam Absen jadi 0 buat minggu depan. Sisa Kas & Ops akan disimpan.")
        with st.form("form_tutup_buku"):
            pass_tutup = st.text_input("Password Master", type="password")
            if st.form_submit_button("LAKUKAN TUTUP BUKU!"):
                if pass_tutup == "ALE1508":
                    success = False
                    try:
                        df_set = df_setting.copy()
                        idx_kas = df_set.index[df_set["Parameter"] == "SALDO_KAS"].tolist()
                        if idx_kas: df_set.at[idx_kas[0], "Value"] = str(sisa_kas_final)
                        else: df_set = pd.concat([df_set, pd.DataFrame([{"Parameter": "SALDO_KAS", "Value": str(sisa_kas_final)}])], ignore_index=True)
                        
                        idx_ops = df_set.index[df_set["Parameter"] == "SALDO_OPS"].tolist()
                        if idx_ops: df_set.at[idx_ops[0], "Value"] = str(sisa_ops_final)
                        else: df_set = pd.concat([df_set, pd.DataFrame([{"Parameter": "SALDO_OPS", "Value": str(sisa_ops_final)}])], ignore_index=True)
                        
                        conn.update(worksheet="Pengaturan", data=df_set)
                        conn.update(worksheet="Pemasukan", data=df_income.iloc[0:0])
                        conn.update(worksheet="Pengeluaran", data=df_expense.iloc[0:0])
                        conn.update(worksheet="Absensi", data=df_att.iloc[0:0])
                        conn.update(worksheet="Tamu", data=df_tamu.iloc[0:0])
                        success = True
                    except Exception as e:
                        st.error(f"Gagal nutup buku. Error sistem: {e}")
                    
                    if success:
                        st.cache_data.clear(); st.success("✅ TUTUP BUKU BERHASIL! Saldo udah disimpan, absen udah di-reset. Siap tempur minggu depan!"); time.sleep(2); st.rerun()
                else:
                    st.error("❌ Password Master Salah!")
