import feedparser
from datetime import datetime

def fetch_rss_items(url, limit=10):
    feed = feedparser.parse(url)

    def get_published(entry):
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        return datetime.min

    # ★ 日付で新しい順にソート
    sorted_entries = sorted(
        feed.entries,
        key=get_published,
        reverse=True
    )

    items = []
    for entry in sorted_entries[:limit]:
        items.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", entry.get("description", "")),
            "link": entry.get("link", "")
        })

    return items