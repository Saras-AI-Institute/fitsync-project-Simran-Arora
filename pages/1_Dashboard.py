import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="FitSync Dashboard")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

.block-container {
    padding-top: 2rem;
}

/* Card Style */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* Section Title */
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #e2e8f0;
}

/* Metric */
.metric {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

/* Subtitle */
.subtitle {
    color: #94a3b8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

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
st.title("🏋️ FitSync Dashboard")
st.markdown('<div class="subtitle">Track your performance, recovery, and daily activity in one place.</div>', unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data available for selected range.")
    st.stop()

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card"><div class="section-title">👣 Avg Steps</div>'
                f'<div class="metric">{filtered_df["Steps"].mean():.0f}</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="section-title">😴 Avg Sleep</div>'
                f'<div class="metric">{filtered_df["Sleep_Hours"].mean():.1f} hrs</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><div class="section-title">⚡ Avg Recovery</div>'
                f'<div class="metric">{filtered_df["Recovery_Score"].mean():.1f}</div></div>', unsafe_allow_html=True)

# ---------------- MAIN CHARTS ----------------
st.markdown("### 📈 Performance Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig1 = px.line(
        filtered_df,
        x='Date',
        y=['Recovery_Score', 'Sleep_Hours'],
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig2 = px.scatter(
        filtered_df,
        x='Steps',
        y='Recovery_Score',
        color='Sleep_Hours',
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SECONDARY CHARTS ----------------
st.markdown("### 📊 Additional Insights")

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig3 = px.scatter(
        filtered_df,
        x='Heart_Rate_bpm',
        y='Recovery_Score',
        template="plotly_dark"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig4 = px.line(
        filtered_df,
        x='Date',
        y='Calories_Burned',
        template="plotly_dark"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)