# -*- coding: utf-8 -*-
###import dataiku
import pandas as pd, numpy as np
#from dataiku import pandasutils as pdu
#from typing import Dict

import os
try:
    import pymupdf4llm
except Exception as e:
    raise Exception("Be sure to set the right code env. {}".format(e))

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

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")

# LangChainのOpenAIモデルを作成
model = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment_id=DEPLOYMENT_ID_FOR_CHAT_COMPLETION,
    openai_api_version=API_VERSION,
    temperature=0,
    max_tokens=100
)
embeddings = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment_id=DEPLOYMENT_ID_FOR_EMBEDDING,
    openai_api_version=API_VERSION
)

# Prompt
prompt_text = """You are an assistant tasked with summarizing tables and text. 
Give a concise summary of the table or text. Table or text chunk: {element} """
prompt = ChatPromptTemplate.from_template(prompt_text)

# Summary chain
summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

cols=['metadata', 'text', 'tables']
idx_cols=(['page', 'filename', 'index'])
idx_cols.extend(cols)
print(idx_cols)

doc_directory = "/home/kazuyoshi/Documents/FDUA202501/validation/validation/documents/"
input_filenames = [filename for filename in os.listdir(doc_directory) if filename.endswith(".pdf")]
print(input_filenames)

def markdown_from_index(test_index):
    fn = input_filenames[test_index]
    fullpath = doc_directory + fn
    fn = fn[1:]
    print("Full path: %s" % (fullpath))
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

def load_pdf_data(collection, input_filenames):
    md=list()
    data_page = dict()
    for col in idx_cols:
        data_page[col]=list()
    for idx, filename in enumerate(input_filenames):
        print("Index: %s => Filename: %s" % (idx, filename))
        md.append(markdown_from_index(idx))
        for col in idx_cols:
            for page in md[idx][col]:
                data_page[col].append(page) 
        for tables in md[idx]['tables']:        
            table_summaries = summarize_chain.batch(tables, {"max_concurrency": 2})
            table_ids = [str(uuid.uuid4()) for _ in tables]
            summary_tables = [
                Document(page_content=s, metadata={id_key: table_ids[i]})
                for i, s in enumerate(table_summaries)
            ]
            retriever.vectorstore.add_documents(summary_tables)
            retriever.docstore.mset(list(zip(table_ids, tables)))
        for texts in md[idx]['text']:        
            text_summaries = summarize_chain.batch(texts, {"max_concurrency": 2})
            doc_ids = [str(uuid.uuid4()) for _ in texts]
            summary_texts = [
                Document(page_content=s, metadata={id_key: doc_ids[i]})
                for i, s in enumerate(text_summaries)
            ]
            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(list(zip(doc_ids, texts)))
    # コミットして変更を保存
    store.commit()
    vectorstore.commit()
    return

db_directory = "./"
doc_db = "documents.db"
vec_db = "vectors.db"

# Chromaに接続
vectorstore = Chroma(persist_directory=db_directory+vec_db, embedding_function=embeddings)
collection_name = "summaries"

# Initialize the persistent storage layer for the parent documents
# The storage layer for the parent documents
fs = LocalFileStore(db_directory+doc_db)
store = create_kv_docstore(fs)
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)

# コレクションが存在するか確認
if vectorstore.has_collection(collection_name):
    # 既存のコレクションを読み込む
    collection = vectorstore.get_collection(collection_name)
else:
    # 新しいコレクションを作成
    collection = vectorstore.create_collection(
        collection_name=collection_name,
        embedding_function=embeddings
    )
    load_pdf_data(collection, input_filenames)


# Prompt template
template = """Answer the question based only on the following context, which can include text and tables:
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

chain.invoke("大成温調が積極的に資源配分を行うとしている高付加価値セグメントを全てあげてください。")

#documents_md_df = pd.DataFrame(data_page)
