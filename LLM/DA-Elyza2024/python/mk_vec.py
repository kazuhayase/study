#!/usr/bin/env python

import os
from varlog import varlog 

# uncomment if needs more than varlog
# from logging import getLogger
# logger = getLogger(__name__)
# # logger = getLogger('uvicorn');; fast api

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

#source_text = "hoken1-ch1.txt"
#source_text = "simple.txt"
source_text = "hoken1.txt"

#ebook_dir ="/content/drive/MyDrive/Actuary/eBooks/"
ebook_dir ="/home/kazu/Books/Actuary-ebook/" ## Ubuntu@lavie
#ebook_dir ="/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1.txt" ## Ubuntu@home
#ebook_dir ="/mnt/c/Users/kazuy/MEGAsync/ebooks/Actuary-ebook/"  ## Debian@mouseNoteWin11

file_path = ebook_dir + source_text
varlog('file_path')

### try llamaindex 
# 1. PDFを読み込む
#todo PDF読み込みはPyPDFではエラーになる。javascriptは読み込めた（はず）が、処理がうまくいかなかったので、テキストに変換して処理している。
#pages = PyPDFLoader(file_path).load()
pages = TextLoader(file_path).load()

# 2. ドキュメントをチャンクに分割
#docs = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0).split_documents(pages)
docs = CharacterTextSplitter().split_documents(pages)
varlog('len(docs)')

# 3. 埋め込みモデルの初期化
### open ai の embeddingがupgrade
#https://platform.openai.com/docs/guides/embeddings/embedding-models
#text-embedding-ada-002 -> text-embedding-3-{small,large}

# models
#EMBEDDING_MODEL = 'text-embedding-ada-002'
#EMBEDDING_MODEL = 'text-embedding-3-small'
#EMBEDDING_MODEL = 'text-embedding-3-large'
### todo; 他のEmbeddingも検証してみたい

# https://qiita.com/akeyhero/items/ce371bfed64399027c23
# https://huggingface.co/intfloat/multilingual-e5-large
# https://huggingface.co/Cohere/Cohere-embed-multilingual-v3.0


e_models=['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']

for e in e_models:
    varlog('e')
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        model_name=e,
        api_key=os.getenv('OPENAI_API_KEY'),
    )
    embeddings = OpenAIEmbeddings(model=e,tiktoken_model_name="cl100k_base")
#https://python.langchain.com/docs/integrations/vectorstores/chroma
#Basic Example(including saving to disk)
    db_dir='./db/'
    db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e.split('-'))}"
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=db_path
    )
    if db:
        db.persist()
        db = None
    else:
        print("Chroma DB has not been initialized.")
