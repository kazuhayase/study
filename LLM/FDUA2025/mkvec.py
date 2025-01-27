#!/usr/bin/env python

import os
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction

# set defalut text and image embedding functions
embedding_function = OpenCLIPEmbeddingFunction()


from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from chromadb.utils.data_loaders import ImageLoader

image_loader = ImageLoader()

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)


from llama_index.readers.file import PyMuPDFReader
llama_reader = PyMuPDFReader()

#import pymupdf4llm
#llama_reader = pymupdf4llm.LlamaMarkdownReader()

#llama_docs = llama_reader.load_data("input.pdf")
file_extractor = dict()
file_extractor["pdf"] = llama_reader

required_exts = [".pdf"]
documents=SimpleDirectoryReader(
    "./validation/validation/documents",
    required_exts=required_exts,
    #file_extractor=file_extractor,
    ).load_data(num_workers=1)

db_dir='./db_llama/'
e_model='text-embedding-3-large'
db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e_model.split('-'))}"
db = chromadb.PersistentClient(path=db_path)
chroma_collection = db.get_or_create_collection(
    'validation_CLIP', 
    embedding_function=embedding_function, 
    data_loader=image_loader)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model = OpenAIEmbedding(model=e_model,tiktoken_model_name="cl100k_base")

Settings.embed_model = embed_model
Settings.node_parser = SentenceSplitter(chunk_size=1000, chunk_overlap=200)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, 
)
