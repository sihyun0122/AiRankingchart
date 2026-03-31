import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="2026 수능 선택과목 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700;900&family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: #eef0ff !important; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 55% at 0%   0%,   rgba(139,92,246,0.16) 0%, transparent 52%),
        radial-gradient(ellipse 65% 45% at 100% 0%,   rgba(6,182,212,0.14)  0%, transparent 52%),
        radial-gradient(ellipse 55% 40% at 55%  100%, rgba(16,185,129,0.11) 0%, transparent 52%),
        radial-gradient(ellipse 45% 35% at 80%  55%,  rgba(245,158,11,0.09) 0%, transparent 52%),
        #eef0ff !important;
}
[data-testid="stHeader"]     { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 0 2.5rem 6rem !important; max-width: 1320px !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e5e7ff; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 10px; }

/* ══ HERO ══ */
.hero {
    padding: 5rem 0 3.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-wm {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    font-family: 'Unbounded', sans-serif;
    font-size: clamp(60px,12vw,180px);
    font-weight: 900;
    color: rgba(99,102,241,0.055);
    white-space: nowrap;
    letter-spacing: 0.06em;
    pointer-events: none;
    animation: wmPulse 6s ease-in-out infinite alternate;
}
@keyframes wmPulse {
    from { transform: translate(-50%,-50%) scale(1);    opacity:.7; }
    to   { transform: translate(-50%,-50%) scale(1.04); opacity:1; }
}
.hero-pill {
    display: inline-flex; align-items: center; gap: .45rem;
    background: rgba(99,102,241,0.1);
    border: 1.5px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    padding: .38rem 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .67rem; letter-spacing: .18em;
    color: #4f46e5; text-transform: uppercase;
    margin-bottom: 1.4rem;
    animation: popIn .7s cubic-bezier(.34,1.56,.64,1) both;
}
.pill-dot {
    width: 7px; height: 7px;
    background: #6366f1; border-radius: 50%;
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.25;} }
@keyframes popIn {
    from { opacity:0; transform: scale(.7) translateY(-8px); }
    to   { opacity:1; transform: scale(1)  translateY(0); }
}
.hero-title {
    font-family: 'Unbounded', sans-serif;
    font-size: clamp(2.4rem,5.5vw,5.2rem);
    font-weight: 900;
    line-height: .95;
    color: #1e1b4b;
    margin-bottom: .7rem;
    animation: slideUp .8s ease .1s both;
}
.hero-title .grad {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 40%, #ec4899 70%, #f59e0b 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: gradAnim 5s ease infinite;
}
@keyframes gradAnim {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
.hero-sub {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: .92rem; color: rgba(30,27,75,.45);
    letter-spacing: .03em;
    animation: slideUp .8s ease .2s both;
}
@keyframes slideUp {
    from { opacity:0; transform: translateY(18px); }
    to   { opacity:1; transform: translateY(0); }
}
.hero-emojis {
    font-size: 1.8rem; letter-spacing: .5em;
    margin-bottom: .9rem;
    animation: slideUp .8s ease .05s both;
}

/* ══ NEON DIVIDER ══ */
.ndiv {
    position: relative; height: 2px; margin: .6rem 0 2.4rem;
    background: linear-gradient(90deg,
        transparent 0%, #6366f1 25%, #a855f7 50%, #ec4899 75%, transparent 100%);
    border-radius: 2px;
    box-shadow: 0 0 12px rgba(139,92,246,.5), 0 0 24px rgba(139,92,246,.2);
    animation: divGlow 3s ease-in-out infinite;
}
@keyframes divGlow {
    0%,100% { opacity:.7; box-shadow: 0 0 10px rgba(139,92,246,.4); }
    50%      { opacity:1;  box-shadow: 0 0 22px rgba(139,92,246,.7), 0 0 40px rgba(139,92,246,.3); }
}
.ndiv::after {
    content: ''; position: absolute;
    inset: -2px 0; background: inherit;
    filter: blur(6px); opacity: .5;
}

.sec-div {
    display: flex; align-items: center; gap: 1rem;
    margin: .5rem 0 2.2rem;
}
.sec-div::before, .sec-div::after {
    content: ''; flex: 1; height: 1.5px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,.35), transparent);
}
.sec-div span {
    font-family: 'JetBrains Mono', monospace;
    font-size: .67rem; letter-spacing: .22em;
    color: rgba(99,102,241,.8); text-transform: uppercase; white-space: nowrap;
}

