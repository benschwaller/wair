#!/usr/bin/env python3
"""Discover working RSS/Atom/JSON feeds for a vendor newsroom or blog.

Used by the evolution agent when a source is marked "NOT A FEED" (HTML page)
or returns 404. Probes the site for real feeds via three strategies:

1. <link rel="alternate" type="application/rss+xml"> tags in the HTML
2. Common feed paths (/feed, /rss, /rss.xml, /atom.xml, /blog/feed, etc.)
3. Backing JSON API endpoints (AEM .model.json, WordPress wp-json, etc.)

Validates each candidate with feedparser to confirm it has entries.

Usage:
    python scripts/discover_feeds.py <entry_url>
    python scripts/discover_feeds.py https://www.hpe.com/us/en/newsroom.html
    python scripts/discover_feeds.py --source rss/hpe-newsroom

Output: JSON with all candidates and their validation status, plus the
winning feed URL (if any). The evolution agent should update the source
.md file with the winning URL, or mark it Type: html / Type: json if no
feed exists but the page is scrapable.

Exit code: 0 if a working feed was found, 1 if not.
"""
import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

import feedparser
import requests

UA = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) nooz-hermes/1.0 (+https://github.com/nooz)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Common feed paths to probe. Appended to the site root or the entry path.
COMMON_FEED_PATHS = [
    "/feed", "/feed/", "/rss", "/rss/", "/rss.xml", "/atom.xml",
    "/blog/feed", "/blog/feed/", "/blog/rss", "/blog/rss.xml",
    "/news/feed", "/news/feed/", "/newsroom/feed", "/newsroom/feed/",
    "/press/feed", "/press-releases/feed", "/pressreleases/feed",
    "/feed.xml", "/index.xml", "/feeds/posts/default",
]

# JSON API patterns to probe (vendor newsrooms that are JS apps).
# {root} is the site root, {path} is the entry path without trailing file.
JSON_API_PATTERNS = [
    # AEM (Adobe Experience Manager) — used by HPE, many enterprise sites
    "{root}{path}/_jcr_content/polaris-body-zone/aem.model.json?type=press-release&restype=press-release&topic=&offset=0",
    # WordPress REST API
    "{root}/wp-json/wp/v2/posts",
]


LINK_RE = re.compile(r'<link[^>]*rel=["\']alternate["\'][^>]*>', re.IGNORECASE)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
TYPE_RE = re.compile(r'type=["\']([^"\']+)["\']', re.IGNORECASE)


def fetch(url, timeout=20):
    """GET with project UA. Returns (response, error)."""
    try:
        resp = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
        return resp, None
    except Exception as e:
        return None, str(e)


def discover_link_tags(html, base_url):
    """Find <link rel=alternate type=application/rss+xml> tags."""
    candidates = []
    for m in LINK_RE.finditer(html):
        tag = m.group(0)
        href_m = HREF_RE.search(tag)
        type_m = TYPE_RE.search(tag)
        if not href_m:
            continue
        href = href_m.group(1)
        ctype = (type_m.group(1).lower() if type_m else "")
        if "rss" in ctype or "atom" in ctype or "xml" in ctype:
            absolute = urljoin(base_url, href)
            candidates.append(absolute)
    return candidates


def validate_feed(url):
    """Return (is_feed, entry_count, feed_title, error)."""
    resp, err = fetch(url, timeout=20)
    if err:
        return False, 0, None, f"fetch error: {err}"
    if resp.status_code != 200:
        return False, 0, None, f"HTTP {resp.status_code}"
    feed = feedparser.parse(resp.content)
    n = len(feed.entries)
    title = feed.feed.get("title") if hasattr(feed, "feed") else None
    is_feed = bool(feed.entries or title)
    return is_feed, n, title, "ok"


def validate_json_api(url):
    """Return (is_valid, item_count, error)."""
    headers = {**UA, "Accept": "application/json"}
    try:
        resp = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
    except Exception as e:
        return False, 0, f"fetch error: {e}"
    if resp.status_code != 200:
        return False, 0, f"HTTP {resp.status_code}"
    try:
        data = resp.json()
    except Exception as e:
        return False, 0, f"JSON parse error: {e}"
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("items", "results", "data", "articles", "posts"):
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
    return bool(items), len(items), "ok"


def site_root(entry_url):
    p = urlsplit(entry_url)
    return urlunsplit((p.scheme, p.netloc, "", "", ""))


def entry_path(entry_url):
    p = urlsplit(entry_url)
    # Path without trailing file (e.g. /newsroom.html -> /newsroom)
    path = p.path
    if path.endswith((".html", ".htm", ".php")):
        path = path.rsplit(".", 1)[0]
    return path.rstrip("/")


def discover(entry_url):
    """Run all discovery strategies against an entry URL."""
    print(f"Probing: {entry_url}", file=sys.stderr)
    resp, err = fetch(entry_url, timeout=40)
    if err:
        return {"entry_url": entry_url, "error": f"entry fetch failed: {err}", "candidates": [], "winner": None}
    if resp.status_code != 200:
        return {"entry_url": entry_url, "error": f"entry HTTP {resp.status_code}", "candidates": [], "winner": None}

    html = resp.text
    final_url = resp.url
    root = site_root(final_url)
    path = entry_path(final_url)

    # Strategy 1: <link rel=alternate> tags
    link_candidates = discover_link_tags(html, final_url)

    # Strategy 2: common feed paths at root and entry path
    path_candidates = []
    for base in (root, root + path):
        for suffix in COMMON_FEED_PATHS:
            path_candidates.append(base + suffix)

    # Strategy 3: JSON API patterns
    json_candidates = []
    for pattern in JSON_API_PATTERNS:
        json_candidates.append(pattern.format(root=root, path=path))

    all_candidates = []
    winner = None

    # Validate feed candidates
    for c in list(dict.fromkeys(link_candidates + path_candidates)):
        is_feed, n, title, status = validate_feed(c)
        all_candidates.append({
            "url": c, "type": "feed", "is_valid": is_feed,
            "entry_count": n, "feed_title": title, "status": status,
        })
        if is_feed and n > 0 and not winner:
            winner = {"url": c, "type": "feed", "entry_count": n, "feed_title": title}

    # Validate JSON API candidates
    for c in json_candidates:
        is_valid, n, status = validate_json_api(c)
        all_candidates.append({
            "url": c, "type": "json", "is_valid": is_valid,
            "entry_count": n, "status": status,
        })
        if is_valid and n > 0 and not winner:
            winner = {"url": c, "type": "json", "entry_count": n}

    # If no feed/json found, check if the page is scrapable (has article-like links)
    if not winner:
        href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        article_patterns = [
            r'/pressreleases?/[^/?#]+', r'/press-releases?/[^/?#]+',
            r'/news/[^/?#]+/?$', r'/newsroom/[^/?#]+/[^/?#]+/?$',
            r'/blog/[^/?#]+/?$', r'/announcement/[^/?#]+',
        ]
        combined = re.compile('|'.join(f'({p})' for p in article_patterns))
        article_links = 0
        for m in href_re.finditer(html):
            href = m.group(1)
            if not href.startswith(('#', 'javascript:', 'mailto:')) and combined.search(href):
                article_links += 1
        if article_links > 0:
            all_candidates.append({
                "url": final_url, "type": "html", "is_valid": True,
                "entry_count": article_links, "status": "scrapable (no feed, use Type: html)",
            })
            winner = {"url": final_url, "type": "html", "entry_count": article_links}

    return {
        "entry_url": entry_url,
        "final_url": final_url,
        "candidates": all_candidates,
        "winner": winner,
    }


def main():
    parser = argparse.ArgumentParser(description="Discover working feeds for a URL or source")
    parser.add_argument("entry_url", nargs="?", help="URL to probe for feeds")
    parser.add_argument("--source", help="Source key (e.g. rss/hpe-newsroom) to look up the URL")
    args = parser.parse_args()

    entry_url = args.entry_url
    if args.source:
        sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
        from fetch_new_rss import load_all_sources
        sources = load_all_sources()
        src = next((s for s in sources if s["source_key"] == args.source), None)
        if not src:
            print(json.dumps({"error": f"unknown source: {args.source}"}))
            sys.exit(1)
        entry_url = src["url"]

    if not entry_url:
        parser.error("entry_url or --source is required")

    result = discover(entry_url)
    print(json.dumps(result, indent=2))

    sys.exit(0 if result.get("winner") else 1)


if __name__ == "__main__":
    main()
