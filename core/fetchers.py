import feedparser
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time


HEADERS = {
    "User-Agent": "hpc-swarm/0.1"
}


def check_source_health(url: str) -> Dict:
    """Check if a source URL is healthy and accessible."""
    result = {
        "url": url,
        "is_active": False,
        "status_code": None,
        "response_time": None,
        "error": None,
        "checked_at": datetime.utcnow().isoformat()
    }

    try:
        start = time.time()
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        result["response_time"] = time.time() - start
        result["status_code"] = response.status_code
        result["is_active"] = response.status_code == 200
    except requests.exceptions.Timeout:
        result["error"] = "Timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error"
    except requests.exceptions.HTTPError as e:
        result["error"] = f"HTTP {e.response.status_code}"
    except Exception as e:
        result["error"] = str(e)

    return result


def fetch_rss(url: str, limit: int = 10) -> List[Dict]:
    """Fetch RSS feed with enhanced metadata."""
    feed = feedparser.parse(url)

    entries = []

    for item in feed.entries[:limit]:
        entry = {
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "summary": item.get("summary", ""),
            "published": item.get("published", ""),
            "published_parsed": item.get("published_parsed"),
        }

        if hasattr(item, "id"):
            entry["id"] = item.id
        if hasattr(item, "author"):
            entry["author"] = item.author
        if hasattr(item, "source"):
            entry["source_name"] = item.source
        if hasattr(item, "links"):
            for link in item.links:
                if link.get("rel") == "alternate":
                    entry["alternate_url"] = link.get("href", "")
                    break

        entries.append(entry)

    return entries


def fetch_url(url: str, timeout: int = 20) -> Tuple[Optional[str], Optional[Dict]]:
    """Fetch URL content with metadata. Returns (content, metadata) tuple."""
    metadata = {
        "url": url,
        "status_code": None,
        "content_type": None,
        "fetched_at": datetime.utcnow().isoformat()
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()

        metadata["status_code"] = response.status_code
        metadata["content_type"] = response.headers.get("Content-Type", "")

        return response.text, metadata
    except requests.exceptions.Timeout:
        metadata["error"] = "Timeout"
    except requests.exceptions.ConnectionError:
        metadata["error"] = "Connection error"
    except requests.exceptions.HTTPError as e:
        metadata["error"] = f"HTTP {e.response.status_code}"
    except Exception as e:
        metadata["error"] = str(e)

    return None, metadata


def fetch_with_trafilatura(url: str) -> Tuple[Optional[str], Optional[Dict]]:
    """Fetch URL and extract main content using trafilatura."""
    try:
        from trafilatura import fetch_url, extract
    except ImportError:
        return fetch_url(url)

    try:
        downloaded = fetch_url(url)
        if downloaded:
            text = extract(downloaded)
            return text, {"url": url, "extracted": True}
    except Exception:
        pass

    return None, {"url": url, "extracted": False}


RSS_FEEDS = {
    "hpcwire": {
        "url": "https://www.hpcwire.com/feed/",
        "topics": ["hpc", "cluster", "supercomputing"],
        "credibility": 0.85
    },
    "nextplatform": {
        "url": "https://www.nextplatform.com/feed/",
        "topics": ["hpc", "ai", "cloud", "infrastructure"],
        "credibility": 0.85
    },
    "phoronix": {
        "url": "https://www.phoronix.com/rss.php",
        "topics": ["linux", "benchmarks", "hardware", "hpc"],
        "credibility": 0.75
    },
    "lwn": {
        "url": "https://lwn.net/headlines/rss",
        "topics": ["linux", "kernel", "open-source"],
        "credibility": 0.80
    },
    "anandtech": {
        "url": "https://www.anandtech.com/rss",
        "topics": ["hardware", "cpus", "gpus", "reviews"],
        "credibility": 0.80
    },
}


def get_feed_metadata(key: str) -> Optional[Dict]:
    """Get metadata for a configured feed."""
    return RSS_FEEDS.get(key)


def list_all_feeds() -> List[Dict]:
    """List all configured RSS feeds with metadata."""
    return [
        {"key": key, **data}
        for key, data in RSS_FEEDS.items()
    ]