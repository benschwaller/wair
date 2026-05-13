from pathlib import Path
import re

from core.llm import ask_llm


async def discover_topics(curated, all_findings=None):
    prompt = f"""You are the Discovery Agent for the HPC Intelligence Swarm.

Your primary mission is to discover NEW SOURCES and identify COVERAGE GAPS.

# Discovery Tasks

## 1. Source Discovery

Identify NEW RSS feeds, websites, and sources that should be tracked:

- HPC vendor blogs (Dell, HPE, Lenovo, NVIDIA, AMD, Intel, Oracle)
- Project official pages with feeds (Slurm, PBS Pro, Lustre, Gluster, GPFS)
- Academic HPC research groups
- Conference proceedings pages (SC, ISC, EuroML, etc.)
- Cloud provider HPC documentation
- GitHub releases for major HPC projects

For each potential source:
- Check if they have RSS feeds or update pages
- Assess their credibility and technical depth
- Identify what topics they cover that are currently missing

## 2. Topic Gap Analysis

Analyze what topics are mentioned but poorly covered:
- Are there mentions of vendors without their official sources?
- Are there technologies mentioned that lack dedicated scouts?
- Are there geographic or sector-specific gaps?

## 3. Emerging Source Detection

Look for:
- New HPC projects and tools mentioned in findings
- Software releases with official announcement pages
- Community discussions pointing to new resources

# Output Format

## Discovered New Sources

[List each new source with URL, type, topics, and suggested agent]

## Coverage Gaps

[List topics that need better coverage]

## Recommended New Agents

[Suggest agents for new topics/sources]

---

Curated Findings (for source extraction):

{curated[:80000]}

---

Recent Findings (for source mining):

{_load_recent_findings()[:40000]}
"""

    result = await ask_llm(prompt, agent="discovery")

    Path("workspace/topics/discovered-topics.md").parent.mkdir(parents=True, exist_ok=True)
    with open("workspace/topics/discovered-topics.md", "w") as f:
        f.write(result)

    return result


def _load_recent_findings() -> str:
    """Load recent findings for source mining."""
    findings_dir = Path("workspace/findings")

    if not findings_dir.exists():
        return ""

    all_content = []
    for finding_file in findings_dir.glob("*.md"):
        if finding_file.name == "curated.md":
            continue
        content = finding_file.read_text()
        if content:
            all_content.append(f"=== {finding_file.name} ===\n{content}")

    return "\n\n".join(all_content)