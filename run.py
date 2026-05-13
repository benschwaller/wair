import asyncio
from datetime import datetime

from core.loader import (
    load_agents,
    load_skills,
    load_sources,
)
from core.scouts import run_scouts
from core.curator import curate_findings
from core.discovery import discover_topics
from core.editor import generate_report
from core.evolution import evolve_swarm
from core.utils import ensure_workspace


async def main():
    print("=== WAIR Starting ===\n")
    ensure_workspace()

    print("Loading agents, skills, and sources...")
    agents = load_agents("agents")
    skills = load_skills("skills")
    sources = load_sources("sources")
    print(f"Loaded {len(agents)} agents, {len(skills)} skills, {len(sources)} sources\n")

    print("Running scouts...")
    findings = await run_scouts(
        agents=agents,
        skills=skills,
        sources=sources,
    )
    print(f"Scouts complete: {len(findings)} findings\n")

    print("Curating findings...")
    curated = await curate_findings(findings)
    print("Curation complete\n")

    print("Discovering topics...")
    discoveries = await discover_topics(curated)
    print("Discovery complete\n")

    print("Generating report...")
    report = await generate_report(
        curated=curated,
        discoveries=discoveries,
    )
    print("Report generated\n")

    print("Evolving swarm...")
    await evolve_swarm(
        report=report,
        curated=curated,
    )
    print("Swarm evolution complete\n")

    date = datetime.utcnow().strftime("%Y-%m-%d")

    with open(f"workspace/reports/{date}.md", "w") as f:
        f.write(report)

    print("\n=== WAIR COMPLETE ===\n")
    print(report[:1500])


if __name__ == "__main__":
    asyncio.run(main())