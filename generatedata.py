import pandas as pd
import numpy as np
from datetime import timedelta, date

# Function to generate date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# Define start and end dates
start_date = date(2025, 1, 1)
end_date = date(2025, 12, 31)

# Generate dates
dates = list(daterange(start_date, end_date))

# Set seed for reproducibility
np.random.seed(42)

# Generate data for each column
steps = np.random.normal(loc=8500, scale=2500, size=len(dates)).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1.2, size=len(dates)).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=len(dates)).clip(48, 110)
calories_burned = np.random.randint(1800, 4200, size=len(dates))
active_minutes = np.random.randint(20, 180, size=len(dates))

# Create DataFrame
data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate_bpm,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5% NaN values randomly in each column
for column in data.columns[1:]:  # Skip 'Date' column for NaN introduction
    data.loc[data.sample(frac=0.05).index, column] = np.nan

# Ensure the 'data' folder exists or create it
import os
os.makedirs('data', exist_ok=True)

# Save to CSV
csv_path = 'data/health_data.csv'
data.to_csv(csv_path, index=False)

print(f'Data saved to {csv_path}')