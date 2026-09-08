# Evolution State

**Last Updated:** 2026-09-07
**Current Cycle:** 9

## Persistent Gaps

### Gap: China-HPC first-party sources unreachable (DNS failures / feed issues)
- **First Observed:** 2026-06-29
- **Cycle Count:** 9
- **Last Observed:** 2026-09-07
- **Status:** open (IMPROVED — 1 finding from Next Platform cross-coverage)
- **Action Taken:** Recovered from 2 consecutive zero-finding cycles. 1 finding (Nvidia/HF acquisition China angle: Qwen, Kimi, DeepSeek now dominate Hugging Face open models). All 5 Chinese-vendor RSS feeds returned 0. Pattern stable: one cross-cutting finding per cycle from HPCwire/Next Platform. Chinese-language feeds remain the only viable path.

### Gap: ACM/IJHPCA journal feeds return 403
- **First Observed:** 2026-06-29
- **Cycle Count:** 9
- **Last Observed:** 2026-09-07
- **Status:** open (acceptable — arXiv fills gap)
- **Action Taken:** arXiv feeds (cs.DC, cs.LG, cs.PF, cs.AR, quant-ph) continue as primary academic HPC research source. 10 arXiv findings this cycle.

### Gap: Emerging accelerator vendor source diversity
- **First Observed:** 2026-06-29
- **Cycle Count:** 9
- **Last Observed:** 2026-09-07
- **Status:** open (IMPROVED — SambaNova SN50 at Hot Chips)
- **Action Taken:** SambaNova SN50 RDU at Hot Chips 2026 is the strongest non-GPU accelerator signal: 432 MB on-chip SRAM, 10×800G Ethernet, MBU framing, 44-51% bandwidth utilization. Cerebras, Groq, QuiX, Intel, Qualcomm returned 0. Coverage adequate via HPCwire/Next Platform.

### Gap: Source health — 6 inactive sources
- **First Observed:** 2026-06-29 (various)
- **Cycle Count:** 9
- **Last Observed:** 2026-09-07
- **Status:** open (stable — same 6 failures, isc recovered)
- **Action Taken:** hpe-newsroom (timeout), inspur-english (SSL), kisti (SSL), nchc-taiwan (DNS), phytium-english (DNS), sugon-english (DNS). All infrastructure-level failures. discover_feeds.py confirmed no working alternatives for hpe-newsroom. isc-hpc.com/rss/ recovered (cycle 2.5 fix holding).

### Gap: conference-standards zero-finding
- **First Observed:** 2026-09-07
- **Cycle Count:** 1
- **Last Observed:** 2026-09-07
- **Status:** open (new — monitor next cycle)
- **Action Taken:** All 7 sources (sc, isc, top500, green500, hpcg, graph500, mlperf) returned 0 new articles. Normal quiet period between conference cycles. Monitor next cycle.

### Gap: openaire-operations zero-finding
- **First Observed:** 2026-09-07
- **Cycle Count:** 1
- **Last Observed:** 2026-09-07
- **Status:** open (new streak — monitor next cycle)
- **Action Taken:** All 3 OpenAIRE sources (administration, monitoring, scheduling) returned 0 new articles. Was 0 in cycle 7, recovered in cycle 8 (5 findings), back to 0 in cycle 9. OpenAIRE API indexing appears intermittent.

### Gap: openaire-systems zero-finding
- **First Observed:** 2026-09-07
- **Cycle Count:** 1
- **Last Observed:** 2026-09-07
- **Status:** open (new streak — monitor next cycle)
- **Action Taken:** All 3 OpenAIRE sources (orchestration, networking, general) returned 0 new articles. Same intermittent pattern as openaire-operations. Monitor next cycle.

## Resolved Gaps

### ~~Gap: middleware zero-finding — between-release quiet period~~ → RESOLVED (Cycle 9)
- After 1 cycle of zero findings, middleware produced 5 findings: 3 Slurm CVE releases (coordinated across 26.05.4, 25.11.8, 25.05.9) and 2 Flux releases (core 0.89.0, accounting 0.61.0).

### ~~Gap: china-hpc zero-finding — 2nd consecutive cycle~~ → RESOLVED (Cycle 9)
- After 2 consecutive zero-finding cycles, china-hpc produced 1 finding: Nvidia/HF acquisition with China angle (Qwen, Kimi, DeepSeek dominate Hugging Face open models).

## Scout Performance Summary

| Scout | Cycles Active | Last Finding | Barren Cycles | Status |
|-------|--------------|--------------|---------------|--------|
| scout-research-arxiv | 9 | 2026-09-07 | 0 | active (10 findings, 22KB) |
| scout-research-news | 9 | 2026-09-07 | 0 | active (7 findings, 18KB) |
| scout-research-labs | 9 | 2026-09-07 | 0 | active (1 finding, 4KB) |
| scout-openaire-operations | 9 | 2026-09-01 | 1 | active (0 new articles — explicit no-findings) |
| scout-openaire-systems | 9 | 2026-09-01 | 1 | active (0 new articles — explicit no-findings) |
| scout-slurm | 9 | 2026-09-07 | 0 | active (5 findings, 13KB) |
| scout-vendors-gpu | 9 | 2026-09-07 | 0 | active (5 findings, 10KB) |
| scout-vendors-systems | 9 | 2026-09-07 | 0 | active (4 findings, 10KB) |
| scout-sovereign-ai | 9 | 2026-09-07 | 0 | active (1 finding, 4KB) |
| scout-china-hpc | 9 | 2026-09-07 | 0 | RECOVERED (1 finding) |
| scout-middleware | 9 | 2026-09-07 | 0 | RECOVERED (5 findings) |
| scout-interconnect-cooling | 9 | 2026-09-07 | 0 | active (1 finding, 6KB) |
| scout-conference-standards | 9 | 2026-09-01 | 1 | active (0 new articles — explicit no-findings) |
| scout-emerging-accelerators | 9 | 2026-09-07 | 0 | active (3 findings, 10KB) |
| scout-quantum-hpc | 9 | 2026-09-07 | 0 | active (2 findings, 7KB) |

## Source Health Summary

**Post-cycle-9:**
- Total sources: 83 (no change)
- Active: 77 (92.8%)
- Inactive: 6 (hpe-newsroom, inspur-english, kisti, nchc-taiwan, phytium-english, sugon-english)
- Fake feeds (NOT A FEED handled by HTML/JSON scraping): 24
- Scouts producing findings: 12/15 (80%)
- Scouts with zero new articles (explicit no-findings): 3/15 (openaire-operations, openaire-systems, conference-standards)
- Total articles marked reported this cycle: 98
- Pipeline wall-clock time: ~90 minutes (scout phase: 5×10 min + curation/report/evolution)
- Curated findings: 27 across 10 major sections