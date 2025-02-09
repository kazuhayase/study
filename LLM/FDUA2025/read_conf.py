import logging.config
import os
import json
import requests
from langchain_openai import AzureChatOpenAI 
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.runnables import RunnableLambda

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def setup_logging(script_name, path='./conf/logging.json'):
    # スクリプト名からログファイル名を設定
    log_filename = f"./log/{script_name}.log"
    os.environ["log_filename"] = log_filename

    # ログ設定ファイルを読み込む
    config = load_config(path)

    # ファイルハンドラを追加
    file_handler = {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "filename": log_filename
    }
    config['handlers'][script_name] = file_handler
    config['loggers']['']['handlers'].append(script_name)

    # ログ設定を適用
    logging.config.dictConfig(config)

def get_retriever_conf(path='./conf/retriever.json'):
    # ログ設定ファイルを読み込む
    config = load_config(path)
    return config

def get_file_directry_conf(path='./conf/file_directory.json'):
    # ログ設定ファイルを読み込む
    config = load_config(path)
    return config
import json
import requests

def get_model(path='./conf/model.json'):
    config = load_config(path)
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
    DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")
    HITACHI_LLAMA_API_URL=os.getenv("HITACHI_LLAMA_API_URL")
    HITACHI_LLAMA_API_KEY=os.getenv("HITACHI_LLAMA_API_KEY")
    HITACHI_QWEN_API_URL=os.getenv("HITACHI_QWEN_API_URL")
    HITACHI_QWEN_API_KEY=os.getenv("HITACHI_QWEN_API_KEY")
    
    # LangChainのOpenAIモデルを作成
    models = {}
    
    models['summarize_azure_chat'] = AzureChatOpenAI(
        api_key=os.getenv(config['AzureOpenAI']['api_key']),
        azure_endpoint=os.getenv(config['AzureOpenAI']['azure_endpoint']),
        azure_deployment=os.getenv(config['SummarizeAzureChat']['deployment_id_for_chat_completion']),
        api_version=os.getenv(config['AzureOpenAI']['api_version']),
        temperature=0,
        max_tokens=3000
    )

    models['answer_azure_chat'] = AzureChatOpenAI(
        api_key=os.getenv(config['AzureOpenAI']['api_key']),
        azure_endpoint=os.getenv(config['AzureOpenAI']['azure_endpoint']),
        azure_deployment=os.getenv(config['AnswerAzureChat']['deployment_id_for_chat_completion']),
        api_version=os.getenv(config['AzureOpenAI']['api_version']),
        temperature=0,
        max_tokens=100
    )

    models['embeddings'] = AzureOpenAIEmbeddings(
        api_key=os.getenv(config['AzureOpenAI']['api_key']),
        azure_endpoint=os.getenv(config['AzureOpenAI']['azure_endpoint']),
        azure_deployment=os.getenv(config['AzureEmbedding']['deployment_id_for_embedding']),
        api_version=os.getenv(config['AzureOpenAI']['api_version']),
        model=config['AzureEmbedding']['model']
    )

    # 推論処理の関数化。引数の変数名はinputにする必要がある
    def inference_llama(input: str) -> str:

        # 呼び出し設定
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": HITACHI_LLAMA_API_KEY
        }    
        data = {
            "temperature": 0,
            "repeat_penalty": 1.0,
            "prompt": input.__dict__
        }
        response = requests.post(HITACHI_LLAMA_API_URL, headers=headers, data=json.dumps(data), verify=False)
        return response.json()

    models['answer_llama_chat'] = RunnableLambda(inference_llama)
    
 
    # 推論処理の関数化。引数の変数名はinputにする必要がある
    def inference_qwen(input: str) -> str:

        # 呼び出し設定
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": HITACHI_QWEN_API_KEY
        }    
        data = {
            "temperature": 0,
            "repeat_penalty": 1.0,
            "prompt": input.__dict__
        }
        response = requests.post(HITACHI_QWEN_API_URL, headers=headers, data=json.dumps(data), verify=False)
        return response.json()

    models['answer_qwen_chat'] = RunnableLambda(inference_qwen)
    
    return models