import asyncio
from pathlib import Path

from core.fetchers import fetch_rss
from core.llm import ask_llm


RSS_FEEDS = {
    "hpcwire": "https://www.hpcwire.com/feed/",
    "nextplatform": "https://www.nextplatform.com/feed/",
    "phoronix": "https://www.phoronix.com/rss.php",
}


async def run_agent(agent, skills):
    findings = []

    for source in agent.sources:
        if source.startswith("rss/"):
            key = source.split("/")[1]

            if key not in RSS_FEEDS:
                continue

            entries = fetch_rss(RSS_FEEDS[key])

            for entry in entries[:5]:
                prompt = build_prompt(
                    agent=agent,
                    entry=entry,
                    skills=skills,
                )

                result = await ask_llm(
                    prompt,
                    model=agent.model,
                )

                findings.append(result)

    output_path = (
        agent.output
        or f"workspace/findings/{agent.name}.md"
    )

    Path(output_path).write_text(
        "\n\n".join(findings)
    )

    return findings


async def run_scouts(agents, skills, sources):
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


def build_prompt(agent, entry, skills):
    skill_text = "\n\n".join(
        skills.get(skill, "")
        for skill in agent.skills
    )

    return f"""
# Agent Role

{agent.role}

# Mission

{agent.mission}

# Skills

{skill_text}

# Content

Title: {entry['title']}
Link: {entry['link']}
Summary: {entry['summary']}

# Task

Analyze this content.
Generate:
- concise summary
- operational impact
- tags
- importance score
- whether this represents an emerging trend

Return markdown.
"""