/* ══ STAT CARDS ══ */
.stat-row { display: flex; gap: 1rem; margin-bottom: 2.6rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 190px;
    background: #fff;
    border: 1.5px solid rgba(99,102,241,.12);
    border-radius: 16px;
    padding: 1.6rem 1.4rem 1.4rem;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 24px rgba(99,102,241,.08), 0 1px 4px rgba(0,0,0,.06);
    transition: transform .22s, box-shadow .22s;
    animation: cardUp .6s ease both;
}
@keyframes cardUp {
    from { opacity:0; transform: translateY(22px); }
    to   { opacity:1; transform: translateY(0); }
}
.stat-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 12px 36px rgba(99,102,241,.16), 0 2px 8px rgba(0,0,0,.08);
}
.stat-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
}
.stat-card::after {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 35% at 50% 0%, rgba(255,255,255,.8), transparent);
    pointer-events: none;
}
.stat-card.c1::before { background: linear-gradient(90deg, #6366f1, #a855f7); }
.stat-card.c2::before { background: linear-gradient(90deg, #06b6d4, #0ea5e9); }
.stat-card.c3::before { background: linear-gradient(90deg, #10b981, #84cc16); }
.stat-card.c4::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }

.stat-card .s-emoji { font-size: 1.8rem; margin-bottom: .5rem; display: block; }
.stat-card .s-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .6rem; letter-spacing: .2em;
    color: rgba(30,27,75,.38); text-transform: uppercase; margin-bottom: .35rem;
}
.stat-card .s-num {
    font-family: 'Unbounded', sans-serif;
    font-size: 2rem; font-weight: 900; line-height: 1; letter-spacing: -.02em;
}
.stat-card.c1 .s-num { color: #6366f1; }
.stat-card.c2 .s-num { color: #0891b2; }
.stat-card.c3 .s-num { color: #059669; }
.stat-card.c4 .s-num { color: #d97706; }
.stat-card .s-sub {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: .7rem; color: rgba(30,27,75,.35); margin-top: .3rem;
}
.stat-card .s-badge {
    display: inline-block;
    margin-top: .5rem;
    padding: .18rem .55rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .6rem; letter-spacing: .08em; font-weight: 700;
}
.badge-up   { background: rgba(16,185,129,.12); color: #059669; }
.badge-down { background: rgba(239,68,68,.1);   color: #dc2626; }
.badge-new  { background: rgba(99,102,241,.12); color: #4f46e5; }

/* ══ SECTION HEADER ══ */
.sh { margin-bottom: 1rem; }
.sh-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: .62rem; letter-spacing: .25em;
    color: rgba(99,102,241,.75); text-transform: uppercase; margin-bottom: .3rem;
}
.sh-title {
    font-family: 'Unbounded', sans-serif;
    font-size: 1.4rem; font-weight: 700;
    color: #1e1b4b; letter-spacing: -.01em;
}

/* ══ INSIGHT BADGES ══ */
.ib-row { display: flex; gap: .55rem; flex-wrap: wrap; margin-bottom: 2rem; }
.ib {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: .75rem; font-weight: 500;
    padding: .4rem 1rem; border-radius: 999px; border: 1.5px solid;
    letter-spacing: .01em;
    transition: transform .15s, box-shadow .15s;
    animation: ibPop .5s cubic-bezier(.34,1.56,.64,1) both;
    backdrop-filter: blur(4px);
}
.ib:hover { transform: translateY(-2px) scale(1.04); box-shadow: 0 4px 16px rgba(0,0,0,.1); }
@keyframes ibPop { from{opacity:0;transform:scale(.8);} to{opacity:1;transform:scale(1);} }
.ib-v  { color: #4f46e5; border-color: rgba(99,102,241,.35);  background: rgba(99,102,241,.07); }
.ib-c  { color: #0369a1; border-color: rgba(6,182,212,.35);   background: rgba(6,182,212,.07); }
.ib-g  { color: #065f46; border-color: rgba(16,185,129,.35);  background: rgba(16,185,129,.07); }
.ib-a  { color: #92400e; border-color: rgba(245,158,11,.35);  background: rgba(245,158,11,.07); }
.ib-p  { color: #7c2d92; border-color: rgba(168,85,247,.35);  background: rgba(168,85,247,.07); }
.ib-r  { color: #991b1b; border-color: rgba(239,68,68,.35);   background: rgba(239,68,68,.07); }

/* ══ CHART GLASS CARD ══ */
.gc {
    background: rgba(255,255,255,.75);
    border: 1.5px solid rgba(99,102,241,.1);
    border-radius: 16px;
    padding: .6rem;
    box-shadow: 0 4px 24px rgba(99,102,241,.07), 0 1px 4px rgba(0,0,0,.05);
    backdrop-filter: blur(12px);
    transition: box-shadow .25s;
    margin-bottom: .3rem;
}
.gc:hover { box-shadow: 0 8px 40px rgba(99,102,241,.14), 0 2px 8px rgba(0,0,0,.07); }

/* ══ TREND ARROW ══ */
.up   { color: #059669; font-weight: 700; }
.down { color: #dc2626; font-weight: 700; }

/* ══ FOOTER ══ */
.footer {
    text-align: center;
    padding: 2.5rem 0 .5rem;
    border-top: 1.5px solid rgba(99,102,241,.12);
    margin-top: 2rem;
}
.footer-emojis { font-size: 1.3rem; letter-spacing: .3em; margin-bottom: .5rem; }
.footer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: .62rem; letter-spacing: .15em;
    color: rgba(30,27,75,.3); text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────
BG    = "rgba(255,255,255,0)"
BGC   = "rgba(255,255,255,0.75)"
GRID  = "rgba(99,102,241,0.08)"
FONT  = "Noto Sans KR, sans-serif"
MFONT = "JetBrains Mono, monospace"
UFONT = "Unbounded, sans-serif"

V = "#6366f1"; C = "#22d3ee"; G = "#10b981"
A = "#f59e0b"; R = "#f87171"; P = "#a855f7"
PK= "#ec4899"; T = "#1e1b4b"

# ── DATA ─────────────────────────────────────────────────────────────
# 출처: 한국교육과정평가원 2025·2026학년도 수능 채점 결과
korean25 = {"화법과 작문": 290_888, "언어와 매체": 170_364}
korean26 = {"화법과 작문": 333_283, "언어와 매체": 157_706}

math25   = {"확률과 통계": 202_266, "미적분": 227_232, "기하": 13_735}
math26   = {"확률과 통계": 264_307, "미적분": 193_475, "기하": 13_623}

satam25  = {
    "사회·문화": 185_014, "생활과 윤리": 183_441, "윤리와 사상": 47_391,
    "한국지리":   40_850,  "정치와 법":   34_706,  "세계지리":   34_333,
    "동아시아사": 20_394,  "세계사":      18_328,  "경제":        7_353,
}
satam26  = {
    "사회·문화": 239_403, "생활과 윤리": 196_382, "윤리와 사상": 46_145,
    "한국지리":   42_518,  "세계지리":    41_655,  "정치와 법":   33_123,
    "동아시아사": 20_507,  "세계사":      19_884,  "경제":         7_085,
}
gwatam25 = {
    "지구과학Ⅰ": 153_987, "생명과학Ⅰ": 141_027, "물리학Ⅰ":  63_740,
    "화학Ⅰ":      48_758, "생명과학Ⅱ":   8_214, "화학Ⅱ":     6_343,
    "물리학Ⅱ":     6_241, "지구과학Ⅱ":   5_196,
}
gwatam26 = {
    "지구과학Ⅰ": 106_729, "생명과학Ⅰ": 102_836, "물리학Ⅰ":  42_232,
    "화학Ⅰ":      23_321, "생명과학Ⅱ":   7_279, "화학Ⅱ":     5_242,
    "물리학Ⅱ":     5_236, "지구과학Ⅱ":   4_264,
}

k_total26  = sum(korean26.values())
m_total26  = sum(math26.values())
s_total26  = sum(satam26.values())
g_total26  = sum(gwatam26.values())

# ── HELPERS ──────────────────────────────────────────────────────────
def pct_change(a, b): return (b - a) / a * 100

def L(h=360, extra=None):
    d = dict(
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        height=h, showlegend=False,
        font=dict(family=FONT, color="rgba(30,27,75,.45)", size=11),
        margin=dict(t=30, b=15, l=10, r=10),
    )
    if extra: d.update(extra)
    return d

def xv(sz=12, col=None):
    return dict(
        showgrid=False, zeroline=False,
        linecolor="rgba(99,102,241,.12)",
        tickfont=dict(color=col or "rgba(30,27,75,.75)", size=sz, family=FONT),
    )

def yv(suf="", mx=None, vis=True):
    d = dict(
        showgrid=vis, gridcolor=GRID, zeroline=False, visible=vis,
        tickfont=dict(color="rgba(30,27,75,.3)", size=10),
    )
    if suf: d["ticksuffix"] = suf
    if mx:  d["range"] = [0, mx]
    return d

def yh():
    return dict(
        showgrid=False, zeroline=False, autorange="reversed",
        tickfont=dict(color="rgba(30,27,75,.75)", size=11, family=FONT),
    )

def xh(mx=None):
    d = dict(showgrid=True, gridcolor=GRID, zeroline=False,
             tickfont=dict(color="rgba(30,27,75,.3)", size=10))
    if mx: d["range"] = [0, mx]
    return d

def arrow(v25, v26):
    d = v26 - v25
    p = pct_change(v25, v26)
    s = "▲" if d > 0 else "▼"
    c = "up" if d > 0 else "down"
    return f'<span class="{c}">{s} {abs(p):.1f}%</span>'

# ── HERO ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-wm">2026 CSAT</div>
  <div style="text-align:center">
    <span class="hero-pill"><span class="pill-dot"></span> 한국교육과정평가원 공식 통계 · 2025.12.04</span>
  </div>
  <div class="hero-emojis">📚 🧮 🌍 🔬</div>
  <div class="hero-title">
    2026 수능<br><span class="grad">선택과목 완전분석</span>
  </div>
  <div class="hero-sub" style="margin-top:.6rem">
    총 응시자 493,896명 &nbsp;·&nbsp; 전년 대비 변화 추이 포함 &nbsp;·&nbsp; 국어 · 수학 · 사탐 9과목 · 과탐 8과목
  </div>
</div>
<div class="ndiv"></div>
""", unsafe_allow_html=True)

# ── STAT CARDS ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
  <div class="stat-card c1" style="animation-delay:.0s">
    <span class="s-emoji">🎓</span>
    <div class="s-label">총 응시자</div>
    <div class="s-num">493,896</div>
    <div class="s-sub">재학생 333,102 · 졸업생 160,794</div>
    <span class="s-badge badge-up">▲ +30,410명 전년比</span>
  </div>
  <div class="stat-card c2" style="animation-delay:.08s">
    <span class="s-emoji">📖</span>
    <div class="s-label">사탐만 선택</div>
    <div class="s-num">284,535</div>
    <div class="s-sub">이과생 사탐 대이동</div>
    <span class="s-badge badge-up">▲ +18.6% 전년比</span>
  </div>
  <div class="stat-card c3" style="animation-delay:.16s">
    <span class="s-emoji">🔬</span>
    <div class="s-label">과탐만 선택</div>
    <div class="s-num">108,353</div>
    <div class="s-sub">역대급 감소</div>
    <span class="s-badge badge-down">▼ −53.5% 전년比</span>
  </div>
  <div class="stat-card c4" style="animation-delay:.24s">
    <span class="s-emoji">🔀</span>
    <div class="s-label">사탐+과탐 혼합</div>
    <div class="s-num">81,023</div>
    <div class="s-sub">사탐런 직격탄</div>
    <span class="s-badge badge-up">▲ +69.8% 전년比</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-div"><span>📝 국어 선택과목</span></div>', unsafe_allow_html=True)

# ══════════════════════════════
# 국어
# ══════════════════════════════
col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown('<div class="sh"><div class="sh-tag">// 01</div><div class="sh-title">📝 국어 — 2025 vs 2026 비교</div></div>', unsafe_allow_html=True)
    k_names = list(korean26.keys())
    k25 = [korean25[n] for n in k_names]
    k26 = [korean26[n] for n in k_names]
    k_cols = [V, PK]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="2025", x=k_names, y=k25,
        marker=dict(color=[f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},.3)" for c in k_cols], line=dict(width=0)),
        width=0.28, offset=-0.17,
        text=[f"{v:,}" for v in k25],
        textposition="outside",
        textfont=dict(size=11, color="rgba(30,27,75,.45)", family=FONT),
        hovertemplate="%{x} 2025<br><b>%{y:,}명</b><extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="2026", x=k_names, y=k26,
        marker=dict(color=k_cols, line=dict(width=0)),
        width=0.28, offset=0.13,
        text=[f"{v:,}" for v in k26],
        textposition="outside",
        textfont=dict(size=11, color=k_cols, family=FONT),
        hovertemplate="%{x} 2026<br><b>%{y:,}명</b><extra></extra>",
    ))
    lo = L(330)
    lo["xaxis"] = xv(13); lo["yaxis"] = yv(mx=420000); lo["bargap"] = 0.3
    lo["showlegend"] = True
    lo["legend"] = dict(orientation="h", x=1, xanchor="right", y=1.12,
                        font=dict(size=11, color="rgba(30,27,75,.6)"), bgcolor="rgba(0,0,0,0)")
    fig.update_layout(lo)
    st.markdown('<div class="gc">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="sh"><div class="sh-tag">// 02</div><div class="sh-title">📝 국어 점유율 (2026)</div></div>', unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=k_names,
        values=k26, hole=0.6,
        marker=dict(colors=k_cols, line=dict(color="#eef0ff", width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family=FONT),
        pull=[0.06, 0], rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo2 = L(330)
    lo2["annotations"] = [dict(text="국어<br>2026", x=0.5, y=0.5, showarrow=False,
                               font=dict(color="#1e1b4b", family=UFONT, size=13))]
    fig2.update_layout(lo2)
    st.markdown('<div class="gc">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="ib-row">
  <div class="ib ib-v">📝 화법과 작문 333,283명 — 67.9% 압도적 1위</div>
  <div class="ib ib-p">🔼 전년比 {arrow(290888,333283)} — 42,395명 폭증</div>
  <div class="ib ib-r">언어와 매체 {arrow(170364,157706)} — 12,658명 감소</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-div"><span>🧮 수학 선택과목</span></div>', unsafe_allow_html=True)

# ══════════════════════════════
# 수학
# ══════════════════════════════
col3, col4 = st.columns([3, 2], gap="medium")

with col3:
    st.markdown('<div class="sh"><div class="sh-tag">// 03</div><div class="sh-title">🧮 수학 — 2025 vs 2026 비교</div></div>', unsafe_allow_html=True)
    m_names = list(math26.keys())
    m25 = [math25[n] for n in m_names]
    m26 = [math26[n] for n in m_names]
    m_cols = [A, G, R]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name="2025", x=m_names, y=m25,
        marker=dict(color=[f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},.3)" for c in m_cols], line=dict(width=0)),
        width=0.28, offset=-0.17,
        text=[f"{v:,}" for v in m25],
        textposition="outside",
        textfont=dict(size=11, color="rgba(30,27,75,.45)", family=FONT),
        hovertemplate="%{x} 2025<br><b>%{y:,}명</b><extra></extra>",
    ))
    fig3.add_trace(go.Bar(
        name="2026", x=m_names, y=m26,
        marker=dict(color=m_cols, line=dict(width=0)),
        width=0.28, offset=0.13,
        text=[f"{v:,}" for v in m26],
        textposition="outside",
        textfont=dict(size=11, color=m_cols, family=FONT),
        hovertemplate="%{x} 2026<br><b>%{y:,}명</b><extra></extra>",
    ))
    lo3 = L(330)
    lo3["xaxis"] = xv(13); lo3["yaxis"] = yv(mx=360000); lo3["bargap"] = 0.3
    lo3["showlegend"] = True
    lo3["legend"] = dict(orientation="h", x=1, xanchor="right", y=1.12,
                         font=dict(size=11, color="rgba(30,27,75,.6)"), bgcolor="rgba(0,0,0,0)")
    fig3.update_layout(lo3)
    st.markdown('<div class="gc">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="sh"><div class="sh-tag">// 04</div><div class="sh-title">🧮 수학 점유율 (2026)</div></div>', unsafe_allow_html=True)
    fig4 = go.Figure(go.Pie(
        labels=m_names, values=m26, hole=0.6,
        marker=dict(colors=m_cols, line=dict(color="#eef0ff", width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family=FONT),
        pull=[0.06, 0, 0], rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo4 = L(330)
    lo4["annotations"] = [dict(text="수학<br>2026", x=0.5, y=0.5, showarrow=False,
                               font=dict(color="#1e1b4b", family=UFONT, size=13))]
    fig4.update_layout(lo4)
    st.markdown('<div class="gc">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="ib-row">
  <div class="ib ib-a">🔄 확통 264,307명 — 56.1% · 미적분 역전! 2026 최대 이변</div>
  <div class="ib ib-r">미적분 {arrow(227232,193475)} — 33,757명 급감</div>
  <div class="ib ib-g">확통 {arrow(202266,264307)} — 62,041명 폭증</div>
  <div class="ib ib-v">기하 13,623명 — 역대 최저 수준 (2.89%)</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-div"><span>📖 사회탐구 9과목</span></div>', unsafe_allow_html=True)

# ══════════════════════════════
# 사탐 가로 바 + 추이
# ══════════════════════════════
st.markdown('<div class="sh"><div class="sh-tag">// 05</div><div class="sh-title">📖 사탐 9과목 — 2025 vs 2026 응시인원</div></div>', unsafe_allow_html=True)

s_names_ord = sorted(satam26.keys(), key=lambda x: satam26[x])
s25 = [satam25[n] for n in s_names_ord]
s26 = [satam26[n] for n in s_names_ord]
s_pcts26 = [v/s_total26*100 for v in s26]
s_cols = ["#f87171","#fb923c","#fbbf24","#a3e635","#34d399","#22d3ee","#60a5fa","#818cf8","#c084fc"]

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    name="2025", x=s25, y=s_names_ord, orientation="h",
    marker=dict(color="rgba(148,163,184,.35)", line=dict(width=0)),
    text=[f"{v:,}" for v in s25],
    textposition="inside",
    textfont=dict(size=10, color="rgba(30,27,75,.5)", family=FONT),
    hovertemplate="%{y} 2025<br><b>%{x:,}명</b><extra></extra>",
))
fig5.add_trace(go.Bar(
    name="2026", x=s26, y=s_names_ord, orientation="h",
    marker=dict(color=s_cols, line=dict(width=0), opacity=0.88),
    text=[f"  {p:.1f}%  {v:,}명" for p, v in zip(s_pcts26, s26)],
    textposition="outside",
    textfont=dict(size=10.5, color="rgba(30,27,75,.65)", family=FONT),
    hovertemplate="%{y} 2026<br><b>%{x:,}명</b><extra></extra>",
))
lo5 = L(400)
lo5["barmode"] = "overlay"
lo5["yaxis"] = yh(); lo5["xaxis"] = xh(mx=max(s26)*1.38)
lo5["showlegend"] = True
lo5["legend"] = dict(orientation="h", x=1, xanchor="right", y=1.06,
                     font=dict(size=11, color="rgba(30,27,75,.6)"), bgcolor="rgba(0,0,0,0)")
lo5["margin"] = dict(t=30, b=15, l=5, r=185)
fig5.update_layout(lo5)
st.markdown('<div class="gc">', unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# 사탐 변화율 바
st.markdown('<div class="sh" style="margin-top:1.5rem"><div class="sh-tag">// 06</div><div class="sh-title">📈 사탐 과목별 전년 대비 변화율 (%)</div></div>', unsafe_allow_html=True)
s_chg = [pct_change(satam25[n], satam26[n]) for n in s_names_ord]
s_chg_cols = [G if v >= 0 else R for v in s_chg]

fig6 = go.Figure()
fig6.add_shape(type="line", x0=-len(s_names_ord), x1=len(s_names_ord),
               y0=0, y1=0, line=dict(color="rgba(30,27,75,.15)", width=1.5, dash="dot"))
fig6.add_trace(go.Bar(
    x=s_names_ord, y=s_chg,
    marker=dict(color=s_chg_cols, line=dict(width=0), opacity=0.85),
    text=[f"{'▲' if v>=0 else '▼'}{abs(v):.1f}%" for v in s_chg],
    textposition="outside",
    textfont=dict(size=11, color=s_chg_cols, family=FONT),
    width=0.6,
    hovertemplate="%{x}<br><b>%{y:+.1f}%</b><extra></extra>",
))
lo6 = L(300)
lo6["xaxis"] = xv(11); lo6["yaxis"] = yv(mx=35, vis=True); lo6["bargap"] = 0.3
lo6["yaxis"]["ticksuffix"] = "%"
lo6["yaxis"]["range"] = [min(s_chg)-5, max(s_chg)+8]
fig6.update_layout(lo6)
st.markdown('<div class="gc">', unsafe_allow_html=True)
st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="ib-row">
  <div class="ib ib-p">🏆 사회·문화 {arrow(185014,239403)} — 239,403명 압도적 1위</div>
  <div class="ib ib-v">생활과 윤리 {arrow(183441,196382)} — 2위 유지</div>
  <div class="ib ib-g">세계지리 {arrow(34333,41655)} — 가장 높은 증가율</div>
  <div class="ib ib-a">경제 {arrow(7353,7085)} — 사탐런 혜택 없는 유일 과목</div>
  <div class="ib ib-r">전 과목 사탐런 영향으로 동반 상승 (경제 제외)</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-div"><span>🔬 과학탐구 8과목</span></div>', unsafe_allow_html=True)

# ══════════════════════════════
# 과탐 가로 바 + 추이
# ══════════════════════════════
st.markdown('<div class="sh"><div class="sh-tag">// 07</div><div class="sh-title">🔬 과탐 8과목 — 2025 vs 2026 응시인원</div></div>', unsafe_allow_html=True)

g_names_ord = sorted(gwatam26.keys(), key=lambda x: gwatam26[x])
g25 = [gwatam25[n] for n in g_names_ord]
g26 = [gwatam26[n] for n in g_names_ord]
g_pcts26 = [v/g_total26*100 for v in g26]
g_cols = ["#f87171","#fb923c","#fbbf24","#a3e635","#34d399","#22d3ee","#60a5fa","#818cf8"]

fig7 = go.Figure()
fig7.add_trace(go.Bar(
    name="2025", x=g25, y=g_names_ord, orientation="h",
    marker=dict(color="rgba(148,163,184,.35)", line=dict(width=0)),
    text=[f"{v:,}" for v in g25],
    textposition="inside",
    textfont=dict(size=10, color="rgba(30,27,75,.5)", family=FONT),
    hovertemplate="%{y} 2025<br><b>%{x:,}명</b><extra></extra>",
))
fig7.add_trace(go.Bar(
    name="2026", x=g26, y=g_names_ord, orientation="h",
    marker=dict(color=g_cols, line=dict(width=0), opacity=0.88),
    text=[f"  {p:.1f}%  {v:,}명" for p, v in zip(g_pcts26, g26)],
    textposition="outside",
    textfont=dict(size=10.5, color="rgba(30,27,75,.65)", family=FONT),
    hovertemplate="%{y} 2026<br><b>%{x:,}명</b><extra></extra>",
))
lo7 = L(370)
lo7["barmode"] = "overlay"
lo7["yaxis"] = yh(); lo7["xaxis"] = xh(mx=max(g25)*1.38)
lo7["showlegend"] = True
lo7["legend"] = dict(orientation="h", x=1, xanchor="right", y=1.06,
                     font=dict(size=11, color="rgba(30,27,75,.6)"), bgcolor="rgba(0,0,0,0)")
lo7["margin"] = dict(t=30, b=15, l=5, r=185)
fig7.update_layout(lo7)
st.markdown('<div class="gc">', unsafe_allow_html=True)
st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# 과탐 변화율 바
st.markdown('<div class="sh" style="margin-top:1.5rem"><div class="sh-tag">// 08</div><div class="sh-title">📉 과탐 과목별 전년 대비 변화율 (%)</div></div>', unsafe_allow_html=True)
g_chg = [pct_change(gwatam25[n], gwatam26[n]) for n in g_names_ord]
g_chg_cols = [G if v >= 0 else R for v in g_chg]

fig8 = go.Figure()
fig8.add_shape(type="line", x0=-1, x1=len(g_names_ord),
               y0=0, y1=0, line=dict(color="rgba(30,27,75,.15)", width=1.5, dash="dot"))
fig8.add_trace(go.Bar(
    x=g_names_ord, y=g_chg,
    marker=dict(color=g_chg_cols, line=dict(width=0), opacity=0.85),
    text=[f"{'▲' if v>=0 else '▼'}{abs(v):.1f}%" for v in g_chg],
    textposition="outside",
    textfont=dict(size=11, color=g_chg_cols, family=FONT),
    width=0.6,
    hovertemplate="%{x}<br><b>%{y:+.1f}%</b><extra></extra>",
))
lo8 = L(300)
lo8["xaxis"] = xv(11); lo8["bargap"] = 0.3
lo8["yaxis"] = dict(showgrid=True, gridcolor=GRID, zeroline=False,
                    ticksuffix="%", tickfont=dict(color="rgba(30,27,75,.3)", size=10),
                    range=[min(g_chg)-6, max(g_chg)+8])
fig8.update_layout(lo8)
st.markdown('<div class="gc">', unsafe_allow_html=True)
st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="ib-row">
  <div class="ib ib-c">🌍 지구과학Ⅰ {arrow(153987,106729)} — 과탐 1위 유지</div>
  <div class="ib ib-g">🧬 생명과학Ⅰ {arrow(141027,102836)} — 2위 유지</div>
  <div class="ib ib-r">⚗️ 화학Ⅰ {arrow(48758,23321)} — 최대 피해 과목</div>
  <div class="ib ib-r">물리학Ⅰ {arrow(63740,42232)} — 전 과목 급감</div>
  <div class="ib ib-a">Ⅱ과목 합계 22,021명 — 과탐의 9.6%</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════
# 종합 비교
# ══════════════════════════════
st.markdown('<div class="sec-div"><span>🎯 영역별 종합</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sh"><div class="sh-tag">// 09</div><div class="sh-title">🎯 5개 영역 응시자 — 2025 vs 2026</div></div>', unsafe_allow_html=True)

area_names = ["📝 국어", "🧮 수학", "🌐 영어", "🇰🇷 한국사", "🔭 탐구"]
area25 = [461_252, 443_233, 459_352, 463_486, 447_507]
area26 = [490_989, 471_374, 487_941, 493_896, 473_911]
a_cols = [V, G, C, A, P]

fig9 = go.Figure()
fig9.add_trace(go.Bar(
    name="2025", x=area_names, y=area25,
    marker=dict(color=[f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},.25)" for c in a_cols], line=dict(width=0)),
    width=0.3, offset=-0.18,
    text=[f"{v:,}" for v in area25],
    textposition="outside",
    textfont=dict(size=11, color="rgba(30,27,75,.4)", family=FONT),
    hovertemplate="%{x} 2025<br><b>%{y:,}명</b><extra></extra>",
))
fig9.add_trace(go.Bar(
    name="2026", x=area_names, y=area26,
    marker=dict(color=a_cols, line=dict(width=0), opacity=0.88),
    width=0.3, offset=0.18,
    text=[f"{v:,}" for v in area26],
    textposition="outside",
    textfont=dict(size=11, color=a_cols, family=FONT),
    hovertemplate="%{x} 2026<br><b>%{y:,}명</b><extra></extra>",
))
lo9 = L(360)
lo9["xaxis"] = xv(12); lo9["yaxis"] = yv(mx=560000); lo9["bargap"] = 0.28
lo9["showlegend"] = True
lo9["legend"] = dict(orientation="h", x=1, xanchor="right", y=1.1,
                     font=dict(size=11, color="rgba(30,27,75,.6)"), bgcolor="rgba(0,0,0,0)")
fig9.update_layout(lo9)
st.markdown('<div class="gc">', unsafe_allow_html=True)
st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-emojis">📚 📊 🎓 ⚡ 🔥</div>
  <div class="footer-text">
    출처: 한국교육과정평가원 · 2026학년도 대학수학능력시험 채점 결과 · 2025.12.04 발표<br>
    비교: 2025학년도 수능 채점 결과 · 2024.12.05 발표
  </div>
</div>
""", unsafe_allow_html=True)
