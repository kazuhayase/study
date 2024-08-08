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
        load_index_from_storage,
)

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

import chromadb.utils.embedding_functions as embedding_functions

db_dir='./db_llama/'

# load from disk
e = 'text-embedding-3-small'
db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e.split('-'))}"
db2=chromadb.PersistentClient(path=db_path)

chroma_collection = db2.get_or_create_collection("digital_agency_standard_guidelines")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
embed_model = OpenAIEmbedding(model=e,tiktoken_model_name="cl100k_base")
index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model = embed_model,
)

# Query Data from the persisted index
query_engine = index.as_query_engine(verbose=True)
#response = query_engine.query("What did the author do growing up?")
response = query_engine.query("PJMOは何ですか?")
print(response)

# Deprecated v0.10
#storage_context = StorageContext.from_defaults(vector_store=vector_store)
#service_context = ServiceContext.from_defaults(chunk_size=1000, embed_model=embed_model)
