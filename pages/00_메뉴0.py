import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="2025 수능 선택과목 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #08080f !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(99,102,241,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(16,185,129,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 50% 30% at 50% 50%, rgba(245,158,11,0.04) 0%, transparent 60%),
        #08080f !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2.5rem 5rem !important; max-width: 1280px !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── HERO ── */
.hero {
    padding: 4.5rem 0 3rem;
    text-align: center;
    position: relative;
}
.hero-bg-text {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -48%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(60px, 12vw, 160px);
    color: rgba(255,255,255,0.018);
    white-space: nowrap;
    letter-spacing: 0.1em;
    pointer-events: none;
    user-select: none;
}
.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.28em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5.5rem);
    letter-spacing: 0.04em;
    line-height: 0.95;
    color: #fff;
    margin-bottom: 0.5rem;
}
.hero-title .accent {
    background: linear-gradient(90deg, #6366f1, #06b6d4, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.28);
    letter-spacing: 0.04em;
    margin-top: 0.4rem;
}

/* ── DIVIDER ── */
.divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 0.5rem 0 2rem;
}
.divider::before, .divider::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.35), transparent);
}
.divider-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: rgba(99,102,241,0.65);
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── STAT CARDS ── */
.stat-row { display: flex; gap: 0.85rem; margin-bottom: 2.5rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 180px;
    border-radius: 3px;
    padding: 1.4rem 1.3rem 1.2rem;
    border: 1px solid rgba(255,255,255,0.055);
    background: rgba(255,255,255,0.025);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.stat-card.blue::before   { background: linear-gradient(90deg, #6366f1, #818cf8); }
.stat-card.cyan::before   { background: linear-gradient(90deg, #06b6d4, #67e8f9); }
.stat-card.green::before  { background: linear-gradient(90deg, #10b981, #6ee7b7); }
.stat-card.amber::before  { background: linear-gradient(90deg, #f59e0b, #fcd34d); }

.stat-card .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.stat-card .number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
    letter-spacing: 0.03em;
}
.stat-card.blue  .number { color: #818cf8; }
.stat-card.cyan  .number { color: #22d3ee; }
.stat-card.green .number { color: #34d399; }
.stat-card.amber .number { color: #fbbf24; }

.stat-card .sublabel {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.25);
    margin-top: 0.3rem;
    letter-spacing: 0.01em;
}

/* ── SECTION HEADER ── */
.sec-head { margin-bottom: 0.8rem; }
.sec-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    color: rgba(99,102,241,0.75);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.75rem;
    letter-spacing: 0.04em;
    color: #fff;
}

/* ── INSIGHT BADGES ── */
.insight-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 2rem; }
.insight-badge {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.76rem;
    padding: 0.35rem 0.85rem;
    border-radius: 2px;
    border: 1px solid;
    letter-spacing: 0.02em;
}
.ins-blue  { color: #818cf8; border-color: rgba(99,102,241,0.3); background: rgba(99,102,241,0.08); }
.ins-cyan  { color: #22d3ee; border-color: rgba(6,182,212,0.3);  background: rgba(6,182,212,0.08); }
.ins-green { color: #34d399; border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.08); }
.ins-amber { color: #fbbf24; border-color: rgba(245,158,11,0.3); background: rgba(245,158,11,0.08); }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ────────────────────────────────────────────────────────
BG   = "#08080f"
GRID = "rgba(255,255,255,0.055)"

BLUE  = "#818cf8"
CYAN  = "#22d3ee"
GREEN = "#34d399"
AMBER = "#fbbf24"
RED   = "#f87171"
PURP  = "#c084fc"

# ── DATA (출처: 한국교육과정평가원, 2025학년도 수능 채점 결과) ────────
korean = {
    "화법과 작문": 290_888,
    "언어와 매체": 170_364,
}
math = {
    "미적분":      227_232,
    "확률과 통계": 202_266,
    "기하":         13_735,
}
satam = {
    "사회·문화":   185_014,
    "생활과 윤리": 183_441,
    "윤리와 사상":  47_391,
    "한국지리":     40_850,
    "정치와 법":    34_706,
    "세계지리":     34_333,
    "동아시아사":   20_394,
    "세계사":       18_328,
    "경제":          7_353,
}
gwatam = {
    "지구과학Ⅰ":  153_987,
    "생명과학Ⅰ":  141_027,
    "물리학Ⅰ":     63_740,
    "화학Ⅰ":       48_758,
    "생명과학Ⅱ":    8_214,
    "화학Ⅱ":        6_343,
    "물리학Ⅱ":      6_241,
    "지구과학Ⅱ":    5_196,
}

total_applicants = 463_486
korean_total = sum(korean.values())
math_total   = sum(math.values())
satam_total  = sum(satam.values())
gwatam_total = sum(gwatam.values())

# ── CHART LAYOUT HELPER ──────────────────────────────────────────────
def L(height=370, extra=None):
    d = dict(
        plot_bgcolor=BG, paper_bgcolor=BG,
        height=height,
        font=dict(family="JetBrains Mono, monospace", color="rgba(255,255,255,0.38)", size=11),
        margin=dict(t=30, b=15, l=10, r=10),
        showlegend=False,
    )
    if extra:
        d.update(extra)
    return d

def xaxis_default(size=12, color="#fff"):
    return dict(showgrid=False, zeroline=False,
                linecolor="rgba(255,255,255,0.07)",
                tickfont=dict(color=color, size=size, family="Noto Sans KR, sans-serif"))

def yaxis_default(suffix="", max_val=None, visible=True):
    d = dict(showgrid=visible, gridcolor=GRID, zeroline=False, visible=visible,
             tickfont=dict(color="rgba(255,255,255,0.28)", size=10))
    if suffix: d["ticksuffix"] = suffix
    if max_val: d["range"] = [0, max_val]
    return d

def yaxis_h():
    """For horizontal bar charts"""
    return dict(showgrid=False, zeroline=False,
                tickfont=dict(color="rgba(255,255,255,0.75)", size=11,
                              family="Noto Sans KR, sans-serif"),
                autorange="reversed")

def xaxis_h(max_val=None):
    d = dict(showgrid=True, gridcolor=GRID, zeroline=False,
             tickfont=dict(color="rgba(255,255,255,0.28)", size=10))
    if max_val: d["range"] = [0, max_val]
    return d

# ── HERO ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-bg-text">2025 CSAT</div>
  <div class="hero-tag">📊 한국교육과정평가원 공식 통계</div>
  <div class="hero-title">2025 수능<br><span class="accent">선택과목 분석</span></div>
  <div class="hero-sub">총 응시자 463,486명 · 국어 · 수학 · 사회탐구 · 과학탐구</div>
</div>
""", unsafe_allow_html=True)

# ── SUMMARY STATS ────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat-card blue">
    <div class="label">총 응시자</div>
    <div class="number">463,486</div>
    <div class="sublabel">명 (재학생 302,589 · 졸업생 160,897)</div>
  </div>
  <div class="stat-card cyan">
    <div class="label">사탐 응시자</div>
    <div class="number">225,135</div>
    <div class="sublabel">명 (사탐만 선택)</div>
  </div>
  <div class="stat-card green">
    <div class="label">과탐 응시자</div>
    <div class="number">174,649</div>
    <div class="sublabel">명 (과탐만 선택)</div>
  </div>
  <div class="stat-card amber">
    <div class="label">혼합 응시자</div>
    <div class="number">47,723</div>
    <div class="sublabel">명 (사탐+과탐 조합 · 전년比 +3배)</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">국어 · 수학 선택과목</span></div>', unsafe_allow_html=True)

# ── ROW 1: 국어 + 수학 ──────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 01 국어</div><div class="sec-title">국어 선택과목</div></div>', unsafe_allow_html=True)

    k_names = list(korean.keys())
    k_vals  = list(korean.values())
    k_pcts  = [v / korean_total * 100 for v in k_vals]
    k_cols  = [BLUE, CYAN]

    fig_k = go.Figure()
    fig_k.add_trace(go.Bar(
        x=k_names, y=k_vals,
        marker=dict(color=k_cols, line=dict(width=0)),
        text=[f"{p:.1f}%<br>{v:,}명" for p, v in zip(k_pcts, k_vals)],
        textposition="outside",
        textfont=dict(size=13, family="Noto Sans KR, sans-serif", color=k_cols),
        width=0.5,
    ))
    fig_k.update_layout(
        L(height=320),
        xaxis=xaxis_default(size=13),
        yaxis=yaxis_default(max_val=max(k_vals) * 1.22),
        bargap=0.45,
    )
    st.plotly_chart(fig_k, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 02 수학</div><div class="sec-title">수학 선택과목</div></div>', unsafe_allow_html=True)

    m_names = list(math.keys())
    m_vals  = list(math.values())
    m_pcts  = [v / math_total * 100 for v in m_vals]
    m_cols  = [GREEN, AMBER, RED]

    fig_m = go.Figure()
    fig_m.add_trace(go.Bar(
        x=m_names, y=m_vals,
        marker=dict(color=m_cols, line=dict(width=0)),
        text=[f"{p:.1f}%<br>{v:,}명" for p, v in zip(m_pcts, m_vals)],
        textposition="outside",
        textfont=dict(size=13, family="Noto Sans KR, sans-serif", color=m_cols),
        width=0.5,
    ))
    fig_m.update_layout(
        L(height=320),
        xaxis=xaxis_default(size=13),
        yaxis=yaxis_default(max_val=max(m_vals) * 1.22),
        bargap=0.4,
    )
    st.plotly_chart(fig_m, use_container_width=True, config={"displayModeBar": False})

# ── 도넛 2개 ────────────────────────────────────────────────────────
col3, col4 = st.columns(2, gap="medium")
with col3:
    fig_kp = go.Figure(go.Pie(
        labels=k_names,
        values=k_vals,
        hole=0.6,
        marker=dict(colors=k_cols, line=dict(color=BG, width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family="Noto Sans KR, sans-serif"),
        pull=[0.04, 0],
        rotation=90,
    ))
    fig_kp.update_layout(
        L(height=270),
        annotations=[dict(text="국어", x=0.5, y=0.5, showarrow=False,
                         font=dict(color="#fff", family="Bebas Neue", size=18))],
    )
    st.plotly_chart(fig_kp, use_container_width=True, config={"displayModeBar": False})

with col4:
    fig_mp = go.Figure(go.Pie(
        labels=m_names,
        values=m_vals,
        hole=0.6,
        marker=dict(colors=m_cols, line=dict(color=BG, width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family="Noto Sans KR, sans-serif"),
        pull=[0.04, 0, 0],
        rotation=90,
    ))
    fig_mp.update_layout(
        L(height=270),
        annotations=[dict(text="수학", x=0.5, y=0.5, showarrow=False,
                         font=dict(color="#fff", family="Bebas Neue", size=18))],
    )
    st.plotly_chart(fig_mp, use_container_width=True, config={"displayModeBar": False})

# 인사이트
st.markdown("""
<div class="insight-row">
  <div class="insight-badge ins-blue">📖 화법과 작문 선호 63% — 압도적 1위</div>
  <div class="insight-badge ins-green">📐 미적분 51.3% — 3년 연속 증가세</div>
  <div class="insight-badge ins-amber">📉 기하 3.1% — 2022년 대비 절반으로 급감</div>
  <div class="insight-badge ins-cyan">🔥 확통→미적분 이동 = 이과 쏠림 심화</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">사회탐구 영역</span></div>', unsafe_allow_html=True)

# ── 사탐 가로 바 ─────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-tag">// 03 사회탐구</div><div class="sec-title">사탐 9과목 응시자 수</div></div>', unsafe_allow_html=True)

s_sorted = dict(sorted(satam.items(), key=lambda x: x[1]))
s_names  = list(s_sorted.keys())
s_vals   = list(s_sorted.values())
s_pcts   = [v / satam_total * 100 for v in s_vals]

# 색 그라디언트 — 많을수록 BLUE 계열
s_colors = [
    "#f87171","#fb923c","#fbbf24","#a3e635",
    "#34d399","#22d3ee","#60a5fa","#818cf8","#c084fc"
]

fig_s = go.Figure()
fig_s.add_trace(go.Bar(
    x=s_vals, y=s_names,
    orientation="h",
    marker=dict(color=s_colors, line=dict(width=0), opacity=0.88),
    text=[f"  {p:.1f}%  {v:,}명" for p, v in zip(s_pcts, s_vals)],
    textposition="outside",
    textfont=dict(size=11, family="Noto Sans KR, sans-serif", color="rgba(255,255,255,0.65)"),
    hovertemplate="%{y}: %{x:,}명<extra></extra>",
))
fig_s.update_layout(
    L(height=360),
    yaxis=yaxis_h(),
    xaxis=xaxis_h(max_val=max(s_vals) * 1.3),
    margin=dict(t=20, b=15, l=5, r=160),
)
st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar": False})

# 사탐 인사이트
total_satam_picks = sum(s_vals)
st.markdown(f"""
<div class="insight-row">
  <div class="insight-badge ins-blue">🏆 사회·문화 185,014명 — 1위 ({s_pcts[-1]:.1f}%)</div>
  <div class="insight-badge ins-cyan">🥈 생활과 윤리 183,441명 — 2위 (두 과목 합산 72.8%)</div>
  <div class="insight-badge ins-amber">⚠️ 경제 7,353명 — 최저 인원 (1.5%)</div>
  <div class="insight-badge ins-green">📈 사탐런: 이과생 사탐 선택 급증 현상</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">과학탐구 영역</span></div>', unsafe_allow_html=True)

# ── 과탐 가로 바 ─────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-tag">// 04 과학탐구</div><div class="sec-title">과탐 8과목 응시자 수</div></div>', unsafe_allow_html=True)

g_sorted = dict(sorted(gwatam.items(), key=lambda x: x[1]))
g_names  = list(g_sorted.keys())
g_vals   = list(g_sorted.values())
g_pcts   = [v / gwatam_total * 100 for v in g_vals]

g_colors = [
    "#f87171","#fb923c","#fbbf24","#a3e635",
    "#34d399","#22d3ee","#60a5fa","#818cf8"
]

fig_g = go.Figure()
fig_g.add_trace(go.Bar(
    x=g_vals, y=g_names,
    orientation="h",
    marker=dict(color=g_colors, line=dict(width=0), opacity=0.88),
    text=[f"  {p:.1f}%  {v:,}명" for p, v in zip(g_pcts, g_vals)],
    textposition="outside",
    textfont=dict(size=11, family="Noto Sans KR, sans-serif", color="rgba(255,255,255,0.65)"),
    hovertemplate="%{y}: %{x:,}명<extra></extra>",
))
fig_g.update_layout(
    L(height=320),
    yaxis=yaxis_h(),
    xaxis=xaxis_h(max_val=max(g_vals) * 1.3),
    margin=dict(t=20, b=15, l=5, r=160),
)
st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"""
<div class="insight-row">
  <div class="insight-badge ins-blue">🌍 지구과학Ⅰ 153,987명 — 과탐 1위</div>
  <div class="insight-badge ins-green">🧬 생명과학Ⅰ 141,027명 — 2위 (Ⅰ과목 양강 체제)</div>
  <div class="insight-badge ins-amber">⚗️ Ⅱ과목 합계 25,994명 — 전체 과탐의 6.2%에 불과</div>
  <div class="insight-badge ins-cyan">📉 지구과학Ⅱ 5,196명 — 과탐 최저</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-label">사탐 vs 과탐 비교</span></div>', unsafe_allow_html=True)

# ── 사탐 vs 과탐 나란히 도넛 ────────────────────────────────────────
col5, col6 = st.columns(2, gap="medium")

with col5:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 05</div><div class="sec-title">사탐 점유율</div></div>', unsafe_allow_html=True)
    fig_sp = go.Figure(go.Pie(
        labels=list(satam.keys()),
        values=list(satam.values()),
        hole=0.55,
        marker=dict(
            colors=["#c084fc","#818cf8","#60a5fa","#22d3ee",
                    "#34d399","#a3e635","#fbbf24","#fb923c","#f87171"],
            line=dict(color=BG, width=2)
        ),
        textinfo="label+percent",
        textfont=dict(size=10, family="Noto Sans KR, sans-serif"),
        insidetextorientation="radial",
        rotation=90,
    ))
    fig_sp.update_layout(
        L(height=370),
        showlegend=False,
        annotations=[dict(text="사회탐구", x=0.5, y=0.5, showarrow=False,
                         font=dict(color="#fff", family="Bebas Neue", size=14))],
    )
    st.plotly_chart(fig_sp, use_container_width=True, config={"displayModeBar": False})

with col6:
    st.markdown('<div class="sec-head"><div class="sec-tag">// 06</div><div class="sec-title">과탐 점유율</div></div>', unsafe_allow_html=True)
    fig_gp = go.Figure(go.Pie(
        labels=list(gwatam.keys()),
        values=list(gwatam.values()),
        hole=0.55,
        marker=dict(
            colors=["#818cf8","#60a5fa","#22d3ee","#34d399",
                    "#a3e635","#fbbf24","#fb923c","#f87171"],
            line=dict(color=BG, width=2)
        ),
        textinfo="label+percent",
        textfont=dict(size=10, family="Noto Sans KR, sans-serif"),
        insidetextorientation="radial",
        rotation=90,
    ))
    fig_gp.update_layout(
        L(height=370),
        showlegend=False,
        annotations=[dict(text="과학탐구", x=0.5, y=0.5, showarrow=False,
                         font=dict(color="#fff", family="Bebas Neue", size=14))],
    )
    st.plotly_chart(fig_gp, use_container_width=True, config={"displayModeBar": False})

# ── 전체 탐구 비교 그룹 바 ───────────────────────────────────────────
st.markdown('<div class="divider"><span class="divider-label">전체 종합</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sec-head"><div class="sec-tag">// 07</div><div class="sec-title">영역별 응시자 수 종합</div></div>', unsafe_allow_html=True)

area_names = ["국어\n(461,252)", "수학\n(443,233)", "영어\n(459,352)", "한국사\n(463,486)", "사회·과학탐구\n(447,507)"]
area_vals  = [461_252, 443_233, 459_352, 463_486, 447_507]
area_cols  = [BLUE, GREEN, CYAN, AMBER, PURP]

fig_area = go.Figure()
fig_area.add_trace(go.Bar(
    x=area_names, y=area_vals,
    marker=dict(color=area_cols, opacity=0.88, line=dict(width=0)),
    text=[f"{v:,}" for v in area_vals],
    textposition="outside",
    textfont=dict(size=12, family="JetBrains Mono, monospace", color=area_cols),
    width=0.55,
))
fig_area.update_layout(
    L(height=350),
    xaxis=xaxis_default(size=11),
    yaxis=yaxis_default(max_val=max(area_vals) * 1.12),
    bargap=0.38,
)
st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 0.5rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top:2rem;">
  <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:0.18em;
               color:rgba(255,255,255,0.2); text-transform:uppercase;">
    출처: 한국교육과정평가원 · 2025학년도 대학수학능력시험 채점 결과 (2024.12.05)
  </span>
</div>
""", unsafe_allow_html=True)
