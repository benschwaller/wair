# NOOZ

**Your AI-powered HPC intelligence hub.** Nooz scours the web, aggregates news from credible HPC sources, and delivers actionable intelligence about supercomputing systems, software, and trends—all in a clean, sourced report.

## Why Nooz?

HPC administrators and engineers face information overload. Vendor blogs, academic papers, release notes, and news outlets produce a constant stream of updates. Missing a critical patch, a new best practice, or an emerging technology can have real consequences.

Nooz is your automated research assistant. It:
- **Monitors** RSS feeds from HPC news leaders (HPCwire, The Next Platform, Phoronix, LWN, AnandTech)
- **Fetches** full article content from across the web
- **Curates** findings to remove noise and duplicates
- **Discovers** new sources and emerging topics
- **Sources** every claim with proper citations and credibility ratings
- **Evolves** itself—after each run, it suggests new agents, sources, and improvements

## What It Does

Every week (or on demand), Nooz generates a structured intelligence report covering:

- **Major Themes** — Deep dives into the most important HPC trends
- **Important Updates** — Version releases, security patches, feature announcements
- **Emerging Topics** — New technologies worth watching
- **Source Credibility Summary** — Know the provenance of your information

Every finding in the report links back to its source with a URL. Nooz marks credibility: `[High Credibility]` for peer-reviewed papers and official documentation, `[Medium Credibility]` for established tech journalism, `[Verify]` for unconfirmed claims.

## Key Features

### Multi-Agent Architecture
Agents are defined in simple Markdown files. Add a new scout by dropping a `.md` file into the `agents/` directory. No code required.

### Parallel Scout Execution
Scouts run concurrently, fetching from multiple RSS feeds simultaneously. Fast by default.

### Source Verification
Nooz verifies that feeds are healthy and reachable before scouting. Dead sources are flagged.

### Full-Content Fetching
Don't settle for RSS summaries. Nooz fetches the full article content for deeper analysis.

### Self-Evolving
After each report, the evolution agent identifies gaps in coverage, suggests new agents and sources, and recommends prompt improvements. Use `python evolve.py` to apply those changes.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/your-org/nooz.git
cd nooz
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
export OPENROUTER_API_KEY=sk-or-...

# Run
python run.py
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | API key for OpenRouter LLM access |

### Adding Sources

RSS feeds are configured in `core/fetchers.py` under `RSS_FEEDS`. Add new feeds by extending the dictionary:

```python
RSS_FEEDS = {
    "myfeed": {
        "url": "https://example.com/feed/",
        "topics": ["hpc", "gpu"],
        "credibility": 0.8
    },
}
```

### Adding Agents

Create a new agent in `agents/` directory:

```markdown
---
name: my-scout
role: HPC GPU specialist
model: openrouter/free
skills:
  - summarize
  - classify
sources:
  - rss/hpcwire
  - rss/nextplatform
output: workspace/findings/gpu.md
---

## Mission

Track GPU scheduler developments, CUDA releases, and GPU cluster management.
```

## The Evolution Loop

Nooz is self-improving. After each run:

1. `workspace/memory/evolution.md` is generated with suggestions
2. Run `python evolve.py --dry-run` to preview changes
3. Run `python evolve.py` (or `--auto`) to apply changes
4. New agents, skills, and sources are created automatically

## Architecture

```
run.py
 └── run_scouts()      → Fetch RSS, analyze articles
     └── run_agent()   → Per-agent processing
 └── curate_findings() → Deduplicate, filter, prioritize
 └── discover_topics() → Find new sources, identify gaps
 └── generate_report()→ Produce final intelligence report
 └── evolve_swarm()    → Generate evolution suggestions
```

Agents, skills, and sources are all Markdown-defined. The system is human-editable at every layer.

## Built With

- **OpenRouter** — Unified LLM API
- **feedparser** — RSS parsing
- **trafilatura** — Full-text web extraction
- **Python 3.10+** — Async-first architecture

## License

MIT