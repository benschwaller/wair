from pathlib import Path

from core.llm import ask_llm


async def evolve_swarm(report, curated):
    prompt = f"""
You are the Evolution Agent.

Your role is to provide high‑level, broadly applicable guidance for improving the swarm. Offer suggestions that:
- Introduce new scout or specialist agents with flexible, reusable missions.
- Refine existing prompts to be more generic and adaptable.
- Recommend additional data sources (RSS feeds, APIs, repositories) to broaden coverage; always suggest adding more sources where possible.
- Identify gaps in current coverage and propose thematic areas for future exploration.
- Suggest structural changes to the workflow that increase extensibility.

Do not over‑specify implementation details; keep recommendations abstract enough to be applicable across varied HPC environments.

Return a concise markdown document with sections for new agents, prompt ideas, source additions, coverage gaps, and workflow improvements.

Report:

{report[:50000]}

Curated Findings:

{curated[:50000]}
"""

    result = await ask_llm(prompt, agent="evolution")

    Path(
        "workspace/memory/evolution.md"
    ).write_text(result)

    return result