import pandas as pd
import os

def load_data(file_path):
    """
    Loads data from a file into a pandas DataFrame.
    The function automatically detects if the file is CSV or JSON and loads it accordingly.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    # Determine file type from the extension
    file_extension = file_path.split('.')[-1].lower()
    
    try:
        if file_extension == 'csv':
            data_df = pd.read_csv(file_path)
            print("Loaded data from CSV file.")
        elif file_extension == 'json':
            data_df = pd.read_json(file_path)
            print("Loaded data from JSON file.")
        else:
            print("Unsupported file format.")
            return None

        # Basic data validation
        if data_df.empty:
            print("Warning: The data frame is empty.")
        else:
            print("Data frame loaded successfully with", len(data_df), "records.")

        return data_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def save_data(data_df, output_file_path):
    """
    Saves the DataFrame to a CSV file.
    """
    try:
        data_df.to_csv(output_file_path, index=False)
        print(f"Data saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the data: {e}")


if __name__ == "__main__":
    # Load our initial_data.csv file and save the processed data to processed_data.csv
    # Paths to your CSV files (please change this to your own absolute paths if needed to run again)
    csv_data = load_data('./data-files/initial_data.csv')
    if csv_data is not None:
        print(csv_data.head())
        save_data(csv_data, './data-files/processed_data.csv')
