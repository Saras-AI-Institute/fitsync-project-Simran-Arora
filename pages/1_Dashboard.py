import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="FitSync Dashboard", page_icon="🏋️")

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
    background: radial-gradient(ellipse 80% 50% at 50% -5%, rgba(56,189,248,0.10) 0%, transparent 70%), #060912 !important;
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
    line-height: 1.1;
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
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: rgba(56,189,248,0.25); }
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, linear-gradient(90deg, #38bdf8, #6366f1));
}
.metric-icon { font-size: 1.2rem; margin-bottom: 10px; display: block; }
.metric-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f4ff;
    line-height: 1;
}
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
.chart-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #94a3b8;
    padding: 16px 20px 0;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    font-size: 11px;
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2rem 0 1.4rem;
}
.section-divider-line { flex: 1; height: 1px; background: rgba(255,255,255,0.06); }
.section-divider-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
}

[data-testid="stSelectbox"] label { color: #94a3b8 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# Plotly theme base
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
)
COLORS = ["#38bdf8", "#6366f1", "#a78bfa", "#34d399", "#f472b6", "#fb923c"]

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
    <div class="page-title">🏋️ FitSync Dashboard</div>
    <div class="page-subtitle">Track your performance, recovery, and daily activity in one place.</div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data available for selected range.")
    st.stop()

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#38bdf8,#0ea5e9)">
        <span class="metric-icon">👣</span>
        <div class="metric-label">Avg Steps</div>
        <div class="metric-value">{filtered_df['Steps'].mean():,.0f}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#6366f1,#8b5cf6)">
        <span class="metric-icon">😴</span>
        <div class="metric-label">Avg Sleep</div>
        <div class="metric-value">{filtered_df['Sleep_Hours'].mean():.1f}<span class="metric-unit">hrs</span></div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#34d399,#10b981)">
        <span class="metric-icon">⚡</span>
        <div class="metric-label">Avg Recovery</div>
        <div class="metric-value">{filtered_df['Recovery_Score'].mean():.1f}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="metric-card" style="--accent: linear-gradient(90deg,#f472b6,#ec4899)">
        <span class="metric-icon">🔥</span>
        <div class="metric-label">Avg Calories</div>
        <div class="metric-value">{filtered_df['Calories_Burned'].mean():,.0f}</div>
    </div>""", unsafe_allow_html=True)

# ---------------- PERFORMANCE TRENDS ----------------
st.markdown("""<div class="section-divider">
    <span class="section-divider-text">📈 Performance Trends</span>
    <div class="section-divider-line"></div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    # Area chart: Recovery + Sleep over time
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'], y=filtered_df['Recovery_Score'],
        name='Recovery Score',
        line=dict(color='#38bdf8', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(56,189,248,0.08)',
        hovertemplate='<b>Recovery</b>: %{y:.1f}<extra></extra>'
    ))
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'], y=filtered_df['Sleep_Hours'],
        name='Sleep Hours',
        line=dict(color='#6366f1', width=2.5, dash='dot'),
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.06)',
        hovertemplate='<b>Sleep</b>: %{y:.1f} hrs<extra></extra>'
    ))
    fig1.update_layout(**CHART_LAYOUT, height=280, title=dict(text="Recovery & Sleep Over Time", font=dict(size=13, color="#e2e8f0"), x=0.01))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Radial gauge: avg recovery
    avg_rec = filtered_df['Recovery_Score'].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_rec,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Recovery Score", 'font': {'size': 13, 'color': '#e2e8f0'}},
        delta={'reference': 70, 'increasing': {'color': '#34d399'}, 'decreasing': {'color': '#f472b6'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#475569', 'tickwidth': 1},
            'bar': {'color': '#38bdf8', 'thickness': 0.22},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(248,113,113,0.15)'},
                {'range': [40, 70], 'color': 'rgba(251,191,36,0.10)'},
                {'range': [70, 100], 'color': 'rgba(52,211,153,0.15)'},
            ],
            'threshold': {'line': {'color': '#34d399', 'width': 3}, 'thickness': 0.75, 'value': 70}
        },
        number={'font': {'size': 36, 'color': '#f0f4ff', 'family': 'Syne'}, 'suffix': ''}
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#94a3b8"), height=280, margin=dict(l=20, r=20, t=40, b=10))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    # Bubble: Steps vs Recovery coloured by Sleep
    chart_df = filtered_df.copy()
    chart_df['Calories_Burned'] = chart_df['Calories_Burned'].fillna(chart_df['Calories_Burned'].median())

    fig2 = px.scatter(
        chart_df, x='Steps', y='Recovery_Score', color='Sleep_Hours',
        size='Calories_Burned',
        color_continuous_scale=['#1e293b','#6366f1','#38bdf8'],
        labels={'Steps': 'Daily Steps', 'Recovery_Score': 'Recovery Score', 'Sleep_Hours': 'Sleep (hrs)'},
        hover_data=['Date'],
        title='Steps vs Recovery (size = Calories)'
    )
    fig2.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color='rgba(255,255,255,0.2)')))
    fig2.update_layout(**CHART_LAYOUT, height=280, title=dict(font=dict(size=13, color="#e2e8f0"), x=0.01),
                       coloraxis_colorbar=dict(thickness=10, tickfont=dict(size=10)))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Calories bar
    fig4 = go.Figure(go.Bar(
        x=filtered_df['Date'], y=filtered_df['Calories_Burned'],
        marker=dict(
            color=filtered_df['Calories_Burned'],
            colorscale=[[0, '#1e293b'], [0.5, '#6366f1'], [1, '#38bdf8']],
            showscale=False,
            line=dict(width=0)
        ),
        hovertemplate='<b>%{x|%b %d}</b>: %{y:.0f} kcal<extra></extra>'
    ))
    fig4.update_layout(**CHART_LAYOUT, height=280, title=dict(text="Calories Burned", font=dict(size=13, color="#e2e8f0"), x=0.01))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ADDITIONAL INSIGHTS ----------------
