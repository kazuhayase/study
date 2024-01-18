### https://note.com/npaka/n/n0fd7bd3ed27b
### LangChain クイックスタートガイド - Python版
# パッケージのインストール
# !pip install langchain #==0.0.329
# !pip install openai
# 環境変数の準備
import os

# set in ~/.profile or other files
#os.environ["OPENAI_API_KEY"] = "XXXXX"

# from langchain.llms import OpenAI

# # LLMの準備
# llm = OpenAI(temperature=0.9)

# # LLMの呼び出し
# print(llm.predict("コンピュータゲームを作る日本語の新会社名をを1つ提案してください。"))

# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage

# # ChatModelの準備
# chat_model = ChatOpenAI(temperature=0.9)

# # ChatModelの呼び出し
# messages = [HumanMessage(content="コンピュータゲームを作る日本語の新会社名をを1つ提案してください。")]
# print(chat_model.predict_messages(messages))

# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # PromptTemplateの準備
# template="{product}を作る日本語の新会社名をを1つ提案してください。"
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template=template,
# )

# # プロンプトの生成
# print(prompt.format(product="家庭用ロボット"))

# from langchain.schema import BaseOutputParser

# # OutputParserの準備
# class CommaSeparatedListOutputParser(BaseOutputParser):
#     def parse(self, text: str):
#         return text.strip().split(", ")

# # LLMの出力のパース
# print(
#     CommaSeparatedListOutputParser().parse("A, B, C")
# )

###5-1. Chain Interface

# from langchain.chains import LLMChain
# #from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate

# # LanguageModelの準備
# chat_model = ChatOpenAI(temperature=0.9)

# # PromptTemplateの準備
# template="""{product}を作る日本語の新会社名をを5つ提案してください。
# カンマ区切りのリストだけを返してください。"""
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template=template,
# )

# # Chainの準備
# chain = LLMChain(llm=chat_model, prompt=prompt)
# print(
#     chain.invoke({"product": "メタバース"})
# )

# # さらに、「Output Parser」を使って「list」で返してもらいます。

# from langchain.chains import LLMChain
# #from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.schema import BaseOutputParser

# # OutputParserの準備
# class CommaSeparatedListOutputParser(BaseOutputParser):
#     def parse(self, text: str):
#         return text.strip().split(", ")

# # LanguageModelの準備
# chat_model = ChatOpenAI(temperature=0.9)

# # PromptTemplateの準備
# template="""{product}を作る日本語の新会社名をを5つ提案してください。
# カンマ区切りのリストだけを返してください。"""
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template=template,
#     output_parser=CommaSeparatedListOutputParser(),
# )

# # Chainの準備
# chain = LLMChain(llm=chat_model, prompt=prompt)
# response = chain.invoke({"product": "メタバース"})

# # LLMの出力のパース
# print(
#     CommaSeparatedListOutputParser().parse(response["text"])
# )

# # 5-2. LCEL (LangChain Expression Language)
# from langchain.prompts import PromptTemplate
# # from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI

# # LanguageModelの準備
# chat_model = ChatOpenAI(temperature=0.9)

# # PromptTemplateの準備
# template="""{product}を作る日本語の新会社名をを5つ提案してください。
# カンマ区切りのリストだけを返してください。"""
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template=template,
# )

# # Chainの準備
# chain = prompt | chat_model
# print(
#     chain.invoke({"product": "メタバース"})
# )

###6. Agent
# 環境変数の準備
import os
#os.environ["SERPAPI_API_KEY"] = "XXXXX"

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import create_react_agent
from langchain.agents import create_json_agent
from langchain.agents import create_structured_chat_agent
from langchain.agents import load_tools
#from langchain.llms import OpenAI
from langchain_openai import OpenAI

# LanguageModelの準備
llm_model = OpenAI(temperature=0)

# Toolの準備
tools = load_tools(["serpapi", "llm-math"], llm=llm_model)

# Agentの準備

agent_executor = initialize_agent(
#agent_executor = create_react_agent( 
#agent_executor = create_json_agent( 
#agent_executor = create_structured_chat_agent(
    tools=tools,
    llm=llm_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
# Agentの実行
#agent_executor.invoke({"input": "富士山の高さは？それに2を掛けると？"})
# Agentの実行
agent_executor.run({"input": "ぼっち・ざ・ろっく!の作者の名前は？"})
