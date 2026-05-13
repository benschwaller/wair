import feedparser
import requests


HEADERS = {
    "User-Agent": "hpc-swarm/0.1"
}


def fetch_rss(url, limit=10):
    feed = feedparser.parse(url)

    entries = []

    for item in feed.entries[:limit]:
        entries.append(
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "summary": item.get("summary", ""),
            }
        )

    return entries


def fetch_url(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    return response.text