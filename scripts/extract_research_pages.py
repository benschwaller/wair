#!/usr/bin/env python3
from pathlib import Path
import trafilatura

items = [
    ("/tmp/arxiv-2607.19539.html", "/tmp/arxiv-2607.19539.txt"),
    ("/tmp/arxiv-2607.19421.html", "/tmp/arxiv-2607.19421.txt"),
    ("/tmp/arxiv-2607.19431.html", "/tmp/arxiv-2607.19431.txt"),
    ("/tmp/arxiv-2607.19623.html", "/tmp/arxiv-2607.19623.txt"),
    ("/tmp/arxiv-2607.20319.html", "/tmp/arxiv-2607.20319.txt"),
    ("/tmp/arxiv-2607.20211.html", "/tmp/arxiv-2607.20211.txt"),
    ("/tmp/hpcwire-rescale.html", "/tmp/hpcwire-rescale.txt"),
    ("/tmp/hpcwire-fermilab.html", "/tmp/hpcwire-fermilab.txt"),
    ("/tmp/hpcwire-planette.html", "/tmp/hpcwire-planette.txt"),
    ("/tmp/nextplatform-salience.html", "/tmp/nextplatform-salience.txt"),
    ("/tmp/nextplatform-investments.html", "/tmp/nextplatform-investments.txt"),
    ("/tmp/arxiv-2607.20120.html", "/tmp/arxiv-2607.20120.txt"),
    ("/tmp/arxiv-2607.19893.html", "/tmp/arxiv-2607.19893.txt"),
    ("/tmp/arxiv-2607.19438.html", "/tmp/arxiv-2607.19438.txt"),
    ("/tmp/arxiv-2607.02541.html", "/tmp/arxiv-2607.02541.txt"),
    ("/tmp/hpcwire-mi400.html", "/tmp/hpcwire-mi400.txt"),
    ("/tmp/hpcwire-genesis.html", "/tmp/hpcwire-genesis.txt"),
    ("/tmp/nextplatform-genesis.html", "/tmp/nextplatform-genesis.txt"),
    ("/tmp/nextplatform-microsoft.html", "/tmp/nextplatform-microsoft.txt"),
]
for source, dest in items:
    data = Path(source).read_text(errors="ignore")
    text = trafilatura.extract(data, include_comments=False, include_tables=True, output_format="txt") or ""
    Path(dest).write_text(text)
    print(f"{dest}: {len(text)} chars")
