import streamlit as st

st.set_page_config(page_title="FitSync Pro", layout="wide", page_icon="⚡")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060912 !important;
    color: #e8eaf0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(56,189,248,0.13) 0%, transparent 70%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,0.10) 0%, transparent 60%),
                #060912 !important;
}

[data-testid="stSidebar"] { background: #0b0f1e !important; border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1200px !important; }

/* ---- HERO ---- */
.hero-wrap {
    position: relative;
    padding: 80px 60px 70px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(14,21,42,0.95) 0%, rgba(10,15,30,0.90) 100%);
    border: 1px solid rgba(56,189,248,0.18);
    overflow: hidden;
    margin: 2rem 0 2.5rem;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 80% at 0% 50%, rgba(56,189,248,0.08) 0%, transparent 65%),
                radial-gradient(ellipse 50% 60% at 100% 20%, rgba(99,102,241,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -2px; left: 10%; right: 10%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, #6366f1, transparent);
    border-radius: 2px;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56,189,248,0.10);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 28px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}
.hero-badge-dot {
    width: 6px; height: 6px;
    background: #38bdf8;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.7); }
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 6vw, 5.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0f4ff;
    margin-bottom: 24px;
}
.hero-title span {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 18px;
    line-height: 1.7;
    color: #94a3b8;
    max-width: 580px;
    font-weight: 300;
    margin-bottom: 40px;
}
.hero-stats {
    display: flex;
    gap: 40px;
    flex-wrap: wrap;
}
.hero-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f0f4ff;
    line-height: 1;
}
.hero-stat-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}
.hero-glyph {
    position: absolute;
    right: 60px; top: 50%;
    transform: translateY(-50%);
    width: 220px; height: 220px;
    opacity: 0.06;
    font-size: 200px;
    line-height: 1;
    pointer-events: none;
    user-select: none;
}

/* ---- SECTION HEADER ---- */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 3rem 0 1.5rem;
}
.section-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(56,189,248,0.3), transparent);
}
.section-header-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e2e8f0;
}

/* ---- FEATURE CARDS ---- */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 2rem;
}
.feat-card {
    background: rgba(14,21,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px 26px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s;
}
.feat-card:hover {
    border-color: rgba(56,189,248,0.30);
    transform: translateY(-3px);
}
.feat-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 80% at 50% 0%, rgba(56,189,248,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.feat-icon {
    font-size: 2rem;
    margin-bottom: 14px;
    display: block;
}
.feat-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 8px;
}
.feat-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.65;
}

/* ---- HOW IT WORKS ---- */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 2rem;
}
.step-card {
    background: rgba(14,21,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 30px 26px;
    position: relative;
    overflow: hidden;
}
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    color: rgba(56,189,248,0.12);
    position: absolute;
    top: 10px; right: 20px;
    line-height: 1;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 10px;
}
.step-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.65;
}

/* ---- CTA BANNER ---- */
.cta-wrap {
    background: linear-gradient(135deg, rgba(56,189,248,0.12) 0%, rgba(99,102,241,0.10) 100%);
    border: 1px solid rgba(56,189,248,0.20);
    border-radius: 20px;
    padding: 36px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    margin: 1.5rem 0;
}
.cta-text-main {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 6px;
}
.cta-text-sub {
    font-size: 14px;
    color: #64748b;
}

[data-testid="stInfo"] {
    background: rgba(56,189,248,0.10) !important;
    border: 1px solid rgba(56,189,248,0.30) !important;
    border-radius: 14px !important;
    color: #38bdf8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ---- HERO ----
st.markdown("""
<div class="hero-wrap">
    <div class="hero-glyph">⚡</div>
    <div class="hero-badge"><span class="hero-badge-dot"></span>Health Intelligence Platform</div>
    <div class="hero-title">Your body,<br>decoded with <span>precision.</span></div>
    <p class="hero-sub">FitSync Pro transforms raw activity data into meaningful health narratives — revealing patterns that help you move, sleep, and recover at your absolute best.</p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">4+</div>
            <div class="hero-stat-label">Vital Metrics</div>
        </div>
        <div>
            <div class="hero-stat-val">Real-time</div>
            <div class="hero-stat-label">Trend Analysis</div>
        </div>
        <div>
            <div class="hero-stat-val">Smart</div>
            <div class="hero-stat-label">Recovery Scoring</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- WHAT IT TELLS YOU ----
st.markdown("""
<div class="section-header">
    <span class="section-header-text">What It Tracks</span>
    <div class="section-header-line"></div>
</div>
<div class="feat-grid">
    <div class="feat-card">
        <span class="feat-icon">😴</span>
        <div class="feat-title">Sleep Intelligence</div>
        <div class="feat-desc">Understand how sleep duration correlates with recovery. Spot the nights that charge you up — and those that drain you.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">❤️</span>
        <div class="feat-title">Recovery Score</div>
        <div class="feat-desc">A daily readiness score that tells you exactly how prepared your body is for training, work, or rest.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">👟</span>
        <div class="feat-title">Activity Tracking</div>
        <div class="feat-desc">Daily step counts and movement consistency visualised across time — see your habits, not just your numbers.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">🔥</span>
        <div class="feat-title">Calorie Burn</div>
        <div class="feat-desc">Monitor energy expenditure and spot trends in your metabolic output over days, weeks, and months.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">💓</span>
        <div class="feat-title">Heart Rate Analysis</div>
        <div class="feat-desc">See how your resting heart rate links to recovery, and how exertion levels evolve over your fitness journey.</div>
    </div>
    <div class="feat-card">
        <span class="feat-icon">📈</span>
        <div class="feat-title">Trend Detection</div>
        <div class="feat-desc">Monthly and weekly breakdowns surface the bigger picture — and pinpoint exactly when things shifted.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- HOW IT WORKS ----
st.markdown("""
<div class="section-header">
    <span class="section-header-text">How It Works</span>
    <div class="section-header-line"></div>
</div>
<div class="steps-grid">
    <div class="step-card">
        <div class="step-num">01</div>
        <div class="step-title">Track</div>
        <div class="step-desc">Your steps, sleep, heart rate, and calories are collected, cleaned, and structured automatically.</div>
    </div>
    <div class="step-card">
        <div class="step-num">02</div>
        <div class="step-title">Analyze</div>
        <div class="step-desc">The system identifies trends, correlations, and anomalies in your daily wellness routine.</div>
    </div>
    <div class="step-card">
        <div class="step-num">03</div>
        <div class="step-title">Improve</div>
        <div class="step-desc">Walk away with clear, visual insights to optimize your recovery, sleep quality, and peak performance.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- CTA ----
st.markdown("""
<div class="cta-wrap">
    <div>
        <div class="cta-text-main">Ready to explore your data?</div>
        <div class="cta-text-sub">Navigate to Dashboard or Trends & Insights from the sidebar.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.info("⚡  Open the **Dashboard** or **Trends & Insights** page from the sidebar to view your analytics.")