from openai import OpenAI
import time

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # ダミーで可
)

models = [
    "deepseek-r1:32b",
    "gemma3:27b", 
    "qwen3:32b",
    "mistral:7b",
    "llama3.2:3b"
]

prompt = "日本の四季について200字以内で教えて"

for model in models:
    print(f"\n{'='*40}")
    print(f"モデル: {model}")
    print('='*40)
    
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    elapsed = time.time() - start
    
    print(response.choices[0].message.content)
    print(f"\n⏱ 応答時間: {elapsed:.1f}秒")