#!/usr/bin/python3

import os
import pandas as pd
import shutil 

def json_to_csv(input_dir, output_dir):
    # os.chdir(input_dir) # Change directory
    # print(type(os.listdir())) -> Returns a list
    os.chdir(input_dir) 
    for filename in os.listdir():
        if filename.endswith(".json"):
            # Reads the JSON file and converts it Pandas DataFrames
            df = pd.read_json(filename, lines=True)
            # DataFrames to CSV file
            df.to_csv((filename.replace('.json', '.csv')), index=False)

def main():
    print('=' * 20 + ' JSON to CSV converter ' + '=' * 20)

    input_dir = input('Enter the input directory path: ') 
    output_dir = input('Enter the output directory path: ')

    json_to_csv(input_dir, output_dir)

    for f in os.listdir():
        input_file = os.path.join(input_dir, f)
        output_file = os.path.join(output_dir, f)
        if f.endswith(".csv"):
            shutil.move(input_file, output_file)

main()

