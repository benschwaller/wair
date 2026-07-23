#!/usr/bin/env python3
"""
Source health checker — verifies all configured sources are reachable
AND are actual RSS/feed sources (not HTML pages).

Usage:
    python scripts/source_health.py                    # Check all sources
    python scripts/source_health.py --source rss/hpcwire # Check one source

Output: JSON with health status for each source.
Also writes a markdown report to workspace/findings/source-verification.md
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_new_rss import load_all_sources, check_source_health


def check_feed_validity(url: str) -> dict:
    """Check if a URL returns a parseable feed (RSS, Atom, etc.)."""
    result = {
        "has_entries": False,
        "entry_count": 0,
        "feed_title": None,
        "is_feed": False,
    }
    try:
        import feedparser
        import requests
        resp = requests.get(url, headers={
            "User-Agent": "nooz-hermes/1.0 (+https://github.com/nooz)"
        }, timeout=15, allow_redirects=True)
        content_type = resp.headers.get("content-type", "").lower()
        # Check content-type hint
        is_xml = "xml" in content_type or "rss" in content_type or "atom" in content_type
        feed = feedparser.parse(resp.content)
        result["feed_title"] = feed.feed.get("title")
        result["entry_count"] = len(feed.entries)
        result["has_entries"] = len(feed.entries) > 0
        # Consider it a real feed if it has entries OR the content-type signals feed
        result["is_feed"] = bool(feed.entries or is_xml or feed.feed.get("title"))
    except Exception:
        pass
    return result


def main():
    parser = argparse.ArgumentParser(description="Check source health")
    parser.add_argument("--source", type=str, help="Check a specific source")
    args = parser.parse_args()
    
    sources = load_all_sources()
    
    if args.source:
        sources = [s for s in sources if s["source_key"] == args.source]
    
    results = []
    for src in sources:
        health = check_source_health(src["url"])
        health["source"] = src["source_key"]
        health["name"] = src["name"]
        health["description"] = src["description"]
        
        # Also check if the URL is a real feed, not just HTTP 200
        if health["is_active"] and src["type"] == "rss":
            feed_info = check_feed_validity(src["url"])
            health["is_feed"] = feed_info["is_feed"]
            health["feed_entry_count"] = feed_info["entry_count"]
            health["feed_title"] = feed_info.get("feed_title")
        else:
            health["is_feed"] = True  # repos don't need feed check
        
        results.append(health)
        status = "OK" if health["is_active"] else "FAIL"
        rt = health.get("response_time", "?")
        feed_warn = ""
        if health["is_active"] and not health.get("is_feed", True):
            feed_warn = " (NOT A FEED!)"
        print(f"  {src['source_key']}: {status} ({rt}s){feed_warn}", file=sys.stderr)
    
    active = [r for r in results if r["is_active"]]
    inactive = [r for r in results if not r["is_active"]]
    fake_feeds = [r for r in results if r["is_active"] and not r.get("is_feed", True)]
    
    output = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "active": len(active),
        "inactive": len(inactive),
        "fake_feeds": len(fake_feeds),
        "sources": results,
    }
    
    # Write markdown report
    report_path = PROJECT_ROOT / "workspace" / "findings" / "source-verification.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md = f"# Source Verification Report\n\n"
    md += f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n"
    md += f"**Active: {len(active)}/{len(results)}**\n\n"
    
    if inactive:
        md += f"**WARNING: {len(inactive)} sources inactive or unreachable**\n\n"
    if fake_feeds:
        md += f"**WARNING: {len(fake_feeds)} sources return HTTP 200 but are NOT real RSS/Atom feeds (HTML pages)**\n\n"
    
    for r in results:
        status = "Active" if r["is_active"] else "Inactive"
        feed_status = ""
        if r["is_active"] and not r.get("is_feed", True):
            feed_status = " (NOT a feed — HTML page)"
        md += f"## {r['source']}{feed_status}\n"
        md += f"- Status: {status}\n"
        md += f"- URL: {r['url']}\n"
        if r.get("response_time"):
            md += f"- Response Time: {r['response_time']}s\n"
        if r.get("status_code"):
            md += f"- HTTP Status: {r['status_code']}\n"
        if r.get("feed_entry_count") is not None:
            md += f"- Feed Entries: {r['feed_entry_count']}\n"
        if r.get("error"):
            md += f"- Error: {r['error']}\n"
        md += "\n"
    
    report_path.write_text(md)
    
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
