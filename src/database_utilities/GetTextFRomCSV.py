import pandas as pd
from src.conf.Configurations import csv_path

 # Replace with your actual file path
def get_text():
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Combine all rows from the 'text' column into a single string
    all_text = ' '.join(df['text'].dropna().astype(str))

    return all_text
