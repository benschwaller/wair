from core.llm import ask_llm


async def curate_findings(findings):
    if not findings:
        return "# No findings to curate\n\nNo scout findings were collected."

    combined = "\n\n".join(findings)

    if not combined.strip():
        return "# No findings to curate\n\nNo content to process."

    prompt = f"""You are the HPC Curator Agent.

Your job is to create a well-organized, sourced, and deduplicated collection of findings.

# Curation Tasks

1. **Merge duplicate stories** - If multiple findings cover the same story, keep the most detailed one
2. **Remove weak findings** - Remove any finding that:
   - Lacks proper source citations
   - Is too vague or lacks technical detail
   - Is just marketing/PR content
3. **Prioritize operational relevance** - HPC admin impact should be paramount
4. **Identify major themes** - Group related findings together
5. **Ensure all findings have sources** - Mark any finding without a source URL as [UNVERIFIED]
6. **Flag emerging trends** - Identify findings that represent new developments

# Quality Standards

Every finding in the curated output MUST have:
- Source URL in markdown link format: [Source Name](URL)
- Publication date if known
- Credibility indicator: [High Credibility], [Medium Credibility], or [Low Credibility]

If a finding lacks a source:
- Either remove it if it's low quality
- Or mark it clearly as [UNVERIFIED - NEEDS SOURCE]

# Output Format

## Curated HPC Findings

### Major Theme 1: [Theme Name]
[Findings related to this theme, each with proper citations]

### Major Theme 2: [Theme Name]
[Findings related to this theme]

...and so on

## Unverified Findings (Needs Source)
[Any findings that lack proper sourcing but might still be valuable]

---

Findings to curate:

{combined[:120000]}

Return organized, deduplicated markdown with proper source citations."""

    curated = await ask_llm(prompt, agent="curator")

    with open("workspace/findings/curated.md", "w") as f:
        f.write(curated)

    return curated