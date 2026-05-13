from pathlib import Path

from core.llm import ask_llm


async def evolve_swarm(report, curated):
    prompt = f"""
You are the Evolution Agent.

You may:
- propose new agents
- rewrite prompts
- suggest source changes
- identify missing coverage
- evolve topics

Return markdown suggestions.

Report:

{report[:50000]}

Curated Findings:

{curated[:50000]}
"""

    result = await ask_llm(prompt)

    Path(
        "workspace/memory/evolution.md"
    ).write_text(result)

    return result