from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain.schema import ChatMessage, AIMessage, HumanMessage, SystemMessage

import chromadb
import os
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
import tiktoken
import logging

logging.basicConfig(
    filename="../log/app.log",
    #stream=sys.stdout,
    level=logging.INFO, #ERROR, WARNING, INFO, DEBUG
    format="[%(process)d-%(thread)d]-%(asctime)s-[%(filename)s:%(lineno)d]-%(levelname)s-%(message)s",
    force=True)

from langchain_core.tools import Tool
from pydantic.v1 import BaseModel, Field # <-- Uses v1 namespace
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class ActQA(BaseModel):
    q: str = Field(default='営業保険料')
    a: str = Field(default='(No Answer)')


#GPT_MODEL = "gpt-3.5-turbo"
#GPT_MODEL = "gpt-4-1106-preview"
GPT_MODEL = "gpt-4-turbo-preview"
EMBEDDING_MODEL = 'text-embedding-3-small'
#EMBEDDING_MODEL = 'text-embedding-3-large'
#EMBEDDING_MODEL = 'text-embedding-ada-002'


embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL,tiktoken_model_name="cl100k_base")

db_dir='../db/'
db_path = f"{db_dir}/chroma_{''.join(name[0] for name in EMBEDDING_MODEL.split('-'))}"

# load from disk
logging.info(f'db_path={db_path}')
db = Chroma(
    embedding_function=embeddings,
    persist_directory=db_path
)
retriever = db.as_retriever()

def ret_kw(kw):
    keyword = kw

    retrieval_query = keyword + "に関わる箇所を抽出してください。"

    # context_docs = retriever.get_relevant_documents(retrieval_query)
    # logging.info(f'len(context_docs)={len(context_docs)}')  # 抽出したドキュメント数
    # #logging.info(f'type(context_docs)={type(context_docs)}')  # 抽出したドキュメントの型
    # #logging.info(f'context_docs={context_docs}')  # 抽出したドキュメント
    # ## Document(page_content"XXXX", metadata={'source': '/xxxx/'})

    question = keyword + "に関わる箇所を1つ選択して100字程度に要約してください。"

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

    logging.info(f"retrieval_query = {retrieval_query}")
    logging.info(f"question = {question}")
    logging.info(f"prompt_qa = {prompt_qa}")
    logging.info(f"chain_type_kwargs = {chain_type_kwargs}")

    qa =RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=GPT_MODEL),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs
    )
    tools = [
        Tool(
            name="vec_search",
            func=qa.run,
            description="vector search result with" + db_path
        ),
    ]
    chat_agent = initialize_agent(
        tools,
        llm=ChatOpenAI(model_name=GPT_MODEL),
        agent = "zero-shot-react-description",
        verbose=True,
        system_message="あなたは親切なアシスタントです。日本語で回答してください!",
    )
    result = chat_agent.run(question)
    logging.info(f'result={result}')
    logging.info(f'type(result)={type(result)}')
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
@app.get("/kw/{kw}", response_model=list)
#@app.get("/kw/{kw}", response_model=dict)
async def QandA(kw: str) -> ActQA: 
    '''
	retrieve from vector store with keyword
    '''
    #    logging.info(f'before call ret_kw')
    #return ActQA(q=kw, a=ret_kw(kw))
    return JSONResponse(content=jsonable_encoder(ActQA(q=kw, a=ret_kw(kw))))

    
