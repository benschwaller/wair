#!/usr/bin/env python3
"""Fetch arXiv abstracts via the arXiv API (which returns full abstracts)."""
import sys
import urllib.request
import xml.etree.ElementTree as ET
import re

def fetch_arxiv_abstract(arxiv_id):
    """Fetch abstract from arXiv API."""
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        xml_data = resp.read().decode('utf-8', errors='replace')
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        if entry is None:
            return "No entry found"
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
        published = entry.find('atom:published', ns).text.strip()
        return f"Title: {title}\nAuthors: {', '.join(authors)}\nPublished: {published}\nAbstract: {summary}"
    except Exception as e:
        return f"ERROR: {e}"


def fetch_hpcwire(url):
    """Try fetching HPCwire with a browser-like user agent."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=30)
        html = resp.read().decode('utf-8', errors='replace')
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        texts = []
        for p in paras:
            text = re.sub(r'<[^>]+>', '', p).strip()
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 30:
                texts.append(text)
        return '\n\n'.join(texts)[:4000] if texts else "No paragraphs found"
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == '__main__':
    # arXiv IDs
    arxiv_ids = [
        '2607.02616',  # MLIR for Quantum
        '2607.02620',  # VQE amino acids
        '2607.02622',  # COMET QAOA
        '2607.02626',  # Krylov-Lie
        '2607.02652',  # Minimally invasive measurement
        '2607.03988',  # PQC TLS 5G
    ]
    
    print("=" * 80)
    print("ARXIV ABSTRACTS")
    print("=" * 80)
    for aid in arxiv_ids:
        print(f"\n--- arXiv:{aid} ---")
        print(fetch_arxiv_abstract(aid))
        print()
    
    print("\n" + "=" * 80)
    print("HPCWIRE ARTICLES")
    print("=" * 80)
    hpcwire_urls = [
        'https://www.hpcwire.com/off-the-wire/pasqal-and-megazonecloud-partner-to-bring-industrial-scale-quantum-computing-to-south-korea/',
        'https://www.hpcwire.com/off-the-wire/eigenq-targets-post-quantum-upgrades-for-existing-intel-xeon-infrastructure/',
        'https://www.hpcwire.com/off-the-wire/iqm-acquires-quantistry-assets-to-expand-industrial-quantum-software-platform/',
        'https://www.hpcwire.com/off-the-wire/alfred-university-and-classiq-launch-quantum-computing-initiative/',
        'https://www.hpcwire.com/off-the-wire/taccs-horizon-nears-early-operations-as-nsf-leadership-class-supercomputer/',
    ]
    for url in hpcwire_urls:
        print(f"\n--- {url.split('/')[-2]} ---")
        print(fetch_hpcwire(url))
        print()
