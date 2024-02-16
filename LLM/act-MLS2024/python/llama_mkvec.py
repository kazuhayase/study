#!/usr/bin/env python

import os
from varlog import varlog 

# uncomment if needs more than varlog
# from logging import getLogger
# logger = getLogger(__name__)
# # logger = getLogger('uvicorn');; fast api

from llama_index.core import (
        VectorStoreIndex,
        SimpleDirectoryReader,
        ServiceContext,
        StorageContext,
        load_index_from_storage,
)

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

import chromadb.utils.embedding_functions as embedding_functions

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

required_exts = [".pdf"]
documents = SimpleDirectoryReader(
        "./Downloads",
        recursive=True,
        required_exts=required_exts,
).load_data()

db_dir='./db_llama/'

e_models=['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']
for e in e_models:
    varlog('e')
    db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e.split('-'))}"

    db = chromadb.PersistentClient(path=db_path)
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    embed_model = OpenAIEmbedding(model=e,tiktoken_model_name="cl100k_base")
    service_context = ServiceContext.from_defaults(chunk_size=1000, embed_model=embed_model)
    index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=service_context
    )

