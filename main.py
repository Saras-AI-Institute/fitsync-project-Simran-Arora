import streamlit as st
import pandas as pd
import plotly.express as px
from modules.processor import process_data

st.set_page_config(
    page_title="FitSync Pro",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        background: #0b1220;
        color: #e2e8f0;
    }

    .stSidebar {
        background: #111827;
        padding-top: 1rem;
        color: #e2e8f0;
    }

    .header-card {
        background: linear-gradient(135deg, #2563eb 0%, #10b981 100%);
        border-radius: 22px;
        padding: 28px;
        color: #ffffff;
        box-shadow: 0 24px 64px rgba(15, 23, 42, 0.45);
    }

    .summary-card {
        background: #111827;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.35);
        margin-bottom: 18px;
    }

    .summary-card h3 {
        margin: 0 0 8px 0;
        color: #e2e8f0;
    }

    .summary-value {
        font-size: 2.45rem;
        font-weight: 700;
        margin: 0;
    }

    .metric-card {
        border-radius: 18px;
        padding: 24px;
        color: #ffffff;
        margin-bottom: 16px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-card h2 {
        margin: 0;
        font-size: 2.3rem;
        letter-spacing: -0.04em;
    }

    .metric-card p {
        margin: 0;
        opacity: 0.88;
        font-size: 0.98rem;
    }

    .steps-card { background: #4f8bf9; }
    .sleep-card { background: #a78bfa; }
    .recovery-card { background: #34d399; }
    .heart-card { background: #f97316; }

    .section-title {
        margin-top: 24px;
        margin-bottom: 12px;
        color: #0f172a;
        font-weight: 700;
    }

    .divider {
        margin: 24px 0;
        height: 1px;
        background: rgba(15, 23, 42, 0.1);
        border: none;
    }

    .st-expander > div {
        border-radius: 18px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        background: #ffffff;
    }

    .css-1d391kg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def get_data():
    return process_data()

@st.cache_data
def filter_data_by_time(data: pd.DataFrame, time_range: str) -> pd.DataFrame:
    if 'Date' not in data.columns:
        return data

    max_date = data['Date'].max()
    if time_range == 'Last 7 Days':
        min_date = max_date - pd.Timedelta(days=7)
        return data[data['Date'] >= min_date]
    if time_range == 'Last 30 Days':
        min_date = max_date - pd.Timedelta(days=30)
    return data[data['Date'] >= min_date] if time_range != 'All Time' else data

@st.cache_data
def style_recovery(val):
    if val > 80:
        return 'background-color: #34d399; color: #ffffff'
    if val >= 60:
        return 'background-color: #fbbf24; color: #000000'
    return 'background-color: #ef4444; color: #ffffff'

# Load data
data = get_data()

# Sidebar
st.sidebar.markdown('# FitSync Pro')
st.sidebar.markdown('**A premium interactive wellness dashboard**')
st.sidebar.write('---')

time_range = st.sidebar.radio(
    'Time window',
    ['Last 7 Days', 'Last 30 Days', 'All Time'],
    index=2,
)

st.sidebar.write('---')
if 'Date' in data.columns:
    st.sidebar.write(f'**Data range:** {data.Date.min().date()} → {data.Date.max().date()}')
    st.sidebar.write(f'**Records:** {len(data)}')

st.sidebar.write('---')
st.sidebar.markdown('Built for athletes, coaches, and wellness professionals. Use filters to compare recent performance and discover trends.')

# Main header
st.markdown(
    f"""
    <div class='header-card'>
        <div style='display: flex; align-items: center; justify-content: space-between; gap: 18px;'>
            <div>
                <h1 style='margin:0; font-size:3rem;'>FitSync Pro</h1>
                <p style='margin:8px 0 0 0; opacity:0.85; font-size:1.05rem;'>A polished health dashboard with actionable insights and modern visuals.</p>
            </div>
            <div style='text-align:right;'>
                <p style='margin:0; opacity:0.8;'>Current view</p>
                <h2 style='margin:4px 0 0 0; font-size:2rem; opacity:0.95;'>{time_range}</h2>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write('---')

filtered_data = filter_data_by_time(data, time_range)

if filtered_data.empty:
    st.warning('No data found for the selected time range. Please expand the filter or check the dataset.')
else:
    average_steps = filtered_data['Steps'].mean()
    average_sleep = filtered_data['Sleep_Hours'].mean()
    average_recovery = filtered_data['Recovery_Score'].mean()
    average_hr = filtered_data['Heart_Rate_bpm'].mean() if 'Heart_Rate_bpm' in filtered_data.columns else None
    total_days_tracked = len(filtered_data['Date'].dt.date.unique())
    best_recovery_day = filtered_data.loc[filtered_data['Recovery_Score'].idxmax(), 'Date'].date() if not filtered_data.empty else 'N/A'

    col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 1])
    col1.markdown(
        """
        <div class='metric-card steps-card'>
            <div>
                <h2>👟 {steps}</h2>
                <p>Avg daily steps</p>
            </div>
        </div>
        """.replace('{steps}', f'{average_steps:,.0f}'), unsafe_allow_html=True,
    )
    col2.markdown(
        """
        <div class='metric-card sleep-card'>
            <div>
                <h2>😴 {sleep} hrs</h2>
                <p>Avg nightly sleep</p>
            </div>
        </div>
        """.replace('{sleep}', f'{average_sleep:.1f}'), unsafe_allow_html=True,
    )
    col3.markdown(
        """
        <div class='metric-card recovery-card'>
            <div>
                <h2>❤️ {recovery} / 100</h2>
                <p>Avg recovery score</p>
            </div>
        </div>
        """.replace('{recovery}', f'{average_recovery:.0f}'), unsafe_allow_html=True,
    )
    col4.markdown(
        """
        <div class='metric-card heart-card'>
            <div>
                <h2>💓 {hr} bpm</h2>
                <p>Avg heart rate</p>
            </div>
        </div>
        """.replace('{hr}', f'{average_hr:.0f}' if average_hr is not None else 'N/A'), unsafe_allow_html=True,
    )

    st.markdown('<hr class="divider" />', unsafe_allow_html=True)

    st.markdown('### Performance Analysis')
    chart_col1, chart_col2 = st.columns([2, 1])

    steps_fig = px.line(
        filtered_data,
        x='Date',
        y='Steps',
        title='Steps Trend',
        labels={'Steps': 'Steps', 'Date': ''},
        color_discrete_sequence=['#2563eb'],
    )
    steps_fig.update_layout(plot_bgcolor='#0b1220', paper_bgcolor='#0b1220', hovermode='x unified')
    chart_col1.plotly_chart(steps_fig, use_container_width=True)

    overview_fig = px.bar(
        filtered_data,
        x='Date',
        y='Recovery_Score',
        title='Recovery Score',
        labels={'Recovery_Score': 'Recovery', 'Date': ''},
        color_discrete_sequence=['#16a34a'],
    )
    overview_fig.update_layout(plot_bgcolor='#0b1220', paper_bgcolor='#0b1220', hovermode='x unified')
    chart_col2.plotly_chart(overview_fig, use_container_width=True)

    st.markdown('### Trends & Comparison')
    trend_col1, trend_col2 = st.columns(2)

    sleep_fig = px.bar(
        filtered_data,
        x='Date',
        y='Sleep_Hours',
        title='Sleep Hours Per Day',
        labels={'Sleep_Hours': 'Sleep Hours', 'Date': ''},
        color_discrete_sequence=['#8b5cf6'],
    )
    sleep_fig.update_layout(plot_bgcolor='#0b1220', paper_bgcolor='#0b1220', hovermode='x unified')
    trend_col1.plotly_chart(sleep_fig, use_container_width=True)

    rest_fig = px.area(
        filtered_data,
        x='Date',
        y='Recovery_Score',
        title='Recovery Score Trend',
        labels={'Recovery_Score': 'Recovery Score', 'Date': ''},
        color_discrete_sequence=['#fb7185'],
    )
    rest_fig.update_layout(plot_bgcolor='#0b1220', paper_bgcolor='#0b1220', hovermode='x unified')
    trend_col2.plotly_chart(rest_fig, use_container_width=True)

    st.markdown('<hr class="divider" />', unsafe_allow_html=True)

    st.markdown('### Insights & Recommendations')
    with st.expander('View personalized recommendations'):
        if average_sleep < 7:
            st.write('• Your average sleep is below 7 hours. Try a consistent bedtime routine and limit screens before bed.')
        else:
            st.write('• Sleep looks strong. Keep prioritizing consistent rest for recovery.')

        if average_steps >= 10000:
            st.write('• Excellent step volume — your activity is in a healthy range for daily fitness.')
        else:
            st.write('• You can improve daily movement with short walking breaks between tasks.')

        if average_recovery >= 80:
            st.write('• Your recovery metrics are excellent. Maintain hydration and light mobility work.')
        elif average_recovery >= 60:
            st.write('• Recovery is decent. Consider balancing harder days with extra rest or gentle recovery sessions.')
        else:
            st.write('• Recovery is lagging. Focus on sleep quality, recovery nutrition, and stress reduction.')

    st.markdown('<hr class="divider" />', unsafe_allow_html=True)

    st.markdown('### Data Table')
    styled_table = filtered_data.style.format({
        'Steps': '{:.0f}',
        'Sleep_Hours': '{:.1f}',
        'Heart_Rate_bpm': '{:.0f}',
        'Recovery_Score': '{:.0f}',
    }).applymap(style_recovery, subset=['Recovery_Score'])

    st.dataframe(styled_table, use_container_width=True)
