from generation_util import generate_chatgpt_original
import pandas as pd
from tqdm import tqdm
from argparse import ArgumentParser
import glob
import os
import openai
import torch
from diffusers import StableDiffusionPipeline, StableDiffusion3Pipeline, EulerDiscreteScheduler
import numpy as np
from huggingface_hub import login
from constants import IMAGE_GENERATION_PROMPT, RACE_DIVERSITY_PROMPT, GENDER_DIVERSITY_PROMPT, RACE_DIVERSITY_PROMPT_2, GENDER_DIVERSITY_PROMPT_2

# Remember to replace this with your huggingface token
login(token=$YOUR_HUGGINGFACE_TOKEN$)

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
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--use_sd3", action="store_true")
    args = parser.parse_args()

    if args.use_sd3:
        model_id = "stabilityai/stable-diffusion-3-medium"
        pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
    else:
        # stable diffusion 2
        model_id = "stabilityai/stable-diffusion-2"
        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)


    if args.diversity_prompt:
        if args.diversity_prompt_type is None:
            output_folder = args.output_folder + 'diversity/'
        else:
            output_folder = args.output_folder + 'diversity_{}/'.format(args.diversity_prompt_type)
    else:
        output_folder = args.output_folder + 'default/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if args.race:
        output_folder = output_folder + 'race_sd/'
    else:
        output_folder = output_folder + 'gender_sd/'

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

    event_names = df['event_name'].tolist()
    group_names = df['group'].tolist()
    df['img_path'] = ''
    df['prompt'] = ''
    
    for i in tqdm(range(len(event_names))):
        file_name = output_folder + '{}_{}.png'.format(group_names[i], event_names[i].replace(' ', '_').replace('.', '').replace(',', ''))

        if file_name in filelist:
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

        print('Prompt: ', prompt)
        df['prompt'][i] += prompt

        image = pipe(prompt).images[0]
        image.save(file_name)
        
        df['img_path'][i] += file_name.replace(args.output_folder, './factuality-tax-t2i/img_output/')
    
    if args.diversity_prompt:
        output_file_name = args.input_file.replace('./output/', './output/sd/').replace('.csv', '_imggen_diverse.csv')

        if args.diversity_prompt_type is not None:
            output_file_name = output_file_name.replace('_diverse', '_diverse{}'.format(args.diversity_prompt_type))
    else:
        output_file_name = args.input_file.replace('./output/', './output/sd/').replace('.csv', '_imggen.csv')

    df.to_csv(output_file_name, index=False)