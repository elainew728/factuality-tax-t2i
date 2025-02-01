import json
import os
import pandas as pd
from tqdm import tqdm
import copy
import random
from argparse import ArgumentParser
from constants import CULTURES, GENDERS, RACE_LIST, RACE_INITIAL_PROMPT, RACE_SELF_CHECK_DOMINANT_PROMPT, RACE_SELF_CHECK_EXISTENCE_PROMPT, GENDER_INITIAL_PROMPT, GENDER_SELF_CHECK_DOMINANT_PROMPT, GENDER_SELF_CHECK_EXISTENCE_PROMPT
from generation_util import generate_chatgpt, generate_chatgpt_text
from src.dataset_construction.google_search import google_search, scrape_and_filter, retrieve_topk_passages
from langchain.schema import Document 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if", "--input_file", type=str, default="./data/events_year_culture_race_roles.csv")
    parser.add_argument("-of", "--output_file", type=str, default="./data/events_year_culture_race_roles_factchecked.jsonl")
    parser.add_argument("-c", "--clear_output", action="store_true")
    parser.add_argument("-r", "--race", action="store_true")
    parser.add_argument("-g", "--gender", action="store_true")
    parser.add_argument("-w", "--wiki_only", action="store_true")
    parser.add_argument("--trim", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.race:
        # Dominant
        INITIAL_PROMPT = RACE_INITIAL_PROMPT
        SELF_CHECK_DOMINANT_PROMPT = RACE_SELF_CHECK_DOMINANT_PROMPT
        # Existence
        predefined_existence_queries = []
        for race in RACE_LIST:
            predefined_existence_queries.append("""Were there any """ + race)
        SELF_CHECK_EXISTENCE_PROMPT = RACE_SELF_CHECK_EXISTENCE_PROMPT

    elif args.gender: 
        # Dominant 
        INITIAL_PROMPT = GENDER_INITIAL_PROMPT
        SELF_CHECK_DOMINANT_PROMPT = GENDER_SELF_CHECK_DOMINANT_PROMPT
        # Existence
        predefined_existence_queries = []
        for gender in GENDERS:
            predefined_existence_queries.append("""Were there any """ + gender)
        SELF_CHECK_EXISTENCE_PROMPT = GENDER_SELF_CHECK_EXISTENCE_PROMPT

    data = pd.read_csv(args.input_file)

    if args.trim:
        per_category = 2
        
        i = 0
        event_count = {}
        drop = []
        if args.race:
            dominant_clm = 'dominant_race'
        elif args.gender:
            dominant_clm = 'dominant_gender'
        while i < len(data):
            tmp_culture = data['culture'][i]
            tmp_year = data['years'][i]
            tmp_event = data['event_name'][i]
            tmp_dominant_clm = data[dominant_clm][i] # dominant_gender
            if (tmp_culture + '_' + tmp_year + '_' + tmp_dominant_clm) not in event_count.keys():
                event_count[tmp_culture + '_' + tmp_year + '_' + tmp_dominant_clm] = 1
            else:
                event_count[tmp_culture + '_' + tmp_year + '_' + tmp_dominant_clm] += 1
        
            event_idxs = [i]
            j = i + 1
            while (j < len(data)) and (data['culture'][j] == tmp_culture) and (data['years'][j] == tmp_year) and (data[dominant_clm][j] == tmp_dominant_clm):
                event_idxs.append(j)
                event_count[tmp_culture + '_' + tmp_year + '_' + tmp_dominant_clm] += 1
                j += 1

            if len(event_idxs) > per_category:
                drop += random.sample(event_idxs, len(event_idxs) - per_category)
            
            i = j

        print('Trimming dataset. Dropping {} entries...'.format(len(drop)))
        data.drop(drop, inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.to_csv(args.input_file.replace('.jsonl', '_droppe_{}.csv'.format(len(data))), index=False)
        print('Completed trimming dataset. Remaining {} entries!'.format(len(data)))

    data = data.to_dict(orient='records')
    if args.test:
        print('\n\n### ------- Testing with the first 10 events... ------###\n\n')
        data = data[:10]
    begin = 0

    if args.race:
        if os.path.isfile(args.output_file):
            df = pd.read_json(path_or_buf=args.output_file, lines=True)
            begin = len(df)
            print('Continuing from index: ', begin)
    elif args.gender:
        if os.path.isfile(args.output_file):
            df = pd.read_json(path_or_buf=args.output_file, lines=True)
            begin = len(df)
            print('Continuing from index: ', begin)

    for entry in tqdm(data[begin:]):
        # Dominant race / gender
        entry['dominant_factcheck_queries'] = []
        entry['dominant_factcheck_docs'] = ''
        dominant_factcheck_q_c = []

        initial_prompt = INITIAL_PROMPT.format_map(entry)
        print('Initial prompt:', initial_prompt)
        queries = generate_chatgpt(initial_prompt)
        dominant_queries = list(set([x['query'] for x in json.loads(queries.strip())['dominant_queries']]))
        print('Dominant queries:', dominant_queries)

        doc_id = 0
        document_list = set()

        for query in dominant_queries:
            search_results = google_search(query, wiki_only=args.wiki_only)
            if len(search_results) > 0:
                all_docs = scrape_and_filter(search_results)
                all_urls = [d['url'] for d in all_docs]
                all_docs = [Document(page_content=d['text'], metadata={'source': d['url']}) for d in all_docs]
                all_docs_content_lens = [len(doc.page_content.strip()) for doc in all_docs]
                if not all_docs or not sum(all_docs_content_lens):
                    relevant_passages = []
                else:
                    relevant_passages = retrieve_topk_passages(query, all_docs, 5)
            else:
                relevant_passages = []
            
            dominant_factcheck_q_c.append({
                'query': query,
                'ctxs': [x.page_content for x in relevant_passages],
                'urls': all_urls
            })

            for i in range(len(relevant_passages)):
                x = relevant_passages[i]
                if x.page_content not in document_list:
                    page_content = 'Document_{}: '.format(doc_id) + x.page_content + '\n\n'
                    entry['dominant_factcheck_docs'] += page_content
                    doc_id += 1
                    document_list.add(x.page_content)
                    
        entry['dominant_factcheck_queries'] = dominant_factcheck_q_c

        self_check_dominant_prompt = SELF_CHECK_DOMINANT_PROMPT.format_map(entry)
        print('Prompt for checking dominant group: ', self_check_dominant_prompt)
        answer = generate_chatgpt_text(self_check_dominant_prompt)
        if args.race:
            entry['dominant_race_chatgpt'] = answer
        elif args.gender:
            entry['dominant_gender_chatgpt'] = answer

        # Existence race / gender
        entry['existence_factcheck_queries'] = []
        entry['existence_factcheck_docs'] = ''
        existence_factcheck_q_c = []

        doc_id = 0
        document_list = set()
        existence_queries = list(set([x['query'] for x in json.loads(queries.strip())['existence_queries']]))
        for q in predefined_existence_queries:
            existence_queries.append(q + """ people among the {group} in the {event_name}?""".format_map(entry))
        print('Existence queries:', existence_queries)

        for query in existence_queries:
            search_results = google_search(query, wiki_only=args.wiki_only)
            if len(search_results) > 0:
                all_docs = scrape_and_filter(search_results)
                all_urls = [d['url'] for d in all_docs]
                all_docs = [Document(page_content=d['text'], metadata={'source': d['url']}) for d in all_docs]
                all_docs_content_lens = [len(doc.page_content.strip()) for doc in all_docs]
                if not all_docs or not sum(all_docs_content_lens):
                    relevant_passages = []
                else:
                    relevant_passages = retrieve_topk_passages(query, all_docs, 5)
            else:
                relevant_passages = []
                all_urls = []
            
            existence_factcheck_q_c.append({
                'query': query,
                'ctxs': [x.page_content for x in relevant_passages],
                'urls': all_urls
            })
            for i in range(len(relevant_passages)):
                x = relevant_passages[i]
                if x.page_content not in document_list:
                    page_content = 'Document_{}: '.format(doc_id) + x.page_content + '\n\n'
                    entry['existence_factcheck_docs'] += page_content
                    doc_id += 1
                    document_list.add(x.page_content)

        entry['existence_factcheck_queries'] = existence_factcheck_q_c

        self_check_existence_prompt = SELF_CHECK_EXISTENCE_PROMPT.format_map(entry)
        print('Prompt for checking existence groups: ', self_check_existence_prompt)
        answer = generate_chatgpt_text(self_check_existence_prompt)
        if args.race:
            entry['existence_race_chatgpt'] = answer
        elif args.gender:
            entry['existence_gender_chatgpt'] = answer

        with open(args.output_file, 'a') as f:
            # for entry in out_data:
            print(json.dumps(entry), file=f)

        if os.path.isfile(args.output_file.replace('.jsonl', '.csv')):
            df= pd.read_csv(args.output_file.replace('.jsonl', '.csv'))
            df = df.append(entry, ignore_index=True, sort=False)
            df.to_csv(args.output_file.replace('.jsonl', '.csv'), index=False)
        else:
            jsonobj = pd.read_json(path_or_buf=args.output_file, lines=True)
            jsonobj.to_csv(args.output_file.replace('.jsonl', '.csv'), index=False)
