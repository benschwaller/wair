from datetime import datetime
import re

from core.llm import ask_llm


async def generate_report(curated, discoveries):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    prompt = f"""You are the Editor Agent for the HPC Intelligence Swarm.

Generate a comprehensive, sourced HPC intelligence report.

# Report Requirements

## Structure

```
# HPC Intelligence Report

Date: {today}

## Executive Summary
[2-3 paragraph overview of the most important findings this week]

## Major Themes
[Deep dives into the top 3-4 themes, each with multiple sourced paragraphs]

## Important Updates
[Itemized updates with proper citations, organized by topic area]

## Emerging Topics
[New technologies, trends, or developments worth watching]

## Source Credibility Summary
[Summary of sources used and their credibility assessment]

## Suggested New Agents
[Based on gaps in coverage]
```

## Critical Requirements

1. **Every claim MUST have a source citation** in the format:
   - For direct facts: `([Source Name](URL), Date)` or `([Source Name](URL))`
   - Example: `The new Slurm release includes GPU partitioning ([HPCwire](https://hpcwire.com/...), 2024)`

2. **Include URLs for all sources** - do not leave any finding unsourced

3. **Credibility indicators**: Mark each section with:
   - `[High Credibility]` for peer-reviewed, official docs, established tech journalism
   - `[Medium Credibility]` for community content, blogs
   - `[Verify]` for unconfirmed claims that need further validation

4. **Technical depth**: Go beyond headlines - include:
   - Version numbers, dates, specific configurations
   - Performance metrics when available
   - Comparison to previous versions/releases
   - Impact on HPC operations

5. **No marketing language**: Use technical, precise language

6. **Traceability**: Every section should be traceable to specific findings

## Curated Findings

{curated[:100000]}

## Discovered Topics

{discoveries[:50000]}
"""

    result = await ask_llm(prompt, agent="editor")

    result = ensure_citations(result)

    return result


def ensure_citations(report: str) -> str:
    """Ensure all sections have source citations."""
    lines = report.split("\n")
    in_section = False
    section_has_citation = False

    for i, line in enumerate(lines):
        if line.startswith("## "):
            if in_section and not section_has_citation:
                lines[i] = line + "\n*[Source needed - verify claims]*"
            in_section = True
            section_has_citation = False

        if "[" in line and "](" in line and "http" in line:
            section_has_citation = True

    return "\n".join(lines)