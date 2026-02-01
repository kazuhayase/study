# -*- coding: utf-8 -*-
###import dataiku
import pandas as pd, numpy as np
#from dataiku import pandasutils as pdu
#from typing import Dict
import os
from langchain_prompty import create_chat_prompt
from pathlib import Path
from tqdm import tqdm
import logging
import os
from read_conf import setup_logging, get_retriever_conf, get_file_directry_conf, get_model

# スクリプト名を取得
script_name = os.path.splitext(os.path.basename(__file__))[0]

# ロギング設定を適用
setup_logging(script_name)

logger = logging.getLogger(__name__)

import json
import pymupdf4llm
import fitz  # import PyMuPDF
if not hasattr(fitz.Page, "find_tables"):
    raise RuntimeError("This PyMuPDF version does not support the table feature")
import uuid
import sqlite3
from email_notify import send_email

from langchain.retrievers.multi_vector import MultiVectorRetriever

##https://zenn.dev/koujimachi2023/articles/7a113a32473166
from langchain.storage import LocalFileStore    
from langchain.storage._lc_store import create_kv_docstore

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings

""" 
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")

# LangChainのOpenAIモデルを作成
model=AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID_FOR_CHAT_COMPLETION,
    api_version=API_VERSION,
    temperature=0,
    max_tokens=3000
)
embeddings = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID_FOR_EMBEDDING,
    model='text-embedding-3-large',
    api_version=API_VERSION
)

 """
models=get_model()
model = models['summarize_azure_chat']
embeddings = models['embeddings']

logger.info("Model: %s" % (model))
logger.info("Embeddings: %s" % (embeddings))

# Prompt
#prompt_text = """You are an assistant tasked with summarizing tables and text. 
#Give a concise summary of the table or text. Table or text chunk: {element} """
#prompt_text = """あなたは、表と文章の要約を担当するアシスタントです。 
#表もしくは文章の要約を簡潔に日本語で述べてください。 表もしくは文章のチャンク: {element} """
#prompt = ChatPromptTemplate.from_template(prompt_text)

folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/FDUA2025_summarize.prompty"
prompt = create_chat_prompt(path_to_prompty)

# Summary chain
summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
fd_conf = get_file_directry_conf()
doc_directory = fd_conf["doc_directory"]
input_filenames = [filename for filename in os.listdir(doc_directory) if filename.endswith(".pdf")]
#input_filenames = ['8.pdf']
logger.info(input_filenames)

def markdown_from_index(test_index):
    fn = input_filenames[test_index]
    fullpath = doc_directory + fn
    fn = fn[1:]
    logger.info("Full path: %s" % (fullpath))
    md_text = pymupdf4llm.to_markdown(fullpath, page_chunks = True)
    md_ret=dict()
    for col in idx_cols:
        md_ret[col]=list()

    for p, body in enumerate(md_text):
        md_ret['page'].append(p)
        md_ret['filename'].append(fn)
        md_ret['index'].append(f'{fn}:{p}')
        for col in cols:
            md_ret[col].append(body[col])
    return md_ret

