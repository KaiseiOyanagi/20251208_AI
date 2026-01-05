from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rss_fetcher import fetch_rss_items
from gemini_client import generate_tags
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CATEGORIES = {
    "game": "https://www.gamespark.jp/rss/index.rdf",
    "sports": "https://www3.nhk.or.jp/rss/news/cat7.xml",
    "music": "https://natalie.mu/music/feed/news"
}

@app.get("/categories")
def get_categories():
    return list(CATEGORIES.keys())

@app.get("/news")
def get_news(category: str):
    rss_url = CATEGORIES.get(category)
    if not rss_url:
        return []

    items = fetch_rss_items(rss_url, limit=10)
    results = []

    for item in items:
        tags = generate_tags(item["title"], item["summary"])

        results.append({
            "title": item["title"],
            "summary": item["summary"],
            "link": item["link"],
            "tags": tags
        })

    return results