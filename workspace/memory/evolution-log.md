# Evolution Log

This file records all autonomous changes made by the evolution step.
Each entry is a cycle. Do not edit manually — the evolution agent appends to this file.

---

## 2026-06-29 — Cycle 1

### Sources Added
- **rss/arxiv-cs.lg**: `https://export.arxiv.org/rss/cs.LG` — Machine learning preprints (distributed training, GPU scaling)
- **rss/arxiv-cs.pf**: `https://export.arxiv.org/rss/cs.PF` — Performance/benchmarking preprints
- **rss/arxiv-cs.ar**: `https://export.arxiv.org/rss/cs.AR` — Computer architecture preprints (accelerator/memory research)
- **rss/arxiv-quant-ph**: `https://export.arxiv.org/rss/quant-ph` — Quantum physics preprints (fault-tolerant quantum, quantum-HPC integration)
- **rss/cerebras-blog**: `https://www.cerebras.net/blog/` — Cerebras wafer-scale accelerator
- **rss/groq-blog**: `https://groq.com/blog/` — Groq LPU inference platform
- **rss/sambanova-blog**: `https://sambanova.ai/blog/` — SambaNova RDU
- **rss/quantinuum-news**: `https://www.quantinuum.com/news` — Quantinuum H-series trapped-ion
- **rss/pasqal-news**: `https://www.pasqal.com/news/` — Pasqal neutral-atom
- **rss/rigetti-news**: `https://www.rigetti.com/news` — Rigetti superconducting
- **rss/quera-blog**: `https://www.quera.com/blog` — QuEra neutral-atom + gigaquop roadmap
- **rss/ionq-blog**: `https://ionq.com/blog` — IonQ trapped-ion (complement to existing rss/ionq)

### Sources Updated (URL fixes)
- **rss/dell-newsroom**: `/en-us/dt/corporate/newsroom/` (404) → `/en-us/press` (200)
- **rss/vertiv-newsroom**: `/en-us/newsroom/` (404) → `/en-us/about/news-and-press/rss` (200, working RSS)
- **rss/green500**: `/green500/` (404) → root `/` (200, results on root)
- **rss/hpcg**: `/hpcg/` (404) → `/lists/hpcg/` (200)
- **rss/coolit-systems**: `/` (HTML) → `/feed/` (RSS, application/rss+xml)
- **rss/grc**: `/news/` (HTML) → `/feed/` (RSS)
- **rss/submer-blog**: `/blog/` (HTML) → `/feed/` (RSS)
- **rss/arxiv-cs.dc**: `/list/cs.DC/recent` (HTML, not parseable) → `export.arxiv.org/rss/cs.DC` (RSS)
- **rss/lustre**: composite URL → `/` (working root)
- **rss/amd-newsroom**: `/en/newsroom` (404) → `ir.amd.com/news-releases` (200, same content)
- **rss/ibm-quantum**: `/quantum` → `/quantum/blog` (200, more announcements)
- **rss/asetek**: kept `/` (no working RSS)

### Scout Skills Modified
- **scout-research**: Added arxiv-cs.lg, arxiv-cs.pf, arxiv-cs.ar; documented journal-feed unreliability in note
- **scout-emerging-accelerators**: Added Cerebras, Groq, SambaNova blog feeds; documented Tenstorrent/Etched/Lightmatter/Graphcore absence
- **scout-quantum-hpc**: Added Quantinuum, Pasqal, Rigetti, QuEra, IonQ blog, arxiv-quant-ph, nextplatform feeds
- **scout-interconnect-cooling**: Added note about URL updates to Submer, CoolIT, GRC, Vertiv

### Scout Skills Created
None — no scout was created this cycle. The evolution rules require 2+ consecutive cycles of persistent gap before creating a new scout. Gaps observed in cycle 1 are mitigated by URL/source updates; will re-evaluate next cycle.

### Scout Skills Archived (if any)
None.

