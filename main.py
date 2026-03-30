import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 투표 결과",
    page_icon="🏆",
    layout="wide",
)

# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
  }

  .main { background: #0f0f17; }

  .title-block {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
  }
  .title-block h1 {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
  }
  .title-block p {
    color: #6b7280;
    font-size: 0.95rem;
  }

  .metric-card {
    background: #1a1a2e;
    border: 1px solid #2d2d44;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
  }
  .metric-card .label { color: #9ca3af; font-size: 0.82rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
  .metric-card .value { font-size: 2.4rem; font-weight: 900; margin-top: 0.2rem; }
  .metric-card.claude  .value { color: #a78bfa; }
  .metric-card.gemini  .value { color: #60a5fa; }
  .metric-card.chatgpt .value { color: #34d399; }

  .section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e5e7eb;
    margin: 2rem 0 1rem;
    padding-left: 0.6rem;
    border-left: 3px solid #a78bfa;
  }
</style>
""", unsafe_allow_html=True)

# ── 원시 데이터 ──────────────────────────────────────────────
raw = [
    ("당곡고 변시현",    [1, 2, 3]),   # 클로드, 제미나이, 챗지피티
    ("수도여고 신연서",  [1, 3, 2]),   # 클로드, 챗지피티→2등, 제미나이→3등  ※ "클로드 챗지피티 제미나이"
    ("당곡고 이마루",   [2, 1, 3]),   # 제미나이, 클로드, 챗지피티
    ("수도여고 최윤영",  [2, 1, 3]),   # 제미나이, 클로드, 지피티
    ("당곡고 이지훈",   [1, 2, 3]),
    ("수도여고 조윤서",  [1, 2, 3]),
    ("당곡고 김도연",   [1, 2, 3]),
    ("수도여고 이서영",  [1, 3, 2]),   # 클로드, 지피티, 재미나이
    ("당곡고 이한규",   [1, 2, 3]),
    ("20105 김준영",    [1, 2, 3]),
]
# 각 row: (이름, [클로드순위, 제미나이순위, 챗지피티순위])

AI_NAMES  = ["Claude", "Gemini", "ChatGPT"]
AI_COLORS = {
    "Claude":  "#a78bfa",
    "Gemini":  "#60a5fa",
    "ChatGPT": "#34d399",
}

# ── 점수 계산 (1등=3점, 2등=2점, 3등=1점) ───────────────────
scores = {"Claude": 0, "Gemini": 0, "ChatGPT": 0}
rank_counts = {ai: {1: 0, 2: 0, 3: 0} for ai in AI_NAMES}

for _, ranks in raw:
    for ai, r in zip(AI_NAMES, ranks):
        scores[ai]       += (4 - r)
        rank_counts[ai][r] += 1

n = len(raw)

# ── 헤더 ────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
  <h1>🏆 AI 선호도 투표 결과</h1>
  <p>당곡고 · 수도여고 학생 10명 참여 · Claude vs Gemini vs ChatGPT</p>
</div>
""", unsafe_allow_html=True)

# ── 요약 메트릭 ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card">
      <div class="label">총 참여자</div>
      <div class="value" style="color:#e5e7eb">{n}명</div>
    </div>""", unsafe_allow_html=True)
for col, ai, cls in zip([c2, c3, c4], AI_NAMES, ["claude","gemini","chatgpt"]):
    with col:
        st.markdown(f"""<div class="metric-card {cls}">
          <div class="label">{ai} 총점</div>
          <div class="value">{scores[ai]}점</div>
        </div>""", unsafe_allow_html=True)

# ── 차트 1 & 2: 총점 바 + 파이 ──────────────────────────────
st.markdown('<div class="section-title">📊 종합 점수 & 점유율</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    fig_bar = go.Figure()
    sorted_ai = sorted(AI_NAMES, key=lambda x: scores[x], reverse=True)
    for ai in sorted_ai:
        fig_bar.add_trace(go.Bar(
            x=[ai], y=[scores[ai]],
            name=ai,
            marker_color=AI_COLORS[ai],
            marker_line_width=0,
            text=[f"{scores[ai]}점"],
            textposition="outside",
            textfont=dict(size=14, color=AI_COLORS[ai], family="Pretendard"),
            width=0.45,
        ))
    fig_bar.update_layout(
        title=dict(text="AI별 총 점수", font=dict(color="#e5e7eb", size=15)),
        plot_bgcolor="#1a1a2e", paper_bgcolor="#1a1a2e",
        font=dict(color="#9ca3af"),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#2d2d44", zeroline=False, range=[0, max(scores.values())+4]),
        margin=dict(t=50, b=20, l=20, r=20),
        height=360,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    fig_pie = go.Figure(go.Pie(
        labels=AI_NAMES,
        values=[scores[ai] for ai in AI_NAMES],
        hole=0.52,
        marker=dict(colors=[AI_COLORS[ai] for ai in AI_NAMES], line=dict(color="#0f0f17", width=3)),
        textinfo="label+percent",
        textfont=dict(size=13, family="Pretendard"),
        insidetextorientation="radial",
        pull=[0.03 if scores[ai] == max(scores.values()) else 0 for ai in AI_NAMES],
    ))
    fig_pie.update_layout(
        title=dict(text="점수 점유율 (도넛)", font=dict(color="#e5e7eb", size=15)),
        plot_bgcolor="#1a1a2e", paper_bgcolor="#1a1a2e",
        font=dict(color="#9ca3af"),
        legend=dict(font=dict(color="#e5e7eb")),
        margin=dict(t=50, b=20, l=20, r=20),
        height=360,
        annotations=[dict(
            text=f"<b>{sorted_ai[0]}</b><br>1위",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=AI_COLORS[sorted_ai[0]], family="Pretendard"),
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── 차트 3: 포디움 ───────────────────────────────────────────
st.markdown('<div class="section-title">🥇 포디움</div>', unsafe_allow_html=True)

podium_order = sorted(AI_NAMES, key=lambda x: scores[x], reverse=True)
podium_heights = [100, 70, 50]
podium_labels  = ["🥇", "🥈", "🥉"]
display_order  = [podium_order[1], podium_order[0], podium_order[2]]  # 2등, 1등, 3등 배치
display_heights= [podium_heights[1], podium_heights[0], podium_heights[2]]
display_medals = [podium_labels[1], podium_labels[0], podium_labels[2]]

fig_pod = go.Figure()
for i, (ai, h, medal) in enumerate(zip(display_order, display_heights, display_medals)):
    fig_pod.add_trace(go.Bar(
        x=[ai], y=[h],
        name=ai,
        marker_color=AI_COLORS[ai],
        marker_line_width=0,
        width=0.5,
        text=[f"{medal}<br><b>{scores[ai]}점</b>"],
        textposition="outside",
        textfont=dict(size=16, family="Pretendard", color=AI_COLORS[ai]),
    ))

fig_pod.update_layout(
    plot_bgcolor="#1a1a2e", paper_bgcolor="#1a1a2e",
    font=dict(color="#9ca3af"),
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=15, color="#e5e7eb")),
    yaxis=dict(visible=False, range=[0, 140]),
    margin=dict(t=30, b=20, l=20, r=20),
    height=300,
    bargap=0.3,
)
st.plotly_chart(fig_pod, use_container_width=True)

# ── 차트 4: 1·2·3등 획득 횟수 누적 바 ───────────────────────
st.markdown('<div class="section-title">📈 순위별 획득 횟수 (누적)</div>', unsafe_allow_html=True)

rank_colors = {1: "#fbbf24", 2: "#94a3b8", 3: "#b45309"}

fig_stk = go.Figure()
for rank in [3, 2, 1]:
    fig_stk.add_trace(go.Bar(
        name=f"{rank}등",
        x=AI_NAMES,
        y=[rank_counts[ai][rank] for ai in AI_NAMES],
        marker_color=rank_colors[rank],
        marker_line_width=0,
        text=[f"{rank_counts[ai][rank]}회" for ai in AI_NAMES],
        textposition="inside",
        textfont=dict(size=13, color="#0f0f17", family="Pretendard"),
    ))

fig_stk.update_layout(
    barmode="stack",
    plot_bgcolor="#1a1a2e", paper_bgcolor="#1a1a2e",
    font=dict(color="#9ca3af"),
    legend=dict(font=dict(color="#e5e7eb"), orientation="h", y=1.08, x=0.5, xanchor="center"),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=14, color="#e5e7eb")),
    yaxis=dict(showgrid=True, gridcolor="#2d2d44", zeroline=False, ticksuffix="회"),
    margin=dict(t=40, b=20, l=20, r=20),
    height=350,
)
st.plotly_chart(fig_stk, use_container_width=True)

# ── 원시 데이터 테이블 ───────────────────────────────────────
with st.expander("📋 원시 투표 데이터 보기"):
    rows = []
    for name, ranks in raw:
        rows.append({
            "이름": name,
            "Claude 순위": f"{ranks[0]}등",
            "Gemini 순위": f"{ranks[1]}등",
            "ChatGPT 순위": f"{ranks[2]}등",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
