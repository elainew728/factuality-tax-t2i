import pandas as pd
import glob
import os
import openai
import json
import random
from tqdm import tqdm
from argparse import ArgumentParser
from constants import IMAGE_GENERATION_PROMPT, RACE_DIVERSITY_PROMPT, GENDER_DIVERSITY_PROMPT, RACE_DIVERSITY_PROMPT_2, GENDER_DIVERSITY_PROMPT_2, COT_PROMPT, HISTORICAL_RACE_COT_PROMPT, HISTORICAL_GENDER_COT_PROMPT, RAG_COT_GENDER_PROMPT, RAG_COT_RACE_PROMPT
from generation_util import get_dalle_response, save_img_from_url, generate_chatgpt_original, generate_chatgpt

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if", "--input_file", type=str, default="./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv")
    parser.add_argument("-o", "--output_folder", type=str, default="./img_output/")
    parser.add_argument("--cot_model", type=str, default=None)
    parser.add_argument("-dpt", "--diversity_prompt_type", type=str, default=None)
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    parser.add_argument("-d", "--diversity_prompt", action="store_true")
    parser.add_argument("-c", "--clear_output", action="store_true")
    parser.add_argument("--cot", action="store_true")
    parser.add_argument("--fai_vk", action="store_true")
    parser.add_argument("--fai_rk", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.diversity_prompt:
        if args.cot: 
            if args.diversity_prompt_type is None:
                output_folder = args.output_folder + 'diversity_cot/'
            else:
                output_folder = args.output_folder + 'diversity{}_cot/'.format(args.diversity_prompt_type)
        elif args.fai_vk:
            print('\n### ----------Using proposed FAI-VK method---------- ###\n')
            if args.diversity_prompt_type is None:
                output_folder = args.output_folder + 'diversity_fai_vk/'
            else:
                output_folder = args.output_folder + 'diversity{}_fai_vk/'.format(args.diversity_prompt_type)
        elif args.fai_rk:
            print('\n### ----------Using proposed FAI-RK method---------- ###\n')
            if args.diversity_prompt_type is None:
                output_folder = args.output_folder + 'diversity_fai_rk/'
            else:
                output_folder = args.output_folder + 'diversity{}_fai_rk/'.format(args.diversity_prompt_type)
        else:
            if args.diversity_prompt_type is None:
                output_folder = args.output_folder + 'diversity/'
            else:
                output_folder = args.output_folder + 'diversity_{}/'.format(args.diversity_prompt_type)
    else:
        output_folder = args.output_folder + 'default/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if args.race:
        output_folder = output_folder + 'race/'
    elif args.gender:
        output_folder = output_folder + 'gender/'
    if args.test: 
        output_folder = output_folder[:-1] + '_10/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    filelist = glob.glob(os.path.join(output_folder, "*.png"))
    if args.clear_output:
        filelist = []
        for f in filelist:
            os.remove(f)

    df = pd.read_csv(args.input_file)
    if args.test:
        print('\n\n### ------- Testing with the first 10 generations... ------###\n\n')
        df = df[:10]
    if args.fai_rk:
        df['rag_docs'] = ''
        if args.gender:
            df2 = pd.read_json('./data/events_year_culture_gender_roles_factchecked.jsonl', lines=True)
        elif args.race:
            df2 = pd.read_json('./data/events_year_culture_race_roles_factchecked.jsonl', lines=True)
        for i in range(len(df)):
            tmp = df2[df2['culture'] == df['culture'][i]]
            tmp = tmp[tmp['event_name'] == df['event_name'][i]]
            tmp.reset_index(drop=True, inplace=True)
            for j in range(len(tmp)):
                document_list = set()
                if tmp['group'][j] == df['group'][i]:
                    for k in range(len(tmp['dominant_factcheck_queries'][j])):
                        docs = tmp['dominant_factcheck_queries'][j][k]['ctxs']
                        for doc in docs:
                            document_list.add(doc)
                    for k in range(len(tmp['existence_factcheck_queries'][j])):
                        docs = tmp['existence_factcheck_queries'][j][k]['ctxs']
                        for doc in docs:
                            document_list.add(doc)
                    for doc_id, doc in enumerate(document_list):
                        df['rag_docs'][i] += 'Document_{}: '.format(doc_id) + doc + '\n\n'
                    break
        del tmp
        del df2
        
    event_names = df['event_name'].tolist()
    group_names = df['group'].tolist()
    if args.fai_rk:
        rag_docs = df['rag_docs'].tolist()
    df['img_path'] = ''
    df['prompt'] = ''
    
    for i in tqdm(range(len(event_names))):
        file_name = output_folder + '{}_{}.png'.format(group_names[i], event_names[i].replace(' ', '_').replace('.', '').replace(',', ''))

        if file_name in filelist:
            if args.gender:
                df['img_path'][i] += file_name.replace(args.output_folder, './factuality-tax-t2i/img_output/')
            elif args.race:
                df['img_path'][i] += file_name.replace(args.output_folder, './factuality-tax-t2i/img_output/')
            continue

        if args.diversity_prompt:
            if args.race:
                if args.diversity_prompt_type is None:
                    prompt = IMAGE_GENERATION_PROMPT.format(group_names[i], event_names[i])[:-1] + RACE_DIVERSITY_PROMPT.format(group_names[i])
                elif args.diversity_prompt_type == '2':
                    prompt = IMAGE_GENERATION_PROMPT.format(group_names[i], event_names[i])[:-1] + RACE_DIVERSITY_PROMPT_2.format(group_names[i])
            elif args.gender:
                if args.diversity_prompt_type is None:
                    prompt = IMAGE_GENERATION_PROMPT.format(group_names[i], event_names[i])[:-1] + GENDER_DIVERSITY_PROMPT.format(group_names[i])
                elif args.diversity_prompt_type == '2':
                    prompt = IMAGE_GENERATION_PROMPT.format(group_names[i], event_names[i])[:-1] + GENDER_DIVERSITY_PROMPT_2.format(group_names[i])
        else:
            prompt = IMAGE_GENERATION_PROMPT.format(group_names[i], event_names[i])

        if args.cot:
            assert args.diversity_prompt
            if 'gpt' in args.cot_model:
                model_extension = generate_chatgpt_original(prompt + ' ' + COT_PROMPT, args.cot_model)
            prompt = prompt + ' ' + model_extension
        elif args.fai_vk:
            if args.race:
                model_extension = generate_chatgpt_original(prompt + ' ' + COT_PROMPT + ' ' + HISTORICAL_RACE_COT_PROMPT.format(group_names[i], event_names[i]), args.cot_model)
            elif args.gender:
                model_extension = generate_chatgpt_original(prompt + ' ' + COT_PROMPT + ' ' + HISTORICAL_GENDER_COT_PROMPT.format(group_names[i], event_names[i]), args.cot_model)
            prompt = prompt + ' ' + model_extension

        if args.fai_rk:
            if args.race:
                model_extension = generate_chatgpt_original(RAG_COT_RACE_PROMPT.format(rag_docs[i], group_names[i], event_names[i], group_names[i], event_names[i]), args.cot_model)
            elif args.gender:
                model_extension = generate_chatgpt_original(RAG_COT_GENDER_PROMPT.format(rag_docs[i], group_names[i], event_names[i], group_names[i], event_names[i]), args.cot_model)
            prompt = prompt + ' ' + model_extension

        print('\n\nPrompt: ', prompt)
        df['prompt'][i] += prompt

        try:
            image_url = get_dalle_response(prompt)
            save_img_from_url(image_url, file_name)
        except openai.BadRequestError as err:
            print('Error: ', err)
            continue
        if args.gender:
            df['img_path'][i] += file_name.replace(args.output_folder, './factuality-tax-t2i/img_output/')
        elif args.race:
            df['img_path'][i] += file_name.replace(args.output_folder, './factuality-tax-t2i/img_output/')
    
    if args.diversity_prompt:
        if args.cot:
            output_file_name = args.input_file.replace('.csv', '_imggen_diverse_cot.csv')
        elif args.fai_vk:
            output_file_name = args.input_file.replace('.csv', '_imggen_diverse_fai_vk.csv')
        elif args.fai_rk:
            output_file_name = args.input_file.replace('.csv', '_imggen_diverse_fai_rk.csv')
        else:
            output_file_name = args.input_file.replace('.csv', '_imggen_diverse.csv')

        if args.diversity_prompt_type is not None:
            output_file_name = output_file_name.replace('_diverse', '_diverse{}'.format(args.diversity_prompt_type))
    else:
        output_file_name = args.input_file.replace('.csv', '_imggen.csv')

    df.to_csv(output_file_name, index=False)