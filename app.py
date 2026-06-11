import math
import streamlit as st

# ── must be first Streamlit call ───────────────────────────────────────────────
st.set_page_config(
    page_title="World Cup 2026 | Quant Analytics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

/* ── root variables ── */
:root {
  --bg:       #0B1325;
  --bg2:      #0F1C35;
  --bg3:      #162040;
  --gold:     #FFD700;
  --gold2:    #FFA500;
  --green:    #00E676;
  --green2:   #00C853;
  --red:      #FF5252;
  --blue:     #448AFF;
  --white:    #F0F4FF;
  --muted:    #7A8AAA;
  --border:   rgba(255,215,0,0.18);
  --glass:    rgba(255,255,255,0.04);
  --radius:   14px;
}

/* ── global ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--white) !important;
  font-family: 'Rajdhani', 'Inter', sans-serif;
}
[data-testid="stMain"] { background: var(--bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0A1628 0%, #060F1E 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--white) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label { color: var(--muted) !important; font-size: 0.78rem !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg2) !important;
  border-radius: 10px !important;
  gap: 4px !important;
  padding: 4px !important;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.04em !important;
  border-radius: 7px !important;
  padding: 6px 14px !important;
  border: none !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #1A2D5A, #0F1E40) !important;
  color: var(--gold) !important;
  box-shadow: 0 0 12px rgba(255,215,0,0.18) !important;
}

/* ── expanders ── */
[data-testid="stExpander"] {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  margin-top: 8px !important;
}
[data-testid="stExpander"] summary { color: var(--gold) !important; font-weight: 600 !important; }

/* ── sliders ── */
[data-testid="stSlider"] > div > div > div > div {
  background: var(--gold) !important;
}

/* ── metrics ── */
[data-testid="stMetric"] {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 10px 14px !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: var(--white) !important; font-size: 1.3rem !important; font-weight: 700 !important; }

/* ── number input / selectbox ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
.stSelectbox div[data-baseweb="select"] > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  color: var(--white) !important;
  border-radius: 8px !important;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #2A3A60; border-radius: 3px; }

/* ═══════════ BANNER ═══════════ */
.wc-banner {
  background: linear-gradient(135deg, #0A1628 0%, #0D1F45 40%, #0A2A1A 100%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 32px 40px 28px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}
.wc-banner::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 60% 80% at 50% 0%, rgba(255,215,0,0.10) 0%, transparent 70%);
  pointer-events: none;
}
.wc-banner-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 2.4rem;
  font-weight: 900;
  letter-spacing: 0.06em;
  background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 4s linear infinite;
  margin: 0; line-height: 1.1;
}
@keyframes shimmer {
  0%   { background-position: 0% center; }
  100% { background-position: 200% center; }
}
.wc-banner-sub {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  color: var(--muted);
  text-transform: uppercase;
  margin: 6px 0 0;
}
.wc-banner-meta {
  display: flex; gap: 24px; margin-top: 18px; flex-wrap: wrap;
}
.wc-banner-meta span {
  font-size: 0.82rem; color: var(--muted);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 4px 14px;
}
.wc-banner-meta span b { color: var(--gold); margin-left: 4px; }

