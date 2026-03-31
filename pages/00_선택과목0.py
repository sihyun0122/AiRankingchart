import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="2026 수능 선택과목 분석",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── 배경 & 파티클 ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #03030a !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 15% -5%, rgba(99,102,241,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 85% 105%, rgba(16,185,129,0.13) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(245,158,11,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 30% 20% at 80% 20%, rgba(236,72,153,0.07) 0%, transparent 50%),
        #03030a !important;
    animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { filter: brightness(1); }
    100% { filter: brightness(1.04); }
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2.5rem 6rem !important; max-width: 1300px !important; }

/* ── 떠다니는 도트 파티클 ── */
.particles {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.dot {
    position: absolute;
    border-radius: 50%;
    animation: floatDot linear infinite;
    opacity: 0;
}
@keyframes floatDot {
    0%   { transform: translateY(100vh) scale(0); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 0.6; }
    100% { transform: translateY(-10vh) scale(1); opacity: 0; }
}

/* ── HERO ── */
.hero {
    padding: 5rem 0 3.5rem;
    text-align: center;
    position: relative;
    z-index: 1;
}
.hero-watermark {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -46%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(70px, 13vw, 200px);
    color: rgba(255,255,255,0.02);
    white-space: nowrap;
    letter-spacing: 0.12em;
    pointer-events: none;
    user-select: none;
    animation: watermarkPulse 6s ease-in-out infinite alternate;
}
@keyframes watermarkPulse {
    from { opacity: 0.6; letter-spacing: 0.12em; }
    to   { opacity: 1;   letter-spacing: 0.14em; }
}

.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    animation: fadeSlideDown 0.8s ease both;
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 7vw, 6.5rem);
    letter-spacing: 0.04em;
    line-height: 0.92;
    color: #fff;
    margin-bottom: 0.6rem;
    animation: fadeSlideUp 0.9s ease 0.1s both;
    text-shadow: 0 0 60px rgba(99,102,241,0.3);
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-title .g1 {
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-size: 200% 100%;
    animation: gradShift 4s ease infinite;
}
.hero-title .g2 {
    background: linear-gradient(90deg, #06b6d4, #10b981, #84cc16);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-size: 200% 100%;
    animation: gradShift 4s ease 0.5s infinite;
}
@keyframes gradShift {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}

.hero-sub {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.06em;
    animation: fadeSlideUp 1s ease 0.25s both;
}
.hero-emoji-row {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    animation: fadeSlideUp 0.8s ease 0.15s both;
    letter-spacing: 0.3em;
}

/* ── 네온 라인 ── */
.neon-line {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(99,102,241,0.8) 30%,
        rgba(168,85,247,0.9) 50%,
        rgba(236,72,153,0.8) 70%,
        transparent 100%
    );
    margin: 0.3rem 0 2.2rem;
    position: relative;
    animation: neonFlow 3s ease-in-out infinite;
}
@keyframes neonFlow {
    0%,100% { opacity: 0.6; }
    50%      { opacity: 1;   box-shadow: 0 0 12px rgba(168,85,247,0.6); }
}
.neon-line::after {
    content: '';
    position: absolute;
    top: -1px; left: 0; right: 0; height: 3px;
    background: inherit;
    filter: blur(4px);
    opacity: 0.5;
}

.divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 0.5rem 0 2rem;
}
.divider::before, .divider::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), transparent);
}
.divider-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: rgba(139,92,246,0.8);
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── STAT CARDS ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 2.5rem; flex-wrap: wrap; }

