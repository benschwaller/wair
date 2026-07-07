#!/usr/bin/env python3
"""Fetch and extract article text for scout 3."""
import re
import sys
import urllib.request

def fetch_text(url, max_chars=6000):
    """Fetch URL and extract readable text."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"FETCH ERROR: {e}"

    # Remove script/style/json-ld blocks
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL)

    # Extract paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    texts = []
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p).strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 30:
            texts.append(text)

    if not texts:
        # Fallback: just strip all tags
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]

    return '\n\n'.join(texts)[:max_chars]


if __name__ == '__main__':
    urls = sys.argv[1:]
    for url in urls:
        print(f"\n{'='*80}")
        print(f"URL: {url}")
        print('='*80)
        print(fetch_text(url))
        print()
