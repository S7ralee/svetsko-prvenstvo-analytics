# ═══════════════════════════════════════════════════════════════════════════════
#  app.py — World Cup 2026 Predictions  |  Sunny Stadium Theme
#  Poisson / xG model  ·  API-Football & football-data.org integration
# ═══════════════════════════════════════════════════════════════════════════════
import math
import re
import requests
from datetime import datetime

import streamlit as st

# ── must be first Streamlit call ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ WC 2026 Predictions",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS — FESTIVE LIGHT THEME  (sunny stadium day)
# ═══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500&display=swap');

:root {
  --bg:      #EEF6EE;
  --card:    #FFFFFF;
  --green:   #2E7D32;
  --glt:     #E8F5E9;
  --gmd:     #43A047;
  --gold:    #FFD700;
  --gold2:   #F9A825;
  --gold3:   #FFF8E1;
  --navy:    #1A2332;
  --text:    #1A2332;
  --muted:   #546E7A;
  --border:  #D5E8D5;
  --shadow:  0 2px 14px rgba(46,125,50,0.10), 0 1px 4px rgba(0,0,0,0.05);
  --r:       14px;
}

/* ── global ── */
html, body { background: var(--bg) !important; color: var(--text) !important; }
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], section.main > div { background: var(--bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; max-width: 1400px !important; }
* { font-family: 'Inter', 'Rajdhani', sans-serif; box-sizing: border-box; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] label {
  color: var(--muted) !important; font-size: 0.78rem !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] .stTextInput input {
  background: var(--bg) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 8px !important; font-size: 0.82rem !important;
}
[data-testid="stSidebar"] .stRadio label { font-size: 0.82rem !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #FFFFFF !important; border-radius: 10px !important;
  gap: 3px !important; padding: 4px !important; border-bottom: none !important;
  box-shadow: 0 1px 5px rgba(0,0,0,0.07) !important; flex-wrap: nowrap !important;
  overflow-x: auto !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--muted) !important;
  font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important;
  font-size: 0.82rem !important; border-radius: 7px !important;
  padding: 5px 12px !important; border: none !important; white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
  background: var(--glt) !important; color: var(--green) !important;
}

/* ── expanders ── */
[data-testid="stExpander"] {
  background: #FAFCFA !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; margin-top: 6px !important;
}
[data-testid="stExpander"] summary { color: var(--green) !important; font-weight: 600 !important; }

/* ── sliders ── */
[data-testid="stSlider"] > div > div > div > div { background: var(--green) !important; }