.stat-card {
    flex: 1; min-width: 200px;
    border-radius: 6px;
    padding: 1.6rem 1.4rem 1.3rem;
    border: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.025);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    animation: cardFadeIn 0.7s ease both;
}
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    animation: lineGlow 2.5s ease-in-out infinite;
}
@keyframes lineGlow {
    0%,100% { opacity: 0.8; }
    50%      { opacity: 1; filter: blur(1px) brightness(1.3); }
}
.stat-card::after {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(255,255,255,0.04), transparent);
    pointer-events: none;
}
.stat-card.blue::before   { background: linear-gradient(90deg, #4f46e5, #6366f1, #818cf8); }
.stat-card.cyan::before   { background: linear-gradient(90deg, #0891b2, #06b6d4, #67e8f9); }
.stat-card.green::before  { background: linear-gradient(90deg, #059669, #10b981, #6ee7b7); }
.stat-card.amber::before  { background: linear-gradient(90deg, #d97706, #f59e0b, #fcd34d); }

.stat-card .emoji { font-size: 1.5rem; margin-bottom: 0.5rem; display: block; }
.stat-card .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.2em;
    color: rgba(255,255,255,0.3); text-transform: uppercase; margin-bottom: 0.4rem;
}
.stat-card .number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem; line-height: 1; letter-spacing: 0.03em;
}
.stat-card.blue  .number { color: #818cf8; text-shadow: 0 0 20px rgba(129,140,248,0.5); }
.stat-card.cyan  .number { color: #22d3ee; text-shadow: 0 0 20px rgba(34,211,238,0.5); }
.stat-card.green .number { color: #34d399; text-shadow: 0 0 20px rgba(52,211,153,0.5); }
.stat-card.amber .number { color: #fbbf24; text-shadow: 0 0 20px rgba(251,191,36,0.5); }
.stat-card .sublabel {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.7rem; color: rgba(255,255,255,0.22); margin-top: 0.3rem;
}

/* ── SECTION HEADER ── */
.sec-head { margin-bottom: 0.9rem; }
.sec-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; letter-spacing: 0.25em;
    color: rgba(99,102,241,0.8); text-transform: uppercase; margin-bottom: 0.3rem;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.85rem; letter-spacing: 0.04em; color: #fff;
}
.sec-title .emoji-inline { font-size: 1.5rem; }

/* ── INSIGHT BADGES ── */
.insight-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 2.2rem; }
.insight-badge {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.75rem;
    padding: 0.38rem 0.9rem;
    border-radius: 999px;
    border: 1px solid;
    letter-spacing: 0.01em;
    transition: transform 0.15s;
    animation: badgePop 0.5s ease both;
}
.insight-badge:hover { transform: scale(1.04); }
@keyframes badgePop {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}
.ins-blue  { color: #a5b4fc; border-color: rgba(99,102,241,0.4);  background: rgba(99,102,241,0.1); }
.ins-cyan  { color: #67e8f9; border-color: rgba(6,182,212,0.4);   background: rgba(6,182,212,0.1); }
.ins-green { color: #6ee7b7; border-color: rgba(16,185,129,0.4);  background: rgba(16,185,129,0.1); }
.ins-amber { color: #fcd34d; border-color: rgba(245,158,11,0.4);  background: rgba(245,158,11,0.1); }
.ins-pink  { color: #f9a8d4; border-color: rgba(236,72,153,0.4);  background: rgba(236,72,153,0.1); }
.ins-purp  { color: #d8b4fe; border-color: rgba(168,85,247,0.4);  background: rgba(168,85,247,0.1); }

/* ── CHART CONTAINER ── */
.chart-wrap {
    background: rgba(255,255,255,0.018);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 8px;
    padding: 0.4rem;
    transition: box-shadow 0.25s;
}
.chart-wrap:hover {
    box-shadow: 0 0 30px rgba(99,102,241,0.08), 0 8px 32px rgba(0,0,0,0.3);
}

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #03030a; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 2px; }
</style>

<!-- 파티클 -->
<div class="particles">
  <div class="dot" style="left:8%;width:3px;height:3px;background:#818cf8;animation-duration:12s;animation-delay:0s;"></div>
  <div class="dot" style="left:18%;width:2px;height:2px;background:#22d3ee;animation-duration:15s;animation-delay:2s;"></div>
  <div class="dot" style="left:32%;width:4px;height:4px;background:#a855f7;animation-duration:10s;animation-delay:1s;"></div>
  <div class="dot" style="left:47%;width:2px;height:2px;background:#34d399;animation-duration:18s;animation-delay:3s;"></div>
  <div class="dot" style="left:61%;width:3px;height:3px;background:#fbbf24;animation-duration:13s;animation-delay:0.5s;"></div>
  <div class="dot" style="left:74%;width:2px;height:2px;background:#ec4899;animation-duration:16s;animation-delay:4s;"></div>
  <div class="dot" style="left:85%;width:3px;height:3px;background:#6366f1;animation-duration:11s;animation-delay:1.5s;"></div>
  <div class="dot" style="left:93%;width:2px;height:2px;background:#22d3ee;animation-duration:14s;animation-delay:2.5s;"></div>
  <div class="dot" style="left:55%;width:2px;height:2px;background:#f87171;animation-duration:17s;animation-delay:5s;"></div>
  <div class="dot" style="left:25%;width:3px;height:3px;background:#818cf8;animation-duration:9s;animation-delay:3.5s;"></div>
</div>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────
BG   = "#03030a"
GRID = "rgba(255,255,255,0.05)"
BLUE  = "#818cf8"; CYAN  = "#22d3ee"; GREEN = "#34d399"
AMBER = "#fbbf24"; RED   = "#f87171"; PURP  = "#c084fc"
PINK  = "#f472b6"

# ── DATA ──────────────────────────────────────────────────────────────
# 출처: 한국교육과정평가원, 2026학년도 수능 채점 결과 (2025.12.04)
korean = {"화법과 작문": 333_283, "언어와 매체": 157_706}
math   = {"확률과 통계": 264_307, "미적분": 193_475, "기하": 13_623}
satam  = {
    "사회·문화":   239_403, "생활과 윤리": 196_382, "윤리와 사상":  46_145,
    "한국지리":     42_518,  "세계지리":    41_655,  "정치와 법":    33_123,
    "동아시아사":   20_507,  "세계사":      19_884,  "경제":          7_085,
}
gwatam = {
    "지구과학Ⅰ":  106_729, "생명과학Ⅰ":  102_836, "물리학Ⅰ":   42_232,
    "화학Ⅰ":       23_321, "생명과학Ⅱ":    7_279, "화학Ⅱ":      5_242,
    "물리학Ⅱ":      5_236, "지구과학Ⅱ":    4_264,
}
korean_total = sum(korean.values())
math_total   = sum(math.values())
satam_total  = sum(satam.values())
gwatam_total = sum(gwatam.values())

# ── CHART HELPERS ─────────────────────────────────────────────────────
def L(h=370):
    return dict(
        plot_bgcolor=BG, paper_bgcolor=BG, height=h,
        font=dict(family="JetBrains Mono, monospace", color="rgba(255,255,255,0.35)", size=11),
        margin=dict(t=30, b=15, l=10, r=10), showlegend=False,
    )
def xv(size=12):
    return dict(showgrid=False, zeroline=False, linecolor="rgba(255,255,255,0.06)",
                tickfont=dict(color="rgba(255,255,255,0.8)", size=size, family="Noto Sans KR, sans-serif"))
def yv(suf="", mx=None, vis=True):
    d = dict(showgrid=vis, gridcolor=GRID, zeroline=False, visible=vis,
             tickfont=dict(color="rgba(255,255,255,0.25)", size=10))
    if suf: d["ticksuffix"] = suf
    if mx:  d["range"] = [0, mx]
    return d
def yh():
    return dict(showgrid=False, zeroline=False, autorange="reversed",
                tickfont=dict(color="rgba(255,255,255,0.78)", size=11, family="Noto Sans KR, sans-serif"))
def xh(mx=None):
    d = dict(showgrid=True, gridcolor=GRID, zeroline=False,
             tickfont=dict(color="rgba(255,255,255,0.25)", size=10))
    if mx: d["range"] = [0, mx]
    return d

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-watermark">2026 CSAT</div>
  <div class="hero-tag">⚡ 한국교육과정평가원 공식 통계 · 2025.12.04 발표</div>
  <div class="hero-emoji-row">📚 🧮 🌍 🧬 ⚗️ 📐</div>
  <div class="hero-title">
    <span class="g1">2026 수능</span><br>
    <span class="g2">선택과목 완전분석</span>
  </div>
  <div class="hero-sub">총 응시자 493,896명 · 국어 · 수학 · 사회탐구 9과목 · 과학탐구 8과목</div>
</div>
<div class="neon-line"></div>
""", unsafe_allow_html=True)

# ── STAT CARDS ────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat-card blue" style="animation-delay:0s">
    <span class="emoji">🎓</span>
    <div class="label">총 응시자</div>
    <div class="number">493,896</div>
    <div class="sublabel">재학생 333,102 · 졸업생 160,794명</div>
  </div>
  <div class="stat-card cyan" style="animation-delay:0.1s">
    <span class="emoji">📖</span>
    <div class="label">사탐만 응시</div>
    <div class="number">284,535</div>
    <div class="sublabel">전년比 +18.6% ↑ 이과생 사탐 대이동</div>
  </div>
  <div class="stat-card green" style="animation-delay:0.2s">
    <span class="emoji">🔬</span>
    <div class="label">과탐만 응시</div>
    <div class="number">108,353</div>
    <div class="sublabel">전년比 -53.5% ↓ 역대급 감소</div>
  </div>
  <div class="stat-card amber" style="animation-delay:0.3s">
    <span class="emoji">🔀</span>
    <div class="label">사탐+과탐 혼합</div>
    <div class="number">81,023</div>
    <div class="sublabel">전년比 +69.8% ↑ 사탐런 직격탄</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">📝 국어 · 🧮 수학 선택과목</span></div>', unsafe_allow_html=True)

# ── 국어 + 수학 바 ────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")
k_names = list(korean.keys()); k_vals = list(korean.values())
k_pcts  = [v/korean_total*100 for v in k_vals]; k_cols = [BLUE, PINK]

with col1:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 01</div><div class="sec-title">📝 국어 선택과목</div></div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=k_names, y=k_vals,
        marker=dict(color=k_cols, line=dict(width=0),
                    pattern=dict(shape="", bgcolor=k_cols)),
        text=[f"<b>{p:.1f}%</b><br>{v:,}명" for p, v in zip(k_pcts, k_vals)],
        textposition="outside",
        textfont=dict(size=13, family="Noto Sans KR, sans-serif", color=k_cols),
        width=0.5,
        hovertemplate="%{x}<br><b>%{y:,}명</b><extra></extra>",
    ))
    lo = L(340); lo["xaxis"] = xv(14); lo["yaxis"] = yv(mx=max(k_vals)*1.25); lo["bargap"] = 0.45
    fig.update_layout(lo)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

m_names = list(math.keys()); m_vals = list(math.values())
m_pcts  = [v/math_total*100 for v in m_vals]; m_cols = [AMBER, GREEN, RED]

with col2:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 02</div><div class="sec-title">🧮 수학 선택과목</div></div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=m_names, y=m_vals,
        marker=dict(color=m_cols, line=dict(width=0)),
        text=[f"<b>{p:.1f}%</b><br>{v:,}명" for p, v in zip(m_pcts, m_vals)],
        textposition="outside",
        textfont=dict(size=13, family="Noto Sans KR, sans-serif", color=m_cols),
        width=0.5,
        hovertemplate="%{x}<br><b>%{y:,}명</b><extra></extra>",
    ))
    lo2 = L(340); lo2["xaxis"] = xv(14); lo2["yaxis"] = yv(mx=max(m_vals)*1.25); lo2["bargap"] = 0.4
    fig2.update_layout(lo2)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# 도넛 2개
col3, col4 = st.columns(2, gap="medium")
with col3:
    fig3 = go.Figure(go.Pie(
        labels=k_names, values=k_vals, hole=0.62,
        marker=dict(colors=k_cols, line=dict(color=BG, width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family="Noto Sans KR, sans-serif"),
        pull=[0.05, 0], rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo3 = L(280)
    lo3["annotations"] = [dict(text="📝<br>국어", x=0.5, y=0.5, showarrow=False,
                               font=dict(color="#fff", family="Bebas Neue", size=16))]
    fig3.update_layout(lo3)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    fig4 = go.Figure(go.Pie(
        labels=m_names, values=m_vals, hole=0.62,
        marker=dict(colors=m_cols, line=dict(color=BG, width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family="Noto Sans KR, sans-serif"),
        pull=[0.05, 0, 0], rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo4 = L(280)
    lo4["annotations"] = [dict(text="🧮<br>수학", x=0.5, y=0.5, showarrow=False,
                               font=dict(color="#fff", family="Bebas Neue", size=16))]
    fig4.update_layout(lo4)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-row">
  <div class="insight-badge ins-blue">📝 화법과 작문 67.9% — 압도적 1위 (전년比 +4.6%p)</div>
  <div class="insight-badge ins-amber">🔄 확통 56.1% — 미적분 역전! 2026 최대 이변</div>
  <div class="insight-badge ins-green">📐 미적분 41.0% — 전년 51.3%에서 급락</div>
  <div class="insight-badge ins-pink">📉 기하 2.89% — 역대 최저 수준 유지</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">📖 사회탐구 영역 9과목</span></div>', unsafe_allow_html=True)

# ── 사탐 가로 바 ──────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-tag">// 03</div><div class="sec-title">📖 사탐 9과목 응시자 수 비교</div></div>', unsafe_allow_html=True)

s_sorted = dict(sorted(satam.items(), key=lambda x: x[1]))
s_names  = list(s_sorted.keys()); s_vals = list(s_sorted.values())
s_pcts   = [v/satam_total*100 for v in s_vals]
s_colors = ["#f87171","#fb923c","#fbbf24","#a3e635","#34d399","#22d3ee","#60a5fa","#818cf8","#c084fc"]

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    x=s_vals, y=s_names, orientation="h",
    marker=dict(color=s_colors, line=dict(width=0), opacity=0.9),
    text=[f"  {p:.1f}%  |  {v:,}명" for p, v in zip(s_pcts, s_vals)],
    textposition="outside",
    textfont=dict(size=11, family="Noto Sans KR, sans-serif", color="rgba(255,255,255,0.7)"),
    hovertemplate="%{y}<br><b>%{x:,}명</b><extra></extra>",
))
lo5 = L(380); lo5["yaxis"] = yh(); lo5["xaxis"] = xh(mx=max(s_vals)*1.35)
lo5["margin"] = dict(t=20, b=15, l=5, r=180)
fig5.update_layout(lo5)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-row">
  <div class="insight-badge ins-purp">🏆 사회·문화 239,403명 — 사탐 1위 (전년比 +29.4%)</div>
  <div class="insight-badge ins-blue">🥈 생활과 윤리 196,382명 — 2위 (두 과목 합산 69.9%)</div>
  <div class="insight-badge ins-amber">⚠️ 경제 7,085명 — 최저 (전체 사탐의 1.1%)</div>
  <div class="insight-badge ins-pink">🔥 사탐런 직격: 이과생 대거 사탐 침공</div>
  <div class="insight-badge ins-green">📈 윤리와 사상·세계지리 등 중위권도 동반 상승</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">🔬 과학탐구 영역 8과목</span></div>', unsafe_allow_html=True)

# ── 과탐 가로 바 ──────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-tag">// 04</div><div class="sec-title">🔬 과탐 8과목 응시자 수 비교</div></div>', unsafe_allow_html=True)

g_sorted = dict(sorted(gwatam.items(), key=lambda x: x[1]))
g_names  = list(g_sorted.keys()); g_vals = list(g_sorted.values())
g_pcts   = [v/gwatam_total*100 for v in g_vals]
g_colors = ["#f87171","#fb923c","#fbbf24","#a3e635","#34d399","#22d3ee","#60a5fa","#818cf8"]

fig6 = go.Figure()
fig6.add_trace(go.Bar(
    x=g_vals, y=g_names, orientation="h",
    marker=dict(color=g_colors, line=dict(width=0), opacity=0.9),
    text=[f"  {p:.1f}%  |  {v:,}명" for p, v in zip(g_pcts, g_vals)],
    textposition="outside",
    textfont=dict(size=11, family="Noto Sans KR, sans-serif", color="rgba(255,255,255,0.7)"),
    hovertemplate="%{y}<br><b>%{x:,}명</b><extra></extra>",
))
lo6 = L(340); lo6["yaxis"] = yh(); lo6["xaxis"] = xh(mx=max(g_vals)*1.35)
lo6["margin"] = dict(t=20, b=15, l=5, r=180)
fig6.update_layout(lo6)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-row">
  <div class="insight-badge ins-blue">🌍 지구과학Ⅰ 106,729명 — 과탐 1위 (전년比 -30.7%)</div>
  <div class="insight-badge ins-green">🧬 생명과학Ⅰ 102,836명 — 2위 (Ⅰ과목 양강 유지)</div>
  <div class="insight-badge ins-amber">⚗️ 화학Ⅰ -52.2% 급감 — 사탐런 최대 피해 과목</div>
  <div class="insight-badge ins-pink">📉 Ⅱ과목 합계 22,021명 — 전체 과탐의 9.6%</div>
  <div class="insight-badge ins-purp">🔻 지구과학Ⅱ 4,264명 — 과탐 최저</div>
</div>
""", unsafe_allow_html=True)

# ── 사탐 vs 과탐 도넛 ────────────────────────────────────────────────
st.markdown('<div class="divider"><span class="divider-label">📊 탐구 영역 점유율 비교</span></div>', unsafe_allow_html=True)
col5, col6 = st.columns(2, gap="medium")

with col5:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 05</div><div class="sec-title">📖 사탐 과목별 점유율</div></div>', unsafe_allow_html=True)
    fig7 = go.Figure(go.Pie(
        labels=list(satam.keys()), values=list(satam.values()), hole=0.55,
        marker=dict(
            colors=["#c084fc","#818cf8","#60a5fa","#22d3ee","#34d399","#a3e635","#fbbf24","#fb923c","#f87171"],
            line=dict(color=BG, width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, family="Noto Sans KR, sans-serif"),
        insidetextorientation="radial", rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo7 = L(400); lo7["annotations"] = [dict(text="📖<br>사탐", x=0.5, y=0.5, showarrow=False,
                                             font=dict(color="#fff", family="Bebas Neue", size=15))]
    fig7.update_layout(lo7)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 06</div><div class="sec-title">🔬 과탐 과목별 점유율</div></div>', unsafe_allow_html=True)
    fig8 = go.Figure(go.Pie(
        labels=list(gwatam.keys()), values=list(gwatam.values()), hole=0.55,
        marker=dict(
            colors=["#818cf8","#60a5fa","#22d3ee","#34d399","#a3e635","#fbbf24","#fb923c","#f87171"],
            line=dict(color=BG, width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, family="Noto Sans KR, sans-serif"),
        insidetextorientation="radial", rotation=90,
        hovertemplate="%{label}<br><b>%{value:,}명</b> (%{percent})<extra></extra>",
    ))
    lo8 = L(400); lo8["annotations"] = [dict(text="🔬<br>과탐", x=0.5, y=0.5, showarrow=False,
                                             font=dict(color="#fff", family="Bebas Neue", size=15))]
    fig8.update_layout(lo8)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── 영역별 종합 ───────────────────────────────────────────────────────
st.markdown('<div class="divider"><span class="divider-label">🎯 영역별 응시자 종합</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-head"><div class="sec-tag">// 07</div><div class="sec-title">🎯 5개 영역 응시자 종합</div></div>', unsafe_allow_html=True)

area_names = ["📝 국어", "🧮 수학", "🌐 영어", "🇰🇷 한국사", "🔭 탐구"]
area_vals  = [490_989, 471_374, 487_941, 493_896, 473_911]
area_cols  = [BLUE, GREEN, CYAN, AMBER, PURP]

fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=area_names, y=area_vals,
    marker=dict(color=area_cols, opacity=0.9, line=dict(width=0)),
    text=[f"<b>{v:,}</b>" for v in area_vals],
    textposition="outside",
    textfont=dict(size=13, family="JetBrains Mono, monospace", color=area_cols),
    width=0.55,
    hovertemplate="%{x}<br><b>%{y:,}명</b><extra></extra>",
))
lo9 = L(370); lo9["xaxis"] = xv(12); lo9["yaxis"] = yv(mx=max(area_vals)*1.12); lo9["bargap"] = 0.38
fig9.update_layout(lo9)
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center; padding: 2.5rem 0 0.5rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
">
  <div style="font-size:1.2rem; margin-bottom:0.6rem; letter-spacing:0.2em;">
    📚 📊 🎓 ⚡ 🔥
  </div>
  <span style="
    font-family:'JetBrains Mono',monospace; font-size:0.63rem;
    letter-spacing:0.18em; color:rgba(255,255,255,0.18); text-transform:uppercase;
  ">
    출처: 한국교육과정평가원 · 2026학년도 대학수학능력시험 채점 결과 · 2025.12.04 발표
  </span>
</div>
""", unsafe_allow_html=True)
