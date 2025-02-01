import pandas as pd
import json
from argparse import ArgumentParser
from tqdm import tqdm
from json import JSONDecoder
import re
import json
from constants import RACES

def fix_json(string):
    modifiedLines = []
    for line in string.splitlines()[1:-1]:
        line = line.strip()
        if line.endswith(','):
            line = line[:-1].strip()
        if line.endswith(':'):
            line = line + "null"
        modifiedLines.append(line)
    return '{\n' + ',\n'.join(modifiedLines) + '\n}'

def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    results = []
    while pos < len(text):
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            end_list = []
            for p in range(match, len(text)):
                end_match = text.find('}', p)
                if end_match == -1:
                    break
                elif end_match in end_list:
                    continue
                try:
                    end_list.append(end_match)
                    result, index = decoder.raw_decode(text[match:end_match])
                    results.append(result)
                    pos = match + index
                    break
                except ValueError as error:
                    continue
            pos = match + 1
        except ValueError:
            pos = match + 1
    return results
            
# RACES = ['white', 'black', 'indian', 'east asian', 'southeast asian', 'middle eastern', 'latino']
GENDERS = ['male', 'female']

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if", "--input_file", type=str, default='./data/events_year_culture_race_roles_chatgpt_cite_wiki_full_new_dedup_json_answer_dropped_existence_200.jsonl')
    parser.add_argument("-of", "--output_file", type=str, default='./data/final_version_200_test.csv')
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    args = parser.parse_args()

    df = pd.read_json(path_or_buf=args.input_file, lines=True)

    if args.race:
        df['dominant_race_list'] = None
        df['existence_race_list'] = None
        identifier = 'race'
    elif args.gender:
        df['dominant_gender_list'] = None
        df['existence_gender_list'] = None
        identifier = 'gender'

    for i in tqdm(range(len(df))):
        try:
            # print(extract_json_objects(df['dominant_{}_chatgpt'.format(identifier)][i]))
            dominant_identity_list = extract_json_objects(df['dominant_{}_chatgpt'.format(identifier)][i].replace(r'\"', '')) # [j for j in extract_json_objects(df['dominant_{}_chatgpt'.format(identifier)][i])][0][identifier + 's']
            if type(dominant_identity_list) == dict and (identifier + 's' in dominant_identity_list.keys()):
                dominant_identity_list = dominant_identity_list[identifier + 's']
            # print(dominant_identity_list)
            dominant_identity_list = list(set([d[identifier] for d in dominant_identity_list if d[identifier] != 'None']))
            if dominant_identity_list == []:
                if args.race:
                    for race in RACES:
                        if race.lower() in df['dominant_{}_chatgpt'.format(identifier)][i].lower():
                            dominant_identity_list.append(race)
                elif args.gender:
                    for gender in GENDERS:
                        if gender.lower() in df['dominant_{}_chatgpt'.format(identifier)][i].lower():
                            dominant_identity_list.append(gender)
        except:
            dominant_identity_list = [] 
            if args.race:
                for race in RACES:
                    if race.lower() in df['dominant_{}_chatgpt'.format(identifier)][i].lower():
                        dominant_identity_list.append(race)
            elif args.gender:
                for gender in GENDERS:
                    if gender.lower() in df['dominant_{}_chatgpt'.format(identifier)][i].lower():
                        dominant_identity_list.append(gender)
        df['dominant_{}_list'.format(identifier)][i] = list(set(dominant_identity_list))

        try: 
            existence_identity_list = extract_json_objects(df['existence_{}_chatgpt'.format(identifier)][i].replace(r'\"', '').replace('*', '')) # [j for j in extract_json_objects(df['existence_{}_chatgpt'.format(identifier)][i])][0][identifier + 's']
            if type(dominant_identity_list) == dict and (identifier + 's' in existence_identity_list.keys()):
                existence_identity_list = existence_identity_list[identifier + 's']
            existence_identity_list = list(set([d[identifier] for d in existence_identity_list if d['existence'] != False]))
            existence_identity_list = [e for e in existence_identity_list if e != 'None']

            if existence_identity_list == []:
                json_dict_list = []
                entry = df['existence_{}_chatgpt'.format(identifier)][i]
                start = 0
                while start < len(entry):
                    json_dict = {}
                    for json_key in [identifier, "existence", "reference", "referenced text"]:
                        tmp = -1
                        json_dict[json_key] = None
                        try:
                            if json_key != 'referenced text':
                                val = re.search(json_key+'": (.*),', entry[start:])
                                tmp, value = val.end(0), val.group(1)
                            else:
                                val = re.search(json_key+'": (.*)}', entry[start:])
                                tmp, value = val.end(0), val.group(1)
                            json_dict[json_key] = value
                            start = tmp + start
                        except AttributeError: # Key does not exist
                            pass
                        except Exception as e:
                            raise e from None
                    if tmp == -1:
                        start += 1
                    if json_dict[identifier] != None and 'False' not in json_dict['existence'] and json_dict['existence'] != False and 'false' not in json_dict['existence'] and 'None' not in json_dict['existence']  and json_dict['existence'] is not None:
                        # print(json_dict['existence'])
                        json_dict_list.append(json_dict)
                existence_identity_list = list(set([json_dict[identifier] for json_dict in json_dict_list]))
                # print(fix_json(df['existence_{}_chatgpt'.format(identifier)][i]))
                # print(df['existence_{}_chatgpt'.format(identifier)][i], '\n\n', extract_json_objects(df['existence_{}_chatgpt'.format(identifier)][i]))
        except:
            print('error 2!')
            # print(df['existence_{}_chatgpt'.format(identifier)][i])
            continue
            # entry = df['existence_{}_chatgpt'.format(identifier)][i]
            # start_pos = entry.find("races")
            # end_pos = entry.find("}")
            # # existence_identity_list = []
            # # if args.race:
            # #     for race in RACES:
            # #         if race in df['existence_race_chatgpt'][i].lower():
            # #             existence_identity_list.append(race)
            # # elif args.gender:
            # #     for gender in GENDERS:
            # #         if gender in df['existence_gender_chatgpt'][i].lower():
            # #             existence_identity_list.append(gender)
        df['existence_{}_list'.format(identifier)][i] = list(set(existence_identity_list))

    df = df[['culture', 'event_name', 'group', 'dominant_{}_list'.format(identifier), 'existence_{}_list'.format(identifier)]]
    drop = []
    for i in range(len(df)):
        if df['dominant_{}_list'.format(identifier)][i] == [] or df['existence_{}_list'.format(identifier)][i] == []:
            drop.append(i)
    df.drop(drop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print('\n\n Finished processing and removing empty entries, remaining: {} entries!'.format(len(df)))
    df.to_csv(args.output_file, index=False)