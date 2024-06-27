#!/usr/bin/python3

import os
import pandas as pd
import time
import json
import csv
import signal
import sys
import shutil
import re

def signal_SIGINT(SignalNumber, Frame):
    print('Exiting')
    sys.exit()

def clean_json(entry):
    pattern = re.compile(r'^/.*\.json:(.*)$')

    keep_keys = ['type', 'timeLogged', 'rcpt', 'dsnAction', 'dsnStatus', 'jobId', 'envId']

    filepath = entry.path
    temp_output_file = filepath + '.tmp'

    with open(filepath, 'r') as f, open(temp_output_file, 'w') as out_f:
        for line in f:
            match = pattern.match(line)
            if match:
                json_str = match.group(1).strip()
                data = json.loads(json_str)

                # Ensure jobId is treated as string
                data['jobId'] = str(data.get('jobId', ''))

                cleaned_data = {key: data[key] for key in keep_keys if key in data}
                json.dump(cleaned_data, out_f, separators=(',', ':'))
                out_f.write('\n')
    os.replace(temp_output_file, filepath)
    print(f"Processed: {entry.name}")

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        # Load JSON data directly from file
        data = [json.loads(line.strip()) for line in f]

    # Ensure jobId is treated as string in each entry
    for entry in data:
        entry['jobId'] = str(entry.get('jobId', ''))

    # Convert JSON data to Pandas DataFrame
    df = pd.DataFrame(data)

    # DataFrames to CSV file
    df.to_csv(csv_file, index=False)

def csv_tail(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        print('Header:')
        print(','.join(header))
        data = list(reader)[-10:]
        row_num = 0
        for row in data:
            print(f'Row {row_num + 1}:')
            print(','.join(row))
            row_num += 1

def monitor_json_dir(json_dir, csv_dir):
    watched_files = set()

    while True:
        with os.scandir(json_dir) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(".json") and entry.name not in watched_files:
                    clean_json(entry)

                    json_file = os.path.join(json_dir, entry.name)
                    csv_file = os.path.join(csv_dir, entry.name.replace('.json', '.csv'))
                    try:
                        json_to_csv(json_file, csv_file)
                        watched_files.add(entry.name)
                        print('*' * 20 + f" Converted {entry.name} to CSV " + '*' * 20)
                        csv_tail(csv_file)
                        print('')
                    except Exception as e:
                        print(f"Error converting {entry.name}: {str(e)}")
        time.sleep(20)

if __name__ == "__main__":
    print('=' * 20 + ' JSON to CSV converter ' + '=' * 20)

    json_dir = input('Enter the input directory path for JSON files: ').strip()
    csv_dir = input('Enter the output directory path for CSV files: ').strip()

    os.makedirs(csv_dir, exist_ok=True)
    signal.signal(signal.SIGINT, signal_SIGINT)

    monitor_json_dir(json_dir, csv_dir)

