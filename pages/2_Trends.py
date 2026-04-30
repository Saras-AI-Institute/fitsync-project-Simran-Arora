import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Cache the data processing function
@st.cache_data
def load_data():
    return process_data()

# Set the page configuration
st.set_page_config(layout="wide", page_title="Trends & Insights")

# Title of the dashboard
st.title("Trends & Insights")

# Add sidebar for filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Load and process data
df = load_data()  # Use cached data
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Filter the data based on the selected time range
today = pd.to_datetime("today")
if time_range == "Last 7 Days":
    filtered_df = df[(df['Date'] >= (today - pd.Timedelta(days=7))) & (df['Date'] <= today)]
elif time_range == "Last 30 Days":
    filtered_df = df[(df['Date'] >= (today - pd.Timedelta(days=30))) & (df['Date'] <= today)]
else:
    filtered_df = df  # "All Time"

# Check for data presence
data_summary = "No data available for the selected time range." if filtered_df.empty else "Data available for insights."
st.info(data_summary)

# Summary statistics
if not filtered_df.empty:
    st.write("### Summary Statistics")
    summary_stats = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max'])
    st.dataframe(summary_stats)

    # Monthly Average Recovery Score
    st.write("### Monthly Average Recovery Score")
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype(str)  # Convert to string to avoid TypeError
    monthly_avg_recovery = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()
    fig_recovery = px.line(monthly_avg_recovery, x='Month', y='Recovery_Score',
                           title="Monthly Average Recovery Score",
                           labels={'Month': 'Month', 'Recovery_Score': 'Average Recovery Score'})
    st.plotly_chart(fig_recovery, use_container_width=True)

    # Histograms
    st.write("### Distribution Histograms")
    for column in ['Steps', 'Calories_Burned', 'Recovery_Score', 'Sleep_Hours']:
        fig_hist = px.histogram(filtered_df, x=column, nbins=30, 
                                title=f"Distribution of {column}", 
                                labels={column: column})
        st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Adjust the time filter to view more data insights.")
