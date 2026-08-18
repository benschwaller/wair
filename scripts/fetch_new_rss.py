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
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# Project root is parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEEN_FILE = PROJECT_ROOT / "workspace" / "memory" / "seen-items.jsonl"
SOURCES_DIR = PROJECT_ROOT / "sources"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) nooz-hermes/1.0 (+https://github.com/nooz)"
}


def parse_source_file(path: Path) -> Optional[Dict]:
    """Parse a source .md file. Extract URL, description, and optional type override.

    The `type:` field is optional and overrides the directory-based type.
    Supported values: "rss" (default for sources/rss/), "repos" (default for
    sources/repos/), "html" (treat the URL as an HTML listing page to scrape
    via trafilatura — used for vendor newsrooms that publish no RSS feed).
    """
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
    dir_type = path.parent.name  # "rss" or "repos"
    
    # Optional type override (e.g. type: html for scrape sources)
    type_match = re.search(r'^Type:\s*(\S+)', text, re.MULTILINE)
    source_type = type_match.group(1).strip().lower() if type_match else dir_type
    
    # Extract name from filename
    name = path.stem
    
    return {
        "name": name,
        "url": url,
        "description": description,
        "type": source_type,
        "source_key": f"{dir_type}/{name}",
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
                "summary": item.get("summary", "")[:5000],
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


def fetch_json_api(url: str, limit: int = 5) -> List[Dict]:
    """Fetch articles from a JSON API endpoint.

    Generic handler for vendor APIs that return a JSON object with an `items`
    (or `results`/`data`) array. Each item is expected to have some
    combination of `title`, `link`/`url`/`cta.link`, `contentDate`/`date`/
    `published`, and `description`/`summary`/`text` fields. Used for vendors
    like HPE whose newsroom is a JS app backed by a JSON API.
    """
    try:
        import requests
    except ImportError:
        return [{"error": "requests not installed"}]
    
    ua = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) nooz-hermes/1.0 (+https://github.com/nooz)",
        "Accept": "application/json",
    }
    
    try:
        resp = requests.get(url, headers=ua, timeout=30, allow_redirects=True)
    except Exception as e:
        return [{"error": f"fetch error: {e}"}]
    
    if resp.status_code != 200:
        return [{"error": f"HTTP {resp.status_code}"}]
    
    try:
        data = resp.json()
    except Exception as e:
        return [{"error": f"JSON parse error: {e}"}]
    
    # Find the items array — check common keys
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("items", "results", "data", "articles", "posts"):
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
        if not items:
            # Maybe the dict itself is a single article
            items = [data]
    
    entries = []
    for item in items[:limit]:
        if not isinstance(item, dict):
            continue
        # Try common field names, including nested cta.link (HPE's format)
        title = (
            item.get("title")
            or (item.get("cta", {}) or {}).get("text")
            or item.get("name")
            or ""
        )
        link = (
            item.get("link")
            or item.get("url")
            or (item.get("cta", {}) or {}).get("link")
            or item.get("href")
            or ""
        )
        published = (
            item.get("contentDate")
            or item.get("date")
            or item.get("published")
            or item.get("published_at")
            or ""
        )
        summary = (
            item.get("description")
            or item.get("summary")
            or item.get("text")
            or item.get("body")
            or ""
        )
        # HPE nests a description under image.text sometimes
        if not summary and isinstance(item.get("image"), dict):
            summary = item["image"].get("text", "")
        summary = summary[:5000] if summary else ""
        if title and link:
            entries.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "author": "",
            })
    
    return entries


