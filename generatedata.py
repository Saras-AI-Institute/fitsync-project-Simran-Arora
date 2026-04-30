import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Settings
num_days = 365
start_date = datetime(2025, 1, 1)
end_date = start_date + timedelta(days=num_days - 1)
dates = pd.date_range(start=start_date, end=end_date)

# Generate data
np.random.seed(42)  # For reproducibility
steps = np.random.normal(loc=8500, scale=2500, size=num_days).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=num_days).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=num_days).clip(48, 110)
calories_burned = np.random.randint(1800, 4200, size=num_days)
active_minutes = np.random.randint(20, 180, size=num_days)

data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate_bpm,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5% NaN values randomly in each column
for column in data.columns[1:]:  # Skip 'Date' column
    data.loc[data.sample(frac=0.05).index, column] = np.nan

data.to_csv('data/health_data.csv', index=False)