def store_tables_and_test(retriever, path):
    fn=os.path.basename(path)
    try:
        doc = fitz.open(path)
    except Exception as e:
        logger.error(f"Error opening document: {e}" )
        return
    for pnum, page in enumerate(tqdm(doc, desc="Processing Pages", leave=False)):
        logger.info("Page number: %s" % (pnum))
        try:
            tables = page.find_tables()
        except Exception as e:
            logger.info("[Exception] Path: %s, Page: %s, Tables: %s" % (os.path.basename(path), page, tables))
            logger.error(f"Error finding tables: {e}")
            tables = []
        if tables.tables != []:
            logger.info("Path: %s, Page: %s, Tables: %s" % (os.path.basename(path), page, tables))
            tabs = [t.to_markdown() for t in tables]
            logger.info("Tabs: %s" % (tabs))
            #table_ids = [str(uuid.uuid4()) for _ in tabs]
            table_ids = [ f"{fn}_{pnum}_{i}_table" for i,t in enumerate(tabs)]
            try:
                table_summaries = summarize_chain.batch(tabs, {"max_concurrency": 4})                
            except Exception as e:
                logger.info("[Exception] Path: %s, Page: %s, Tables: %s..." % (os.path.basename(path), page, tables))
                logger.error("Error: %s" % (e))
                table_summaries = tabs

            logger.info("Table summaries: %s" % (table_summaries))

            summary_tables = []
            for i, s in enumerate(table_summaries):
                doc = Document(page_content=s, metadata={id_key: table_ids[i]})
                summary_tables.append(doc)
                logger.info("[Document] id_key: %s, Table summary: %s" % (table_ids[i], s))
            retriever.vectorstore.add_documents(summary_tables)

            tables_doc=[]
            for i,s in enumerate(tabs):
                doc = Document(page_content=s, metadata={id_key: table_ids[i]})
                tables_doc.append(doc)
                logger.info("[Document] id_key: %s, Table: %s" % (table_ids[i], s))
            retriever.docstore.mset(list(zip(table_ids, tables_doc)))

        text = page.get_text()
        logger.info("Filename: %s, Page: %s, Text: %s..." % (fn, page, text))

        if len(text) > 0:
            #doc_ids = str(uuid.uuid4())
            doc_ids = [ f"{fn}_{pnum}_text" ]
            
           # try:
           #    text_summary = summarize_chain.batch([text], {"max_concurrency": 4})
           # except Exception as e:
           #     logger.info("[Exception] Path: %s, Page: %s, Text: %s" % (os.path.basename(path), page, text))
           #     logger.error("Error: %s" % (e))
           #     text_summary = text

           # logger.info("Text summary: %s" % (text_summary))

            doc_texts = [
                Document(page_content=str(text), metadata={id_key: doc_ids[0]})
            ]
            logger.info("[Document] id_key: %s, Text: %s" % (doc_ids[0], text))

            retriever.vectorstore.add_documents(doc_texts)
            retriever.docstore.mset(list(zip(doc_ids, doc_texts)))

"""             summary_texts = [
                Document(page_content=str(text_summary), metadata={id_key: doc_ids})
                logger.info("[Document] id_key: %s, Text summary: %s" % (doc_ids, text_summary))
            ]
 """
            #retriever.vectorstore.add_documents(summary_texts)

# 進捗を保存するファイル
progress_file = fd_conf['progress_file']
def save_progress(data):
    with open(progress_file, 'w') as f:
        json.dump(data, f)

def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {}

def update_progress(file_idx):
    progress = load_progress()
    progress['file_idx'] = file_idx
    save_progress(progress)


def load_pdf_data(retriever, input_filenames):
    # 前回の進捗を読み込む
    progress = load_progress()
    start_file_idx = progress.get('file_idx', 0)
    for idx, filename in enumerate(tqdm(input_filenames[start_file_idx:], desc="Processing Files"), start=start_file_idx):
        logger.info("Index: %s => Filename: %s" % (idx, filename))
        fullpath = doc_directory + filename
        store_tables_and_test(retriever, fullpath)
        update_progress(idx)
    return

db_directory = fd_conf['db_directory']
doc_db = fd_conf['doc_db']
vec_db = fd_conf['vec_db']
collection_name = fd_conf['collection_name']
# Chromaに接続
vectorstore = Chroma(persist_directory=db_directory+vec_db, embedding_function=embeddings, collection_name=collection_name)

# Initialize the persistent storage layer for the parent documents
# The storage layer for the parent documents
doc_path = db_directory+doc_db
fs = LocalFileStore(doc_path)
store = create_kv_docstore(fs)
id_key = "doc_id"

# The retriever (empty to start)
# TOP_K for retriever
TOP_K = 20
retriever_conf = get_retriever_conf()
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
    **retriever_conf
)

try:
    load_pdf_data(retriever, input_filenames)
    logger.info("*** End answering questions ***")
    send_email('Process Completed', 'Built semistructured store.', 'kazuyoshi.hayase@jcom.home.ne.jp')
except Exception as e:
    logger.error(f"Error: {e}")
    send_email('Process Failed', 'Failed to build semistructured store.', 'kazuyoshi.hayase@jcom.home.ne.jp')

#print(test_store())

def test_store():
    # Prompt template
    template = """Answer the question based only on the following context in Japanese, which can include text and tables:
    {context}
    Question: {question}"""
    prompt = ChatPromptTemplate.from_template(template)

    # RAG pipeline
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    ret=chain.invoke("電通グループPurposeは何ですか？")
