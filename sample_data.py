import pandas as pd

def main():
    # Load the CSV file
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)
    
    # Print the first 5 rows of the DataFrame
    print('First 5 rows of the data:')
    print(data.head())
    
    # Calculate the number of missing values in each column
    print('\nNumber of missing values in each column:')
    print(data.isnull().sum())

if __name__ == "__main__":
    main()