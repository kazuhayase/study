"""Summarize podcast transcript using mlx-lm (Apple MLX, local)."""

import os
from mlx_lm import load, generate

SUMMARY_PROMPT = """以下の形式で要約してください。

【概要】（2〜3文）

【主なトピック】
-

【重要なポイント】（3〜5点）
-

【キーワード・固有名詞】
"""

# 4-bit quantized, ~4GB, good Japanese support
DEFAULT_MODEL = "mlx-community/Qwen2.5-7B-Instruct-4bit"

_cache: dict = {}


def _get_model(model_name: str):
    if model_name not in _cache:
        print(f"モデルを読み込み中: {model_name}")
        _cache[model_name] = load(model_name)
    return _cache[model_name]


def summarize(title: str, podcast: str, transcript: str, model: str | None = None) -> str:
    model_name = model or os.environ.get("PODCAST_MODEL", DEFAULT_MODEL)
    mlx_model, tokenizer = _get_model(model_name)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes podcast episodes. Respond in Japanese.",
        },
        {
            "role": "user",
            "content": (
                f"Podcast: {podcast}\nEpisode: {title}\n\n"
                f"Transcript:\n{transcript}\n\n"
                f"{SUMMARY_PROMPT}"
            ),
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )
    response = generate(mlx_model, tokenizer, prompt=prompt, max_tokens=1500, verbose=False)
    return response