/* ── metrics ── */
[data-testid="stMetric"] {
  background: #FFFFFF !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; padding: 10px 14px !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.72rem !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-size: 1.25rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #B5CCB5; border-radius: 3px; }

/* ════════════ HEADER BANNER ════════════ */
.wc-banner {
  background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #1B5E20 100%);
  border-radius: 18px; padding: 28px 36px 24px; margin-bottom: 20px;
  position: relative; overflow: hidden;
  box-shadow: 0 6px 28px rgba(27,94,32,0.28);
}
.wc-banner::before {
  content: ''; position: absolute; top: -30%; right: -5%; width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(255,215,0,0.22) 0%, transparent 65%);
  pointer-events: none;
}
.wc-banner::after {
  content: ''; position: absolute; bottom: -35%; left: 8%; width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 65%);
  pointer-events: none;
}
.wc-title {
  font-family: 'Orbitron', sans-serif; font-size: 2.0rem; font-weight: 900;
  color: var(--gold); letter-spacing: 0.04em; margin: 0; line-height: 1.15;
  text-shadow: 0 2px 10px rgba(255,215,0,0.28);
}
.wc-sub {
  font-family: 'Rajdhani', sans-serif; font-size: 0.90rem; font-weight: 600;
  color: rgba(255,255,255,0.72); letter-spacing: 0.22em; text-transform: uppercase; margin-top: 5px;
}
.wc-pills { display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap; align-items: center; }
.wc-pill {
  font-size: 0.75rem; color: rgba(255,255,255,0.85); font-weight: 500;
  background: rgba(255,255,255,0.13); border: 1px solid rgba(255,255,255,0.22);
  border-radius: 20px; padding: 4px 13px;
}
.wc-pill b { color: var(--gold); }
.src-badge-live { background: rgba(0,230,118,0.18); border: 1px solid rgba(0,230,118,0.50); color: #00C853; border-radius: 20px; padding: 4px 13px; font-size: 0.72rem; font-weight: 700; }
.src-badge-fall { background: rgba(255,255,255,0.10); border: 1px solid rgba(255,255,255,0.20); color: rgba(255,255,255,0.70); border-radius: 20px; padding: 4px 13px; font-size: 0.72rem; }

/* ════════════ STAT STRIP ════════════ */
.stat-strip {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 22px;
}
.stat-cell {
  background: #FFFFFF; border: 1px solid var(--border); border-radius: 12px;
  padding: 15px 12px 11px; text-align: center; position: relative; overflow: hidden;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}
.stat-cell::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.sc-green::after { background: var(--green); }
.sc-gold::after  { background: var(--gold2); }
.sc-blue::after  { background: #1565C0; }
.sc-red::after   { background: #C62828; }
.sc-gray::after  { background: #78909C; }
.stat-val {
  font-family: 'Orbitron', sans-serif; font-size: 1.55rem; font-weight: 700; line-height: 1; margin-bottom: 4px;
}
.sc-green .stat-val { color: var(--green); }
.sc-gold  .stat-val { color: var(--gold2); }
.sc-blue  .stat-val { color: #1565C0; }
.sc-red   .stat-val { color: #C62828; }
.sc-gray  .stat-val { color: #78909C; }
.stat-lbl { font-size: 0.67rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }

/* ════════════ GROUP HEADER ════════════ */
.grp-hdr {
  display: flex; align-items: center; gap: 12px;
  border-left: 4px solid var(--green); padding-left: 14px; margin: 26px 0 10px;
}
.grp-hdr h3 {
  font-family: 'Orbitron', sans-serif; font-size: 0.85rem; font-weight: 700;
  color: var(--green); letter-spacing: 0.14em; text-transform: uppercase; margin: 0;
}
.grp-hdr span { font-size: 0.76rem; color: var(--muted); }

/* ════════════ MATCH CARD ════════════ */
.mc {
  background: #FFFFFF; border: 1.5px solid var(--border);
  border-radius: var(--r); margin-bottom: 14px; overflow: hidden;
  box-shadow: var(--shadow); transition: box-shadow 0.22s, transform 0.15s;
}
.mc:hover { box-shadow: 0 6px 24px rgba(46,125,50,0.16), 0 2px 6px rgba(0,0,0,0.07); }
.mc.value-card { border-color: #FFB300; border-width: 2px; }

/* card stripe */
.mc-stripe {
  background: linear-gradient(90deg, #2E7D32, #388E3C);
  padding: 9px 16px; display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 5px;
}
.mc-stripe-meta { font-size: 0.71rem; color: rgba(255,255,255,0.88); font-weight: 500; letter-spacing: 0.03em; }
.mc-stripe-meta b { color: var(--gold); }
.mc-badges { display: flex; gap: 5px; flex-wrap: wrap; align-items: center; }

/* badges */
.bdg {
  font-size: 0.63rem; font-weight: 700; letter-spacing: 0.04em;
  text-transform: uppercase; border-radius: 20px; padding: 2.5px 9px; white-space: nowrap;
}
.bdg-grp   { background: rgba(255,255,255,0.18); color: #FFFFFF; border: 1px solid rgba(255,255,255,0.28); }
.bdg-val   { background: var(--gold); color: #1A2332; box-shadow: 0 1px 6px rgba(255,215,0,0.50); }
.bdg-tight { background: #E65100; color: #FFFFFF; }
.bdg-fav   { background: rgba(255,255,255,0.25); color: #FFFFFF; }

/* teams */
.teams-row {
  display: grid; grid-template-columns: 1fr 56px 1fr;
  align-items: center; gap: 8px; padding: 14px 18px 10px;
}
.tb  { display: flex; align-items: center; gap: 10px; }
.tb.away { flex-direction: row-reverse; text-align: right; }
.t-flag { font-size: 2.1rem; line-height: 1; flex-shrink: 0; }
.t-name { font-family: 'Rajdhani', sans-serif; font-size: 1.10rem; font-weight: 700; color: var(--text); line-height: 1.1; }
.t-rank { font-size: 0.66rem; color: var(--muted); margin-top: 2px; }
.vs-box {
  text-align: center; font-family: 'Orbitron', sans-serif; font-size: 0.74rem;
  font-weight: 700; color: var(--muted); background: var(--bg);
  border: 1px solid var(--border); border-radius: 8px; padding: 5px 3px;
}

/* prob chips */
.pgrid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; padding: 4px 18px 10px;
}
.pchip {
  border-radius: 10px; padding: 9px 5px 7px; text-align: center;
  border: 1.5px solid transparent; position: relative;
}
.pchip.edge-chip {
  border-color: #FFB300 !important;
  animation: edgePulse 2.6s ease-in-out infinite;
}
@keyframes edgePulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(255,179,0,0); }
  50%      { box-shadow: 0 0 10px 2px rgba(255,179,0,0.30); }
}
.pc1  { background: #E3F2FD; border-color: #BBDEFB; }
.pcx  { background: #F5F5F5; border-color: #E0E0E0; }
.pc2  { background: #FFEBEE; border-color: #FFCDD2; }
.pcov { background: #E8F5E9; border-color: #C8E6C9; }
.pcgg { background: #F3E5F5; border-color: #E1BEE7; }
.pchip-lbl { font-size: 0.58rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; font-weight: 600; }
.pc1  .pchip-val { color: #1565C0; }
.pcx  .pchip-val { color: #546E7A; }
.pc2  .pchip-val { color: #C62828; }
.pcov .pchip-val { color: #2E7D32; }
.pcgg .pchip-val { color: #6A1B9A; }
.pchip-val  { font-family: 'Orbitron', sans-serif; font-size: 0.95rem; font-weight: 700; }
.pchip-edge { font-size: 0.60rem; margin-top: 2px; font-weight: 700; }
.edge-pos   { color: #2E7D32; }
.edge-neg   { color: #BDBDBD; }

/* prob bars */
.barsec { padding: 0 18px 6px; }
.brow   { display: flex; align-items: center; gap: 7px; margin-bottom: 4px; }
.b-lbl  { font-size: 0.68rem; color: var(--muted); width: 60px; flex-shrink: 0; font-weight: 500; }
.b-pct  { font-size: 0.68rem; color: var(--text); width: 36px; text-align: right; flex-shrink: 0; font-weight: 700; }
.btrack { flex: 1; height: 5px; background: #EEEEEE; border-radius: 3px; overflow: hidden; }
.bfill  { height: 100%; border-radius: 3px; }
.bf-h   { background: linear-gradient(90deg, #1565C0, #64B5F6); }
.bf-x   { background: linear-gradient(90deg, #78909C, #B0BEC5); }
.bf-a   { background: linear-gradient(90deg, #C62828, #EF9A9A); }
.bf-ov  { background: linear-gradient(90deg, #2E7D32, #81C784); }
.bf-gg  { background: linear-gradient(90deg, #6A1B9A, #CE93D8); }

/* venue */
.venue-chip {
  display: inline-block; font-size: 0.67rem; color: var(--muted); font-weight: 500;
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 2px 10px; margin: 4px 18px 14px;
}

/* ════════════ SIDEBAR COMPONENTS ════════════ */
.sb-sec {
  font-family: 'Rajdhani', sans-serif; font-size: 0.70rem; font-weight: 700;
  letter-spacing: 0.13em; text-transform: uppercase; color: var(--green);
  border-bottom: 2px solid var(--glt); padding-bottom: 7px; margin: 16px 0 10px;
}
.src-ok  { background: #E8F5E9; border: 1px solid #A5D6A7; border-radius: 8px; padding: 8px 12px; font-size: 0.76rem; color: var(--green); font-weight: 600; }
.src-err { background: var(--gold3); border: 1px solid #FFE082; border-radius: 8px; padding: 8px 12px; font-size: 0.76rem; color: #E65100; font-weight: 600; }
.src-def { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; font-size: 0.76rem; color: var(--muted); }
.help-link { font-size: 0.73rem; color: var(--green); text-decoration: none; font-weight: 600; }

/* ════════════ RESPONSIVE ════════════ */
@media (max-width: 768px) {
  .wc-title     { font-size: 1.5rem; }
  .stat-strip   { grid-template-columns: repeat(3, 1fr); }
  .pgrid        { grid-template-columns: repeat(3, 1fr); }
  .teams-row    { grid-template-columns: 1fr 44px 1fr; }
  .t-flag       { font-size: 1.6rem; }
}
</style>"""
st.markdown(_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TEAM PROFILES  (48 nations · WC 2026)
# ═══════════════════════════════════════════════════════════════════════════════
TEAMS: dict = {
    # GROUP A
    "Mexico":             dict(flag="🇲🇽", atk=1.55, def_=1.05, rank=16, style="High Press"),
    "South Africa":       dict(flag="🇿🇦", atk=1.08, def_=1.25, rank=62, style="Physical"),
    "South Korea":        dict(flag="🇰🇷", atk=1.40, def_=1.08, rank=23, style="Hard-working"),
    "Czechia":            dict(flag="🇨🇿", atk=1.35, def_=1.10, rank=33, style="Disciplined"),
    # GROUP B
    "Canada":             dict(flag="🇨🇦", atk=1.42, def_=1.05, rank=41, style="Athletic"),
    "Bosnia Herzegovina": dict(flag="🇧🇦", atk=1.22, def_=1.15, rank=58, style="Counter"),
    "Qatar":              dict(flag="🇶🇦", atk=1.08, def_=1.30, rank=37, style="Compact"),
    "Switzerland":        dict(flag="🇨🇭", atk=1.45, def_=1.00, rank=19, style="Disciplined"),
    # GROUP C
    "Brazil":             dict(flag="🇧🇷", atk=2.05, def_=0.85, rank=4,  style="Total Football"),
    "Morocco":            dict(flag="🇲🇦", atk=1.48, def_=0.90, rank=14, style="Defensive Solid"),
    "Scotland":           dict(flag="🏴󠁧󠁢󠁳󠁣󠁴󠁿", atk=1.28, def_=1.15, rank=40, style="Physical"),
    "Haiti":              dict(flag="🇭🇹", atk=0.92, def_=1.45, rank=83, style="Defensive"),
    # GROUP D
    "USA":                dict(flag="🇺🇸", atk=1.45, def_=1.05, rank=11, style="Athletic"),
    "Paraguay":           dict(flag="🇵🇾", atk=1.22, def_=1.18, rank=64, style="Physical"),
    "Australia":          dict(flag="🇦🇺", atk=1.22, def_=1.12, rank=25, style="Compact"),
    "Türkiye":            dict(flag="🇹🇷", atk=1.45, def_=1.06, rank=26, style="Pressing"),
    # GROUP E
    "Germany":            dict(flag="🇩🇪", atk=1.82, def_=0.94, rank=12, style="Structured"),
    "Curaçao":            dict(flag="🇨🇼", atk=0.95, def_=1.38, rank=90, style="Defensive"),
    "Ivory Coast":        dict(flag="🇨🇮", atk=1.45, def_=1.06, rank=20, style="Attack-minded"),
    "Ecuador":            dict(flag="🇪🇨", atk=1.32, def_=1.08, rank=44, style="Counter"),
    # GROUP F
    "Netherlands":        dict(flag="🇳🇱", atk=1.80, def_=0.95, rank=8,  style="Direct"),
    "Japan":              dict(flag="🇯🇵", atk=1.44, def_=1.00, rank=18, style="Compact Block"),
    "Sweden":             dict(flag="🇸🇪", atk=1.35, def_=1.08, rank=27, style="Physical"),
    "Tunisia":            dict(flag="🇹🇳", atk=1.12, def_=1.15, rank=30, style="Counter"),
    # GROUP G
    "Belgium":            dict(flag="🇧🇪", atk=1.70, def_=1.00, rank=5,  style="Veteran Quality"),
    "Egypt":              dict(flag="🇪🇬", atk=1.35, def_=1.05, rank=35, style="Counter"),
    "Iran":               dict(flag="🇮🇷", atk=1.22, def_=1.10, rank=22, style="Defensive"),
    "New Zealand":        dict(flag="🇳🇿", atk=0.92, def_=1.38, rank=97, style="Physical"),
    # GROUP H
    "Spain":              dict(flag="🇪🇸", atk=1.92, def_=0.88, rank=3,  style="Possession"),
    "Cape Verde":         dict(flag="🇨🇻", atk=1.08, def_=1.22, rank=72, style="Counter"),
    "Saudi Arabia":       dict(flag="🇸🇦", atk=1.28, def_=1.12, rank=58, style="Defensive"),
    "Uruguay":            dict(flag="🇺🇾", atk=1.60, def_=0.95, rank=16, style="Garra Charrúa"),
    # GROUP I
    "France":             dict(flag="🇫🇷", atk=1.95, def_=0.87, rank=2,  style="Direct & Fast"),
    "Senegal":            dict(flag="🇸🇳", atk=1.50, def_=1.02, rank=17, style="Physical"),
    "Norway":             dict(flag="🇳🇴", atk=1.55, def_=1.00, rank=29, style="Direct"),
    "Iraq":               dict(flag="🇮🇶", atk=1.12, def_=1.22, rank=67, style="Organized"),
    # GROUP J
    "Argentina":          dict(flag="🇦🇷", atk=2.02, def_=0.87, rank=1,  style="Elite Possession"),
    "Algeria":            dict(flag="🇩🇿", atk=1.38, def_=1.06, rank=35, style="Physical"),
    "Austria":            dict(flag="🇦🇹", atk=1.40, def_=1.05, rank=24, style="Press & Run"),
    "Jordan":             dict(flag="🇯🇴", atk=1.08, def_=1.26, rank=74, style="Defensive"),
    # GROUP K
    "Portugal":           dict(flag="🇵🇹", atk=1.95, def_=0.92, rank=7,  style="Wing Play"),
    "Colombia":           dict(flag="🇨🇴", atk=1.55, def_=1.00, rank=13, style="Attack-minded"),
    "Uzbekistan":         dict(flag="🇺🇿", atk=1.18, def_=1.15, rank=68, style="Organized"),
    "DR Congo":           dict(flag="🇨🇩", atk=1.12, def_=1.22, rank=57, style="Physical"),
    # GROUP L
    "England":            dict(flag="🏴󠁧󠁢󠁥󠁮󠁧󠁿", atk=1.85, def_=0.90, rank=5,  style="Press & Power"),
    "Croatia":            dict(flag="🇭🇷", atk=1.58, def_=0.98, rank=10, style="Midfield Control"),
    "Ghana":              dict(flag="🇬🇭", atk=1.28, def_=1.12, rank=55, style="Athletic"),
    "Panama":             dict(flag="🇵🇦", atk=1.02, def_=1.27, rank=48, style="Defensive"),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  FALLBACK MATCHES — Real WC 2026 Matchday 1 · All 12 Groups
# ═══════════════════════════════════════════════════════════════════════════════
FALLBACK_MATCHES: list = [
    # ── GROUP A ──
    dict(id=0,  home="Mexico",        away="South Africa",      group="A", date="Jun 11", venue="Estadio Azteca, Mexico City",          odds=dict(h=1.55, x=3.80, a=7.50, ov25=2.05, gg=2.20)),
    dict(id=1,  home="South Korea",   away="Czechia",           group="A", date="Jun 11", venue="Estadio Akron, Guadalajara",           odds=dict(h=2.10, x=3.20, a=3.70, ov25=2.10, gg=1.98)),
    # ── GROUP B ──
    dict(id=2,  home="Canada",        away="Bosnia Herzegovina", group="B", date="Jun 12", venue="BMO Field, Toronto",                  odds=dict(h=1.80, x=3.40, a=5.00, ov25=2.00, gg=2.05)),
    dict(id=3,  home="Qatar",         away="Switzerland",        group="B", date="Jun 13", venue="Levi's Stadium, San Francisco Bay",   odds=dict(h=4.50, x=3.50, a=1.80, ov25=2.25, gg=2.30)),
    # ── GROUP C ──
    dict(id=4,  home="Brazil",        away="Scotland",           group="C", date="Jun 13", venue="SoFi Stadium, Los Angeles",           odds=dict(h=1.20, x=6.50, a=18.0, ov25=1.95, gg=2.40)),
    dict(id=5,  home="Morocco",       away="Haiti",              group="C", date="Jun 13", venue="BC Place, Vancouver",                 odds=dict(h=1.30, x=5.00, a=12.0, ov25=2.20, gg=2.50)),
    # ── GROUP D ──
    dict(id=6,  home="USA",           away="Paraguay",           group="D", date="Jun 12", venue="LA Stadium, Inglewood CA",            odds=dict(h=1.80, x=3.50, a=4.80, ov25=2.00, gg=2.05)),
    dict(id=7,  home="Australia",     away="Türkiye",            group="D", date="Jun 13", venue="Lumen Field, Seattle",                odds=dict(h=2.80, x=3.20, a=2.50, ov25=2.05, gg=2.00)),
    # ── GROUP E ──
    dict(id=8,  home="Germany",       away="Curaçao",            group="E", date="Jun 14", venue="NRG Stadium, Houston",                odds=dict(h=1.07, x=14.0, a=38.0, ov25=1.65, gg=2.80)),
    dict(id=9,  home="Ivory Coast",   away="Ecuador",            group="E", date="Jun 14", venue="Lincoln Financial, Philadelphia",     odds=dict(h=2.20, x=3.20, a=3.40, ov25=2.05, gg=1.95)),
    # ── GROUP F ──
    dict(id=10, home="Netherlands",   away="Japan",              group="F", date="Jun 14", venue="AT&T Stadium, Arlington TX",          odds=dict(h=1.65, x=3.60, a=5.50, ov25=1.95, gg=1.95)),
    dict(id=11, home="Sweden",        away="Tunisia",            group="F", date="Jun 14", venue="Estadio BBVA, Monterrey",             odds=dict(h=1.90, x=3.30, a=4.50, ov25=2.10, gg=2.10)),
    # ── GROUP G ──
    dict(id=12, home="Belgium",       away="Egypt",              group="G", date="Jun 15", venue="Lumen Field, Seattle",                odds=dict(h=1.50, x=4.00, a=7.00, ov25=1.95, gg=1.90)),
    dict(id=13, home="Iran",          away="New Zealand",        group="G", date="Jun 15", venue="LA Stadium, Inglewood CA",            odds=dict(h=2.10, x=3.20, a=3.80, ov25=2.15, gg=2.10)),
    # ── GROUP H ──
    dict(id=14, home="Spain",         away="Cape Verde",         group="H", date="Jun 15", venue="Mercedes-Benz Stadium, Atlanta",      odds=dict(h=1.14, x=7.50, a=22.0, ov25=1.90, gg=2.30)),
    dict(id=15, home="Saudi Arabia",  away="Uruguay",            group="H", date="Jun 15", venue="Hard Rock Stadium, Miami",            odds=dict(h=3.00, x=3.10, a=2.40, ov25=2.20, gg=2.20)),
    # ── GROUP I ──
    dict(id=16, home="France",        away="Senegal",            group="I", date="Jun 16", venue="MetLife Stadium, East Rutherford NJ", odds=dict(h=1.50, x=3.80, a=7.00, ov25=1.95, gg=1.95)),
    dict(id=17, home="Iraq",          away="Norway",             group="I", date="Jun 16", venue="Gillette Stadium, Foxborough MA",     odds=dict(h=4.50, x=3.40, a=1.78, ov25=2.20, gg=2.15)),
    # ── GROUP J ──
    dict(id=18, home="Argentina",     away="Algeria",            group="J", date="Jun 16", venue="Arrowhead Stadium, Kansas City",      odds=dict(h=1.28, x=5.50, a=11.0, ov25=2.00, gg=2.20)),
    dict(id=19, home="Austria",       away="Jordan",             group="J", date="Jun 16", venue="Levi's Stadium, Santa Clara CA",      odds=dict(h=1.55, x=3.50, a=6.50, ov25=2.10, gg=2.00)),
    # ── GROUP K ──
    dict(id=20, home="Portugal",      away="DR Congo",           group="K", date="Jun 17", venue="NRG Stadium, Houston",                odds=dict(h=1.25, x=6.00, a=14.0, ov25=2.00, gg=2.25)),
    dict(id=21, home="Colombia",      away="Uzbekistan",         group="K", date="Jun 17", venue="Arrowhead Stadium, Kansas City",      odds=dict(h=1.58, x=3.80, a=5.50, ov25=2.00, gg=1.95)),
    # ── GROUP L ──
    dict(id=22, home="England",       away="Croatia",            group="L", date="Jun 17", venue="AT&T Stadium, Arlington TX",          odds=dict(h=1.65, x=3.50, a=5.50, ov25=2.00, gg=1.95)),
    dict(id=23, home="Ghana",         away="Panama",             group="L", date="Jun 17", venue="Gillette Stadium, Foxborough MA",     odds=dict(h=2.20, x=3.20, a=3.60, ov25=2.10, gg=1.95)),
]

# quick reverse lookups built from fallback
_TEAM_TO_GROUP:   dict = {}
_PAIR_TO_ODDS:    dict = {}
for _m in FALLBACK_MATCHES:
    _TEAM_TO_GROUP[_m["home"]] = _m["group"]
    _TEAM_TO_GROUP[_m["away"]] = _m["group"]
    _PAIR_TO_ODDS[frozenset([_m["home"], _m["away"]])] = _m["odds"]

# ═══════════════════════════════════════════════════════════════════════════════
#  API TEAM-NAME NORMALISATION MAP
# ═══════════════════════════════════════════════════════════════════════════════
_API_NAME_MAP: dict = {
    # API-Football variants
    "Korea Republic":        "South Korea",
    "Czech Republic":        "Czechia",
    "Cote d'Ivoire":         "Ivory Coast",
    "Côte d'Ivoire":         "Ivory Coast",
    "Congo DR":              "DR Congo",
    "Democratic Republic of the Congo": "DR Congo",
    "Cabo Verde":            "Cape Verde",
    "Turkey":                "Türkiye",
    "Curacao":               "Curaçao",
    "Bosnia-Herzegovina":    "Bosnia Herzegovina",
    "Bosnia & Herzegovina":  "Bosnia Herzegovina",
    "Bosnia and Herzegovina":"Bosnia Herzegovina",
    # football-data.org variants
    "Korea Republic":        "South Korea",
    "IR Iran":               "Iran",
    "Uzbekistan":            "Uzbekistan",
    "New Zealand":           "New Zealand",
}

# ═══════════════════════════════════════════════════════════════════════════════
#  MATHEMATICAL ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
HOME_ADV = 1.08
_AVG_ATK = sum(t["atk"]  for t in TEAMS.values()) / len(TEAMS)
_AVG_DEF = sum(t["def_"] for t in TEAMS.values()) / len(TEAMS)


def _pois(k: int, lam: float) -> float:
    """Pure-Python Poisson PMF — no scipy required."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def compute_probs(hxg: float, axg: float, cap: int = 9) -> dict:
    """Independent Poisson: returns P(home win/draw/away/over 2.5/BTTS)."""
    ph = pa = over = gg = 0.0
    for i in range(cap + 1):
        pi = _pois(i, hxg)
        for j in range(cap + 1):
            pj = _pois(j, axg)
            p  = pi * pj
            if   i > j: ph   += p
            elif i < j: pa   += p
            if i + j > 2:       over += p
            if i > 0 and j > 0: gg   += p
    return dict(h=ph, x=max(0.0, 1.0 - ph - pa), a=pa, ov25=over, gg=gg)


def get_xg(match: dict, hm: float, am: float, hl: float, al: float) -> tuple:
    """Dixon-Coles-style xG with motivation + lineup modifiers."""
    ht = TEAMS.get(match["home"], dict(atk=1.3, def_=1.1))
    at = TEAMS.get(match["away"], dict(atk=1.3, def_=1.1))
    hxg = (ht["atk"] / _AVG_ATK) * (at["def_"] / _AVG_DEF) * _AVG_ATK * hm * hl * HOME_ADV
    axg = (at["atk"] / _AVG_ATK) * (ht["def_"] / _AVG_DEF) * _AVG_ATK * am * al
    return round(hxg, 3), round(axg, 3)


def calc_edges(probs: dict, odds: dict) -> dict:
    """Model probability minus market-implied probability for each market."""
    def _e(p, o): return round(p - 1.0 / o, 4) if o and o > 1 else 0.0
    return dict(
        h=_e(probs["h"],    odds["h"]),
        x=_e(probs["x"],    odds["x"]),
        a=_e(probs["a"],    odds["a"]),
        ov25=_e(probs["ov25"], odds.get("ov25", 1.90)),
        gg=_e(probs["gg"],   odds.get("gg",   1.85)),
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  API INTEGRATION — API-Football (api-sports.io / RapidAPI) + football-data.org
# ═══════════════════════════════════════════════════════════════════════════════

def _norm(name: str) -> str:
    return _API_NAME_MAP.get(name, name)


def _group_from_round(rnd: str) -> str:
    """Extract group letter from round strings like 'Group Stage - 1' or 'GROUP_A'."""
    # football-data.org format: "GROUP_A"
    m = re.search(r'GROUP_([A-L])', rnd or "", re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # API-Football format: "Group Stage - 1" (no letter — use team lookup)
    return ""


def _est_odds(home: str, away: str) -> dict:
    """Return stored odds for this pair, or estimate from team xG profiles."""
    pair = frozenset([home, away])
    if pair in _PAIR_TO_ODDS:
        return _PAIR_TO_ODDS[pair]
    ht = TEAMS.get(home, dict(atk=1.3, def_=1.1))
    at = TEAMS.get(away, dict(atk=1.3, def_=1.1))
    ratio = (ht["atk"] / at["def_"]) / (at["atk"] / ht["def_"])
    if   ratio > 2.0: return dict(h=1.18, x=6.50, a=20.0, ov25=2.00, gg=2.30)
    elif ratio > 1.6: return dict(h=1.40, x=4.20, a=8.50, ov25=2.00, gg=2.15)
    elif ratio > 1.2: return dict(h=1.70, x=3.50, a=5.50, ov25=2.00, gg=2.00)
    elif ratio > 0.9: return dict(h=2.20, x=3.20, a=3.60, ov25=2.00, gg=1.95)
    elif ratio > 0.65: return dict(h=3.20, x=3.10, a=2.30, ov25=2.00, gg=1.95)
    else:              return dict(h=7.00, x=3.60, a=1.50, ov25=2.00, gg=2.00)


def _fmt_date(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%-d %b")
    except Exception:
        return "TBD"


def _build_fixture(home: str, away: str, group: str,
                   date: str, venue: str, fid: int) -> dict | None:
    """Build a normalised match dict; skip if teams unknown."""
    h, a = _norm(home), _norm(away)
    if h not in TEAMS or a not in TEAMS:
        return None
    if not group:
        group = _TEAM_TO_GROUP.get(h) or _TEAM_TO_GROUP.get(a) or "?"
    return dict(id=fid, home=h, away=a, group=group,
                stage="Group Stage", date=date, venue=venue,
                odds=_est_odds(h, a))


@st.cache_data(ttl=300, show_spinner=False)
def _call_api_football(api_key: str) -> list | None:
    """Try API-Football via direct (api-sports.io) then RapidAPI."""
    configs = [
        # Direct API-Sports endpoint
        dict(
            url="https://v3.football.api-sports.io/fixtures",
            headers={"x-apisports-key": api_key,
                     "Accept": "application/json"},
        ),
        # RapidAPI endpoint
        dict(
            url="https://api-football-v1.p.rapidapi.com/v3/fixtures",
            headers={"X-RapidAPI-Key": api_key,
                     "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"},
        ),
    ]
    params = {"league": "1", "season": "2026", "status": "NS"}
    for cfg in configs:
        try:
            resp = requests.get(cfg["url"], headers=cfg["headers"],
                                params=params, timeout=9)
            if resp.status_code != 200:
                continue
            data = resp.json()
            if data.get("errors") or not data.get("response"):
                continue
            out, fid = [], 1000
            for item in data["response"]:
                rnd    = item.get("league", {}).get("round", "")
                grp    = _group_from_round(rnd)
                date   = _fmt_date(item["fixture"]["date"])
                vname  = item["fixture"].get("venue", {}).get("name", "")
                vcity  = item["fixture"].get("venue", {}).get("city", "")
                venue  = f"{vname}, {vcity}".strip(", ")
                fx = _build_fixture(
                    item["teams"]["home"]["name"],
                    item["teams"]["away"]["name"],
                    grp, date, venue, fid,
                )
                if fx:
                    out.append(fx)
                    fid += 1
            if len(out) >= 8:
                return out
        except Exception:
            continue
    return None


@st.cache_data(ttl=300, show_spinner=False)
def _call_football_data(api_key: str) -> list | None:
    """Try football-data.org free tier."""
    try:
        url = "https://api.football-data.org/v4/competitions/WC/matches"
        resp = requests.get(url,
                            headers={"X-Auth-Token": api_key},
                            params={"status": "SCHEDULED,TIMED"},
                            timeout=9)
        if resp.status_code != 200:
            return None
        data = resp.json()
        raw  = data.get("matches", [])
        if not raw:
            return None
        out, fid = [], 2000
        for item in raw:
            if item.get("stage") not in ("GROUP_STAGE", None):
                continue
            grp_raw = item.get("group", "")
            grp     = _group_from_round(grp_raw)
            date    = _fmt_date(item.get("utcDate", ""))
            venue   = item.get("venue") or ""
            fx = _build_fixture(
                item["homeTeam"]["name"],
                item["awayTeam"]["name"],
                grp, date, venue, fid,
            )
            if fx:
                out.append(fx)
                fid += 1
        return out if len(out) >= 8 else None
    except Exception:
        return None


def load_matches(api_key: str) -> tuple:
    """
    Returns (matches_list, source_tag).
    source_tag: 'live' | 'fallback'
    """
    if api_key and len(api_key.strip()) > 5:
        k = api_key.strip()
        live = _call_api_football(k)
        if live:
            return live, "live"
        live = _call_football_data(k)
        if live:
            return live, "live"
        return FALLBACK_MATCHES, "api_error"
    return FALLBACK_MATCHES, "fallback"


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def _chip(label: str, pct: float, edge: float, cls: str) -> str:
    edge_html = (
        f'<div class="pchip-edge edge-pos">▲ {edge*100:.1f}% edge</div>'
        if edge > 0.03 else
        f'<div class="pchip-edge edge-pos">+{edge*100:.1f}%</div>'
        if edge > 0 else
        '<div class="pchip-edge edge-neg">—</div>'
    )
    ec = " edge-chip" if edge > 0.03 else ""
    return (
        f'<div class="pchip {cls}{ec}">'
        f'<div class="pchip-lbl">{label}</div>'
        f'<div class="pchip-val">{pct:.0f}%</div>'
        f'{edge_html}</div>'
    )


def _bar(label: str, pct: float, cls: str) -> str:
    return (
        f'<div class="brow">'
        f'<span class="b-lbl">{label}</span>'
        f'<div class="btrack"><div class="bfill {cls}" style="width:{min(100,pct):.1f}%"></div></div>'
        f'<span class="b-pct">{pct:.1f}%</span></div>'
    )


def build_card(match: dict, probs: dict, edges: dict,
               hxg: float, axg: float) -> str:
    ht = TEAMS.get(match["home"], dict(flag="⚽", rank="?", style=""))
    at = TEAMS.get(match["away"], dict(flag="⚽", rank="?", style=""))
    any_val = any(e > 0.03 for e in edges.values())
    glow    = " value-card" if any_val else ""

    # badges
    badges = f'<span class="bdg bdg-grp">🏆 Group {match["group"]}</span>'
    if any_val:
        badges += '<span class="bdg bdg-val">🔥 VALUE PICK</span>'
    if abs(probs["h"] - probs["a"]) < 0.12:
        badges += '<span class="bdg bdg-tight">⚡ TIGHT</span>'
    if probs["h"] > 0.60:
        badges += f'<span class="bdg bdg-fav">★ {match["home"]} fav</span>'
    elif probs["a"] > 0.60:
        badges += f'<span class="bdg bdg-fav">★ {match["away"]} fav</span>'

    meta = (
        f'<span class="mc-stripe-meta">'
        f'<b>Group {match["group"]}</b> &nbsp;·&nbsp; {match["date"]} '
        f'&nbsp;·&nbsp; xG <b>{hxg:.2f}</b> – <b>{axg:.2f}</b>'
        f'</span>'
    )

    teams = (
        f'<div class="teams-row">'
        f'  <div class="tb"><span class="t-flag">{ht["flag"]}</span>'
        f'    <div><div class="t-name">{match["home"]}</div>'
        f'         <div class="t-rank">FIFA #{ht["rank"]} · {ht["style"]}</div></div></div>'
        f'  <div class="vs-box">VS</div>'
        f'  <div class="tb away"><span class="t-flag">{at["flag"]}</span>'
        f'    <div><div class="t-name">{match["away"]}</div>'
        f'         <div class="t-rank">FIFA #{at["rank"]} · {at["style"]}</div></div></div>'
        f'</div>'
    )

    chips = (
        '<div class="pgrid">'
        + _chip("Home Win", probs["h"]    * 100, edges["h"],    "pc1")
        + _chip("Draw",     probs["x"]    * 100, edges["x"],    "pcx")
        + _chip("Away Win", probs["a"]    * 100, edges["a"],    "pc2")
        + _chip("Over 2.5", probs["ov25"] * 100, edges["ov25"], "pcov")
        + _chip("BTTS",     probs["gg"]   * 100, edges["gg"],   "pcgg")
        + '</div>'
    )

    bars = (
        '<div class="barsec">'
        + _bar("Home Win",  probs["h"]    * 100, "bf-h")
        + _bar("Draw",      probs["x"]    * 100, "bf-x")
        + _bar("Away Win",  probs["a"]    * 100, "bf-a")
        + _bar("Over 2.5",  probs["ov25"] * 100, "bf-ov")
        + _bar("BTTS",      probs["gg"]   * 100, "bf-gg")
        + '</div>'
    )

    venue = f'<span class="venue-chip">📍 {match["venue"]}</span>' if match.get("venue") else ""

    return (
        f'<div class="mc{glow}">'
        f'  <div class="mc-stripe">{meta}<div class="mc-badges">{badges}</div></div>'
        f'  {teams}{chips}{bars}{venue}'
        f'</div>'
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

def render_sidebar(source: str) -> str:
    with st.sidebar:
        st.markdown("## ⚽ WC 2026")
        st.markdown("**Match Predictions**", help="Poisson/xG quant model")

        # data source status
        st.markdown('<div class="sb-sec">📡 Data Source</div>', unsafe_allow_html=True)
        if source == "live":
            st.markdown('<div class="src-ok">🟢 Live API data loaded</div>', unsafe_allow_html=True)
        elif source == "api_error":
            st.markdown('<div class="src-err">⚠️ API error — using built-in data</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="src-def">📦 Built-in Matchday 1 data</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-sec">🔑 API Key (optional)</div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Paste key for live data",
            type="password",
            placeholder="Enter API key…",
            help=(
                "Supports API-Football (api-sports.io / RapidAPI) "
                "and football-data.org free tier.\n\n"
                "Free keys: api-sports.io · football-data.org"
            ),
        )
        st.caption(
            "🔗 Free key: [api-sports.io](https://api-sports.io) · "
            "[football-data.org](https://www.football-data.org/client/register)"
        )

        st.markdown('<div class="sb-sec">🔬 Model Info</div>', unsafe_allow_html=True)
        st.caption(
            "Independent Poisson · Dixon-Coles xG\n"
            "Home advantage ×1.08 · Goal cap: 9\n"
            "5 markets: 1 · X · 2 · Over 2.5 · BTTS\n"
            "🔥 VALUE PICK = model edge > 3%"
        )

    return api_key or ""


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════

def render_header(source: str) -> None:
    src_badge = (
        '<span class="src-badge-live">🟢 Live Data</span>'
        if source == "live" else
        '<span class="src-badge-fall">📦 Built-in Data</span>'
    )
    st.markdown(
        f'<div class="wc-banner">'
        f'  <div class="wc-title">🏆 World Cup 2026 ⚽🌍</div>'
        f'  <div class="wc-sub">World Cup 2026 Live Quant Analytics</div>'
        f'  <div class="wc-pills">'
        f'    <span class="wc-pill">🌎 USA · Canada · Mexico</span>'
        f'    <span class="wc-pill">📅 Jun 11 – Jul 19, 2026</span>'
        f'    <span class="wc-pill">🏟️ 16 Venues</span>'
        f'    <span class="wc-pill">48 Teams · 12 Groups</span>'
        f'    {src_badge}'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  STAT STRIP
# ═══════════════════════════════════════════════════════════════════════════════

def render_stats(all_probs: list, all_edges: list) -> None:
    n_val   = sum(1 for e in all_edges if any(v > 0.03 for v in e.values()))
    avg_ov  = sum(p["ov25"] for p in all_probs) / max(len(all_probs), 1) * 100
    n_tight = sum(1 for p in all_probs if abs(p["h"] - p["a"]) < 0.12)
    st.markdown(
        f'<div class="stat-strip">'
        f'  <div class="stat-cell sc-green"><div class="stat-val">{len(all_probs)}</div><div class="stat-lbl">Fixtures</div></div>'
        f'  <div class="stat-cell sc-gold"><div class="stat-val">{n_val}</div><div class="stat-lbl">Value Picks 🔥</div></div>'
        f'  <div class="stat-cell sc-blue"><div class="stat-val">{avg_ov:.0f}%</div><div class="stat-lbl">Avg Over 2.5</div></div>'
        f'  <div class="stat-cell sc-red"><div class="stat-val">{n_tight}</div><div class="stat-lbl">Tight Matches</div></div>'
        f'  <div class="stat-cell sc-gray"><div class="stat-val">{len(TEAMS)}</div><div class="stat-lbl">Teams</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  MATCH RENDERER
# ═══════════════════════════════════════════════════════════════════════════════

def render_match(match: dict) -> tuple:
    idx = match["id"]

    # initialise session state (avoids Streamlit key-conflict warning)
    for key, val in [(f"hm_{idx}", 1.0), (f"am_{idx}", 1.0),
                     (f"hl_{idx}", 1.0), (f"al_{idx}", 1.0)]:
        if key not in st.session_state:
            st.session_state[key] = val

    hm = st.session_state[f"hm_{idx}"]
    am = st.session_state[f"am_{idx}"]
    hl = st.session_state[f"hl_{idx}"]
    al = st.session_state[f"al_{idx}"]

    hxg, axg = get_xg(match, hm, am, hl, al)
    probs     = compute_probs(hxg, axg)
    edges     = calc_edges(probs, match["odds"])

    # render card HTML
    st.markdown(build_card(match, probs, edges, hxg, axg), unsafe_allow_html=True)

    # collapsible adjustments panel
    ht_flag = TEAMS.get(match["home"], {}).get("flag", "⚽")
    at_flag = TEAMS.get(match["away"], {}).get("flag", "⚽")
    with st.expander(f"⚙️ Adjust assumptions · {match['home']} vs {match['away']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{ht_flag} {match['home']}**")
            st.slider("Motivation",  0.50, 1.50, key=f"hm_{idx}", step=0.05)
            st.slider("Lineup Str.", 0.70, 1.30, key=f"hl_{idx}", step=0.05)
        with col2:
            st.markdown(f"**{at_flag} {match['away']}**")
            st.slider("Motivation",  0.50, 1.50, key=f"am_{idx}", step=0.05)
            st.slider("Lineup Str.", 0.70, 1.30, key=f"al_{idx}", step=0.05)

        st.divider()
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Home Win",  f"{probs['h']*100:.1f}%",    f"{edges['h']*100:+.1f}%")
        c2.metric("Draw",      f"{probs['x']*100:.1f}%",    f"{edges['x']*100:+.1f}%")
        c3.metric("Away Win",  f"{probs['a']*100:.1f}%",    f"{edges['a']*100:+.1f}%")
        c4.metric("Over 2.5",  f"{probs['ov25']*100:.1f}%", f"{edges['ov25']*100:+.1f}%")
        c5.metric("BTTS",      f"{probs['gg']*100:.1f}%",   f"{edges['gg']*100:+.1f}%")

    return probs, edges


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # ── load data first so sidebar can show the right status ──────────────────
    # We need a 2-pass: render sidebar after knowing source.
    # Trick: store api_key in session_state so first run uses "" (fallback),
    # and re-runs after user types key update the source correctly.
    _tmp_key = st.session_state.get("_api_key_val", "")
    matches, source = load_matches(_tmp_key)

    api_key = render_sidebar(source)

    # persist key so next rerun uses it
    if api_key != _tmp_key:
        st.session_state["_api_key_val"] = api_key
        st.rerun()

    # ── header + stats (using default slider = 1.0 for stats strip) ───────────
    render_header(source)

    default_probs, default_edges = [], []
    for m in matches:
        hxg, axg = get_xg(m, 1.0, 1.0, 1.0, 1.0)
        dp = compute_probs(hxg, axg)
        de = calc_edges(dp, m["odds"])
        default_probs.append(dp)
        default_edges.append(de)

    render_stats(default_probs, default_edges)

    # ── tabs: All + one per group ──────────────────────────────────────────────
    groups     = sorted(set(m["group"] for m in matches))
    tab_labels = ["🌍 All Matches"] + [f"Group {g}" for g in groups]
    tabs       = st.tabs(tab_labels)

    # ALL tab — 2-column grid, grouped with headers
    with tabs[0]:
        for g in groups:
            gm = [m for m in matches if m["group"] == g]
            st.markdown(
                f'<div class="grp-hdr"><h3>Group {g}</h3>'
                f'<span>{len(gm)} fixtures — Matchday 1</span></div>',
                unsafe_allow_html=True,
            )
            col_l, col_r = st.columns(2)
            for i, m in enumerate(gm):
                with (col_l if i % 2 == 0 else col_r):
                    render_match(m)

    # Per-group tabs
    for tab, g in zip(tabs[1:], groups):
        with tab:
            gm = [m for m in matches if m["group"] == g]
            st.markdown(
                f'<div class="grp-hdr"><h3>Group {g}</h3>'
                f'<span>{len(gm)} fixtures</span></div>',
                unsafe_allow_html=True,
            )
            for m in gm:
                render_match(m)


main()
