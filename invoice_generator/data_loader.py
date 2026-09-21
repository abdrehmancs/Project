import csv
import pandas as pd
import os

def load_client_data(file_path):
    """
    Iteration 5: Excel Support
    Reads either a CSV or XLSX file and returns a list of dictionaries.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} was not found.")
        return []

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please provide a .csv or .xlsx file.")
            return []

        # Convert DataFrame to list of dicts (Iteration 1 behavior preserved)
        return df.to_dict('records')

    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return []
