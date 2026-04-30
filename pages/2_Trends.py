import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="Trends & Insights", page_icon="📊")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060912 !important;
    color: #e8eaf0;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 70% 45% at 50% -5%, rgba(99,102,241,0.10) 0%, transparent 65%), #060912 !important;
}
[data-testid="stSidebar"] { background: #0b0f1e !important; border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1300px !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #f0f4ff;
    letter-spacing: -0.03em;
}
.page-subtitle { font-size: 15px; color: #64748b; margin-top: 6px; font-weight: 300; }
.title-bar { margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.06); }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(14,21,42,0.95) 0%, rgba(10,15,30,0.90) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px 24px 18px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, linear-gradient(90deg, #38bdf8, #6366f1));
}
.metric-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; color: #64748b; margin-bottom: 6px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: #f0f4ff; line-height: 1; }
.metric-unit { font-size: 1rem; font-weight: 400; color: #94a3b8; margin-left: 4px; }

/* Chart containers */
.chart-wrap {
    background: rgba(14,21,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 4px;
    margin-bottom: 18px;
    overflow: hidden;
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2rem 0 1.4rem;
}
.section-divider-line { flex: 1; height: 1px; background: rgba(255,255,255,0.06); }
.section-divider-text { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #e2e8f0; }

[data-testid="stDataFrame"] { border-radius: 14px !important; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return process_data()

df = load_data()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

today = df['Date'].max()
if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] >= (today - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] >= (today - pd.Timedelta(days=30))]
else:
    filtered_df = df

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-bar">
    <div class="page-title">📊 Trends & Insights</div>
    <div class="page-subtitle">Uncover the patterns behind your performance data.</div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data available for selected range.")
    st.stop()

# ---------------- METRIC CARDS ----------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#38bdf8,#0ea5e9)">
        <div class="metric-label">Avg Recovery</div>
        <div class="metric-value">{filtered_df['Recovery_Score'].mean():.1f}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#6366f1,#8b5cf6)">
        <div class="metric-label">Avg Sleep</div>
        <div class="metric-value">{filtered_df['Sleep_Hours'].mean():.1f}<span class="metric-unit">hrs</span></div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#34d399,#10b981)">
        <div class="metric-label">Avg Steps</div>
        <div class="metric-value">{filtered_df['Steps'].mean():,.0f}</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#f472b6,#ec4899)">
        <div class="metric-label">Avg Calories</div>
        <div class="metric-value">{filtered_df['Calories_Burned'].mean():,.0f}</div>
    </div>""", unsafe_allow_html=True)

# ---------------- RECOVERY TREND ----------------
st.markdown("""<div class="section-divider">
    <span class="section-divider-text">📈 Recovery Trend</span>
    <div class="section-divider-line"></div>
</div>""", unsafe_allow_html=True)

filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype(str)
monthly = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()

# Styled area + bar combo
fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=monthly['Month'], y=monthly['Recovery_Score'],
    name='Monthly Avg',
    marker=dict(
        color=monthly['Recovery_Score'],
        colorscale=[[0, 'rgba(56,189,248,0.15)'], [1, 'rgba(56,189,248,0.55)']],
        showscale=False,
        line=dict(width=0)
    ),
    hovertemplate='<b>%{x}</b>: %{y:.1f}<extra></extra>'
))
fig_trend.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Recovery_Score'],
    mode='lines+markers',
    name='Trend',
    line=dict(color='#38bdf8', width=3),
    marker=dict(size=8, color='#38bdf8', line=dict(width=2, color='#0f172a')),
    hovertemplate='<b>%{x}</b>: %{y:.1f}<extra></extra>'
))
fig_trend.update_layout(**CHART_LAYOUT, height=300, title=dict(text="Monthly Recovery Score", font=dict(size=13, color="#e2e8f0"), x=0.01))
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig_trend, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DISTRIBUTIONS ----------------
st.markdown("""<div class="section-divider">
    <span class="section-divider-text">📊 Distributions</span>
    <div class="section-divider-line"></div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Steps — violin chart
    fig_steps = go.Figure(go.Violin(
        y=filtered_df['Steps'],
        box_visible=True,
        meanline_visible=True,
        fillcolor='rgba(56,189,248,0.15)',
        line_color='#38bdf8',
        name='Steps',
        points='suspectedoutliers',
        marker=dict(color='#38bdf8', opacity=0.5, size=4)
    ))
    fig_steps.update_layout(dict(
        CHART_LAYOUT,
        height=300,
        title=dict(text="Steps Distribution", font=dict(size=13, color="#e2e8f0"), x=0.01),
        xaxis=dict(showticklabels=False, gridcolor="rgba(0,0,0,0)")
    ))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_steps, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Calories — gradient histogram
    fig_cal = go.Figure(go.Histogram(
        x=filtered_df['Calories_Burned'],
        nbinsx=30,
        marker=dict(
            color=filtered_df['Calories_Burned'].sort_values(),
            colorscale=[[0, 'rgba(244,114,182,0.3)'], [1, '#f472b6']],
            showscale=False,
            line=dict(width=0)
        ),
        hovertemplate='%{x:.0f} kcal: %{y} days<extra></extra>'
    ))
    fig_cal.update_layout(**CHART_LAYOUT, height=300,
                          title=dict(text="Calories Burned", font=dict(size=13, color="#e2e8f0"), x=0.01))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_cal, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    # Recovery — donut/ring
    bins = [0, 40, 60, 80, 100]
    labels_r = ['Low (0–40)', 'Fair (40–60)', 'Good (60–80)', 'Peak (80–100)']
    filtered_df['Rec_Cat'] = pd.cut(filtered_df['Recovery_Score'], bins=bins, labels=labels_r)
    rec_dist = filtered_df['Rec_Cat'].value_counts().reset_index()
    rec_dist.columns = ['Category', 'Count']
    fig_rec = px.pie(
        rec_dist, names='Category', values='Count', hole=0.60,
        color_discrete_sequence=['#f87171', '#fbbf24', '#34d399', '#38bdf8'],
        title='Recovery Score Breakdown'
    )
    fig_rec.update_traces(textfont=dict(size=11), hovertemplate='<b>%{label}</b>: %{value} (%{percent})<extra></extra>')
    fig_rec.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="DM Sans", color="#94a3b8"),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                          title=dict(font=dict(size=13, color="#e2e8f0"), x=0.01),
                          height=300, margin=dict(l=10, r=10, t=40, b=10))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_rec, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Sleep — horizontal bar of binned counts
    bins_s = [0, 5, 6, 7, 8, 9, 24]
    labels_s2 = ['<5h', '5–6h', '6–7h', '7–8h', '8–9h', '>9h']
    filtered_df['Sleep_Bin'] = pd.cut(filtered_df['Sleep_Hours'], bins=bins_s, labels=labels_s2)
    sleep_counts = filtered_df['Sleep_Bin'].value_counts().sort_index().reset_index()
    sleep_counts.columns = ['Bucket', 'Count']

    fig_sleep = go.Figure(go.Bar(
        x=sleep_counts['Count'],
        y=sleep_counts['Bucket'],
        orientation='h',
        marker=dict(
            color=['#f87171','#fbbf24','#a78bfa','#34d399','#38bdf8','#6366f1'],
            line=dict(width=0)
        ),
        text=sleep_counts['Count'],
        textposition='outside',
        textfont=dict(color='#94a3b8', size=11),
        hovertemplate='<b>%{y}</b>: %{x} nights<extra></extra>'
    ))
    fig_sleep.update_layout(dict(
        CHART_LAYOUT,
        height=300,
        title=dict(text="Sleep Quality Breakdown", font=dict(size=13, color="#e2e8f0"), x=0.01),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)")
    ))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_sleep, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SUMMARY TABLE ----------------
st.markdown("""<div class="section-divider">
    <span class="section-divider-text">📋 Summary Statistics</span>
    <div class="section-divider-line"></div>
</div>""", unsafe_allow_html=True)

summary = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max']).round(1)
st.dataframe(summary.style.background_gradient(cmap='Blues', axis=1), use_container_width=True)