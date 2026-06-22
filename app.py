import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="THEATER LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# --- 2. STABLE REFRESH (5 Detik) ---
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
.ldp-title { font-weight: 800; font-size: 2.5rem; margin: 0; margin-bottom: 5px; }
.ldp-subtitle { font-weight: 600; font-size: 1.2rem; opacity: 0.7; margin-bottom: 10px; margin-top: 0; }

/* Credits & Donation */
.credit-container { display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 15px; font-size: 14px; }
.credit-container a { color: #10B981; text-decoration: none; font-weight: 700; }
.credit-container a:hover { text-decoration: underline; }
.tako-btn { background: #FF424D; color: white !important; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; text-decoration: none !important; display: inline-flex; align-items: center; gap: 5px; }
.tako-btn:hover { background: #E0353F; transform: translateY(-1px); box-shadow: 0 4px 10px rgba(255,66,77,0.3); }

.live-badge { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 12px; color: #10B981; background: rgba(16,185,129,0.1); padding: 5px 15px; border-radius: 30px; border: 1px solid rgba(16,185,129,0.2); }
.live-dot { height: 8px; width: 8px; background: #10B981; border-radius: 50%; animation: blink 2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.2); } }

/* Grid System */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; justify-content: center; margin-bottom: 30px; }

/* Link Badge Styling */
a.badge-link { text-decoration: none !important; display: block; margin-top: auto; width: 100%; }

/* Card Design */
.ldp-card { 
    background: rgba(128,128,128,0.05); 
    border-radius: 15px; 
    padding: 20px 15px; 
    border: 1px solid rgba(128,128,128,0.15); 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between; 
    align-items: center;
    text-align: center; 
    transition: 0.3s ease;
    height: 100%;
}
.ldp-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: rgba(128,128,128,0.3); }

/* Border Status */
.ldp-card.avail { border-bottom: 5px solid #10B981; }
.ldp-card.warn { border-bottom: 5px solid #FBBF24; animation: glow 2s infinite; }
.ldp-card.sold { border-bottom: 5px solid #EF4444; opacity: 0.7; filter: grayscale(30%); }

@keyframes glow { 0% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } 50% { box-shadow: 0 0 15px rgba(251,191,36,0.3); } 100% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } }

/* Foto Kabesha CDN Proxy Async */
.c-photo { 
    width: 74px; 
    height: 74px; 
    border-radius: 50%; 
    background-size: cover; 
    background-position: center 10%; 
    background-repeat: no-repeat;
    margin: 0 auto 12px auto; 
    border: 2px solid rgba(255, 255, 255, 0.9); 
    box-shadow: 0 4px 10px rgba(0,0,0,0.2); 
    background-color: #2a2a2a; 
}

.c-jalur { font-size: 10px; opacity: 0.5; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; width: 100%; }
.c-member { font-weight: 700; font-size: 15px; line-height: 1.2; margin-bottom: 8px; height: 2.4em; overflow: hidden; display: flex; align-items: center; justify-content: center; width: 100%; }

/* --- SMART PROGRESS BUTTON --- */
.c-stats { 
    font-size: 11px; 
    color: #888; 
    margin-bottom: 6px; 
    display: flex; 
    justify-content: center;
    width: 100%; 
    padding: 0 4px; 
}
.c-stats b { color: #ccc; margin-left: 3px; }

.c-prog-btn { 
    position: relative; 
    width: 100%; 
    height: 32px; 
    background: rgba(255,255,255,0.05); 
    border-radius: 8px; 
    overflow: hidden; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    border: 1px solid rgba(255,255,255,0.1); 
    transition: all 0.2s ease; 
}
.c-prog-btn:hover { border-color: rgba(255,255,255,0.3); transform: translateY(-1px); }
.c-prog-fill { 
    position: absolute; 
    left: 0; 
    top: 0; 
    height: 100%; 
    transition: width 0.5s ease; 
    z-index: 0; 
}

/* Pewarnaan Indikator Fill Button */
.ldp-card.avail .c-prog-fill { background: rgba(16,185,129, 0.8); }
.ldp-card.warn .c-prog-fill { background: rgba(217,119,6, 0.8); }
.ldp-card.sold .c-prog-fill { background: rgba(239,68,68, 0.8); }

.c-prog-text { 
    position: relative; 
    z-index: 1; 
    font-size: 11px; 
    font-weight: 800; 
    color: #fff; 
    letter-spacing: 0.5px; 
    text-shadow: 0 1px 3px rgba(0,0,0,0.8); 
}

/* Mobile optimization */
@media (max-width: 500px) { 
    .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; } 
    .ldp-card { padding: 18px 10px; }
    .c-member { font-size: 13px; }
    .ldp-title { font-size: 2rem; }
    .credit-container { flex-direction: column; gap: 10px; }
}
</style>
"""
st.markdown(css.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

# --- 4. RENDER HEADER ---
st.markdown(
    """
    <div class="ldp-header">
        <h1 class="ldp-title">Theater Love Dream Passion</h1>
        <p class="ldp-subtitle">Surabaya & Yogyakarta</p>
        <div class="credit-container">
            <span>Developed by <a href="https://x.com/estrellawin19" target="_blank">@estrellawin19</a></span>
            <a href="https://tako.id/Sportagame19Win" target="_blank" class="tako-btn">🐙 Support via Tako</a>
        </div>
        <div class="live-badge"><span class="live-dot"></span> MONITORING LIVE</div>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- 5. DATA ENGINE & FOTO MEMBER ---
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

@st.cache_data(ttl=3600)
def get_photo_map():
    url = "https://jkt48.com/api/v1/members?lang=id"
    photo_map = {}
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            for member in response.json().get("data", []):
                name = member.get("name", "").strip().lower()
                photo = member.get("photo", "")
                if name and photo:
                    photo_map[name] = photo
    except:
        pass
    return photo_map

@st.cache_data(ttl=4)
def fetch_data(url):
    if not url:
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def draw_section(url, ev_type, query, team_filter=None, photo_map=None):
    if not url:
        return

    data = fetch_data(url)
    if not data:
        st.info("Menunggu data terbaru dari server JKT48...")
        return

    try:
        event_id = url.split("/exclusives/")[1].split("/")[0].split("?")[0]
    except:
        event_id = ""
        
    purchase_link = f"https://jkt48.com/purchase/exclusive?code={event_id}"

    raw_data = data.get('data')
    if isinstance(raw_data, dict):
        sessions = raw_data.get('session', [])
    elif isinstance(raw_data, list):
        sessions = raw_data
    else:
        sessions = []

    has_data = False
    for sesi in sessions:
        if team_filter and team_filter.upper() not in sesi.get('label', '').upper():
            continue

        members = sesi.get('session_detail', sesi.get('session_members', []))
        
        if query:
            members = [m for m in members if query in m.get('jkt48_member_name', m.get('member_name', '')).lower()]
        
        if not members: 
            continue

        has_data = True
        display_label = sesi.get('label', '').replace(" (LOVE)", "").replace(" (DREAM)", "").replace(" (PASSION)", "")
        
        st.markdown(f"#### {display_label} <small style='opacity:0.5'>| {sesi.get('start_time', '')[:5]} - {sesi.get('end_time', '')[:5]}</small>", unsafe_allow_html=True)
        
        html = '<div class="cards-grid">'
        for m in members:
            member_name = m.get('jkt48_member_name', m.get('member_name', ''))
            current_quota = m.get('available_quota', m.get('quota', 0))
            tickets_sold = m.get('tickets_sold', 0)
            jalur_label = m.get("label", "-")
            limit = 5 if ev_type == "2shot" else 20
            
            # --- FOTO KABESHA ---
            safe_name = member_name.strip().lower()
            raw_photo_url = photo_map.get(safe_name, "") if photo_map else ""
            if raw_photo_url:
                proxy_url = f"https://wsrv.nl/?url={raw_photo_url}&w=100&output=webp"
            else:
                proxy_url = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
            
            img_html = f'<div class="c-photo" style="background-image: url(\'{proxy_url}\');" title="{member_name}"></div>'

            # --- RESTOCK TOAST ---
            ticket_key = f"{ev_type}_{sesi.get('label', '')}_{member_name}_{jalur_label}"
            if ticket_key in st.session_state.quota_history:
                prev_quota = st.session_state.quota_history[ticket_key]
                if current_quota > prev_quota:
                    st.toast(f"RESTOCK: {member_name} ({jalur_label}) - Sesi {display_label} (Kuota: {current_quota})", icon="🚨")
            st.session_state.quota_history[ticket_key] = current_quota
            
            # --- SMART PROGRESS LOGIC ---
            total_slot_capacity = tickets_sold + current_quota
            sold_percentage = (tickets_sold / total_slot_capacity * 100) if total_slot_capacity > 0 else 0

            if current_quota <= 0: 
                cls, btn_text = "sold", "HABIS"
                sold_percentage = 100
                bar_color = "#EF4444"
            elif current_quota < limit: 
                cls, btn_text = "warn", f"SISA {current_quota}"
                bar_color = "#FBBF24"
            else: 
                cls, btn_text = "avail", f"SISA {current_quota}"
                bar_color = "#10B981"

            combined_ui = f"""
            <div class="c-stats">
                <span>Terjual: <b>{tickets_sold}</b></span>
            </div>
            <div class="c-prog-btn">
                <div class="c-prog-fill" style="width: {sold_percentage}%; background-color: {bar_color};"></div>
                <div class="c-prog-text">{btn_text}</div>
            </div>
            """
                
            # Render HTML
            if current_quota <= 0:
                html += (
                    f'<div class="ldp-card {cls}">'
                    f'<div class="c-jalur">{jalur_label}</div>'
                    f'{img_html}'
                    f'<div class="c-member">{member_name}</div>'
                    f'<div style="margin-top: auto; width: 100%;">{combined_ui}</div>'
                    f'</div>'
                )
            else:
                html += (
                    f'<div class="ldp-card {cls}">'
                    f'<div class="c-jalur">{jalur_label}</div>'
                    f'{img_html}'
                    f'<div class="c-member">{member_name}</div>'
                    f'<a href="{purchase_link}" target="_blank" class="badge-link">{combined_ui}</a>'
                    f'</div>'
                )
        
        st.markdown(html + '</div>', unsafe_allow_html=True)
        st.write("")
        
    if not has_data and query:
        st.warning(f"Member tidak ditemukan di tim ini.")

# --- 6. LAYOUT LOKASI & TABS ---
photo_map = get_photo_map()

kota = st.radio("📍 Pilih Lokasi Event:", ["Surabaya", "Yogyakarta"], horizontal=True)

st.info("💡 **Petunjuk:** Klik bagian bawah kartu member (yang ada warna hijaunya) untuk langsung menuju halaman pembelian tiket JKT48.")
st.write("") 

t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

# --- CONTROLLER JALUR API ---
if kota == "Surabaya":
    api_2shot_ld = "https://jkt48.com/api/v1/exclusives/EX3773?lang=id" 
    api_2shot_p  = "https://jkt48.com/api/v1/exclusives/EX38A5?lang=id" 
    api_mng_ld   = "https://jkt48.com/api/v1/exclusives/EX9A4A?lang=id" 
    api_mng_p    = "https://jkt48.com/api/v1/exclusives/EXAFB8?lang=id" 
else: # Yogyakarta
    api_2shot_ld = "https://jkt48.com/api/v1/exclusives/EXEXFB66?lang=id" 
    api_2shot_p  = "https://jkt48.com/api/v1/exclusives/EXCD2C?lang=id"
    api_mng_ld   = "https://jkt48.com/api/v1/exclusives/EXA340?lang=id" 
    api_mng_p    = "https://jkt48.com/api/v1/exclusives/EXCB75?lang=id"

# --- TAB 1: INTERFACE 2-SHOT ---
with t1:
    tabs_2s_config = []
    if api_2shot_ld:
        tabs_2s_config.append(("🩷 TEAM LOVE", api_2shot_ld, "LOVE"))
        tabs_2s_config.append(("⭐ TEAM DREAM", api_2shot_ld, "DREAM"))
    if api_2shot_p:
        tabs_2s_config.append(("🔥 TEAM PASSION", api_2shot_p, "PASSION"))
        
    if tabs_2s_config:
        query_2s = st.text_input("🔍 Cari Member di 2-Shot...", key=f"s_2s_{kota}").lower().strip()
        rendered_tabs_2s = st.tabs([t[0] for t in tabs_2s_config])
        
        for idx, tab in enumerate(rendered_tabs_2s):
            with tab:
                draw_section(tabs_2s_config[idx][1], "2shot", query_2s, tabs_2s_config[idx][2], photo_map)
    else:
        st.info("🎟️ Data/API 2-Shot belum dirilis untuk kota ini.")

# --- TAB 2: INTERFACE MEET & GREET ---
with t2:
    tabs_mng_config = []
    if api_mng_ld:
        tabs_mng_config.append(("🩷 TEAM LOVE", api_mng_ld, "LOVE"))
        tabs_mng_config.append(("⭐ TEAM DREAM", api_mng_ld, "DREAM"))
    if api_mng_p:
        tabs_mng_config.append(("🔥 TEAM PASSION", api_mng_p, "PASSION"))
        
    if tabs_mng_config:
        query_mng = st.text_input("🔍 Cari Member di Meet & Greet...", key=f"s_mng_{kota}").lower().strip()
        rendered_tabs_mng = st.tabs([t[0] for t in tabs_mng_config])
        
        for idx, tab in enumerate(rendered_tabs_mng):
            with tab:
                draw_section(tabs_mng_config[idx][1], "mng", query_mng, tabs_mng_config[idx][2], photo_map)
    else:
        st.info("🎟️ Data/API Meet & Greet belum dirilis untuk kota ini.")
