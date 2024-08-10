from langchain_openai import OpenAI
#from langchain.llms import OpenAI
import httpx

class Elyza(OpenAI):
    def __init__(self, api_key, base_url, **kwargs):
        super().__init__(api_key=api_key, base_url=base_url, **kwargs)
        #self.endpoint_url = endpoint_url
        #self._endpoint = endpoint_url

"""
    def _call(self, prompt, stop=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stop": stop
        }
        response = httpx.post(self.endpoint_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]
    
    def _send_request(self, url, headers, data):
        # リクエスト情報をログに出力
        logger.info(f"LLM Request: url={url}, headers={headers}, data={data}")
        response = requests.post(url, headers=headers, data=data)
        return response
    def _post(self, url, data, headers):
        # リクエスト情報をログに出力
        logger.info(f"LLM Request: url={url}, headers={headers}, data={data}")
        return super(). _post(url, data, headers)

    def _request(self, url, method, data, headers):
        # リクエスト情報をログに出力
        logger.info(f"LLM Request: url={url}, method={method}, headers={headers}, data={data}")
        return super()._request(url, method, data, headers)    
    @property
    def _endpoint(self) -> str:
        #return f"{OPENAI_BASE_URL}/models/llama-3-elyza-japanese-70b/records"
        return f"{ELYZA_BASE_URL}/models/llama-3-elyza-japanese-70b/records"
"""
