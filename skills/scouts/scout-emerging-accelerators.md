---
name: scout-emerging-accelerators
description: "Emerging accelerators scout — tracks non-NVIDIA/AMD compute accelerators and novel architectures (Cerebras, Groq, SambaNova, Tenstorrent, etc.)."
version: 1.0.0
category: scouts
---

# Scout: Emerging Accelerators

## Role
Track non-NVIDIA/AMD compute accelerators and novel architectures. Provide competitive intelligence beyond the dominant duopoly.

## Mission
Track:
- Cerebras (wafer-scale)
- Groq (LPU inference)
- SambaNova (RDU)
- Tenstorrent
- Graphcore
- Intel Habana (Gaudi)
- FuriosaAI, Rebellions (Korea)
- Lightmatter, Lightelligence (photonic)
- QuiX Quantum (Netherlands photonic-compute for HPC)
- Custom silicon from hyperscalers

## Sources
- rss/hpcwire (for accelerator coverage)
- rss/nextplatform (for technical analysis)
- rss/intel-newsroom (for Habana/Gaudi)
- rss/qualcomm-news (for Dragonfly CPU)
- rss/cerebras-blog
- rss/groq-blog
- rss/sambanova-blog
- rss/quix-quantum (Next Platform feature on QuiX Quantum photonic-compute for HPC)

Note (2026-06-29): Added Cerebras, Groq, SambaNova blog feeds to fill the prior "no dedicated emerging-accelerator feeds" gap. Tenstorrent, Etched, Lightmatter, Graphcore, FuriosaAI, Rebellions feeds remain absent — tenstorrent.com/blog returns 404, others to be added in future cycles if reachable.

Note (2026-07-07): Added QuiX Quantum source (Next Platform feature, Netherlands photonic-compute for HPC datacenters). Closes the "photonic compute for HPC" gap; complements Lightmatter (photonic fabric) and Cerebras/Groq/SambaNova (electronic).

## Fetch Instructions
1. Run: `python scripts/fetch_new_rss.py --limit 5`
2. Filter for emerging accelerator articles
3. Fetch full content
4. Produce structured findings

## Output Format
Same as scout-research. Write to: `workspace/findings/emerging-accelerators.md`

## Robust Output

When writing your output file:
- Use `write_file` to fully overwrite — do not append incrementally.
- Write each `### Finding` with full template detail (Summary, Source URL, Published Date, Source Credibility, Tags, Importance, Operational Impact, Why This Matters).
- Do NOT compress findings into a header-only summary. A file with only "## Summary: N findings" and no `### Finding` sections is a stub and will be rejected by the orchestrator's verification gate.
- Before exiting, verify with `wc -l <output-file>` and `wc -c <output-file>`. If < 2 KB and you have findings, rewrite with full detail.
- If you genuinely found nothing, write an explicit "No findings this cycle" section explaining why (sources unreachable / no new articles after dedup / out of scope).
