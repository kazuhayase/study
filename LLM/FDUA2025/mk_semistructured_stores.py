# -*- coding: utf-8 -*-
###import dataiku
import pandas as pd, numpy as np
#from dataiku import pandasutils as pdu
#from typing import Dict
import os
import logging
import logging.config
import json
import pymupdf4llm
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

from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings

# logging.jsonのパスを確認
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

# Prompt
#prompt_text = """You are an assistant tasked with summarizing tables and text. 
#Give a concise summary of the table or text. Table or text chunk: {element} """
prompt_text = """あなたは、表と文章の要約を担当するアシスタントです。 
表もしくは文章の要約を簡潔に日本語で述べてください。 表もしくは文章のチャンク: {element} """

prompt = ChatPromptTemplate.from_template(prompt_text)

# Summary chain
summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

doc_directory = "./validation/documents/"
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
    doc = fitz.open(path)
    for pnum, page in enumerate(doc):
        logger.info("Page number: %s" % (pnum))
        tables = page.find_tables()
        if tables.tables != []:
            logger.info("Tables: %s" % (tables))
            tabs = [t.to_markdown() for t in tables]
            logger.info("Tabs: %s" % (tabs))
            table_ids = [str(uuid.uuid4()) for _ in tabs]
            try:
                table_summaries = summarize_chain.batch(tabs, {"max_concurrency": 2})                
                logger.info("Table summaries: %s" % (table_summaries))
                summary_tables = [
                    Document(page_content=s, metadata={id_key: table_ids[i]})
                    for i, s in enumerate(table_summaries)
                ]
            except Exception as e:
                logger.error("Error: %s" % (e))
        
            doc_tables = [
                Document(page_content=str(s), metadata={id_key: table_ids[i]})
                for i, s in enumerate(tabs)
            ]
            retriever.vectorstore.add_documents(summary_tables)
            retriever.docstore.mset(list(zip(table_ids, doc_tables)))
        text = page.get_text()
        logger.info("Text: %s" % (text))
        if len(text) > 0:
            doc_ids = str(uuid.uuid4())
            try:
                text_summaries = summarize_chain.batch([text], {"max_concurrency": 2})
                logger.info("Text summaries: %s" % (text_summaries))
                summary_texts = [
                    Document(page_content=str(text_summaries), metadata={id_key: doc_ids})
                ]
            except Exception as e:
                logger.error("Error: %s" % (e))
            doc_texts = [
                Document(page_content=str(text), metadata={id_key: doc_ids})
            ]
            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(list(zip(doc_ids, doc_texts)))

def load_pdf_data(retriever, input_filenames):
    for idx, filename in enumerate(input_filenames):
        logger.info("Index: %s => Filename: %s" % (idx, filename))
        fullpath = doc_directory + filename
        store_tables_and_test(retriever, fullpath)
    return

db_directory = "./"
doc_db = "documents.db"
vec_db = "vectors.db"
collection_name = "summaries"

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

load_pdf_data(retriever, input_filenames)

# Prompt template
template = """Answer the question based only on the following context in Japanese, which can include text and tables:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG pipeline
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

ret=chain.invoke("電通グループPurposeは何ですか？")
print(ret)
#documents_md_df = pd.DataFrame(data_page)
