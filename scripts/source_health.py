#!/usr/bin/env python3
"""
Source health checker — verifies all configured sources are reachable.

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
        results.append(health)
        status = "OK" if health["is_active"] else "FAIL"
        rt = health.get("response_time", "?")
        print(f"  {src['source_key']}: {status} ({rt}s)", file=sys.stderr)
    
    active = [r for r in results if r["is_active"]]
    inactive = [r for r in results if not r["is_active"]]
    
    output = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "active": len(active),
        "inactive": len(inactive),
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
    
    for r in results:
        status = "Active" if r["is_active"] else "Inactive"
        md += f"## {r['source']}\n"
        md += f"- Status: {status}\n"
        md += f"- URL: {r['url']}\n"
        if r.get("response_time"):
            md += f"- Response Time: {r['response_time']}s\n"
        if r.get("status_code"):
            md += f"- HTTP Status: {r['status_code']}\n"
        if r.get("error"):
            md += f"- Error: {r['error']}\n"
        md += "\n"
    
    report_path.write_text(md)
    
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
