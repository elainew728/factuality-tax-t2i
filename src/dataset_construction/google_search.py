import numpy as np
import os
import json
import requests
import sys
from tqdm import tqdm
from typing import List
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from newspaper import Article
import openai
from bs4 import BeautifulSoup # Required to parse HTML
from urllib.parse import unquote # Required to unquote URLs
from huggingface_hub import login

login(token=$YOUR_HUGGINGFACE_TOKEN$)

text_splitter = CharacterTextSplitter(separator=' ', chunk_size=1000, chunk_overlap=200)

#####
# OPENAI
#####

### --- ### 
# WARNING: NEVER change the API setting
OPENAI_API_KEY = $YOUR_OPENAI_API_KEY$
ORGANIZATION = $YOUR_OPENAI_ORGANIZATION$
### --- ### 

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#####
# Google Search
#####

def google_search(
        query: str,
        api_key: str = None,
        cx: str = None,
        wiki_only: bool = False,
):
    """Get top 10 webpages from Google search.

    Args:
        query: search query
        api_key: custom search engine api key
        cx: programmable search engine id
    Returns:
        top-10 search results in json format
    """
    response = requests.get(f"https://www.google.com/search?q={query}") # Make the request
    soup = BeautifulSoup(response.text, "html.parser") # Parse the HTML
    links = soup.find_all("a") # Find all the links in the HTML

    urls = []
    for l in [link for link in links if link["href"].startswith("/url?q=")]:
        # get the url
        url = l["href"]
        # remove the "/url?q=" part
        url = url.replace("/url?q=", "")
        # remove the part after the "&sa=..."
        url = unquote(url.split("&sa=")[0])
        # special case for google scholar
        if url.startswith("https://scholar.google.com/scholar_url?url=http"):
            url = url.replace("https://scholar.google.com/scholar_url?url=", "").split("&")[0]
        elif 'google.com/' in url: # skip google links
            continue
        if url.endswith('.pdf'): # skip pdf links
            continue
        if '#' in url: # remove anchors (e.g. wikipedia.com/bob#history and wikipedia.com/bob#genetics are the same page)
            url = url.split('#')[0]
        if not wiki_only or 'wikipedia' in url:
            # print the url
            urls.append(url)

    # Use numpy to dedupe the list of urls after removing anchors
    urls = list(np.unique(urls))
    return urls

def scrape_and_parse(url: str):
    """Scrape a webpage and parse it into a Document object"""
    a = Article(url)
    try:
        a.download()
        a.parse()
    except Exception as e:
        return None

    return {
        "url": url,
        "text": a.text,
    }


def scrape_and_filter(urls: list):
    doc_list = []
    for u in urls:
        print(f"Processing: {u}")
        doc = scrape_and_parse(u)
        if doc is None:
            continue
        elif "Access" in doc["text"] and "Denied" in doc["text"]:
            continue
        else:
            doc_list.append(doc)

    return doc_list


def retrieve_topk_passages(query: str,
                           retrieved_documents: List[Document],
                           topk: int):

    texts = text_splitter.split_documents(retrieved_documents)
    embeddings = OpenAIEmbeddings() #openai_api_key=OPENAI_API_KEY, max_retries=1000)
    while True:
        try:
            docsearch = Chroma.from_documents(texts, embeddings)
            print(docsearch)
        except Exception as e:
            print(e)
            exit()
            continue
        break
    doc_retriever = docsearch.as_retriever(search_kwargs={"k": topk})
    topk_relevant_passages = doc_retriever.get_relevant_documents(query)
    return topk_relevant_passages

if __name__ == '__main__':    
    # run offline google search
    query = 'What is a lobster roll?'
    wiki_only = True
    search_results = google_search(query, wiki_only=wiki_only)
    
    if len(search_results) > 0:
        all_docs = scrape_and_filter(search_results)
        all_docs = [Document(page_content=d['text'], metadata={'source': d['url']}) for d in all_docs]
        all_docs_content_lens = [len(doc.page_content.strip()) for doc in all_docs]
        if not all_docs or not sum(all_docs_content_lens):
            relevant_passages = []
        else:
            relevant_passages = retrieve_topk_passages(query, all_docs, 5)
    else:
        relevant_passages = []
                                
    print(*relevant_passages, sep='\n\n')