### Gaps Identified
- **arXiv/IEEE/ACM research feeds**: Mitigated via URL switch to arXiv RSS feeds. Re-evaluate.
- **China-HPC first-party sources (DNS)**: Unmitigated — DNS failures for 4 Chinese national HPC vendor feeds. Continue covering via third-party.
- **Liquid-cooling vendor feeds**: Mitigated via URL updates. Re-evaluate.
- **Emerging accelerator vendor feeds**: Partially mitigated (Cerebras, Groq, SambaNova added; Tenstorrent, Etched, Lightmatter, Graphcore, FuriosaAI, Rebellions absent).
- **Quantum vendor feeds**: Partially mitigated (5 vendors added; photonic modality PsiQuantum, Xanadu still absent).
- **HPE/AMD/IBM newsroom feeds**: Partially mitigated (AMD and IBM fixed; HPE timeouts from this network).
- **Green500/HPCG top500.org subpages**: Mitigated via URL switch.
- **ACM/IJHPCA journal feeds (403)**: Unmitigated — paywall/ACL.

### Quality Issues
- The Next Platform's deep dives provided 80%+ of high-impact technical content this cycle — single point of analysis failure if feed degraded.
- No first-party Chinese sources for LineShine; relying on The Next Platform analysis is acceptable but second-party.
- HPCwire press-wire aggregation is one-step removed from first-party; should be paired with first-party sources where possible.
- GitHub release notes (ROCm, Slurm) are first-party and provided operational details unavailable elsewhere — these are the highest-quality signals.

---

## 2026-07-06 — Cycle 2

### Sources Added
- **rss/quix-quantum**: Next Platform feature on QuiX Quantum (Netherlands) photonic-compute architecture for HPC datacenters. Closes the "photonic-compute for HPC" gap; complements Lightmatter (photonic fabric) and electronic accelerators (Cerebras/Groq/SambaNova).

### Sources Updated (URL fixes)
None this cycle — all cycle-1 URL updates holding stable (Vertiv, Submer, GRC, CoolIT, AMD Newsroom, IBM Quantum, arXiv-cs.dc all returning content).

### Scout Skills Modified
- **scout-emerging-accelerators**: Added QuiX Quantum to mission list and source list. Note documenting the photonic-compute-for-HPC coverage gap closure.

### Scout Skills Created
None — no scout was created this cycle. New gaps observed: (a) arXiv returned 0 new items in this cycle, (b) Scout 3 (interconnect/cooling/china/quantum) failed to write output file. Neither has a 2-cycle history yet, so no new scout was created.

### Scout Skills Archived (if any)
None.

### Gaps Identified
- **arXiv/IEEE/ACM research feeds**: Same status as cycle 1 — feeds reachable but returned 0 new items this cycle. Re-evaluate next cycle.
- **China-HPC first-party sources (DNS)**: Unmitigated — DNS failures persist. Continue covering via third-party.
- **Liquid-cooling vendor feeds**: Mitigated — Vertiv (5), Submer (5), GRC (5) all returned articles.
- **Emerging accelerator vendor feeds**: QuiX Quantum added (photonic-compute-for-HPC). Cerebras/Groq/SambaNova blogs reachable but empty. Tenstorrent/Etched/Lightmatter/Graphcore/FuriosaAI/Rebellions still absent.
- **Quantum vendor feeds**: Pasqal/MegazoneCloud Korea partnership covered. PsiQuantum/Xanadu still absent.
- **HPE/AMD/IBM newsroom feeds**: Same status. AMD and IBM working; HPE timeout.
- **Green500/HPCG top500.org subpages**: Mitigated. No Top500 announcements this cycle.
- **ACM/IJHPCA journal feeds (403)**: Unmitigated — paywall/ACL.
- **Scout subagent output-write reliability**: NEW GAP. Scout 3 (interconnect/cooling/china/quantum) dispatched but never wrote its consolidated output file before returning. Root cause unclear — subagent may have timed out, may have returned without writing, or may have written to a path the orchestrator didn't find. Need to investigate subagent goal structure.

### Quality Issues
- **Linux 7.2-rc2 and 7.3 scheduler details** (Phoronix articles M2, M3, M4) — JS-rendered pages returned empty RSS summaries; full article content not fetched. Marked Medium credibility.
- **Next Platform QuiX Quantum article** — RSS summary returned empty content. Photonic-compute technical specifics (wavelength, mode count, benchmarks) not yet verified.
- **Next Platform "Do We Still Need GPUs?" article** (referenced by scout 1 fetch list but not promoted to findings) — RSS summary empty; coverage on Dongarra/Hoefler/Matsuoka LineShine-vs-Fugaku paper was covered in cycle 1 and not re-promoted this cycle.
- **Slurm 26.05.0 and 26.05.1** — both surfaced as new in this cycle because cycle 1 (2026-06-29) did not curate them. Reported here as current-cycle confirmation, not as new news.
- **No EuroHPC/RIKEN/NCHC/KISTI/Pawsey/NSCC/NSC/DoE/NSF feed activity this cycle** — feeds quiet; only TACC Horizon via HPCwire surfaced as major national-lab news.

