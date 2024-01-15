### https://note.com/npaka/n/n0fd7bd3ed27b
### LangChain クイックスタートガイド - Python版
# パッケージのインストール
# !pip install langchain #==0.0.329
# !pip install openai
# 環境変数の準備
import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain.llms import OpenAI

# LLMの準備
llm = OpenAI(temperature=0.9)

# LLMの呼び出し
print(llm.predict("コンピュータゲームを作る日本語の新会社名をを1つ提案してください。"))
