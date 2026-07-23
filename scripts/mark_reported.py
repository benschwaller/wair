#!/usr/bin/env python3
"""
Mark all articles in seen-items.jsonl as reported.

This script should be run AFTER the weekly report is successfully saved.
It flips 'reported' from false to true on all entries, so that next cycle's
fetch skips them. If the pipeline crashes before this runs, articles remain
unreported and will be re-fetched next cycle — no data loss.

Usage:
    python scripts/mark_reported.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEEN_FILE = PROJECT_ROOT / "workspace" / "memory" / "seen-items.jsonl"


def main():
    if not SEEN_FILE.exists():
        print("No seen-items.jsonl found — nothing to mark", file=sys.stderr)
        return

    lines = SEEN_FILE.read_text().splitlines()
    updated = 0

    with open(SEEN_FILE, "w") as f:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                f.write(line + "\n")
                continue

            if not entry.get("reported", False):
                entry["reported"] = True
                entry["marked_reported_at"] = datetime.now(timezone.utc).isoformat()
                updated += 1

            f.write(json.dumps(entry) + "\n")

    print(f"Marked {updated} articles as reported in {SEEN_FILE}")


if __name__ == "__main__":
    main()
