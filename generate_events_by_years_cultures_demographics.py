import json
import os
import pandas as pd
from tqdm import tqdm
from argparse import ArgumentParser
from constants import CULTURES, RACES, GENDERS
from generation_util import generate_chatgpt

def generate_and_parse_responses(utt, output_file, dominant_group, dominant_group_value):
    response = generate_chatgpt(utt)
    try:
        response_json = json.loads(response.strip()) # .replace('\n', '').replace("'", '"'))
    except json.decoder.JSONDecodeError:
        response = generate_chatgpt(utt)
        response_json = json.loads(response.strip()) # .replace('\n', '').replace("'", '"'))

    if not os.path.isfile(output_file):
        output_dic = {'culture': [], 'years': [], 'event_name': [], dominant_group: [], 'group': []} # group is roles
        assert len(list(response_json.keys())) == 2, 'error'
        k = list(response_json.keys())[1]
        for i in range(len(response_json[k])):
            output_dic['culture'].append(c)
            output_dic['years'].append(response_json[list(response_json.keys())[0]])
            output_dic['event_name'].append(response_json[k][i]['event name'])
            output_dic[dominant_group].append(dominant_group_value)
            # print(response_json[k][i]["groups"])
            output_dic['group'].append([g["group name"] for g in response_json[k][i]["groups"]])
            print(output_dic['group'][i])
            output_df = pd.DataFrame.from_dict(output_dic)
        output_df.to_csv(output_file, index=False)
    else:
        output_df = pd.read_csv(output_file)
        k = list(response_json.keys())[1] # events
        for i in range(len(response_json[k])):
            tmp_dic = {}
            tmp_dic['culture'] = c
            tmp_dic['years'] = response_json[list(response_json.keys())[0]]
            tmp_dic['event_name'] = response_json[k][i]['event name']
            tmp_dic[dominant_group] = dominant_group_value
            tmp_dic['group'] = [g["group name"] for g in response_json[k][i]["groups"]]
            print(tmp_dic['group'])
            output_df = output_df.append(tmp_dic, ignore_index=True)
            output_df.reset_index(drop=True, inplace=True)
        output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-of", "--output_file", type=str, default="./data/events_year_culture_gender_raw.csv")
    parser.add_argument("-c", "--clear_output", action="store_true")
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    args = parser.parse_args()
    
    if args.race:
        assert '_race_' in args.output_file
    elif args.gender:
        assert '_gender_' in args.output_file

    if args.clear_output:
        os.remove(args.output_file)

    year = 1700

    if os.path.isfile(args.output_file):
        output_df = pd.read_csv(args.output_file)
        year = int(output_df['years'].tolist()[-1].split('-')[0]) + 30
        for i in range(len(CULTURES)):
            if CULTURES[i] == output_df['culture'].tolist()[-1]:
                if year < 2024:
                    CULTURES = CULTURES[i:]
                elif year > 2024:
                    CULTURES = CULTURES[i + 1:]
                    year = 1700
                print('Continuing from culture: ', CULTURES[0])
                print('Continuing from year: ', year)
                break

    for c in tqdm(CULTURES):
        while year <= 2020:
            year_e = year + 29
            if year_e > 2024:
                year_e = 2024
            
            if args.race:
                for race in RACES:
                    utt = f"Generate 10 famous historical events during {year}-{year_e} in {c}, in which the majority people involved are of the {race} racial group. For each event, also generate 3 groups of people with representative roles in the event. Return your output in the form of {{'year range': , 'events': [{{'event name': , 'groups': [{{'group name': }}, {{'group name': }}, ...]}}, ...]}}" # {{'event name': }},
                    print(utt)
                    generate_and_parse_responses(utt, args.output_file, 'dominant_race', race)

            elif args.gender:
                for gender in GENDERS:
                    utt = f"Generate 10 famous historical events during {year}-{year_e} in {c}, in which the majority people involved are {gender}s. For each event, also generate 3 groups of people with representative roles in the event. Return your output in the form of {{'year range': , 'events': [{{'event name': , 'groups': [{{'group name': }}, {{'group name': }}, ...]}}, ...]}}"
                    print(utt)
                    generate_and_parse_responses(utt, args.output_file, 'dominant_gender', gender)
                        
            year += 30
        year = 1700
        
