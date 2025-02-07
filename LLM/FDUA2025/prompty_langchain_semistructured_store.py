# This Python file uses the following encoding: utf-8
import getpass
import os
import logging
import logging.config
import json
import pandas as pd, numpy as np
#import pymupdf4llm
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
#from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings
# pip install langchain-prompty
from langchain_prompty import create_chat_prompt
from pathlib import Path

logging_json_path = os.path.join(os.path.dirname(__file__), 'logging.json')

with open(logging_json_path, 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")

# LangChainのOpenAIモデルを作成
model = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID_FOR_CHAT_COMPLETION,
    api_version=API_VERSION,
    temperature=0,
    max_tokens=100
)
embeddings = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID_FOR_EMBEDDING,
    model='text-embedding-3-large',
    api_version=API_VERSION
)

logger.info("Model: %s" % (model))
logger.info("Embeddings: %s" % (embeddings))
db_directory = "./"
doc_db = "documents.db"
vec_db = "vectors.db"
collection_name = "summaries"
query_directory = "./validation/"

# Chromaに接続
vectorstore = Chroma(persist_directory=db_directory+vec_db, embedding_function=embeddings, collection_name=collection_name)

# Initialize the persistent storage layer for the parent documents
# The storage layer for the parent documents
doc_path = db_directory+doc_db
fs = LocalFileStore(doc_path)
store = create_kv_docstore(fs)
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)
# load prompty as langchain ChatPromptTemplate
# Important Note: Langchain only support mustache templating. Add 
#  template: mustache
# to your prompty and use mustache syntax.
folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/FDUA2025.prompty"
prompt = create_chat_prompt(path_to_prompty)

output_parser = StrOutputParser()


# RAG pipeline
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# CSVファイルを読み込む
df = pd.read_csv(query_directory + 'query.csv')

# 各行を処理するループ
for index, row in df.iterrows():
    # 各列の値を取得
    column1 = row['index']
    column2 = row['problem']
    
    # ここに処理内容を記述
    logger.info(f"Row {index}: index = {column1}, problem = {column2}")
    result = chain.invoke(problem)
    print(result)
