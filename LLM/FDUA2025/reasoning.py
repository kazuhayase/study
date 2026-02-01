# This Python file uses the following encoding: utf-8
import getpass
import os
import tqdm
import logging
import logging.config
from read_conf import setup_logging, get_retriever_conf, get_file_directry_conf, get_model

# スクリプト名を取得
script_name = os.path.splitext(os.path.basename(__file__))[0]
setup_logging(script_name)

logger = logging.getLogger(__name__)
logger.info("*** Start answering questions ***")

import json
import pandas as pd, numpy as np
import fitz  # import PyMuPDF
if not hasattr(fitz.Page, "find_tables"):
    raise RuntimeError("This PyMuPDF version does not support the table feature")
import uuid
import sqlite3
from langchain.retrievers.multi_vector import MultiVectorRetriever

##https://zenn.dev/koujimachi2023/articles/7a113a32473166
from langchain.storage import LocalFileStore    
from langchain.storage._lc_store import create_kv_docstore
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings
# pip install langchain-prompty
from langchain_prompty import create_chat_prompt
from pathlib import Path

models=get_model()
model = models['answer_openai_chat']
#model = models['answer_azure_chat']
#model = models['answer_llama_chat']
#model = models['answer_qwen_chat']
embeddings = models['embeddings']

logger.info("Model: %s" % (model))
logger.info("Embeddings: %s" % (embeddings))
fd_conf=get_file_directry_conf()
db_directory = fd_conf['db_directory']
doc_db = fd_conf['doc_db']
vec_db = fd_conf['vec_db']
collection_name = fd_conf['collection_name']
query_directory = fd_conf['query_directory']

# Chromaに接続
vectorstore = Chroma(persist_directory=db_directory+vec_db, embedding_function=embeddings, collection_name=collection_name)

# Initialize the persistent storage layer for the parent documents
# The storage layer for the parent documents
doc_path = db_directory+doc_db
fs = LocalFileStore(doc_path)
store = create_kv_docstore(fs)
id_key = "doc_id"

# The retriever (empty to start)

retriever_conf = get_retriever_conf()
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
    **retriever_conf
)
# load prompty as langchain ChatPromptTemplate
# Important Note: Langchain only support mustache templating. Add 
#  template: mustache
# to your prompty and use mustache syntax.
folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/FDUA2025-reasoning.prompty"
prompt = create_chat_prompt(path_to_prompty)

output_parser = StrOutputParser()

# RAG pipeline
chain = (
    {"context": retriever, "question": RunnablePassthrough(verbose=True)}
    | prompt
    | model
#    | StrOutputParser()
)

# CSVファイルを読み込む
df = pd.read_csv(query_directory + 'query.csv')

# 各行を処理するループ
answer_list = []
for index, row in tqdm.tqdm(df.iterrows()):
    # 各列の値を取得
    index = row['index']
    problem = row['problem']
    
    # ここに処理内容を記述
    logger.info(f"Row {index}: index = {index}, problem = {problem}")
    try:
        result = chain.invoke(problem, **retriever_conf)
        logger.info(f"Result: {result}")
        logger.info(f'type(result)={type(result)}')
        parsed_result = StrOutputParser().invoke(result)
        logger.info(f'parsed_result={parsed_result}')        
        logger.info(f'type(parsed_result)={type(parsed_result)}')
        answer_list.append([index,parsed_result])
    except Exception as e: 
        logger.error(f"Error: {e}")
        answer_list.append([index,"わからない(エラー)"])
for row in answer_list:
    print(f'{row[0]},"{row[1]}"')

logger.info("*** End answering questions ***")

#from email_notify import send_email
#send_email('Process Completed', 'Answered by prompty with semistructured store.', 'kazuyoshi.hayase@jcom.home.ne.jp')