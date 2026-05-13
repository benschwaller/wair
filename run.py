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
    ensure_workspace()

    agents = load_agents("agents")
    skills = load_skills("skills")
    sources = load_sources("sources")

    findings = await run_scouts(
        agents=agents,
        skills=skills,
        sources=sources,
    )

    curated = await curate_findings(findings)

    discoveries = await discover_topics(curated)

    report = await generate_report(
        curated=curated,
        discoveries=discoveries,
    )

    await evolve_swarm(
        report=report,
        curated=curated,
    )

    date = datetime.utcnow().strftime("%Y-%m-%d")

    with open(f"workspace/reports/{date}.md", "w") as f:
        f.write(report)

    print("\n=== HPC SWARM COMPLETE ===\n")
    print(report[:1500])


if __name__ == "__main__":
    asyncio.run(main())