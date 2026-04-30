import streamlit as st

st.set_page_config(page_title="FitSync Pro", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #0b1220;
    color: #e2e8f0;
}

/* Hide sidebar content except navigation */
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
    display: none;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #2563eb, #10b981);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: #111827;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
}

/* Title */
.title {
    font-size: 2.8rem;
    font-weight: bold;
}

/* Subtitle */
.subtitle {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="title">FitSync Pro</div>
    <p class="subtitle">A premium interactive wellness dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- WHAT IS IT ----------------
st.markdown("## What is FitSync Pro?")
st.markdown("""
<div class="card">
FitSync Pro is a modern health analytics dashboard that transforms your daily activity data into clear, actionable insights.  
It helps you understand your body better — not just numbers, but patterns and meaning.
</div>
""", unsafe_allow_html=True)

# ---------------- HOW IT WORKS ----------------
st.markdown("## How it Works")
col1, col2, col3 = st.columns(3)

col1.markdown("""
<div class="card">
<b>1. Track</b><br>
Your steps, sleep, heart rate, and calories are collected and organized.
</div>
""", unsafe_allow_html=True)

col2.markdown("""
<div class="card">
<b>2. Analyze</b><br>
The system identifies trends and patterns in your daily routine.
</div>
""", unsafe_allow_html=True)

col3.markdown("""
<div class="card">
<b>3. Improve</b><br>
You get insights to optimize recovery, sleep, and performance.
</div>
""", unsafe_allow_html=True)

# ---------------- WHAT IT TELLS ----------------
st.markdown("## What It Tells You")

col1, col2 = st.columns(2)

col1.markdown("""
<div class="card">
<b>😴 Sleep Insights</b><br>
Understand how your sleep duration impacts recovery and performance.
</div>
""", unsafe_allow_html=True)

col2.markdown("""
<div class="card">
<b>❤️ Recovery Score</b><br>
Know how ready your body is for the next day.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1.markdown("""
<div class="card">
<b>👟 Activity Tracking</b><br>
Track your daily steps and movement consistency.
</div>
""", unsafe_allow_html=True)

col2.markdown("""
<div class="card">
<b>🔥 Calories Burned</b><br>
Monitor energy output and fitness level.
</div>
""", unsafe_allow_html=True)

# ---------------- CTA ----------------
st.markdown("## Explore")
st.info("Go to the Dashboard page from the sidebar to view your analytics.")