st.markdown("""<div class="section-divider">
    <span class="section-divider-text">📊 Additional Insights</span>
    <div class="section-divider-line"></div>
</div>""", unsafe_allow_html=True)

col5, col6 = st.columns([2, 3])

with col5:
    # Donut: sleep quality buckets
    bins = [0, 5, 7, 9, 24]
    labels_s = ['Poor (<5h)', 'Fair (5–7h)', 'Good (7–9h)', 'Excess (>9h)']
    filtered_df['Sleep_Cat'] = pd.cut(filtered_df['Sleep_Hours'], bins=bins, labels=labels_s)
    sleep_dist = filtered_df['Sleep_Cat'].value_counts().reset_index()
    sleep_dist.columns = ['Category', 'Count']
    fig_donut = px.pie(
        sleep_dist, names='Category', values='Count', hole=0.62,
        color_discrete_sequence=['#f87171', '#fbbf24', '#34d399', '#6366f1'],
        title='Sleep Quality Distribution'
    )
    fig_donut.update_traces(textfont=dict(size=11), hovertemplate='<b>%{label}</b>: %{value} nights (%{percent})<extra></extra>')
    fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="DM Sans", color="#94a3b8"),
                            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                            title=dict(font=dict(size=13, color="#e2e8f0"), x=0.01),
                            height=300, margin=dict(l=10, r=10, t=40, b=10))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    # Heart rate vs recovery with trendline
    fig3 = px.scatter(
        filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
        trendline='lowess',
        color_discrete_sequence=['#38bdf8'],
        labels={'Heart_Rate_bpm': 'Heart Rate (bpm)', 'Recovery_Score': 'Recovery Score'},
        title='Heart Rate vs Recovery Score',
        hover_data=['Date', 'Sleep_Hours']
    )
    fig3.update_traces(marker=dict(opacity=0.7, size=7))
    fig3.data[1].line.color = '#f472b6'  # trendline colour
    fig3.data[1].line.width = 2.5
    fig3.update_layout(**CHART_LAYOUT, height=300, title=dict(font=dict(size=13, color="#e2e8f0"), x=0.01))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)