def fetch_html_page(url: str, source_key: str, limit: int = 5) -> List[Dict]:
    """Scrape an HTML listing page (e.g. a vendor newsroom with no RSS feed).

    Strategy: use trafilatura to extract the main content (which naturally
    excludes navigation/boilerplate), then pull article links from the
    extracted markdown. Each discovered article URL is fetched and extracted
    individually. Falls back to a regex scan of raw hrefs if trafilatura
    finds no links in the extracted content.

    This is content-aware: no hardcoded URL patterns or nav-slug blocklists.
    """
    _ = source_key  # reserved for future per-source tuning (e.g. link XPath)
    try:
        import requests
        import trafilatura
    except ImportError as e:
        return [{"error": f"{e.name} not installed"}]
    
    ua = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) nooz-hermes/1.0 (+https://github.com/nooz)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    try:
        resp = requests.get(url, headers=ua, timeout=25, allow_redirects=True)
    except Exception as e:
        return [{"error": f"fetch error: {e}"}]
    
    if resp.status_code != 200:
        return [{"error": f"HTTP {resp.status_code}"}]
    
    html = resp.text
    final_url = resp.url
    from urllib.parse import urljoin, urlsplit
    
    # Primary: trafilatura extracts main content (excludes nav/boilerplate)
    # and emits markdown links [label](href) for in-content links.
    candidates = []
    try:
        doc = trafilatura.bare_extraction(
            html, include_links=True, include_tables=True
        )
        if doc:
            text = (doc.as_dict().get("text") if hasattr(doc, "as_dict") else "") or ""
            # Markdown links: [label](href)
            md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
            for label, href in md_links:
                if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                    continue
                absolute = urljoin(final_url, href)
                p = urlsplit(absolute)
                absolute = p._replace(query='', fragment='').geturl()
                candidates.append((label, absolute))
    except Exception:
        pass
    
    # Fallback: if trafilatura found no links, scan raw hrefs for article-like
    # paths. This is less precise but catches cases where the listing page is
    # mostly links with little body text.
    if not candidates:
        article_patterns = [
            r'/pressreleases?/[^/?#]+',
            r'/press-releases?/[^/?#]+',
            r'/newsroom/[^/?#]+/[^/?#]+/?$',
            r'/news/[^/?#]+/?$',
            r'/announcement/[^/?#]+',
            r'/blog/[^/?#]+/?$',
        ]
        combined = re.compile('|'.join(f'({p})' for p in article_patterns))
        href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        for m in href_re.finditer(html):
            href = m.group(1)
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                continue
            if not combined.search(href):
                continue
            absolute = urljoin(final_url, href)
            p = urlsplit(absolute)
            absolute = p._replace(query='', fragment='').geturl()
            candidates.append(("", absolute))
    
    # Dedup by URL, preserve order, cap at limit. Skip the listing page itself
    # and obvious non-article slugs (section index pages).
    section_slugs = {
        'news', 'press-releases', 'pressreleases', 'blog', 'newsroom',
        'press', 'announcements', 'resources', 'category', 'categories',
    }
    seen_local = set()
    unique = []
    for label, c in candidates:
        if c in seen_local or c == final_url:
            continue
        path = urlsplit(c).path.rstrip('/')
        slug = path.rsplit('/', 1)[-1].lower() if path else ''
        # Skip section index pages (e.g. /newsroom/pressreleases with no slug)
        if slug in section_slugs:
            continue
        seen_local.add(c)
        unique.append((label, c))
        if len(unique) >= limit:
            break
    
    entries = []
    for label, article_url in unique:
        try:
            art_resp = requests.get(article_url, headers=ua, timeout=20, allow_redirects=True)
        except Exception as e:
            entries.append({"error": f"fetch error: {e}", "link": article_url})
            continue
        if art_resp.status_code != 200:
            entries.append({"error": f"HTTP {art_resp.status_code}", "link": article_url})
            continue
        extracted = trafilatura.extract(
            art_resp.text,
            include_links=True,
            include_tables=True,
            output_format='json',
            url=article_url,
        )
        title = None
        body = ""
        published = ""
        if extracted:
            try:
                data = json.loads(extracted)
                title = data.get("title")
                body = data.get("text", "")[:5000]
                # trafilatura sometimes returns date in 'date' field
                published = data.get("date", "") or ""
            except (json.JSONDecodeError, AttributeError):
                pass
        if not title:
            # Fallback: use the link label from the listing page, or <title> tag
            if label:
                title = label
            else:
                t_match = re.search(r'<title[^>]*>([^<]+)</title>', art_resp.text, re.IGNORECASE)
                title = t_match.group(1).strip() if t_match else article_url
        entries.append({
            "title": title,
            "link": article_url,
            "summary": body,
            "published": published,
            "author": "",
        })
    
    return entries


def check_source_health(url: str, timeout: int = 10) -> Dict:
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
        response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
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
    elif source["type"] == "html":
        entries = fetch_html_page(url, source_key, limit=limit)
    elif source["type"] == "json":
        entries = fetch_json_api(url, limit=limit)
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
            key = key.rstrip(",").strip()
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
