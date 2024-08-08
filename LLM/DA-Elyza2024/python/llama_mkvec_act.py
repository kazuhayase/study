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

from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline

required_exts = [".pdf"]
kamoku=['hoken1_seiho', 'hoken2_seiho']
#kamoku=['hoken1_seiho', 'hoken2_seiho', 'sonpo', 'nenkin']
documents=dict()
for k in kamoku:
    varlog(k)
    documents[k] = SimpleDirectoryReader(
        "./Downloads/actuaries-examin-textbook/"+k,
        recursive=True,
        required_exts=required_exts,
    ).load_data(num_workers=1)

db_dir='./db_llama/'

e_models=['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']
for e in e_models:
    varlog('e')
    db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e.split('-'))}"
    varlog('db_path')

    db = chromadb.PersistentClient(path=db_path)
    for k in kamoku:
        chroma_collection = db.get_or_create_collection(k)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        embed_model = OpenAIEmbedding(model=e,tiktoken_model_name="cl100k_base")
        service_context = ServiceContext.from_defaults(chunk_size=1000, embed_model=embed_model)
        index = VectorStoreIndex.from_documents(
            documents[k], storage_context=storage_context, service_context=service_context
        )

        ### try to delete deprecated contexts, but failed.
        # index = VectorStoreIndex.from_documents(
        #     documents[k],
        #     embed_model = embed_model,
        #     chunk_size=1000,
        #     vector_store = vector_store
        # )


        # pipeline = IngestionPipeline(
        #     transformations=[
        #         SimpleFileNodeParser(),
        #         #SentenceSplitter(chunk_size=25, chunk_overlap=0),
        #         #TitleExtractor(),
        #         embed_model,
        #     ],
        #     vector_store = vector_store,
        # )
        # pipeline.run(documents[k])
        # index = VectorStoreIndex.from_vector_store(vector_store)

        

