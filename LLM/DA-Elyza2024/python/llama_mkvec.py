#!/usr/bin/env python

import os
from logging import getLogger
import inspect

### https://github.com/pistatium/about_python_logging
import json
from logging.config import dictConfig

# 設定ファイルから読み込む
with open('logging.json') as f:
    dictConfig(json.load(f))

logger = getLogger('app')
    
def varlog(name):
    # 変数が定義されているスコープを取得
    frame = inspect.currentframe().f_back
    variable_value = frame.f_globals.get(name) or frame.f_locals.get(name)
    
    if variable_value is not None:
        logger.info(f'{name}={variable_value}')
    else:
        logger.warning(f'{name} is not defined')

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

from chromadb import PersistentClient 
from chromadb import HttpClient
from chromadb.utils import embedding_functions
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
#from llama_index.core import Settings

from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from tqdm import tqdm


required_exts = [".pdf"]
reader = SimpleDirectoryReader(
    "./Downloads/digital_agency_standard_guidelines/",
    recursive=True,
    required_exts=required_exts,
    filename_as_id=True
)
documents=reader.load_data(num_workers=1)

db_dir='./db_llama/'

#e_models=['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']
e_models=['text-embedding-3-small']
for e in e_models:
    varlog('e')
    db_path = f"{db_dir}/chroma_{''.join(name[0] for name in e.split('-'))}"
    varlog('db_path')

    ef = embedding_functions.OpenAIEmbeddingFunction( model_name=e, api_key=os.getenv('OPENAI_API_KEY') )
    client = PersistentClient(path=db_path)
    #client = HttpClient(host='localhost', port=10000)
    collection = client.get_or_create_collection(
        name="digital_agency_standard_guidelines",
        embedding_function=ef
    )
    for docs in documents:
        collection.add(documents=docs.text,ids=docs.doc_id)
        pass
    pass
