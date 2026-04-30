import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide", page_title="Trends & Insights")

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

/* Headings */
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #e2e8f0;
}

/* Metrics */
.metric {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return process_data()

df = load_data()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# ---------------- SIDEBAR FILTER ----------------
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
st.title("📊 Trends & Insights")

if filtered_df.empty:
    st.warning("No data available for selected range.")
    st.stop()

# ---------------- METRIC CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card"><div class="section-title">Avg Recovery</div>'
                f'<div class="metric">{filtered_df["Recovery_Score"].mean():.1f}</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="section-title">Avg Sleep</div>'
                f'<div class="metric">{filtered_df["Sleep_Hours"].mean():.1f} hrs</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><div class="section-title">Avg Steps</div>'
                f'<div class="metric">{filtered_df["Steps"].mean():.0f}</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card"><div class="section-title">Avg Calories</div>'
                f'<div class="metric">{filtered_df["Calories_Burned"].mean():.0f}</div></div>', unsafe_allow_html=True)

# ---------------- MONTHLY TREND ----------------
st.markdown("### 📈 Recovery Trend")

filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype(str)
monthly = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()

fig1 = px.line(monthly, x='Month', y='Recovery_Score',
               template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)

# ---------------- DISTRIBUTION ----------------
st.markdown("### 📊 Distributions")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("#### Steps Distribution")
        fig_steps = px.histogram(filtered_df, x='Steps', nbins=30, template="plotly_dark")
        st.plotly_chart(fig_steps, use_container_width=True)

with col2:
    with st.container():
        st.markdown("#### Calories Burned")
        fig_cal = px.histogram(filtered_df, x='Calories_Burned', nbins=30, template="plotly_dark")
        st.plotly_chart(fig_cal, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.markdown("#### Recovery Score")
        fig_rec = px.histogram(filtered_df, x='Recovery_Score', nbins=30, template="plotly_dark")
        st.plotly_chart(fig_rec, use_container_width=True)

with col4:
    with st.container():
        st.markdown("#### Sleep Hours")
        fig_sleep = px.histogram(filtered_df, x='Sleep_Hours', nbins=30, template="plotly_dark")
        st.plotly_chart(fig_sleep, use_container_width=True)

# ---------------- SUMMARY ----------------
st.markdown("### 📋 Summary")

summary = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max'])

st.dataframe(summary, use_container_width=True)