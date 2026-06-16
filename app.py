import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION - SBY & YGY", layout="wide", page_icon="🔴")

# --- 2. STABLE REFRESH (5 Detik) ---
# Menggunakan key yang unik untuk mencegah interferensi saat halaman reload
st_autorefresh(interval=5000, key="ldp_tour_refresh_system")

# --- INISIALISASI SESSION STATE UNTUK TRACKING KUOTA ---
if "quota_history" not in st.session_state:
    st.session_state.quota_history = {}

# --- 3. PREMIUM UI STYLING ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }

/* Header & Badge */
.ldp-header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 20px; }
.ldp-title { font-weight: 800; font-size: 2.5rem; margin: 0; margin-bottom: 10px; }
.live-badge { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 12px; color: #10B981; background: rgba(16,185,129,0.1); padding: 5px 15px; border-radius: 30px; border: 1px solid rgba(16,185,129,0.2); }
.live-dot { height: 8px; width: 8px; background: #10B981; border-radius: 50%; animation: blink 2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.2); } }

/* Grid System */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; justify-content: center; }

/* Card Design */
.ldp-card { 
    background: rgba(128,128,128,0.05); 
    border-radius: 15px; 
    padding: 24px 15px; 
    border: 1px solid rgba(128,128,128,0.15); 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between; 
    text-align: center; 
    transition: 0.3s ease;
}
.ldp-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: rgba(128,128,128,0.3); }

