import pandas as pd
pd.options.mode.chained_assignment = None
import collections
from argparse import ArgumentParser
import ast
from constants import RACES, GENDERS
from tqdm import tqdm
import numpy as np
from sklearn.metrics import f1_score

fairface2fact = {
    'White': 'white',
    'Black': 'black',
    'Latino_Hispanic': 'latino', 
    'East Asian': 'east asian',
    'Southeast Asian': 'southeast asian',
    'Indian': 'indian',
    'Middle Eastern': 'middle eastern'
}

fact2fairface = {
    'chinese': 'east asian',
    'arab': 'middle eastern',
    'caucasian or circassian': 'white',
    'african american': 'black', 
    'egyptian': 'middle eastern', 
    'vietnamese': 'southeast asian',
    'filipino': 'southeast asian',
    'fulani': 'black',
    'austronesian': 'east asian',
    'indonesian': 'southeast asian'
}

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-ff", "--fairface_file", type=str, default="./FairFace/final_version_100_test_imggen_output_raw.csv")
    parser.add_argument("-of", "--original_file", type=str, default="./output/final_version_100_test_imggen.csv")
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    parser.add_argument("-w", "--write_results", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.fairface_file)
    df2 = pd.read_csv(args.original_file)

    if args.race:
        df2['image_races'] = None
    elif args.gender:
        df2['image_genders'] = None

    for i in tqdm(range(len(df2))):
        try:
            img_file_name = df2['img_path'][i].split('/')[-1].replace('.png', '')
        except AttributeError:
            continue

        j = 0
        start = False
        while j < len(df):
            if not start and img_file_name in df['face_name_align'][j]:
                start = True
                if args.race:
                    df2['image_races'][i] = []
                elif args.gender:
                    df2['image_genders'][i] = []
            if start:
                if img_file_name in df['face_name_align'][j]:
                    if args.race:
                        df2['image_races'][i].append(df['race'][j])
                    elif args.gender:
                        df2['image_genders'][i].append(df['gender'][j])
                else:
                    break
            j += 1
            
    if args.race:
        df2['dominant_image_race'] = None
        df2['dominant_race_correctness'] = -1
        df2['existence_race_correctness'] = -1
        df2['existence_race_diversity'] = -1
        df2['gold_race_diversity'] = -1
        df2['existence_race_f1'] = -1

        for i in range(len(df2)):
            if df2['image_races'][i] is not None:
                img_race_list = df2['image_races'][i]
                c = collections.Counter(img_race_list)

                # existence race correctness
                existence_race_list = ast.literal_eval(df2['existence_race_list'][i])
                existence_race_list = list(map(lambda x: x.replace('Latino', 'Latino_Hispanic'), existence_race_list))
                df2['gold_race_diversity'][i] = len(existence_race_list) / len(RACES)
                true_positive, false_positive = 0, 0
                for r in list(set(img_race_list)):
                    if r not in existence_race_list:
                        false_positive += 1
                    else:
                        true_positive += 1
                true_negative, false_negative = 0, 0
                for r in RACES:
                    if r in existence_race_list and r not in list(set(img_race_list)):
                        false_negative += 1
                    elif r not in existence_race_list and r not in list(set(img_race_list)):
                        true_negative += 1
                df2['existence_race_correctness'][i] = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
                if true_negative == false_positive and true_negative == false_negative and true_negative == 0:
                    df2['existence_race_f1'][i] = ((2 * true_positive) / (2 * true_positive + false_positive + false_negative) + 1) / 2
                else:
                    df2['existence_race_f1'][i] = ((2 * true_positive) / (2 * true_positive + false_positive + false_negative) + (2 * true_negative) / (2 * true_negative + false_positive + false_negative)) / 2
                
                most_common = c.most_common()
                df2['existence_race_diversity'][i] = len(most_common) / len(RACES)

                dominant_race_list = ast.literal_eval(df2['dominant_race_list'][i])
                dominant_image_races = [most_common[i][0] for i in range(min(len(most_common), len(dominant_race_list)))]
                true_positive, false_positive = 0, 0
                df2['dominant_image_race'][i] = dominant_image_races
                dominant_race_list = list(map(lambda x: x.replace('Latino', 'Latino_Hispanic'), dominant_race_list))
                for r in list(set(dominant_image_races)):
                    if r in dominant_race_list:
                        true_positive += 1
                    else:
                        false_positive += 1
                df2['dominant_race_correctness'][i] = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
                
        dominant_res_list = list(filter(lambda x: x != -1, df2['dominant_race_correctness'].tolist()))
        print('Dominant race correctness: ', sum(dominant_res_list) / len(dominant_res_list))
        existence_res_list = list(filter(lambda x: x != -1, df2['existence_race_correctness'].tolist()))
        print('Existence race correctness: ', sum(existence_res_list) / len(existence_res_list))
        diversity_res_list = list(filter(lambda x: x != -1, df2['existence_race_diversity'].tolist()))
        gold_diversity_res_list = list(filter(lambda x: x != -1, df2['gold_race_diversity'].tolist()))
        print('Generation-Gold Diversity Gap: ', sum(diversity_res_list) / len(diversity_res_list) - sum(gold_diversity_res_list) / len(gold_diversity_res_list))
        existence_f1_res_list = list(filter(lambda x: x != -1, df2['existence_race_f1'].tolist()))
        print('Existence race F1: ', sum(existence_f1_res_list) / len(existence_f1_res_list))
        
        if args.write_results:
            if '/sd/' in args.fairface_file:
                df2.to_csv('./final_results/sd_' + args.fairface_file.split('/')[-1].replace('.csv', '_results.csv'), index=False)
            else:
                df2.to_csv('./final_results/' + args.fairface_file.split('/')[-1].replace('.csv', '_results.csv'), index=False)
    
    elif args.gender:
        df2['dominant_image_gender'] = None
        df2['dominant_gender_correctness'] = -1
        df2['existence_gender_correctness'] = -1
        df2['existence_gender_diversity'] = -1
        df2['gold_gender_diversity'] = -1
        df2['existence_gender_f1'] = -1

        for i in range(len(df2)):
            if df2['image_genders'][i] is not None:
                img_gender_list = df2['image_genders'][i]
                img_gender_list = [g.lower() for g in img_gender_list]
                c = collections.Counter(img_gender_list)

                # existence gender correctness
                existence_gender_list = ast.literal_eval(df2['existence_gender_list'][i])
                df2['gold_gender_diversity'][i] = len(existence_gender_list) / len(GENDERS)
                true_positive, false_positive = 0, 0
                for r in list(set(img_gender_list)):
                    if r not in existence_gender_list:
                        false_positive += 1
                    else:
                        true_positive += 1
                true_negative, false_negative = 0, 0
                for r in GENDERS:
                    if r in existence_gender_list and r not in list(set(img_gender_list)):
                        false_negative += 1
                    elif r not in existence_gender_list and r not in list(set(img_gender_list)):
                        true_negative += 1
                print(existence_gender_list, list(set(img_gender_list)))
                print(true_positive, false_positive, true_negative, false_negative)
                df2['existence_gender_correctness'][i] = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
                if true_negative == false_positive and true_negative == false_negative and true_negative == 0:
                    df2['existence_gender_f1'][i] = ((2 * true_positive) / (2 * true_positive + false_positive + false_negative) + 1) / 2
                else:
                    df2['existence_gender_f1'][i] = ((2 * true_positive) / (2 * true_positive + false_positive + false_negative) + (2 * true_negative) / (2 * true_negative + false_positive + false_negative)) / 2

                most_common = c.most_common()
                df2['existence_gender_diversity'][i] = len(most_common) / len(GENDERS)

                dominant_gender_list = ast.literal_eval(df2['dominant_gender_list'][i])
                dominant_image_genders = [most_common[i][0] for i in range(min(len(most_common), len(dominant_gender_list)))]
                true_positive, false_positive = 0, 0
                df2['dominant_image_gender'][i] = dominant_image_genders
                for r in list(set(dominant_image_genders)):
                    if r in dominant_gender_list:
                        true_positive += 1
                    else:
                        false_positive += 1
                df2['dominant_gender_correctness'][i] = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
    
        print('Percentage of Successful Generations: ', len(list(filter(lambda x: x is not None, df2['image_genders'].tolist()))), len(list(filter(lambda x: x is not None, df2['image_genders'].tolist()))) / len(df2))
        dominant_res_list = list(filter(lambda x: x != -1, df2['dominant_gender_correctness'].tolist()))
        print('Dominant gender correctness: ', sum(dominant_res_list) / len(dominant_res_list))
        existence_res_list = list(filter(lambda x: x != -1, df2['existence_gender_correctness'].tolist()))
        print('Existence gender correctness: ', sum(existence_res_list) / len(existence_res_list))
        diversity_res_list = list(filter(lambda x: x != -1, df2['existence_gender_diversity'].tolist()))
        gold_diversity_res_list = list(filter(lambda x: x != -1, df2['gold_gender_diversity'].tolist()))
        print('Generation-Gold Diversity Gap: ', sum(diversity_res_list) / len(diversity_res_list) - sum(gold_diversity_res_list) / len(gold_diversity_res_list))
        existence_f1_res_list = list(filter(lambda x: x != -1, df2['existence_gender_f1'].tolist()))
        print('Existence gender F1: ', sum(existence_f1_res_list) / len(existence_f1_res_list))
        
        if args.write_results:
            if '/sd/' in args.fairface_file:
                df2.to_csv('./final_results/sd_' + args.fairface_file.split('/')[-1].replace('.csv', '_results.csv'), index=False)
            else:
                df2.to_csv('./final_results/' + args.fairface_file.split('/')[-1].replace('.csv', '_results.csv'), index=False)