#!/usr/bin/env python3
"""
Fetch new RSS articles and GitHub releases with dedup against seen-items registry.

Usage:
    python scripts/fetch_new_rss.py                     # Fetch from all sources
    python scripts/fetch_new_rss.py --scout research     # Fetch only sources for a scout
    python scripts/fetch_new_rss.py --source rss/hpcwire # Fetch a specific source
    python scripts/fetch_new_rss.py -s rss/hpcwire repos/slurm-schedmd  # Fetch specific source keys
    python scripts/fetch_new_rss.py --limit 3            # Max articles per source
    python scripts/fetch_new_rss.py --health-check       # Only check source health, don't fetch

Output: JSON array of new articles to stdout.
Each article: {source, source_file, url, title, summary, published, author, content}

The seen-items registry is at workspace/memory/seen-items.jsonl.
Each line: {"url_hash": "...", "title_hash": "...", "url": "...", "title": "...",
             "first_seen": "...", "last_fetched": "...", "source": "...", "reported": false}

Articles are marked 'reported: false' at fetch time and only become 'reported: true'
after the weekly report is successfully saved (via scripts/mark_reported.py).
If the pipeline crashes mid-cycle, unreported items are re-fetched next cycle.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Project root is parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEEN_FILE = PROJECT_ROOT / "workspace" / "memory" / "seen-items.jsonl"
SOURCES_DIR = PROJECT_ROOT / "sources"

HEADERS = {
    "User-Agent": "nooz-hermes/1.0 (+https://github.com/nooz)"
}


def parse_source_file(path: Path) -> Optional[Dict]:
    """Parse a source .md file. Extract URL and description."""
    text = path.read_text().strip()
    
    # Find URL line
    url_match = re.search(r'URL:\s*(.+)', text)
    if not url_match:
        return None
    
    url = url_match.group(1).strip()
    
    # Find description
    desc_match = re.search(r'Description:\s*(.+)', text)
    description = desc_match.group(1).strip() if desc_match else ""
    
    # Determine source type from path
    source_type = path.parent.name  # "rss" or "repos"
    
    # Extract name from filename
    name = path.stem
    
    return {
        "name": name,
        "url": url,
        "description": description,
        "type": source_type,
        "source_key": f"{source_type}/{name}",
        "file_path": str(path),
    }


def load_all_sources() -> List[Dict]:
    """Load all source definitions from sources/rss/ and sources/repos/."""
    sources = []
    
    for subdir in ["rss", "repos"]:
        dir_path = SOURCES_DIR / subdir
        if not dir_path.exists():
            continue
        for md_file in sorted(dir_path.glob("*.md")):
            parsed = parse_source_file(md_file)
            if parsed:
                sources.append(parsed)
    
    return sources


def load_seen_items() -> Dict[str, dict]:
    """Load seen-items registry. Returns dict keyed by URL hash."""
    seen = {}
    if SEEN_FILE.exists():
        for line in SEEN_FILE.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                key = entry.get("url_hash") or entry.get("title_hash", "")
                seen[key] = entry
            except json.JSONDecodeError:
                continue
    return seen


def url_hash(url: str) -> str:
    """Create a hash for dedup. Normalize URL first."""
    # Remove tracking params
    url_clean = re.sub(r'[?&](utm_\w+|ref|source|campaign|medium)=', '', url)
    url_clean = url_clean.rstrip('/')
    return hashlib.sha256(url_clean.encode()).hexdigest()[:16]


def title_hash(title: str) -> str:
    """Hash title for secondary dedup."""
    normalized = re.sub(r'[^a-z0-9]', '', title.lower())[:200]
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def mark_seen(url: str, title: str, source: str, reported: bool = False):
    """Mark an article as seen by appending to the registry.

    Articles are marked 'reported: false' at fetch time. They only become
    'reported: true' after the weekly report is successfully saved
    (via scripts/mark_reported.py). If the pipeline crashes mid-cycle,
    unreported items will be re-fetched next cycle.
    """
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "url_hash": url_hash(url),
        "title_hash": title_hash(title),
        "url": url,
        "title": title[:200],
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "last_fetched": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "reported": reported,
    }
    
    with open(SEEN_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def is_seen(url: str, title: str, seen: Dict[str, dict]) -> bool:
    """Check if an article has been seen AND successfully reported.

    Articles from a previous cycle that were never reported (pipeline crashed)
    are NOT considered "seen" — they will be re-fetched so they don't get lost.
    """
    uh = url_hash(url)
    th = title_hash(title)
    
    for h in (uh, th):
        entry = seen.get(h)
        if entry and entry.get("reported", False):
            # Only skip if the article was previously reported in a completed cycle
            return True
    return False


def fetch_rss_feed(url: str, limit: int = 5) -> List[Dict]:
    """Fetch RSS feed entries."""
    try:
        import feedparser
    except ImportError:
        print(json.dumps({"error": "feedparser not installed. Run: pip install feedparser"}), file=sys.stderr)
        return []

    try:
        feed = feedparser.parse(url)
        entries = []
        
        for item in feed.entries[:limit]:
            entry = {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "summary": item.get("summary", "")[:500],
                "published": item.get("published", ""),
            }
            if hasattr(item, "author"):
                entry["author"] = item.author
            entries.append(entry)
        
        return entries
    except Exception as e:
        return [{"error": str(e)}]


def fetch_github_releases(url: str, limit: int = 3) -> List[Dict]:
    """Fetch GitHub releases from a releases URL or API."""
    # Convert github.com URL to API URL if needed
    # e.g. https://github.com/SchedMD/slurm/releases -> https://api.github.com/repos/SchedMD/slurm/releases
    api_url = url
    match = re.match(r'https?://github\.com/([^/]+)/([^/]+)', url)
    if match:
        owner, repo = match.group(1), match.group(2)
        repo = re.sub(r'\.git$', '', repo)
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    try:
        import requests
    except ImportError:
        print(json.dumps({"error": "requests not installed"}), file=sys.stderr)
        return []
    
    try:
        resp = requests.get(api_url, headers={
            **HEADERS,
            "Accept": "application/vnd.github+json"
        }, timeout=15)
        
        if resp.status_code != 200:
            return [{"error": f"HTTP {resp.status_code}"}]
        
        releases = resp.json()
        if not isinstance(releases, list):
            return []
        
        entries = []
        for rel in releases[:limit]:
            entries.append({
                "title": f"{rel.get('name', rel.get('tag_name', 'release'))}",
                "link": rel.get("html_url", url),
                "summary": (rel.get("body") or "")[:500],
                "published": rel.get("published_at", ""),
                "author": rel.get("author", {}).get("login", ""),
            })
        return entries
    except Exception as e:
        return [{"error": str(e)}]


def check_source_health(url: str) -> Dict:
    """Check if a source URL is healthy."""
    try:
        import requests
    except ImportError:
        return {"url": url, "is_active": False, "error": "requests not installed"}
    
    result = {
        "url": url,
        "is_active": False,
        "status_code": None,
        "response_time": None,
        "error": None,
        "checked_at": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        start = time.time()
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        result["response_time"] = round(time.time() - start, 2)
        result["status_code"] = response.status_code
        result["is_active"] = response.status_code == 200
    except Exception as e:
        result["error"] = str(e)[:200]
    
    return result


def fetch_source(source: Dict, limit: int, seen: Dict[str, dict]) -> List[Dict]:
    """Fetch new articles from a single source."""
    url = source["url"]
    source_key = source["source_key"]
    
    # Determine fetch method based on source type
    if source["type"] == "repos" or "github.com" in url:
        entries = fetch_github_releases(url, limit=limit)
    else:
        entries = fetch_rss_feed(url, limit=limit)
    
    new_articles = []
    
    for entry in entries:
        if "error" in entry:
            continue
        
        url = entry.get("link", "")
        title = entry.get("title", "")
        
        if not url or not title:
            continue
        
        if is_seen(url, title, seen):
            continue
        
        # Mark as seen (unreported — will become reported after report is saved)
        mark_seen(url, title, source_key, reported=False)
        
        new_articles.append({
            "source": source_key,
            "source_name": source["name"],
            "source_description": source["description"],
            "url": url,
            "title": title,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "author": entry.get("author", ""),
        })
    
    return new_articles


def main():
    parser = argparse.ArgumentParser(description="Fetch new RSS/GitHub articles with dedup")
    parser.add_argument("--scout", type=str, help="Fetch only sources for a specific scout")
    parser.add_argument("--source", type=str, help="Fetch a specific source (e.g., rss/hpcwire)")
    parser.add_argument("-s", "--sources", nargs="+", help="Fetch only matching source keys (space-separated)")
    parser.add_argument("--limit", type=int, default=5, help="Max articles per source")
    parser.add_argument("--health-check", action="store_true", help="Only check source health")
    args = parser.parse_args()
    
    all_sources = load_all_sources()
    seen = load_seen_items()
    all_keys = {s["source_key"] for s in all_sources}
    
    # Filter sources
    sources_to_fetch = all_sources
    
    if args.source:
        sources_to_fetch = [s for s in all_sources if s["source_key"] == args.source]
    elif args.sources:
        requested = []
        for key in args.sources:
            key = key.rstrip(",\s").strip()
            if not key:
                continue
            if key in all_keys:
                requested.append(key)
            else:
                print(f"Warning: unknown source key '{key}'", file=sys.stderr)
        sources_to_fetch = [s for s in all_sources if s["source_key"] in requested]
    elif args.scout:
        # Scout-based filtering could be added if scout skills list their sources
        # For now, fetch all — the scout subagent will filter by relevance
        pass
    
    # Health check mode
    if args.health_check:
        results = []
        for src in sources_to_fetch:
            health = check_source_health(src["url"])
            health["source"] = src["source_key"]
            health["name"] = src["name"]
            results.append(health)
        
        active = sum(1 for r in results if r["is_active"])
        print(json.dumps({
            "total": len(results),
            "active": active,
            "inactive": len(results) - active,
            "sources": results,
        }, indent=2))
        return
    
    # Fetch mode
    all_new_articles = []
    source_stats = []
    
    for src in sources_to_fetch:
        articles = fetch_source(src, args.limit, seen)
        all_new_articles.extend(articles)
        source_stats.append({
            "source": src["source_key"],
            "new_articles": len(articles),
        })
    
    output = {
        "fetch_time": datetime.now(timezone.utc).isoformat(),
        "total_sources": len(sources_to_fetch),
        "total_new_articles": len(all_new_articles),
        "source_stats": source_stats,
        "articles": all_new_articles,
    }
    
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
