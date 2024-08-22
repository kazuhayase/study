from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from langchain.schema import ChatMessage, AIMessage, HumanMessage, SystemMessage

from chromadb import PersistentClient 
from chromadb import HttpClient

import os
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

import tiktoken


#from logging import getLogger #, StreamHandler, DEBUG, Formatter
import logging

logger = logging.getLogger(__name__)
uv_logger = logging.getLogger('uvicorn') ## fast api
lc_logger = logging.getLogger('langchain') 
httpx_logger = logging.getLogger('httpx') 

# ログ出力先を設定（標準出力）
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
uv_logger.addHandler(stream_handler)
lc_logger.addHandler(stream_handler)
httpx_logger.addHandler(stream_handler)

# ログ出力のフォーマットを設定
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)
uv_logger.setLevel(logging.INFO)
lc_logger.setLevel(logging.INFO)
httpx_logger.setLevel(logging.INFO)

#https://api.python.langchain.com/en/latest/chains/langchain.chains.retrieval_qa.base.RetrievalQA.html#langchain.chains.retrieval_qa.base.RetrievalQA
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent

from langchain_core.tools import Tool
from pydantic.v1 import BaseModel, Field # <-- Uses v1 namespace
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

from da_elyza import Elyza

from langchain.globals import set_debug
set_debug(True)

class ActQA(BaseModel):
    q: str = Field(default='営業保険料')
    a: str = Field(default='(No Answer)')


#GPT_MODEL = "gpt-3.5-turbo"
#GPT_MODEL = "gpt-4-1106-preview"
GPT_MODEL = "gpt-4-turbo-preview"
GPT_MODEL = "gpt-4o"
EMBEDDING_MODEL = 'text-embedding-3-small'
#EMBEDDING_MODEL = 'text-embedding-3-large'
#EMBEDDING_MODEL = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL,tiktoken_model_name="cl100k_base")

# load from disk
db_dir='../db_llama/'
db_path = f"{db_dir}/chroma_{''.join(name[0] for name in EMBEDDING_MODEL.split('-'))}"

client = PersistentClient(path=db_path)
#client = HttpClient(host='localhost', port=10000)
# collection = client.get_or_create_collection(
#     name="digital_agency_standard_guidelines",
#     embedding_function=ef
# )

kamoku=['hoken1_seiho', 'hoken2_seiho', 'sonpo', 'nenkin', 'digital_agency_standard_guidelines']
#collection = dict()
db=dict()
retriever=dict()
ef = embedding_functions.OpenAIEmbeddingFunction( model_name=EMBEDDING_MODEL, api_key=os.getenv('OPENAI_API_KEY') )
for k in kamoku:
    logger.info(f"k={k}")
#    collection[k] = client.get_or_create_collection(name=k, embedding_function=ef)
#    retriever[k] = collection[k].as_retriever()
    db[k] = Chroma(
         client = client,
         collection_name=k,
         embedding_function=embeddings,
         #persist_directory=db_path
    )
    retriever[k] = db[k].as_retriever()

import re

def ret_kw(kw,txt='hoken1_seiho'):
    keyword = kw
    textbook = txt
    logger.info(f'keyword={keyword}, textbook={textbook}')

    # retrieval_query = keyword + "に関わる箇所を抽出してください。"

    # context_docs = retriever.get_relevant_documents(retrieval_query)
    # logging.info(f'len(context_docs)={len(context_docs)}')  # 抽出したドキュメント数
    # #logging.info(f'type(context_docs)={type(context_docs)}')  # 抽出したドキュメントの型
    # #logging.info(f'context_docs={context_docs}')  # 抽出したドキュメント
    # ## Document(page_content"XXXX", metadata={'source': '/xxxx/'})

    # question = keyword + "に関わる箇所を1つ選択して100字程度に要約してください。"
    question = keyword + "について、100字程度に要約して教えてください。"

    prompt_template_qa = """あなたは親切で優しいアシスタントです。丁寧に、日本語でお答えください！
    もし以下の情報が探している情報に関連していない場合は、そのトピックに関する自身の知識を用いて質問
    に答えてください。

    {context}

    質問: {question}
    回答（日本語）:"""

    prompt_qa = PromptTemplate(
        template=prompt_template_qa,
        input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": prompt_qa}

    # logger.info(f"retrieval_query = {retrieval_query}")
    logger.info(f"question = {question}")
    logger.info(f"prompt_qa = {prompt_qa}")
    logger.info(f"chain_type_kwargs = {chain_type_kwargs}")

    e_key=os.environ.get('ELYZA_API_KEY')
    e_url=os.environ.get('ELYZA_BASE_URL')
    logger.info(f"ELYZA_BASE_URL = {e_url}")
    e_endpoint=f"{e_url}/models/llama-3-elyza-japanese-70b/records"
    logger.info(f"e_endpoint = {e_endpoint}")


    qa =RetrievalQA.from_chain_type(
        llm=Elyza(api_key=e_key, base_url=e_url, top_p=1, temperature=0.5),
        #llm=ChatOpenAI(model_name=GPT_MODEL),
        chain_type="stuff",
        retriever=retriever[txt], ##todo:  txtが期待したものでなければException??
        chain_type_kwargs=chain_type_kwargs
    )
    tools = [
        Tool(
            name="vec_search",
            func=qa.run,
            #description="vector search result with" + db_path
            description="vector search" 
        ),
        Tool(
            name="wikipedia",
            func=wikipedia.run,
            description="wikipedia"
        ),
    ]
    chat_agent = initialize_agent(
        tools,
        #llm=ChatOpenAI(model_name=GPT_MODEL),
        #llm=Elyza(api_key=os.environ.get('ELYZA_API_KEY')),

        llm=Elyza(api_key=e_key, base_url=e_url, top_p=1, temperature=0.5),

        #https://github.com/langchain-ai/langchain/issues/1559
        agent = "zero-shot-react-description",
        #agent = "chat-zero-shot-react-description",

        handle_parsing_errors=True,
        verbose=True,
        system_message="あなたは親切なアシスタントです。日本語で回答してください!",
    )
    #result = chat_agent.run(question)


    #siwtch back to old style chain
    elyza_regex = re.compile(r'回答（日本語）:(.*)$')
    result = elyza_regex.search(qa.run(question)).group(1)

    logger.info(f'result={result}')
    logger.info(f'type(result)={type(result)}')
#    return ActQA(q=kw, a=result)
    return result
    
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## todo: response_model の設定とJSON; Done
#@app.get("/kw/{kw}", response_model=ChatMessage)
#@app.get("/kw/{kw}", response_model=ActQA)
#@app.get("/kw/{kw}")
#@app.get("/kw/{kw}", response_model=dict)
@app.get("/kw/", response_model=list)
async def QandA(kw: str, txt: str = 'hoken1_seiho') -> ActQA: 
    '''
	retrieve from vector store with keyword
    '''
    #    logger.info(f'before call ret_kw')
    #return ActQA(q=kw, a=ret_kw(kw))
    if txt not in kamoku:
        txt = 'hoken1_seiho'
    return JSONResponse(content=jsonable_encoder(ActQA(q=kw, a=ret_kw(kw,txt))))

    
