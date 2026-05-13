import asyncio
from pathlib import Path
from typing import List, Dict, Any

from core.fetchers import fetch_rss, fetch_url, fetch_with_trafilatura, RSS_FEEDS, get_feed_metadata
from core.llm import ask_llm


async def run_agent(agent, skills) -> List[str]:
    findings = []

    for source in agent.sources:
        if source.startswith("rss/"):
            key = source.split("/")[1]

            if key not in RSS_FEEDS:
                continue

            feed_info = RSS_FEEDS[key]
            entries = fetch_rss(feed_info["url"], limit=10)

            for entry in entries[:5]:
                full_content = await fetch_full_article(entry["link"])

                prompt = build_prompt(
                    agent=agent,
                    entry=entry,
                    full_content=full_content,
                    skills=skills,
                    feed_info=feed_info,
                )

                result = await ask_llm(
                    prompt,
                    model=agent.model,
                    agent=agent.name,
                )

                if result:
                    findings.append(result)

    output_path = (
        agent.output
        or f"workspace/findings/{agent.name}.md"
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n\n".join(findings))

    return findings


async def fetch_full_article(url: str) -> str:
    """Fetch the full article content from a URL."""
    content, _ = fetch_with_trafilatura(url)

    if content:
        if len(content) > 15000:
            content = content[:15000] + "\n\n[Content truncated...]"
        return content

    fallback, meta = fetch_url(url)
    if fallback:
        if len(fallback) > 15000:
            fallback = fallback[:15000] + "\n\n[Content truncated...]"
        return fallback

    return ""


async def run_scouts(agents, skills, sources) -> List[str]:
    scout_agents = [
        a for a in agents
        if "scout" in a.name
    ]

    tasks = [
        run_agent(agent, skills)
        for agent in scout_agents
    ]

    results = await asyncio.gather(*tasks)

    flattened = []

    for r in results:
        flattened.extend(r)

    return flattened


def build_prompt(agent, entry, full_content, skills, feed_info) -> str:
    skill_text = "\n\n".join(
        skills.get(skill, "")
        for skill in agent.skills
    )

    content_to_analyze = full_content if full_content else entry.get("summary", "")

    return f"""# Agent Role

{agent.role}

# Mission

{agent.mission}

# Skills

{skill_text}

# Source Information

**Feed Name**: {feed_info.get("topics", ["unknown"])[0].title()}
**Feed URL**: {entry.get("link", "")}
**Publication Date**: {entry.get("published", "Unknown")}
**Author**: {entry.get("author", "Unknown")}

# Article Title

{entry.get("title", "")}

# Article Content

{content_to_analyze[:15000]}

# Task

Analyze this content thoroughly.
Generate a structured finding with:
- **Title**: Clear, descriptive title
- **Summary**: 2-3 paragraph detailed summary with key technical details
- **Source URL**: {entry.get("link", "")}
- **Published Date**: {entry.get("published", "Unknown")}
- **Source Credibility**: [High/Medium/Low] - based on source type
- **Operational Impact**: What this means for HPC administrators
- **Tags**: [scheduler, orchestration, networking, storage, research, vendor, GPU, observability, etc.]
- **Importance**: [Critical/High/Medium/Low]
- **Why This Matters**: 1-2 sentences on why HPC admins should care

IMPORTANT: You MUST include the source URL in your output. Every finding must be traceable to its origin.

Return markdown with proper structure. Be thorough and technical - avoid marketing language."""