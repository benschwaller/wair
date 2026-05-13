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

    print("Verifying sources...")
    await verify_all_sources()
    print("Source verification complete\n")

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

    print("Discovering topics and new sources...")
    discoveries = await discover_topics(curated, all_findings=findings)
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


async def verify_all_sources():
    """Verify all configured RSS feeds are healthy."""
    from core.fetchers import list_all_feeds, check_source_health, RSS_FEEDS

    verification_results = []

    for feed in list_all_feeds():
        result = check_source_health(feed["url"])
        verification_results.append(result)

        status = "OK" if result["is_active"] else "FAILED"
        resp_time = result.get("response_time")
        if resp_time is not None:
            print(f"  {feed['key']}: {status} ({resp_time:.2f}s)")
        else:
            print(f"  {feed['key']}: {status}")

    active_feeds = [r for r in verification_results if r["is_active"]]
    print(f"  Active: {len(active_feeds)}/{len(verification_results)} feeds")

    inactive_feeds = [r for r in verification_results if not r["is_active"]]
    if inactive_feeds:
        print(f"  WARNING: {len(inactive_feeds)} feeds inactive or unreachable")

    verification_report = "# Source Verification Report\n\n"
    verification_report += f"Generated: {datetime.utcnow().isoformat()}\n\n"

    for result in verification_results:
        status = "Active" if result["is_active"] else "Inactive"
        verification_report += f"## {result['url']}\n"
        verification_report += f"- Status: {status}\n"
        verification_report += f"- Checked: {result['checked_at']}\n"
        if result.get("response_time"):
            verification_report += f"- Response Time: {result['response_time']:.2f}s\n"
        if result.get("status_code"):
            verification_report += f"- HTTP Status: {result['status_code']}\n"
        if result.get("error"):
            verification_report += f"- Error: {result['error']}\n"
        verification_report += "\n"

    from pathlib import Path
    Path("workspace/findings").mkdir(parents=True, exist_ok=True)
    Path("workspace/findings/source-verification.md").write_text(verification_report)


if __name__ == "__main__":
    asyncio.run(main())