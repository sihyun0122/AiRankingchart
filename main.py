import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(
    page_title="AI Battle Results",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #060608 !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 20% 0%, rgba(139,92,246,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(16,185,129,0.08) 0%, transparent 60%),
        #060608 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1200px !important; }

/* ── HERO ── */
.hero {
    position: relative;
    padding: 5rem 0 3.5rem;
    text-align: center;
    overflow: hidden;
}
.hero::before {
    content: 'AI BATTLE';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(80px, 14vw, 180px);
    color: rgba(255,255,255,0.025);
    white-space: nowrap;
    pointer-events: none;
    letter-spacing: 0.08em;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: #8b5cf6;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    letter-spacing: 0.05em;
    line-height: 0.95;
    color: #fff;
    margin-bottom: 0.6rem;
}
.hero-title span {
    background: linear-gradient(90deg, #8b5cf6, #06b6d4, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.08em;
}

/* ── DIVIDER ── */
.slash-divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 0.5rem 0 2rem;
}
.slash-divider::before, .slash-divider::after {
    content: ''; flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), transparent);
}
.slash-divider span {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.2em;
    color: rgba(139,92,246,0.7);
}

/* ── SCORE CARDS ── */
.score-row { display: flex; gap: 1rem; margin-bottom: 2.5rem; }
.score-card {
    flex: 1;
    position: relative;
    border-radius: 2px;
    padding: 1.8rem 1.5rem 1.5rem;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    transition: transform 0.2s;
}
.score-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 2px;
}
.score-card.claude::before  { background: linear-gradient(90deg, #8b5cf6, #c4b5fd); }
.score-card.gemini::before  { background: linear-gradient(90deg, #06b6d4, #67e8f9); }
.score-card.chatgpt::before { background: linear-gradient(90deg, #10b981, #6ee7b7); }

.score-card .rank-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    margin-bottom: 0.8rem;
    opacity: 0.5;
    text-transform: uppercase;
}
.score-card.claude  .rank-tag { color: #c4b5fd; }
.score-card.gemini  .rank-tag { color: #67e8f9; }
.score-card.chatgpt .rank-tag { color: #6ee7b7; }

.score-card .ai-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 0.1em;
    color: #fff;
    margin-bottom: 0.4rem;
}
.score-card .ai-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    line-height: 1;
}
.score-card.claude  .ai-score { color: #a78bfa; }
.score-card.gemini  .ai-score { color: #22d3ee; }
.score-card.chatgpt .ai-score { color: #34d399; }

.score-card .ai-score-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}
.score-card .bg-num {
    position: absolute; right: 1rem; bottom: 0.5rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    opacity: 0.04;
    color: #fff;
    line-height: 1;
}

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: rgba(139,92,246,0.8);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.05em;
    color: #fff;
    margin-bottom: 1.5rem;
}

/* ── TABLE ── */
.raw-table-wrap { margin-top: 1rem; }
.raw-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}
.raw-table th {
    padding: 0.6rem 1rem;
    text-align: left;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.12em;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-weight: 400;
}
.raw-table td {
    padding: 0.7rem 1rem;
    color: rgba(255,255,255,0.7);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.raw-table tr:hover td { background: rgba(255,255,255,0.03); }
.badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
}
.badge-1 { background: rgba(139,92,246,0.2); color: #c4b5fd; }
.badge-2 { background: rgba(6,182,212,0.2);  color: #67e8f9; }
.badge-3 { background: rgba(16,185,129,0.18); color: #6ee7b7; }

[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 2px !important;
    background: rgba(255,255,255,0.02) !important;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────
raw = [
    ("변시현 · 당곡고",   [1, 2, 3]),
    ("신연서 · 수도여고", [1, 3, 2]),
    ("이마루 · 당곡고",   [2, 1, 3]),
    ("최윤영 · 수도여고", [2, 1, 3]),
    ("이지훈 · 당곡고",   [1, 2, 3]),
    ("조윤서 · 수도여고", [1, 2, 3]),
    ("김도연 · 당곡고",   [1, 2, 3]),
    ("이서영 · 수도여고", [1, 3, 2]),
    ("이한규 · 당곡고",   [1, 2, 3]),
    ("김준영 · 20105",   [1, 2, 3]),
]

AI       = ["Claude", "Gemini", "ChatGPT"]
C        = {"Claude": "#a78bfa", "Gemini": "#22d3ee", "ChatGPT": "#34d399"}
BG       = "#060608"
BG2      = "rgba(255,255,255,0.03)"
GRID     = "rgba(255,255,255,0.05)"

scores      = {a: 0 for a in AI}
rank_counts = {a: {1: 0, 2: 0, 3: 0} for a in AI}
for _, ranks in raw:
    for a, r in zip(AI, ranks):
        scores[a] += (4 - r)
        rank_counts[a][r] += 1

ordered = sorted(AI, key=lambda x: scores[x], reverse=True)
rank_labels = {ordered[0]: "01 — GOLD", ordered[1]: "02 — SILVER", ordered[2]: "03 — BRONZE"}
css_class   = {ordered[0]: "claude", ordered[1]: "gemini", ordered[2]: "chatgpt"}
# remap css class by actual AI name
ai_css = {"Claude": "claude", "Gemini": "gemini", "ChatGPT": "chatgpt"}

LAYOUT = dict(
    plot_bgcolor=BG, paper_bgcolor=BG,
    font=dict(family="JetBrains Mono, monospace", color="rgba(255,255,255,0.45)", size=11),
    margin=dict(t=30, b=10, l=10, r=10),
    xaxis=dict(showgrid=False, zeroline=False, tickcolor="transparent",
               linecolor=GRID, tickfont=dict(color="rgba(255,255,255,0.5)", size=11)),
    yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
               tickfont=dict(color="rgba(255,255,255,0.35)", size=10)),
)

# ── HERO ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">⚡ Student Vote · 10 Participants</div>
  <div class="hero-title">Which AI<br><span>Wins?</span></div>
  <div class="hero-sub">당곡고 × 수도여고 — Claude vs Gemini vs ChatGPT</div>
</div>
""", unsafe_allow_html=True)

# ── SCORE CARDS ─────────────────────────────────────────────────────
cards_html = '<div class="score-row">'
for i, a in enumerate(ordered):
    cls   = ai_css[a]
    medal = ["🥇","🥈","🥉"][i]
    cards_html += f"""
    <div class="score-card {cls}">
      <div class="rank-tag">{medal} &nbsp;{rank_labels[a]}</div>
      <div class="ai-name">{a}</div>
      <div class="ai-score">{scores[a]}</div>
      <div class="ai-score-label">TOTAL POINTS</div>
      <div class="bg-num">{scores[a]}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

st.markdown('<div class="slash-divider"><span>CHARTS</span></div>', unsafe_allow_html=True)

# ── ROW 1: BAR + DONUT ──────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown('<div class="sec-label">// 01</div><div class="sec-title">Total Score</div>', unsafe_allow_html=True)
    fig = go.Figure()
    for a in ordered:
        fig.add_trace(go.Bar(
            x=[a], y=[scores[a]],
            marker=dict(
                color=C[a],
                opacity=0.85,
                line=dict(width=0),
            ),
            width=0.55,
            text=[str(scores[a])],
            textposition="outside",
            textfont=dict(size=18, color=C[a], family="Bebas Neue"),
            showlegend=False,
        ))
    fig.update_layout(
        **LAYOUT, height=340,
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   range=[0, max(scores.values()) + 5],
                   tickfont=dict(color="rgba(255,255,255,0.3)")),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color="#fff", size=14, family="Bebas Neue")),
        bargap=0.35,
    )
    # subtle glow via shape
    for a in ordered:
        fig.add_shape(type="rect",
            x0=ordered.index(a)-0.3, x1=ordered.index(a)+0.3,
            y0=0, y1=scores[a],
            fillcolor=C[a], opacity=0.06, line_width=0,
        )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="sec-label">// 02</div><div class="sec-title">Share</div>', unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=AI,
        values=[scores[a] for a in AI],
        hole=0.65,
        marker=dict(
            colors=[C[a] for a in AI],
            line=dict(color=BG, width=4),
        ),
        textinfo="label+percent",
        textfont=dict(size=11, family="JetBrains Mono"),
        insidetextorientation="radial",
        pull=[0.05 if a == ordered[0] else 0 for a in AI],
        rotation=90,
    ))
    fig2.update_layout(
        **LAYOUT, height=340,
        showlegend=False,
        annotations=[dict(
            text=f'<b style="font-size:20px">{ordered[0]}</b><br><span style="font-size:11px; color:rgba(255,255,255,0.4)">WINNER</span>',
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#fff", family="Bebas Neue", size=14),
        )],
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── ROW 2: PODIUM + STACKED ─────────────────────────────────────────
col3, col4 = st.columns([2, 3], gap="medium")

with col3:
    st.markdown('<div class="sec-label">// 03</div><div class="sec-title">Podium</div>', unsafe_allow_html=True)
    pod_order   = [ordered[1], ordered[0], ordered[2]]
    pod_heights = [70, 100, 50]
    pod_medals  = ["🥈", "🥇", "🥉"]

    fig3 = go.Figure()
    for ai, h, m in zip(pod_order, pod_heights, pod_medals):
        fig3.add_trace(go.Bar(
            x=[ai], y=[h],
            marker=dict(
                color=C[ai], opacity=0.9,
                line=dict(width=0),
                pattern=dict(shape="", bgcolor=C[ai]),
            ),
            width=0.6,
            text=[f"{m}"],
            textposition="outside",
            textfont=dict(size=22),
            showlegend=False,
        ))
        # score annotation inside bar
        fig3.add_annotation(
            x=ai, y=h / 2,
            text=f"<b>{scores[ai]}</b>",
            showarrow=False,
            font=dict(size=20, color=BG, family="Bebas Neue"),
        )
    fig3.update_layout(
        **LAYOUT, height=340,
        yaxis=dict(visible=False, range=[0, 145]),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color="#fff", size=13, family="Bebas Neue")),
        bargap=0.25,
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with col4:
    st.markdown('<div class="sec-label">// 04</div><div class="sec-title">Rank Distribution</div>', unsafe_allow_html=True)
    rank_color = {1: "#fbbf24", 2: "#94a3b8", 3: "#92400e"}
    rank_names = {1: "🥇 1st", 2: "🥈 2nd", 3: "🥉 3rd"}

    fig4 = go.Figure()
    for r in [3, 2, 1]:
        fig4.add_trace(go.Bar(
            name=rank_names[r],
            x=AI,
            y=[rank_counts[a][r] for a in AI],
            marker=dict(color=rank_color[r], opacity=0.85, line=dict(width=0)),
            text=[f"{rank_counts[a][r]}" for a in AI],
            textposition="inside",
            textfont=dict(size=14, color="#000", family="Bebas Neue"),
        ))
    fig4.update_layout(
        **LAYOUT,
        barmode="stack", height=340,
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=1.08,
            font=dict(color="rgba(255,255,255,0.6)", size=11),
            bgcolor="transparent",
        ),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(color="#fff", size=13, family="Bebas Neue")),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   ticksuffix="회", tickfont=dict(color="rgba(255,255,255,0.3)")),
        bargap=0.35,
    )
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ── RAW DATA ────────────────────────────────────────────────────────
st.markdown('<div class="slash-divider"><span>RAW DATA</span></div>', unsafe_allow_html=True)
with st.expander("📋 원시 투표 데이터"):
    badge = {1: "badge-1", 2: "badge-2", 3: "badge-3"}
    rows_html = """
    <div class="raw-table-wrap">
    <table class="raw-table">
      <thead><tr>
        <th>NAME</th><th>CLAUDE</th><th>GEMINI</th><th>CHATGPT</th>
      </tr></thead><tbody>"""
    for name, ranks in raw:
        r = [f'<span class="badge {badge[x]}">{x}등</span>' for x in ranks]
        rows_html += f"<tr><td>{name}</td><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    rows_html += "</tbody></table></div>"
    st.markdown(rows_html, unsafe_allow_html=True)
