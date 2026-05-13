from core.llm import ask_llm


async def curate_findings(findings):
    combined = "\n\n".join(findings)

    prompt = f"""
You are the HPC Curator Agent.

Tasks:
- merge duplicate stories
- remove weak findings
- prioritize operational relevance
- identify major themes
- reduce hype

Findings:

{combined[:120000]}

Return curated markdown.
"""

    curated = await ask_llm(prompt, agent="curator")

    with open("workspace/findings/curated.md", "w") as f:
        f.write(curated)

    return curated