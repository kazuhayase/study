from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from langchain.schema import ChatMessage, AIMessage, HumanMessage, SystemMessage

import chromadb
import os
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

# from llama_index.core import (
#         VectorStoreIndex,
#         load_index_from_storage,
# )
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.core import Settings

import tiktoken

#https://docs.llamaindex.ai/en/latest/community/integrations/using_with_langchain.html#
# from llama_index.core.langchain_helpers.agents import (
#     IndexToolConfig,
#     LlamaIndexTool,
# )

#from '../varlog' import varlog 

# uncomment if needs more than varlog
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

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent

from langchain_core.tools import Tool
from pydantic.v1 import BaseModel, Field # <-- Uses v1 namespace
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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
persistent_client=chromadb.PersistentClient(path=db_path)

kamoku=['hoken1_seiho', 'hoken2_seiho', 'sonpo', 'nenkin']
collection = dict()
db=dict()
retriever=dict()
for k in kamoku:
    logger.info(f"k={k}")
    collection[k] = persistent_client.get_or_create_collection(k)
    db[k] = Chroma(
        client = persistent_client,
        collection_name=k,
        embedding_function=embeddings,
        #persist_directory=db_path
    )
    retriever[k] = db[k].as_retriever()

# chroma_collection = db2.get_or_create_collection("hoken1_seiho")
# vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL, tiktoken_model_name="cl100k_base")
# index = VectorStoreIndex.from_vector_store(
#         vector_store,
#         embed_model = embed_model,
# )

# retriever = index.as_retriever(verbose=True)

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

    qa =RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=GPT_MODEL),
        chain_type="stuff",
        retriever=retriever[txt], ##todo:  txtが期待したものでなければException??
        chain_type_kwargs=chain_type_kwargs
    )
    tools = [
        Tool(
            name="vec_search",
            func=qa.run,
            description="vector search result with" + db_path
        ),
    ]
    e_key=os.environ.get('ELYZA_API_KEY')
    logger.info(f"ELYZA_API_KEY = {e_key}")
    e_url=os.environ.get('ELYZA_BASE_URL')
    logger.info(f"ELYZA_BASE_URL = {e_url}")
    e_endpoint=f"{e_url}/models/llama-3-elyza-japanese-70b/records"
    #e_endpoint=f"{e_url}/models/llama-3-elyza-japanese-70b"
    logger.info(f"e_endpoint = {e_endpoint}")

    chat_agent = initialize_agent(
        tools,
        #llm=ChatOpenAI(model_name=GPT_MODEL),
        #llm=Elyza(api_key=os.environ.get('ELYZA_API_KEY')),

        llm=Elyza(api_key=e_key, base_url=e_url, top_p=1, temperature=0.5),
        agent = "zero-shot-react-description",
        handle_parsing_errors=True,
        verbose=True,
        system_message="あなたは親切なアシスタントです。日本語で回答してください!",
    )
    result = chat_agent.run(question)
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

    
