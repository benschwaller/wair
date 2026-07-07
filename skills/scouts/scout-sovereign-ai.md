---
name: scout-sovereign-ai
description: "Sovereign AI scout — tracks national HPC programs, sovereign AI buildouts, and government compute initiatives."
version: 1.0.0
category: scouts
---

# Scout: Sovereign AI & National HPC

## Role
Track national HPC programs, sovereign AI infrastructure buildouts, public funding initiatives, and government-acquired compute capacity worldwide.

## Mission
Track:
- National HPC centers and their deployments
- Sovereign AI infrastructure programs
- Government HPC funding and procurement
- National lab announcements
- International HPC cooperation programs

## Sources
- rss/nchc-taiwan
- rss/eurohpc-ju
- rss/riken-r-ccs
- rss/kisti
- rss/pawsey
- rss/nscc-singapore
- rss/nsc-shenzhen
- rss/doe-office-of-science
- rss/nsf

## Fetch Instructions
1. Run: `python scripts/fetch_new_rss.py --limit 5`
2. Filter for sovereign AI / national HPC articles
3. Fetch full content
4. Produce structured findings

## Output Format
Same as scout-research. Write to: `workspace/findings/sovereign-ai.md`

## Robust Output

When writing your output file:
- Use `write_file` to fully overwrite — do not append incrementally.
- Write each `### Finding` with full template detail (Summary, Source URL, Published Date, Source Credibility, Tags, Importance, Operational Impact, Why This Matters).
- Do NOT compress findings into a header-only summary. A file with only "## Summary: N findings" and no `### Finding` sections is a stub and will be rejected by the orchestrator's verification gate.
- Before exiting, verify with `wc -l <output-file>` and `wc -c <output-file>`. If < 2 KB and you have findings, rewrite with full detail.
- If you genuinely found nothing, write an explicit "No findings this cycle" section explaining why (sources unreachable / no new articles after dedup / out of scope).