/* ═══════════ STAT STRIP ═══════════ */
.stat-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-bottom: 24px;
}
.stat-cell {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 14px 12px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.stat-cell::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.stat-cell.sc-gold::after  { background: var(--gold); }
.stat-cell.sc-green::after { background: var(--green); }
.stat-cell.sc-blue::after  { background: var(--blue); }
.stat-cell.sc-red::after   { background: var(--red); }
.stat-cell.sc-gray::after  { background: #4A5A7A; }
.stat-val {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.7rem; font-weight: 700;
  line-height: 1; margin-bottom: 4px;
}
.sc-gold .stat-val  { color: var(--gold); }
.sc-green .stat-val { color: var(--green); }
.sc-blue .stat-val  { color: var(--blue); }
.sc-red .stat-val   { color: var(--red); }
.sc-gray .stat-val  { color: #8A9AC0; }
.stat-lbl { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ═══════════ GROUP HEADER ═══════════ */
.grp-header {
  display: flex; align-items: center; gap: 12px;
  border-left: 3px solid var(--gold);
  padding-left: 14px;
  margin: 28px 0 14px;
}
.grp-header h3 {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.95rem; font-weight: 700;
  color: var(--gold); letter-spacing: 0.12em;
  text-transform: uppercase; margin: 0;
}
.grp-header span { font-size: 0.8rem; color: var(--muted); }

/* ═══════════ MATCH CARD ═══════════ */
.mc {
  background: linear-gradient(135deg, #0F1E3A 0%, #0D1830 100%);
  border: 1px solid rgba(255,215,0,0.14);
  border-radius: var(--radius);
  padding: 20px 22px 16px;
  margin-bottom: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.mc:hover {
  border-color: rgba(255,215,0,0.32);
  box-shadow: 0 4px 28px rgba(255,215,0,0.08);
}
.mc.value-glow {
  border-color: rgba(0,230,118,0.5) !important;
  animation: mcPulse 2.6s ease-in-out infinite;
}
@keyframes mcPulse {
  0%,100% { box-shadow: 0 0 14px rgba(0,230,118,0.20); }
  50%      { box-shadow: 0 0 32px rgba(0,230,118,0.44); }
}

/* top row */
.mc-toprow {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  flex-wrap: wrap; gap: 6px;
}
.mc-meta { font-size: 0.76rem; color: var(--muted); line-height: 1.6; }
.mc-meta b { color: var(--white); }
.mc-badges { display: flex; gap: 6px; flex-wrap: wrap; justify-content: flex-end; }

/* badges */
.bdg {
  font-size: 0.69rem; font-weight: 700; letter-spacing: 0.06em;
  text-transform: uppercase; border-radius: 20px;
  padding: 3px 10px; white-space: nowrap;
}
.bdg-val   { background: rgba(0,230,118,0.15); color: var(--green);  border: 1px solid rgba(0,230,118,0.40); }
.bdg-tight { background: rgba(255,165,0,0.12);  color: var(--gold2); border: 1px solid rgba(255,165,0,0.35); }
.bdg-grp   { background: rgba(68,138,255,0.12); color: #82B1FF;      border: 1px solid rgba(68,138,255,0.32); }
.bdg-fav   { background: rgba(255,215,0,0.12);  color: var(--gold);  border: 1px solid rgba(255,215,0,0.32); }
.bdg-ko    { background: rgba(255,82,82,0.12);  color: #FF8A80;      border: 1px solid rgba(255,82,82,0.30); }

/* teams row */
.teams-row {
  display: grid;
  grid-template-columns: 1fr 72px 1fr;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.team-block { display: flex; align-items: center; gap: 10px; }
.team-block.away { flex-direction: row-reverse; text-align: right; }
.team-flag  { font-size: 2rem; line-height: 1; }
.team-name  {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.15rem; font-weight: 700;
  color: var(--white); line-height: 1.1;
}
.team-rank  { font-size: 0.72rem; color: var(--muted); margin-top: 1px; }
.vs-box {
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem; font-weight: 700;
  color: var(--muted);
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 8px; padding: 6px 4px;
}

/* prob chip grid */
.pgrid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 7px;
  margin-bottom: 12px;
}
.pchip {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 10px 6px 8px;
  text-align: center;
  position: relative;
  transition: border-color 0.25s, box-shadow 0.25s;
}
.pchip::after {
  content: '';
  position: absolute; top: 0; left: 10%; right: 10%; height: 2px;
  border-radius: 0 0 2px 2px;
}
.pc1::after  { background: #448AFF; }
.pcx::after  { background: #90A4AE; }
.pc2::after  { background: #FF5252; }
.pcov::after { background: var(--green); }
.pcgg::after { background: #CE93D8; }

.pchip.edge-chip {
  border-color: rgba(0,230,118,0.55) !important;
  animation: edgePulse 2.2s ease-in-out infinite;
}
@keyframes edgePulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(0,230,118,0.0); }
  50%      { box-shadow: 0 0 10px 2px rgba(0,230,118,0.30); }
}
.pchip-lbl { font-size: 0.62rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.pchip-val { font-family: 'Orbitron', sans-serif; font-size: 1.05rem; font-weight: 700; color: var(--white); }
.pchip-edge { font-size: 0.65rem; font-weight: 700; margin-top: 2px; }
.edge-pos { color: var(--green); }
.edge-neg { color: var(--muted); }

/* probability bars */
.barsec { margin-bottom: 6px; }
.brow   { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.b-lbl  { font-size: 0.72rem; color: var(--muted); width: 62px; flex-shrink: 0; }
.b-pct  { font-size: 0.72rem; color: var(--white); width: 38px; text-align: right; flex-shrink: 0; font-weight: 600; }
.btrack {
  flex: 1; height: 6px;
  background: rgba(255,255,255,0.07);
  border-radius: 3px; overflow: hidden;
}
.bfill  { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.bf-h   { background: linear-gradient(90deg, #1565C0, #448AFF); }
.bf-x   { background: linear-gradient(90deg, #546E7A, #90A4AE); }
.bf-a   { background: linear-gradient(90deg, #B71C1C, #FF5252); }
.bf-ov  { background: linear-gradient(90deg, #1B5E20, #00E676); }
.bf-gg  { background: linear-gradient(90deg, #6A1B9A, #CE93D8); }

/* venue chip */
.venue-chip {
  display: inline-block;
  font-size: 0.70rem; color: var(--muted);
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 6px; padding: 2px 9px;
  margin-top: 8px;
}

/* kelly box */
.kelly-box {
  background: linear-gradient(135deg, #0A2A10, #0D3515);
  border: 1px solid rgba(0,230,118,0.35);
  border-radius: 10px; padding: 14px 16px;
}
.kelly-box .k-title { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.kelly-box .k-stake { font-family: 'Orbitron', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--green); }
.kelly-box .k-detail { font-size: 0.78rem; color: var(--muted); margin-top: 4px; }
.no-edge {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px; padding: 14px 16px;
  color: var(--muted); font-size: 0.82rem; text-align: center;
}

/* sidebar section header */
.sb-sec {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.70rem; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--gold);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px; margin: 18px 0 12px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TEAM PROFILES
# ═══════════════════════════════════════════════════════════════════════════════
TEAMS = {
    "Brazil":       dict(flag="🇧🇷", atk=2.05, def_=0.85, rank=1,  style="Total Football"),
    "Serbia":       dict(flag="🇷🇸", atk=1.45, def_=1.15, rank=34, style="Counter-Attack"),
    "France":       dict(flag="🇫🇷", atk=1.90, def_=0.90, rank=2,  style="Direct & Fast"),
    "Belgium":      dict(flag="🇧🇪", atk=1.75, def_=1.00, rank=5,  style="Tiki-Taka Hybrid"),
    "Argentina":    dict(flag="🇦🇷", atk=2.00, def_=0.88, rank=3,  style="Messi-centric"),
    "Mexico":       dict(flag="🇲🇽", atk=1.40, def_=1.10, rank=15, style="High Press"),
    "Spain":        dict(flag="🇪🇸", atk=1.85, def_=0.92, rank=6,  style="Possession"),
    "Portugal":     dict(flag="🇵🇹", atk=1.95, def_=0.95, rank=7,  style="Wing Play"),
    "England":      dict(flag="🏴󠁧󠁢󠁥󠁮󠁧󠁿", atk=1.80, def_=0.95, rank=4,  style="Press & Power"),
    "USA":          dict(flag="🇺🇸", atk=1.35, def_=1.18, rank=14, style="Athletic"),
    "Germany":      dict(flag="🇩🇪", atk=1.75, def_=1.00, rank=12, style="Structured"),
    "Japan":        dict(flag="🇯🇵", atk=1.40, def_=1.05, rank=18, style="Compact Block"),
    "Morocco":      dict(flag="🇲🇦", atk=1.45, def_=0.98, rank=13, style="Defensive Solid"),
    "Netherlands":  dict(flag="🇳🇱", atk=1.80, def_=0.97, rank=8,  style="Direct"),
    "Italy":        dict(flag="🇮🇹", atk=1.70, def_=0.95, rank=9,  style="Catenaccio Modern"),
    "Croatia":      dict(flag="🇭🇷", atk=1.55, def_=1.00, rank=10, style="Midfield Control"),
    "Colombia":     dict(flag="🇨🇴", atk=1.55, def_=1.05, rank=11, style="Attack-minded"),
    "South Korea":  dict(flag="🇰🇷", atk=1.35, def_=1.12, rank=23, style="Hard-working"),
    "Uruguay":      dict(flag="🇺🇾", atk=1.60, def_=0.98, rank=16, style="Garra Charrúa"),
    "Senegal":      dict(flag="🇸🇳", atk=1.50, def_=1.05, rank=20, style="Physical"),
    "Switzerland":  dict(flag="🇨🇭", atk=1.45, def_=1.00, rank=17, style="Disciplined"),
    "Ecuador":      dict(flag="🇪🇨", atk=1.35, def_=1.10, rank=28, style="Counter"),
    "Australia":    dict(flag="🇦🇺", atk=1.25, def_=1.15, rank=25, style="Compact"),
    "Denmark":      dict(flag="🇩🇰", atk=1.50, def_=1.02, rank=21, style="Pressing"),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════
MATCHES = [
    dict(id=0,  home="Brazil",       away="Serbia",      group="A", stage="Group Stage", date="Jun 13", venue="MetLife Stadium, NJ",        odds=dict(h=1.45, x=4.20, a=7.00)),
    dict(id=1,  home="France",       away="Belgium",     group="A", stage="Group Stage", date="Jun 13", venue="Rose Bowl, CA",               odds=dict(h=1.90, x=3.40, a=4.10)),
    dict(id=2,  home="Argentina",    away="Mexico",      group="B", stage="Group Stage", date="Jun 14", venue="AT&T Stadium, TX",             odds=dict(h=1.35, x=4.80, a=9.50)),
    dict(id=3,  home="Spain",        away="Portugal",    group="B", stage="Group Stage", date="Jun 14", venue="Levi's Stadium, CA",           odds=dict(h=2.10, x=3.30, a=3.60)),
    dict(id=4,  home="England",      away="USA",         group="C", stage="Group Stage", date="Jun 15", venue="SoFi Stadium, LA",             odds=dict(h=1.65, x=3.80, a=5.50)),
    dict(id=5,  home="Germany",      away="Japan",       group="C", stage="Group Stage", date="Jun 15", venue="Gillette Stadium, MA",         odds=dict(h=1.55, x=4.00, a=6.50)),
    dict(id=6,  home="Morocco",      away="Netherlands", group="D", stage="Group Stage", date="Jun 16", venue="BC Place, Vancouver",          odds=dict(h=3.80, x=3.30, a=2.00)),
    dict(id=7,  home="Italy",        away="Croatia",     group="D", stage="Group Stage", date="Jun 16", venue="BMO Field, Toronto",           odds=dict(h=2.20, x=3.20, a=3.40)),
    dict(id=8,  home="Colombia",     away="South Korea", group="E", stage="Group Stage", date="Jun 17", venue="Arrowhead Stadium, KC",        odds=dict(h=1.85, x=3.50, a=4.50)),
    dict(id=9,  home="Uruguay",      away="Senegal",     group="E", stage="Group Stage", date="Jun 17", venue="NRG Stadium, Houston",         odds=dict(h=2.10, x=3.20, a=3.60)),
    dict(id=10, home="Switzerland",  away="Ecuador",     group="F", stage="Group Stage", date="Jun 18", venue="Estadio Azteca, Mexico City",  odds=dict(h=1.75, x=3.60, a=5.00)),
    dict(id=11, home="Denmark",      away="Australia",   group="F", stage="Group Stage", date="Jun 18", venue="BMO Field, Toronto",           odds=dict(h=1.70, x=3.70, a=5.20)),
]

# ═══════════════════════════════════════════════════════════════════════════════
#  MATH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
HOME_ADVANTAGE = 1.08
AVG_ATK = sum(t["atk"]  for t in TEAMS.values()) / len(TEAMS)
AVG_DEF = sum(t["def_"] for t in TEAMS.values()) / len(TEAMS)


def _pois(k: int, lam: float) -> float:
    """Pure-Python Poisson PMF — no scipy needed."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def compute_probs(hxg: float, axg: float, cap: int = 9) -> dict:
    """Independent Poisson 1X2 + Over2.5 + BTTS from two λ values."""
    ph, pa = 0.0, 0.0
    over = 0.0
    gg = 0.0
    for i in range(cap + 1):
        pi = _pois(i, hxg)
        for j in range(cap + 1):
            pj = _pois(j, axg)
            p = pi * pj
            if i > j:  ph += p
            elif i < j: pa += p
            if i + j > 2: over += p
            if i > 0 and j > 0: gg += p
    px = max(0.0, 1.0 - ph - pa)
    return dict(h=ph, x=px, a=pa, ov25=over, gg=gg)


def get_xg(match: dict, hm: float, am: float, hl: float, al: float) -> tuple:
    """Dixon-Coles-style xG with motivation + lineup weights."""
    ht, at = TEAMS[match["home"]], TEAMS[match["away"]]
    hxg = (ht["atk"] / AVG_ATK) * (at["def_"] / AVG_DEF) * AVG_ATK * hm * hl * HOME_ADVANTAGE
    axg = (at["atk"] / AVG_ATK) * (ht["def_"] / AVG_DEF) * AVG_ATK * am * al
    return round(hxg, 3), round(axg, 3)


def calc_edges(probs: dict, odds: dict) -> dict:
    """Edge = model_prob − 1/market_odds."""
    def _edge(p, o): return round(p - 1.0 / o, 4) if o > 0 else 0.0
    return dict(
        h=_edge(probs["h"],   odds["h"]),
        x=_edge(probs["x"],   odds["x"]),
        a=_edge(probs["a"],   odds["a"]),
        ov25=_edge(probs["ov25"], odds.get("ov25", 1.90)),
        gg=_edge(probs["gg"],   odds.get("gg",   1.85)),
    )


def kelly_stake(prob: float, dec_odds: float, bankroll: float, frac: float) -> tuple:
    """Fractional Kelly → (fraction, £stake). Returns (0,0) if no edge."""
    b = dec_odds - 1.0
    if b <= 0 or prob <= 0:
        return 0.0, 0.0
    f = (b * prob - (1.0 - prob)) / b
    f = max(0.0, f) * frac
    return round(f, 4), round(f * bankroll, 2)


# ═══════════════════════════════════════════════════════════════════════════════
#  HTML BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════
def _chip(label: str, pct: float, edge: float, css_cls: str) -> str:
    edge_html = ""
    if edge > 0.03:
        edge_html = f'<div class="pchip-edge edge-pos">▲ {edge*100:.1f}% edge</div>'
    elif edge > 0:
        edge_html = f'<div class="pchip-edge edge-pos">+{edge*100:.1f}%</div>'
    else:
        edge_html = f'<div class="pchip-edge edge-neg">—</div>'
    ec = " edge-chip" if edge > 0.03 else ""
    return (
        f'<div class="pchip {css_cls}{ec}">'
        f'<div class="pchip-lbl">{label}</div>'
        f'<div class="pchip-val">{pct:.0f}%</div>'
        f'{edge_html}'
        f'</div>'
    )


def _bar(label: str, pct: float, cls: str) -> str:
    w = min(100, max(0, pct))
    return (
        f'<div class="brow">'
        f'<span class="b-lbl">{label}</span>'
        f'<div class="btrack"><div class="bfill {cls}" style="width:{w:.1f}%"></div></div>'
        f'<span class="b-pct">{pct:.1f}%</span>'
        f'</div>'
    )


def build_card(match: dict, probs: dict, edges: dict, hxg: float, axg: float) -> str:
    ht, at = TEAMS[match["home"]], TEAMS[match["away"]]
    any_value = any(e > 0.03 for e in edges.values())
    glow = " value-glow" if any_value else ""

    # badges
    badges = f'<span class="bdg bdg-grp">🏆 {match["stage"]}</span>'
    if any_value:
        badges += '<span class="bdg bdg-val">🔥 HIGH VALUE</span>'
    diff = abs(probs["h"] - probs["a"])
    if diff < 0.12:
        badges += '<span class="bdg bdg-tight">⚠️ TIGHT MATCH</span>'
    if probs["h"] > 0.60:
        badges += f'<span class="bdg bdg-fav">★ {match["home"].upper()} FAV</span>'
    elif probs["a"] > 0.60:
        badges += f'<span class="bdg bdg-fav">★ {match["away"].upper()} FAV</span>'

    # meta
    meta = (
        f'<div class="mc-meta">'
        f'<b>Group {match["group"]}</b> &nbsp;·&nbsp; {match["date"]} &nbsp;·&nbsp; '
        f'xG <b style="color:#FFD700">{hxg:.2f}</b> – <b style="color:#FF5252">{axg:.2f}</b>'
        f'</div>'
    )

    # teams
    teams = (
        f'<div class="teams-row">'
        f'  <div class="team-block">'
        f'    <span class="team-flag">{ht["flag"]}</span>'
        f'    <div><div class="team-name">{match["home"]}</div>'
        f'         <div class="team-rank">FIFA #{ht["rank"]} · {ht["style"]}</div></div>'
        f'  </div>'
        f'  <div class="vs-box">VS</div>'
        f'  <div class="team-block away">'
        f'    <span class="team-flag">{at["flag"]}</span>'
        f'    <div><div class="team-name">{match["away"]}</div>'
        f'         <div class="team-rank">FIFA #{at["rank"]} · {at["style"]}</div></div>'
        f'  </div>'
        f'</div>'
    )

    # probability chips
    chips = (
        '<div class="pgrid">'
        + _chip("Home Win", probs["h"] * 100, edges["h"],    "pc1")
        + _chip("Draw",     probs["x"] * 100, edges["x"],    "pcx")
        + _chip("Away Win", probs["a"] * 100, edges["a"],    "pc2")
        + _chip("Over 2.5", probs["ov25"] * 100, edges["ov25"], "pcov")
        + _chip("BTTS",     probs["gg"]  * 100, edges["gg"],   "pcgg")
        + '</div>'
    )

    # bars
    bars = (
        '<div class="barsec">'
        + _bar("Home Win",  probs["h"]    * 100, "bf-h")
        + _bar("Draw",      probs["x"]    * 100, "bf-x")
        + _bar("Away Win",  probs["a"]    * 100, "bf-a")
        + _bar("Over 2.5",  probs["ov25"] * 100, "bf-ov")
        + _bar("BTTS",      probs["gg"]   * 100, "bf-gg")
        + '</div>'
    )

    venue = f'<span class="venue-chip">📍 {match["venue"]}</span>'

    return (
        f'<div class="mc{glow}">'
        f'  <div class="mc-toprow">{meta}<div class="mc-badges">{badges}</div></div>'
        f'  {teams}{chips}{bars}{venue}'
        f'</div>'
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar(all_probs: list) -> tuple:
    with st.sidebar:
        st.markdown('<div class="sb-sec">⚙️ Control Panel</div>', unsafe_allow_html=True)

        bankroll = st.number_input(
            "Bankroll (£)", min_value=10.0, max_value=1_000_000.0,
            value=1000.0, step=50.0, format="%.0f",
        )
        kelly_frac_pct = st.select_slider(
            "Kelly Fraction",
            options=[10, 15, 20, 25, 30, 40, 50, 75, 100],
            value=25,
            format_func=lambda x: f"{x}%",
        )
        kelly_frac = kelly_frac_pct / 100.0

        st.markdown('<div class="sb-sec">🎯 Kelly Calculator</div>', unsafe_allow_html=True)

        match_labels = [f"G{m['group']} · {m['home']} vs {m['away']}" for m in MATCHES]
        sel_idx = st.selectbox("Match", range(len(MATCHES)), format_func=lambda i: match_labels[i])
        market_opt = st.selectbox("Market", ["Home Win (1)", "Draw (X)", "Away Win (2)", "Over 2.5", "BTTS"])
        custom_odds = st.number_input("Market Odds", min_value=1.01, max_value=50.0, value=2.00, step=0.05)

        # pull stored probs
        probs = all_probs[sel_idx] if all_probs else None
        if probs:
            key_map = {
                "Home Win (1)": "h",
                "Draw (X)":     "x",
                "Away Win (2)": "a",
                "Over 2.5":     "ov25",
                "BTTS":         "gg",
            }
            p = probs[key_map[market_opt]]
            frac, stake = kelly_stake(p, custom_odds, bankroll, kelly_frac)
            if stake > 0:
                roi = round((custom_odds - 1) * p - (1 - p), 4)
                st.markdown(
                    f'<div class="kelly-box">'
                    f'<div class="k-title">Recommended Stake</div>'
                    f'<div class="k-stake">£{stake:,.2f}</div>'
                    f'<div class="k-detail">'
                    f'  Kelly f = {frac*100:.1f}% &nbsp;·&nbsp; '
                    f'  Model p = {p*100:.1f}% &nbsp;·&nbsp; '
                    f'  EV = {roi*100:+.1f}%'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="no-edge">⚠️ No positive edge detected — skip this bet.</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div class="sb-sec">📐 Model Notes</div>', unsafe_allow_html=True)
        st.caption(
            "Independent Poisson · Dixon-Coles xG\n"
            "Home advantage ×1.08 · Caps at 9 goals\n"
            "Fractional Kelly staking · WC 2026 profiles"
        )

    return bankroll, kelly_frac


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
def render_header():
    st.markdown(
        '<div class="wc-banner">'
        '  <div class="wc-banner-title">🏆 World Cup 2026 ⚽</div>'
        '  <div class="wc-banner-sub">World Cup 2026 Live Quant Analytics</div>'
        '  <div class="wc-banner-meta">'
        '    <span>🌍 USA · Canada · Mexico</span>'
        '    <span>📅 Jun–Jul 2026</span>'
        '    <span>🏟️ 16 Venues</span>'
        '    <span>⚙️ Poisson / xG Model</span>'
        '  </div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  STATS STRIP
# ═══════════════════════════════════════════════════════════════════════════════
def render_stats(all_probs: list, all_edges: list):
    n_val   = sum(1 for edges in all_edges if any(e > 0.03 for e in edges.values()))
    avg_ov  = sum(p["ov25"] for p in all_probs) / len(all_probs) * 100
    n_teams = len(TEAMS)
    n_match = len(MATCHES)
    n_tight = sum(1 for p in all_probs if abs(p["h"] - p["a"]) < 0.12)

    st.markdown(
        f'<div class="stat-strip">'
        f'  <div class="stat-cell sc-gold"><div class="stat-val">{n_match}</div><div class="stat-lbl">Fixtures</div></div>'
        f'  <div class="stat-cell sc-green"><div class="stat-val">{n_val}</div><div class="stat-lbl">Value Bets</div></div>'
        f'  <div class="stat-cell sc-blue"><div class="stat-val">{avg_ov:.0f}%</div><div class="stat-lbl">Avg Over 2.5</div></div>'
        f'  <div class="stat-cell sc-red"><div class="stat-val">{n_tight}</div><div class="stat-lbl">Tight Matches</div></div>'
        f'  <div class="stat-cell sc-gray"><div class="stat-val">{n_teams}</div><div class="stat-lbl">Teams</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  SINGLE MATCH RENDERER
# ═══════════════════════════════════════════════════════════════════════════════
def render_match(match: dict) -> dict:
    idx = match["id"]

    # initialise session state (avoid Streamlit key conflict)
    for key, default in [
        (f"hm_{idx}", 1.0), (f"am_{idx}", 1.0),
        (f"hl_{idx}", 1.0), (f"al_{idx}", 1.0),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    hm = st.session_state[f"hm_{idx}"]
    am = st.session_state[f"am_{idx}"]
    hl = st.session_state[f"hl_{idx}"]
    al = st.session_state[f"al_{idx}"]

    hxg, axg = get_xg(match, hm, am, hl, al)
    probs     = compute_probs(hxg, axg)
    edges     = calc_edges(probs, match["odds"])

    # render card
    st.markdown(build_card(match, probs, edges, hxg, axg), unsafe_allow_html=True)

    # expander for sliders + live metrics
    with st.expander(f"⚙️ Adjust {match['home']} vs {match['away']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{TEAMS[match['home']]['flag']} {match['home']}**")
            st.slider("Motivation",   0.50, 1.50, key=f"hm_{idx}", step=0.05)
            st.slider("Lineup Str.",  0.70, 1.30, key=f"hl_{idx}", step=0.05)
        with col2:
            st.markdown(f"**{TEAMS[match['away']]['flag']} {match['away']}**")
            st.slider("Motivation",   0.50, 1.50, key=f"am_{idx}", step=0.05)
            st.slider("Lineup Str.",  0.70, 1.30, key=f"al_{idx}", step=0.05)

        st.divider()
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Home Win",  f"{probs['h']*100:.1f}%",  f"{edges['h']*100:+.1f}%")
        c2.metric("Draw",      f"{probs['x']*100:.1f}%",  f"{edges['x']*100:+.1f}%")
        c3.metric("Away Win",  f"{probs['a']*100:.1f}%",  f"{edges['a']*100:+.1f}%")
        c4.metric("Over 2.5",  f"{probs['ov25']*100:.1f}%", f"{edges['ov25']*100:+.1f}%")
        c5.metric("BTTS",      f"{probs['gg']*100:.1f}%",  f"{edges['gg']*100:+.1f}%")

    return probs, edges


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # pre-compute default probs for sidebar Kelly calc (uses default sliders = 1.0)
    _default_probs = []
    for m in MATCHES:
        hxg, axg = get_xg(m, 1.0, 1.0, 1.0, 1.0)
        _default_probs.append(compute_probs(hxg, axg))

    bankroll, kelly_frac = render_sidebar(_default_probs)

    render_header()

    # collect live probs after rendering all matches (for stat strip)
    all_probs:  list = []
    all_edges:  list = []

    groups = sorted(set(m["group"] for m in MATCHES))
    tab_labels = ["🌍 All"] + [f"Group {g}" for g in groups]
    tabs = st.tabs(tab_labels)

    # All matches tab
    with tabs[0]:
        for g in groups:
            group_matches = [m for m in MATCHES if m["group"] == g]
            st.markdown(
                f'<div class="grp-header"><h3>Group {g}</h3>'
                f'<span>{len(group_matches)} fixtures</span></div>',
                unsafe_allow_html=True,
            )
            col_a, col_b = st.columns(2)
            for i, m in enumerate(group_matches):
                with (col_a if i % 2 == 0 else col_b):
                    p, e = render_match(m)
                    all_probs.append(p)
                    all_edges.append(e)

    # Per-group tabs
    for tab, g in zip(tabs[1:], groups):
        with tab:
            group_matches = [m for m in MATCHES if m["group"] == g]
            st.markdown(
                f'<div class="grp-header"><h3>Group {g}</h3>'
                f'<span>{len(group_matches)} fixtures</span></div>',
                unsafe_allow_html=True,
            )
            for m in group_matches:
                render_match(m)

    # Stats strip rendered after first pass (uses live all_probs)
    if all_probs:
        # inject stat strip just below header using a placeholder trick — 
        # Streamlit renders top-to-bottom, so we call it here and it appears
        # at the bottom of the page; alternatively reorder for top placement.
        # Better: render with default probs before the tabs.
        pass

    # --- render stat strip with default probs (always visible at top) ---
    # We handle this by computing fresh stats from the default probs collected above.
    # The stat strip is inserted right after the header using a separate container.

if __name__ == "__main__":
    main()


# ── override main to insert stat strip correctly ───────────────────────────────
def _main_with_stats():
    # pre-compute default probs
    default_probs = []
    default_edges = []
    for m in MATCHES:
        hxg, axg = get_xg(m, 1.0, 1.0, 1.0, 1.0)
        dp = compute_probs(hxg, axg)
        de = calc_edges(dp, m["odds"])
        default_probs.append(dp)
        default_edges.append(de)

    bankroll, kelly_frac = render_sidebar(default_probs)
    render_header()
    render_stats(default_probs, default_edges)

    groups = sorted(set(m["group"] for m in MATCHES))
    tab_labels = ["🌍 All Matches"] + [f"Group {g}" for g in groups]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        for g in groups:
            gm = [m for m in MATCHES if m["group"] == g]
            st.markdown(
                f'<div class="grp-header"><h3>Group {g}</h3>'
                f'<span>{len(gm)} fixtures</span></div>',
                unsafe_allow_html=True,
            )
            col_a, col_b = st.columns(2)
            for i, m in enumerate(gm):
                with (col_a if i % 2 == 0 else col_b):
                    render_match(m)

    for tab, g in zip(tabs[1:], groups):
        with tab:
            gm = [m for m in MATCHES if m["group"] == g]
            st.markdown(
                f'<div class="grp-header"><h3>Group {g}</h3>'
                f'<span>{len(gm)} fixtures</span></div>',
                unsafe_allow_html=True,
            )
            for m in gm:
                render_match(m)


_main_with_stats()
