#!/usr/bin/env python3
"""Quick check for feedparser and requests availability."""
import sys
print("python:", sys.version)
try:
    import feedparser
    print("feedparser:", feedparser.__version__)
except ImportError as e:
    print("feedparser MISSING:", e)
try:
    import requests
    print("requests:", requests.__version__)
except ImportError as e:
    print("requests MISSING:", e)
