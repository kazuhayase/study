"""Summarize podcast transcript using Claude API."""

import anthropic

SUMMARY_PROMPT = """以下の形式で要約してください。

【概要】（2〜3文）

【主なトピック】
-

【重要なポイント】（3〜5点）
-

【キーワード・固有名詞】
"""

MODEL = "claude-sonnet-4-6"


def summarize(title: str, podcast: str, transcript: str) -> str:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system="You are a helpful assistant that summarizes podcast episodes. Respond in Japanese.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Podcast: {podcast}\nEpisode: {title}\n\nTranscript:\n{transcript}",
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": SUMMARY_PROMPT,
                    },
                ],
            }
        ],
    )
    return response.content[0].text
