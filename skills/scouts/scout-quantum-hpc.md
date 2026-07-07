---
name: scout-quantum-hpc
description: "Quantum-HPC convergence scout — tracks quantum computing developments relevant to HPC and post-quantum cryptography."
version: 1.0.0
category: scouts
---

# Scout: Quantum-HPC Convergence

## Role
Track quantum computing developments relevant to HPC, quantum-HPC hybrid systems, and post-quantum cryptography for HPC.

## Mission
Track:
- IBM Quantum roadmap and developments
- IonQ (trapped ion)
- Quantinuum (H-Series)
- Quantum-HPC integration efforts
- Post-quantum cryptography (NIST PQC)
- Quantum networking

## Sources
- rss/ibm-quantum
- rss/ionq
- rss/ionq-blog
- rss/quantinuum-news
- rss/pasqal-news
- rss/rigetti-news
- rss/quera-blog
- rss/arxiv-quant-ph
- rss/hpcwire (for quantum-adjacent coverage)
- rss/nextplatform (for quantum-HPC integration deep dives)

Note (2026-06-29): Added Quantinuum, Pasqal, Rigetti, QuEra, IonQ blog feeds and arXiv quant-ph RSS to fill the prior "IBM/IonQ-only" coverage gap. Coverage now spans the 5 major quantum hardware modalities: superconducting (IBM, Rigetti), trapped ion (IonQ, Quantinuum), neutral atom (Pasqal, QuEra), photonic (none currently configured — add PsiQuantum/DELTA-9 when reachable), SFQ/digital (SEEQC).

## Fetch Instructions
1. Run: `python scripts/fetch_new_rss.py --limit 5`
2. Filter for quantum-HPC articles
3. Fetch full content
4. Produce structured findings

## Output Format
Same as scout-research. Write to: `workspace/findings/quantum-hpc.md`

## Robust Output

When writing your output file:
- Use `write_file` to fully overwrite — do not append incrementally.
- Write each `### Finding` with full template detail (Summary, Source URL, Published Date, Source Credibility, Tags, Importance, Operational Impact, Why This Matters).
- Do NOT compress findings into a header-only summary. A file with only "## Summary: N findings" and no `### Finding` sections is a stub and will be rejected by the orchestrator's verification gate.
- Before exiting, verify with `wc -l <output-file>` and `wc -c <output-file>`. If < 2 KB and you have findings, rewrite with full detail.
- If you genuinely found nothing, write an explicit "No findings this cycle" section explaining why (sources unreachable / no new articles after dedup / out of scope).
