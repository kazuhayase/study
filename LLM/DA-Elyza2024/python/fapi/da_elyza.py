from langchain_openai import OpenAI
class Elyza(OpenAI):
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
