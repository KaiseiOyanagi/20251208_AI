import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


def generate_tags(title: str, summary: str):
    if not API_KEY:
        return ["タグ未生成"]

    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
以下は日本語のニュース記事です。
内容を表す日本語タグを3つ生成してください。
タグのみを「,」区切りで出力してください。

タイトル: {title}
要約: {summary}
"""
            }]
        }]
    }

    try:
        response = requests.post(
            f"{URL}?key={API_KEY}",
            json=payload,
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]

        tags = [t.strip() for t in text.split(",") if t.strip()]
        return tags[:3] if tags else ["タグ生成失敗"]

    except Exception as e:
        print("Gemini REST error:", e)
        return ["タグ生成失敗"]