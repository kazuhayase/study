from langchain_openai import OpenAI
class Elyza(OpenAI):
    @property
    def _endpoint(self) -> str:
        #return f"{OPENAI_BASE_URL}/models/llama-3-elyza-japanese-70b/records"
        return f"{ELYZA_BASE_URL}/models/llama-3-elyza-japanese-70b/records"
