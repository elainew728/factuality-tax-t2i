import pandas as pd
import random
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    args = parser.parse_args()

    if args.gender:
        df = pd.read_json('./data/events_year_culture_gender_roles_factchecked_processed.csv', lines=True)

        i = 0
        event_count = {}
        drop = []
        while i < len(df):
            tmp_culture = df['culture'][i]
            tmp_event = df['event_name'][i]
            tmp_group = df['group'][i] # dominant_gender
            if (tmp_culture + '_'  + tmp_event) not in event_count.keys():
                event_count[tmp_culture + '_' + tmp_event] = 1
            else:
                event_count[tmp_culture + '_' + tmp_event] += 1
        
            event_idxs = [i]
            j = i + 1
            while (j < len(df)) and (df['culture'][j] == tmp_culture) and (df['event_name'][j] == tmp_event):
                event_idxs.append(j)
                event_count[tmp_culture + '_' + tmp_event] += 1
                j += 1

            if len(event_idxs) > 1:
                drop += random.sample(event_idxs, len(event_idxs) - 1)
            
            i = j

        df.drop(drop, inplace=True)
        df.reset_index(drop=True, inplace=True)
        # df.to_csv('./output/events_year_culture_gender_roles_factchecked_processed_drop_dup.csv', index=False)

        drop = []
        cultures = list(df['culture'].unique())
        for culture in cultures:
            tmp = df[df['culture'] == culture]
            num_drop = len(tmp) - 26
            tmp_f = tmp[tmp['dominant_gender_list'] == "['female']"]
            tmp_m = tmp[tmp['dominant_gender_list'] == "['male']"]
            tmp_fm = tmp[tmp['dominant_gender_list'] == "['female', 'male']"]
            drop += random.sample(list(tmp_m.index), num_drop)

        df.drop(drop, inplace=True)
        df.reset_index(drop=True, inplace=True)

        df.to_csv('./data/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv', index=False)
    
    elif args.race:
        df = pd.read_csv('./data/events_year_culture_race_roles_factchecked_processed.csv')

        i = 0
        event_count = {}
        drop = []
        while i < len(df):
            tmp_culture = df['culture'][i]
            tmp_event = df['event_name'][i]
            tmp_group = df['group'][i] # dominant_gender
            if (tmp_culture + '_'  + tmp_event) not in event_count.keys():
                event_count[tmp_culture + '_' + tmp_event] = 1
            else:
                event_count[tmp_culture + '_' + tmp_event] += 1
        
            event_idxs = [i]
            j = i + 1
            while (j < len(df)) and (df['culture'][j] == tmp_culture) and (df['event_name'][j] == tmp_event):
                event_idxs.append(j)
                event_count[tmp_culture + '_' + tmp_event] += 1
                j += 1

            if len(event_idxs) > 1:
                drop += random.sample(event_idxs, len(event_idxs) - 1)
            
            i = j

            df.drop(drop, inplace=True)
            df.reset_index(drop=True, inplace=True)
            # df.to_csv('./output/events_year_culture_race_roles_factchecked_processed_drop_dup.csv', index=False)

            drop = []
            cultures = list(df['culture'].unique())
            for culture in cultures:
                tmp = df[df['culture'] == culture]
                drop += random.sample(list(tmp.index), len(tmp) - 100)
            
            df.drop(drop, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.to_csv('./data/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv', index=False)