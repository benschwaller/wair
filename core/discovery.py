from core.llm import ask_llm


async def discover_topics(curated):
    prompt = f"""
You are the Discovery Agent.

Analyze the curated findings.

Identify:
- recurring themes
- emerging ecosystems
- unusual technologies
- under-covered topics
- potential future scout agents

Return markdown.

Curated Findings:

{curated[:120000]}
"""

    result = await ask_llm(prompt)

    with open("topics/discovered-topics.md", "w") as f:
        f.write(result)

    return result