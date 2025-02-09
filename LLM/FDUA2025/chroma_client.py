# This Python file uses the following encoding: utf-8
import os
import tqdm
import json
import logging
import logging.config
from read_conf import setup_logging, get_retriever_conf, get_file_directry_conf, get_model

# スクリプト名を取得
script_name = os.path.splitext(os.path.basename(__file__))[0]
setup_logging(script_name)

logger = logging.getLogger(__name__)
logger.info("*** Start ChromaDB client ***")

import pandas as pd, numpy as np
import sqlite3
import chromadb
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
""" 
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")

embeddings = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_ID_FOR_EMBEDDING,
    model='text-embedding-3-large',
    api_version=API_VERSION
)
 """
models = get_model()
embeddings = models['embeddings']
logger.info("Embeddings: %s" % (embeddings))
fd_conf=get_file_directry_conf()
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

retriever_conf = get_retriever_conf()
logger.info(f"Retriever configuration: {retriever_conf}")
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
    **retriever_conf
)

# retriever の全ての属性をログに出力するために、 dir() 関数を使用
#attributes = dir(retriever)
#logger.info(f"Retriever attributes: {attributes}")
#exit()

# method と _ で始まる属性を除外してログに出力
attributes = retriever.__dict__
for attr,value in attributes.items():
    if not attr.startswith('_') and not callable(value):
        logger.info(f"Attribute: {attr}, Value: {value}")

retriever_config = {
    "id_key": retriever.id_key,
    "search_kwargs": retriever.search_kwargs
}
# 設定をJSON形式でログに出力
logger.info(f"Retriever configuration: {json.dumps(retriever_config, indent=4)}")
#exit()

chroma_client = chromadb.PersistentClient(path=db_directory+vec_db)

# すべてのコレクションをリストアップ
collections = chroma_client.list_collections()

# 各コレクションをループして docids を取得
for collection_name in collections:
    collection = chroma_client.get_collection(collection_name)
    result = collection.get(limit=0, where_document={"$contains": '{"text": ""}'})
    print(f"Collection: {collection_name}, #DocIDs: {len(result['ids'])}")