### Pipeline Reliability
- **Iteration cap hit on original July 6 cron run.** Orchestrator improvised scout fetch work while `delegate_task` scouts ran in parallel, doubling effective tool-call count.
- **Fix applied 2026-07-07 (manual):** consolidated skills into repo at `skills/`, removed `~/.hermes/skills/nooz` symlink, dropped `--skill` flag from cron-create, added explicit anti-pattern guard to orchestrator skill, updated cron prompt to instruct `read_file` of skill markdown from repo. Verify on next cron run (2026-07-13).
- **Scout 3 (interconnect/cooling/china/quantum) partial failure.** Subagent returned without writing output file. Root cause unknown — needs investigation. Suggested next-cycle fix: add explicit "verify output file exists before returning" step to all scout subagent goals.

---

## 2026-07-07 — Cycle 2.5 (manual source-quality audit + bulk fix)

### Sources Fixed (16 RSS feeds discovered and patched)
- **rss/sc**: `supercomputing.org/feed/` (was homepage, now real RSS)
- **rss/top500**: `top500.org/news/feed/` (was homepage)
- **rss/green500**: `top500.org/news/feed/` (shared with top500, dedup expected)
- **rss/mlperf**: `mlcommons.org/feed/` (was benchmarks page)
- **rss/usenix-osdi-atc**: `usenix.org/rss.xml` (was homepage)
- **rss/nvidia-developer-blog**: `developer.nvidia.com/blog/feed/` (100 entries)
- **rss/amd-newsroom**: `ir.amd.com/news-events/press-releases/rss` (was press-release listing)
- **rss/intel-newsroom**: `intel.com/.../newsroom.html/feed/` (was homepage)
- **rss/lenovo-press**: `lenovopress.lenovo.com/rss/` (50 entries)
- **rss/lustre**: `lustre.org/feed/` (was homepage)
- **rss/openhpc**: `openhpc.community/feed/` (was homepage)
- **rss/flux-framework**: `flux-framework.org/feed` (was homepage)
- **rss/pawsey**: `pawsey.org.au/feed/` (was homepage)
- **rss/sambanova-blog**: `sambanova.ai/blog/rss.xml` (was blog homepage)
- **rss/ionq**: `ionq.com/news/rss.xml` (100 entries, was news page)
- **rss/ionq-blog**: `ionq.com/blog/rss.xml` (91 entries, was blog page)
- **rss/isc**: `isc-hpc.com/rss/` (was conference homepage — root cause of ISC content missing from July 6 report)

### Scout Skills Updated
- All 10 scout skills (scout-research, scout-slurm, scout-vendors, scout-sovereign-ai, scout-china-hpc, scout-middleware, scout-interconnect-cooling, scout-conference-standards, scout-emerging-accelerators, scout-quantum-hpc) — added "## Robust Output" section with explicit instructions to write full findings with template detail, verify with wc -l/wc -c, and never exit with a header-only stub.

### Orchestrator Skill Updated
- `skills/meta/nooz-orchestrator.md` — added "Scout Output Verification Gate" section: after each batch returns, orchestrator must run a stub-detection shell snippet (file < 1 KB + no `### Finding` headers = stub), either re-dispatch or mark failed, and NOT advance to next batch until all scouts in current batch verified.

### Source-Quality Audit Finding
- Audited all 71 RSS sources with feedparser. **Only 13 (18%) were real RSS feeds.** The other 58 (82%) were homepage URLs that return HTML, not RSS — the same bug that caused ISC content to be missed. `source_health.py` passed them all because it only checks HTTP 200, not feed format.
- After this fix: 29/71 (41%) are real feeds. 25 high-priority sources still broken (no RSS found by automated probing). 17 lower-priority sources also still broken. These need manual research or alternative coverage strategies.
- **Recommended evolution action next cycle:** (a) enhance `source_health.py` to use feedparser and check for `entries > 0`, not just HTTP 200; (b) continue probing the 25 not-found sources manually; (c) consider alternative sources for paywalled journals (IEEE/ACM/IJHPCA).
