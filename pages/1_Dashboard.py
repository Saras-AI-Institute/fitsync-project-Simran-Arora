from ast import main

import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Function to create plots
def create_plotly_charts(filtered_data):
    col1, col2 = st.columns(2)

    # Dual Line Chart: Recovery Score & Sleep Trend
    fig1 = px.line(filtered_data, x='Date', y=['Recovery_Score', 'Sleep_Hours'], title='Recovery Score & Sleep Trend')
    col1.plotly_chart(fig1, use_container_width=True)

    # Scatter Plot: Recovery Score vs Daily Steps
    fig2 = px.scatter(filtered_data, x='Steps', y='Recovery_Score', color='Sleep_Hours',
                      title='Recovery Score vs Daily Steps')
    col2.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)

    # Scatter Plot: Recovery Score vs Resting Heart Rate
    fig3 = px.scatter(filtered_data, x='Heart_Rate_bpm', y='Recovery_Score',
                      title='Recovery Score vs Resting Heart Rate')
    col1.plotly_chart(fig3, use_container_width=True)

    # Line Chart: Daily Calories Burned Trend
    fig4 = px.line(filtered_data, x='Date', y='Calories_Burned', title='Daily Calories Burned Trend')
    col2.plotly_chart(fig4, use_container_width=True)

# Cache the data processing function
@st.cache_data
def load_data():
    return process_data()

def main():
    st.write("Welcome to FitSync! This dashboard provides insights into your health and recovery based on your activity data.")

    # Sidebar filter for time range selection
    st.sidebar.header("Filters")
    time_range = st.sidebar.selectbox(
        "Select Time Range",
        options=["Last 7 Days", "Last 30 Days", "All Time"],
        index=2
    )

    # Load and filter data based on the selected time range
    data = load_data()  # Use cached data
    if time_range == "Last 7 Days":
        filtered_data = data[data['Date'] >= (data['Date'].max() - pd.Timedelta(days=7))]
    elif time_range == "Last 30 Days":
        filtered_data = data[data['Date'] >= (data['Date'].max() - pd.Timedelta(days=30))]
    else:
        filtered_data = data

    # Set up a professional 3-column layout
    col1, col2, col3 = st.columns(3)

    # Calculate metrics using the filtered DataFrame
    average_steps = filtered_data['Steps'].mean()
    average_sleep = filtered_data['Sleep_Hours'].mean()
    average_recovery = filtered_data['Recovery_Score'].mean()

    # Display metrics using st.metric
    with col1:
        st.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
    with col2:
        st.metric(label="Average Sleep Hours", value=f"{average_sleep:.1f}", delta=None)
    with col3:
        st.metric(label="Average Recovery Score", value=f"{average_recovery:.1f}", delta=None)

    # Visualization
    create_plotly_charts(filtered_data)

# Display processed data
# st.dataframe(data)

# Additional features and visualizations can be added here

# Run the main function to execute the dashboard
if __name__ == "__main__":
    main()