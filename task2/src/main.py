#!/usr/bin/python3

import os
import pandas as pd
import time

def json_to_csv(json_dir, csv_dir):
    # os.chdir(json_dir) 
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_file = os.path.join(json_dir, filename)
            csv_file = os.path.join(csv_dir, filename)
            # Reads the JSON file and converts it Pandas DataFrames
            df = pd.read_json(json_file, lines=True, encoding='utf-8')
            csv_file = os.path.join(csv_dir, filename.replace('.json', '.csv'))

            # DataFrames to CSV file
            df.to_csv(csv_file, index=False)

def monitor_json_dir(json_dir, csv_dir):
    watched_files = set()

    while True:
        for filename in os.listdir(json_dir):
            if filename.endswith(".json") and filename not in watched_files:
                json_file = os.path.join(json_dir, filename)
                csv_file = os.path.join(csv_dir, filename)
                df = pd.read_json(json_file, lines=True, encoding='utf-8')
                csv_file = os.path.join(csv_dir, filename.replace('.json', '.csv'))
                df.to_csv(csv_file, index=False)

                watched_files.add(filename)
    time.sleep(10)
                
if __name__ == "__main__":
    print('=' * 20 + ' JSON to CSV converter ' + '=' * 20)

    json_dir = input('Enter the input directory path for JSON files: ').strip()
    csv_dir = input('Enter the output directory path for CSV files: ').strip()

    # Create output directory if it doesn't exist
    os.makedirs(csv_dir, exist_ok=True)

    # Convert existing JSON files
    json_to_csv(json_dir, csv_dir)

    # Monitor the JSON directory for new JSON files to be converted
    monitor_json_dir(json_dir, csv_dir)
