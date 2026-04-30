import pandas as pd
from datetime import datetime


def load_data():
    """
    Load and preprocess the health_data.csv file.

    Returns:
        pd.DataFrame: The cleaned DataFrame
    """
    # Step 1: Load the CSV file
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)
    
    # Step 2: Handle missing values intelligently
    # Fill missing 'Steps' with median value
    data['Steps'].fillna(data['Steps'].median(), inplace=True)
    
    # Fill missing 'Sleep_Hours' with 7.0 (general optimal sleep hours)
    data['Sleep_Hours'].fillna(7.0, inplace=True)
    
    # Fill missing 'Heart_Rate_bpm' with 68 (average human resting heart rate)
    data['Heart_Rate_bpm'].fillna(68.0, inplace=True)
    
    # Fill other columns with their median values
    for column in data.columns:
        if data[column].isnull().any():
            data[column].fillna(data[column].median(), inplace=True)

    # Step 3: Convert the 'Date' column to datetime objects
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

    # Returns the cleaned DataFrame
    return data


def calculate_recovery_score(df):
    """
    Calculate a recovery score for each entry in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing health data.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'Recovery_Score'.
    """
    # Create a new column 'Recovery_Score' initialized to 50 (neutral average score)
    df['Recovery_Score'] = 50

    # Adjust score based on Sleep_Hours
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_Score'] += 20  # Good sleep increases score significantly
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_Score'] -= 20   # Poor sleep decreases score significantly

    # Adjust score based on Heart_Rate_bpm
    df['Recovery_Score'] -= (df['Heart_Rate_bpm'] - 68) / 2  # Lower heart rate is better for recovery

    # Adjust score based on Steps
    df['Recovery_Score'] -= (df['Steps'] - 10000) / 1000  # High activity may cause slight strain

    # Ensure Recovery_Score stays within the bounds of 0 to 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(0, 100)

    return df


def process_data():
    """
    Main function to process the data and prepare it for the dashboard.

    Returns:
        pd.DataFrame: The processed DataFrame with an added Recovery Score.
    """
    # Load the cleaned data
    df = load_data()

    # Calculate the recovery score
    df = calculate_recovery_score(df)

    # Return the final processed DataFrame
    return df

