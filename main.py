import streamlit as st
import pandas as pd
import plotly.express as px
from modules.theme import apply_theme, render_theme_toggle
from modules.processor import process_data

# Set page config
st.set_page_config(layout="wide", page_title="FitSync")

# Apply the theme and render toggle
apply_theme()
render_theme_toggle()

# Custom CSS for fonts, spacing, border-radius, etc.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    body { font-family: 'Inter', sans-serif; }

    .metric-card {
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
        color: white;
        text-align: center;
        transition: transform 0.2s ease;
    }

    .metric-card:hover {
        transform: scale(1.02);
    }

    .steps-card { background-color: #4f8bf9; }
    .sleep-card { background-color: #a78bfa; }
    .recovery-card { background-color: #34d399; }

    .divider { margin-top: 20px; margin-bottom: 20px; height: 1px; background-color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(
    "<div style='background: linear-gradient(to right, #4f8bf9, #34d399); padding: 20px; border-radius: 10px; text-align: center;'>"
    "<h1 style='color: white;'>FitSync</h1>"
    "<h3 style='color: white;'>Your Personal Health Command Center 💪</h3>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Load and process data
data = process_data()

# Sidebar enhancements
st.sidebar.image('https://placekitten.com/200/200', width=100)  # Placeholder for user avatar
st.sidebar.write("Welcome, Athlete! 🏃")

# Render time range filter
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

def filter_data_by_time(data, time_range):
    if 'Date' in data.columns:
        max_date = data['Date'].max()
        if time_range == "Last 7 Days":
            min_date = max_date - pd.Timedelta(days=7)
            return data[data['Date'] >= min_date]
        elif time_range == "Last 30 Days":
            min_date = max_date - pd.Timedelta(days=30)
            return data[data['Date'] >= min_date]
    return data  # For "All Time"

# Enhance Sidebar with Additional Stats
if 'Date' in data.columns:
    total_days_tracked = len(data['Date'].unique())
    best_recovery_day = data.loc[data['Recovery_Score'].idxmax(), 'Date'] if not data.empty else 'N/A'
    st.sidebar.write("Total Days Tracked:", total_days_tracked)
    st.sidebar.write("Best Recovery Day:", best_recovery_day)

# Filter the data based on the sidebar selection
filtered_data = filter_data_by_time(data, time_range)

# Style Metric Cards
average_steps = filtered_data['Steps'].mean()
average_sleep = filtered_data['Sleep_Hours'].mean()
average_recovery = filtered_data['Recovery_Score'].mean()

st.markdown(
    f"""
    <div class='metric-card steps-card'>
        <h2>👟 {average_steps:.0f}</h2>
        <p>Average Steps</p>
    </div>

    <div class='metric-card sleep-card'>
        <h2>😴 {average_sleep:.1f}</h2>
        <p>Avg Sleep Hours</p>
    </div>

    <div class='metric-card recovery-card'>
        <h2>❤️ {average_recovery:.0f}</h2>
        <p>Average Recovery Score</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Interactive Charts
st.write("### Interactive Charts")

# Steps over time
steps_fig = px.line(filtered_data, x='Date', y='Steps', title='Steps Over Time', color_discrete_sequence=['#4f8bf9'])
st.plotly_chart(steps_fig)

# Sleep hours per day
sleep_fig = px.bar(filtered_data, x='Date', y='Sleep_Hours', title='Sleep Hours Per Day', color_discrete_sequence=['#a78bfa'])
st.plotly_chart(sleep_fig)

# Recovery score gauge or area chart
gauge_fig = px.area(filtered_data, x='Date', y='Recovery_Score', title='Recovery Score Over Time', color_discrete_sequence=px.colors.sequential.Greens)
st.plotly_chart(gauge_fig)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Health Insights Panel
st.write("### Health Insights")
with st.expander("View Personalized Health Tips"):
    if average_sleep < 7:
        st.markdown("Your average sleep is below 7 hours — consider improving sleep hygiene 🛌")
    if average_steps > 10000:
        st.markdown("Great job! Your steps are above 10,000 on most days 🎉")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Data Table
st.write("### Data Table")
# Conditional formatting for Recovery_Score
def style_recovery(val):
    if val > 80:
        return 'background-color: #34d399'  # green
    elif 60 <= val <= 80:
        return 'background-color: #fbbf24'  # yellow
    else:
        return 'background-color: #ef4444'  # red

st.dataframe(filtered_data.style.applymap(style_recovery, subset=['Recovery_Score']))
