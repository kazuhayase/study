#!/usr/bin/env python
# coding: utf-8

# 環境変数の準備
import os
import logging

#import sys
#todo logger設定の高度化
#https://kewton.blog/archives/1350
logging.basicConfig(
    filename="log/app.log",
    #stream=sys.stdout,
    level=logging.INFO, #ERROR, WARNING, INFO, DEBUG
    format="[%(process)d-%(thread)d]-%(asctime)s-[%(filename)s:%(lineno)d]-%(levelname)s-%(message)s",
    force=True)

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
import tiktoken
import chromadb
#import datetime

## Deprecated
#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain_community.embeddings.openai import OpenAIEmbeddings
#from langchain.chat_models import ChatOpenAI
#from langchain.document_loaders import PyPDFLoader
#from langchain.document_loaders import TextLoader
#from langchain.vectorstores import Chroma
#from langchain import PromptTemplate


def _input(prompt):
    print(prompt, end='', flush=True)
    #s = sys.stdin.buffer.readline()
    s = input()
    s = s.replace("\r", "") \
         .replace("\n", "")
    return s

# 公式のExampleを参考にしたプロンプト組み立て関数
def make_prompt(log):
    prompt = [
        f"{uttr['speaker']}: {uttr['text']}"
        for uttr in log
    ]
    prompt = "<NL>".join(prompt)
    return prompt

# 対話については辞書で持っておくようにする
def add_log(log, role, text):
    log.append({
        "speaker": role,
        "text": text
    })

# https://qiita.com/Isaka-code/items/f45a9a8288710aa807d9
# 【2023年12月最新】LangChainを用いてPDFから演習問題を抽出する方法【RAG】
## メインの処理
if __name__ == "__main__":

    #file_path = "hoken1-ch1.txt"
    #file_path = "/content/drive/MyDrive/simple.txt"
    #file_path = "/content/drive/MyDrive/Actuary/eBooks/hoken1-ch1.txt"
    ###file_path = "/content/drive/MyDrive/Actuary/eBooks/hoken1.txt"
    #file_path = "/home/kazu/Books/Actuary-ebook/hoken1.txt" ## Ubuntu@lavie
    file_path = "/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1.txt" ## Ubuntu@home

    # 1. PDFを読み込む
    #todo PDF読み込みはPyPDFではエラーになる。javascriptは読み込めた（はず）が、処理がうまくいかなかったので、テキストに変換して処理している。
    #pages = PyPDFLoader(file_path).load()
    pages = TextLoader(file_path).load()

    # 2. ドキュメントをチャンクに分割
    #docs = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0).split_documents(pages)
    docs = CharacterTextSplitter().split_documents(pages)
    logging.info(f"#docs = {len(docs)}") # 抽出したドキュメントの数

    # 3. 埋め込みモデルの初期化
    ### open ai の embeddingがupgrade
    #https://platform.openai.com/docs/guides/embeddings/embedding-models
    #text-embedding-ada-002 -> text-embedding-3-{small,large}

    # models
    #todo 3.5-turboではtoken数が超過するというエラーを回避する必要がある。
    #GPT_MODEL = "gpt-3.5-turbo"
    #GPT_MODEL = "gpt-4-1106-preview"
    GPT_MODEL = "gpt-4-turbo-preview"
    #EMBEDDING_MODEL = 'text-embedding-ada-002'
    EMBEDDING_MODEL = 'text-embedding-3-small'
    #EMBEDDING_MODEL = 'text-embedding-3-large'

    logging.info(f"GPT_MODEL = {GPT_MODEL}")
    logging.info(f"EMBEDDING_MODEL = {EMBEDDING_MODEL}")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL,tiktoken_model_name="cl100k_base")
    #embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    ### todo; 他のEmbeddingも検証してみたい

    # https://qiita.com/akeyhero/items/ce371bfed64399027c23
    # https://huggingface.co/intfloat/multilingual-e5-large
    # https://huggingface.co/Cohere/Cohere-embed-multilingual-v3.0


    # 4. ベクトルストアにドキュメントを格納
    # todo ChromaDB 永続化
    db_path = "db/chroma_{''.join(name[0] for name in EMBEDDING_MODEL.split('-'))}"
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name=os.path.basename(file_path), embedding_function=embeddings)
    collection.add(docs)
    retriever = Chroma.from_documents(docs, embeddings).as_retriever()

    while "[exit]" not in (keyword := _input("\n保険1教科書第1章から、箇所を特定するキーワードを入力してください（例；営業保険料）。終了は[exit]。\n> ")):
      retrieval_query = keyword + "に関わる箇所を抽出してください。"
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

      # 5. ドキュメントを抽出
      context_docs = retriever.get_relevant_documents(retrieval_query)
      logging.info(f"#context_docs = {len(context_docs)}") # 抽出したドキュメントの数
      encoding = tiktoken.encoding_for_model(GPT_MODEL)
      str_docs=''
      for doc in context_docs:
        str_docs = ' '.join(doc.page_content)
      logging.info(f"#tokens_context_docs = {len(encoding.encode(str_docs))}") # 抽出したドキュメントのtoken数

      ###pythonだとmetadataはsource(ファイル名)のみで詳細箇所が不明なため、以下のログは意味なし
      #for i in range(len(context_docs)):
        #current_doc = context_docs[i] # i[0..len-1] のドキュメント
        #logging.info(f"i = {i}")
        #logging.info(f"metadata = {current_doc.metadata}") # ドキュメントのメタデータ
        #logging.info(current_doc.page_content) # ドキュメントの中身

      # 6. QAチェーンの初期化・エージェント化
      print('\n***エージェントが要約を実行***')
      #https://qiita.com/mashmoeiar11/items/214984400e3452615ea5
      # RetrievalQAの引数やAgent化
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
              description="vector search result with" + file_path
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
      print(result)