/* Border Status */
.ldp-card.avail { border-bottom: 5px solid #10B981; }
.ldp-card.warn { border-bottom: 5px solid #FBBF24; animation: glow 2s infinite; }
.ldp-card.sold { border-bottom: 5px solid #EF4444; opacity: 0.7; filter: grayscale(30%); }

@keyframes glow { 0% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } 50% { box-shadow: 0 0 15px rgba(251,191,36,0.3); } 100% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } }

.c-jalur { font-size: 10px; opacity: 0.5; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; }
.c-member { font-weight: 700; font-size: 16px; line-height: 1.2; margin-bottom: 20px; height: 2.5em; overflow: hidden; }

.c-badge { font-size: 10px; font-weight: 800; padding: 7px; border-radius: 20px; text-transform: uppercase; width: 100%; display: block; }
.ldp-card.avail .c-badge { background: rgba(16,185,129,0.15); color: #10B981; }
.ldp-card.warn .c-badge { background: rgba(251,191,36,0.2); color: #D97706; }
.ldp-card.sold .c-badge { background: #EF4444; color: #fff; }

/* Mobile optimization */
@media (max-width: 500px) { 
    .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; } 
    .ldp-card { padding: 18px 10px; }
    .c-member { font-size: 14px; }
}
</style>
"""
st.markdown(css.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

# --- 4. RENDER HEADER ---
st.markdown('<div class="ldp-header"><h1 class="ldp-title">LDP Tour: Surabaya & Yogyakarta</h1><div class="live-badge"><span class="live-dot"></span> MONITORING LIVE</div></div>', unsafe_allow_html=True)

# --- 5. DATA ENGINE ---
@st.cache_data(ttl=4)
def fetch_data(url):
    if not url:
        return None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def draw_section(url, key_prefix, ev_type):
    if not url:
        st.info("Menunggu API JKT48 dibuka / Data belum tersedia untuk sesi ini.")
        return

    # Menambahkan key_prefix pada text_input agar state pencarian antar kota/tab tidak bentrok
    s_key = f"input_{key_prefix}"
    st.text_input("Cari Oshi...", key=s_key, placeholder="Ketik nama member...")
    query = st.session_state.get(s_key, "").lower().strip()
    
    data = fetch_data(url)
    if not data:
        st.info("Menunggu data terbaru dari server JKT48...")
        return

    for sesi in data.get('data', []):
        members = sesi.get('session_members', [])
        if query:
            members = [m for m in members if query in m.get('member_name', '').lower()]
        
        if not members: 
            continue

        st.markdown(f"#### {sesi['label']} <small style='opacity:0.5'>| {sesi['start_time'][:5]}-{sesi['end_time'][:5]}</small>", unsafe_allow_html=True)
        
        html = '<div class="cards-grid">'
        for m in members:
            current_quota = m.get('quota', 0)
            limit = 5 if ev_type == "2shot" else 20
            
            # --- CEK RESTOCK TIKET ---
            ticket_key = f"{ev_type}_{sesi['label']}_{m['member_name']}_{m['label']}"
            
            if ticket_key in st.session_state.quota_history:
                prev_quota = st.session_state.quota_history[ticket_key]
                if current_quota > prev_quota:
                    st.toast(f"RESTOCK: {m['member_name']} ({m['label']}) - Sesi {sesi['label']} (Kuota: {current_quota})", icon="🚨")
                    
            # Simpan kuota ke session state
            st.session_state.quota_history[ticket_key] = current_quota
            
            # Pengkondisian Badge Status Berdasarkan Sisa Kuota
            if current_quota <= 0: 
                cls, lbl = "sold", "HABIS"
            elif current_quota < limit: 
                cls, lbl = "warn", f"SISA {current_quota}"
            else: 
                cls, lbl = "avail", f"SISA {current_quota}"
            
            html += f'<div class="ldp-card {cls}"><div class="c-jalur">{m["label"]}</div><div class="c-member">{m["member_name"]}</div><div class="c-badge">{lbl}</div></div>'
        
        st.markdown(html + '</div>', unsafe_allow_html=True)
        st.write("")

# --- 6. LAYOUT LOKASI & TABS ---
# Radio button untuk memilih filter kota utama
kota = st.radio("📍 Pilih Lokasi Event:", ["Surabaya", "Yogyakarta"], horizontal=True)
st.write("") 

t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

# --- CONTROLLER JALUR API ---
# Mengelompokkan URL API berdasarkan pilihan kota dan tipe tiket
if kota == "Surabaya":
    api_2shot_ld = "https://jkt48.com/api/v1/exclusives/EX3773/bonus?lang=id"
    api_2shot_p  = "" # Sesuai request, kosongkan dulu jika belum ada API
    api_mng_ld   = "https://jkt48.com/api/v1/exclusives/EX9A4A/bonus?lang=id"
    api_mng_p    = "" # Sesuai request, kosongkan dulu jika belum ada API
else: # Yogyakarta
    api_2shot_ld = "" # Sesuai request, kosongkan dulu jika belum ada API
    api_2shot_p  = "https://jkt48.com/api/v1/exclusives/EXCD2C/bonus?lang=id"
    api_mng_ld   = "" # Sesuai request, kosongkan dulu jika belum ada API
    api_mng_p    = "https://jkt48.com/api/v1/exclusives/EXCB75/bonus?lang=id"

# --- TAB 1: INTERFACE 2-SHOT ---
with t1:
    if kota == "Surabaya":
        st.markdown("### 💙 Team Love & 💛 Team Dream (Surabaya)")
        draw_section(api_2shot_ld, "2s_sby_ld", "2shot")
        
        st.markdown("---")
        st.markdown("### ❤️ Team Passion (Surabaya)")
        draw_section(api_2shot_p, "2s_sby_p", "2shot")
        
    elif kota == "Yogyakarta":
        st.markdown("### ❤️ Team Passion (Yogyakarta)")
        draw_section(api_2shot_p, "2s_ygy_p", "2shot")
        
        st.markdown("---")
        st.markdown("### 💙 Team Love & 💛 Team Dream (Yogyakarta)")
        draw_section(api_2shot_ld, "2s_ygy_ld", "2shot")

# --- TAB 2: INTERFACE MEET & GREET ---
with t2:
    if kota == "Surabaya":
        st.markdown("### 💙 Team Love & 💛 Team Dream (Surabaya)")
        draw_section(api_mng_ld, "mng_sby_ld", "mng")
        
        st.markdown("---")
        st.markdown("### ❤️ Team Passion (Surabaya)")
        draw_section(api_mng_p, "mng_sby_p", "mng")
        
    elif kota == "Yogyakarta":
        st.markdown("### ❤️ Team Passion (Yogyakarta)")
        draw_section(api_mng_p, "mng_ygy_p", "mng")
        
        st.markdown("---")
        st.markdown("### 💙 Team Love & 💛 Team Dream (Yogyakarta)")
        draw_section(api_mng_ld, "mng_ygy_ld", "mng")