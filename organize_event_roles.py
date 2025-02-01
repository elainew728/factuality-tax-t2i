import json
import copy
import os
import pandas as pd
import csv
import ast
from tqdm import tqdm
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if", "--input_file", type=str, default="./output/events_year_culture_race_raw.csv")
    parser.add_argument("-of", "--output_file", type=str, default="./output/events_year_culture_race_roles.csv")
    parser.add_argument("-c", "--clear_output", action="store_true")
    args = parser.parse_args()
    
    with open(args.input_file, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    out_data = []

    for entry in tqdm(data):
        groups = list(set(ast.literal_eval(entry['group'])))

        for group in groups:
            tmp = copy.deepcopy(entry)
            tmp['group'] = group
            out_data.append(tmp)

    df = pd.DataFrame(out_data)
    print('Total number of data: ', len(df))
    df.to_csv(args.output_file, index=False)