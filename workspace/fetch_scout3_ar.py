#!/usr/bin/env python3
"""Fetch the two arXiv CS.AR interconnect-relevant abstracts."""
import urllib.request
import xml.etree.ElementTree as ET

def fetch_arxiv_abstract(arxiv_id):
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

for aid in ['2607.02610', '2607.02729']:
    print(f"\n--- arXiv:{aid} ---")
    print(fetch_arxiv_abstract(aid))
    print()
