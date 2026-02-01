# This Python file uses the following encoding: utf-8
import getpass
import os
import tqdm
import logging
import logging.config
from read_conf import setup_logging, get_retriever_conf, get_file_directry_conf, get_model

# スクリプト名を取得
script_name = os.path.splitext(os.path.basename(__file__))[0]
setup_logging(script_name)

logger = logging.getLogger(__name__)
logger.info("*** Start answering questions ***")

import json
import pandas as pd, numpy as np
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

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain_core.tools import Tool
from pydantic.v1 import BaseModel, Field # <-- Uses v1 namespace

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings
# pip install langchain-prompty
from langchain_prompty import create_chat_prompt
from pathlib import Path

models=get_model()
model = models['answer_openai_chat']
#model = models['answer_azure_chat']
#model = models['answer_llama_chat']
#model = models['answer_qwen_chat']
embeddings = models['embeddings']

logger.info("Model: %s" % (model))
logger.info("Embeddings: %s" % (embeddings))
fd_conf=get_file_directry_conf()
db_directory = fd_conf['db_directory']
doc_db = fd_conf['doc_db']
vec_db = fd_conf['vec_db']
collection_name = fd_conf['collection_name']
query_directory = fd_conf['query_directory']

# Chromaに接続
vectorstore = Chroma(persist_directory=db_directory+vec_db, embedding_function=embeddings, collection_name=collection_name)

# Initialize the persistent storage layer for the parent documents
# The storage layer for the parent documents
doc_path = db_directory+doc_db
fs = LocalFileStore(doc_path)
store = create_kv_docstore(fs)
id_key = "doc_id"

# The retriever (empty to start)

retriever_conf = get_retriever_conf()
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
    **retriever_conf
)
# load prompty as langchain ChatPromptTemplate
# Important Note: Langchain only support mustache templating. Add 
#  template: mustache
# to your prompty and use mustache syntax.
folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/FDUA2025.prompty"
prompt = create_chat_prompt(path_to_prompty)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_chain = (
    {
        "context": vectorstore.as_retriever() | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

tools = [
    Tool(
        name="multi_vector_search",
        func=qa_chain.invoke,
        description="multi vector search result with" + vec_db + "and" + doc_db
    ),
]
from langgraph.prebuilt import create_react_agent
graph = create_react_agent(model, tools=tools)
from langchain.schema import AIMessage, HumanMessage
import tiktoken
def make_answer(problem):
    # Ensure the input includes 'messages'
    input = {
        "messages": [
            {"role": "user", "content": problem}
        ]
    }

    #input={"problem" : problem}
    try:
        result=graph.invoke(input)
        logger.info(f'result={result}')
        logger.info(f'type(result)={type(result)}')
        parsed_result = StrOutputParser().parse(result)
        logger.info(f'parsed_result={parsed_result}')
    except Exception as e:
        logger.error(f"Error in make_answer: {e}")
    # Filter and process only AIMessage objects
    # メッセージのリストを取得
    messages = result['messages']

    # 最後のAIMessageを取得
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            final_ai_message_content = message.content
            break
 
   # Extract the content from AIMessage objects
    ret =  ' '.join(final_ai_message_content.splitlines()) 
    return ret
    #return  parsed_result

# CSVファイルを読み込む
df = pd.read_csv(query_directory + 'query.csv')

# 各行を処理するループ
answer_list = []
for index, row in tqdm.tqdm(df.iterrows()):
    # 各列の値を取得
    index = row['index']
    problem = row['problem']
    
    # ここに処理内容を記述
    logger.info(f"Row {index}: index = {index}, problem = {problem}")
    try:
        result={}
        result = make_answer(problem)
        logger.info(f"Result: {result}")
        answer_list.append([index,result])
    except Exception as e: 
        logger.error(f"Error: {e}")
        answer_list.append([index,"わからない(エラー)"])
for row in answer_list:
    print(f'{row[0]},"{row[1]}"')

logger.info("*** End answering questions ***")

#from email_notify import send_email
#send_email('Process Completed', 'Answered by prompty with semistructured store.', 'kazuyoshi.hayase@jcom.home.ne.jp')