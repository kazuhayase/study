import chromadb
import os
import chromadb.utils.embedding_functions as embedding_functions
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import tiktoken
import logging
logging.basicConfig(
    filename="log/vec_client.log",
    #stream=sys.stdout,
    level=logging.INFO, #ERROR, WARNING, INFO, DEBUG
    format="[%(process)d-%(thread)d]-%(asctime)s-[%(filename)s:%(lineno)d]-%(levelname)s-%(message)s",
    force=True)

# logging var with varname (:str)
def varlog(name):
        logging.info(f'{name}={eval(name)}')

#https://python.langchain.com/docs/integrations/vectorstores/chroma
#Basic Example(including saving to disk)

EMBEDDING_MODEL = 'text-embedding-3-small'
#EMBEDDING_MODEL = 'text-embedding-3-large'
#EMBEDDING_MODEL = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL,tiktoken_model_name="cl100k_base")

db_dir='./db/'
db_path = f"{db_dir}/chroma_{''.join(name[0] for name in EMBEDDING_MODEL.split('-'))}"

# load from disk
varlog('db_path')
db = Chroma(
    embedding_function=embeddings,
    persist_directory=db_path
)
retriever = db.as_retriever()
keyword = '営業保険料'
retrieval_query = keyword + "に関わる箇所を抽出してください。"

varlog('retrieval_query')

#docs = db.similarity_search(retrieval_query)
#print(docs[0].page_content)

context_docs = retriever.get_relevant_documents(retrieval_query)
varlog('len(context_docs)')  # 抽出したドキュメント数
