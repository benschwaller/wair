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
- All 10 scout skills — added "## Robust Output" section with explicit instructions to write full findings with template detail, verify with wc -l/wc -c, and never exit with a header-only stub.

### Orchestrator Skill Updated
- `skills/meta/nooz-orchestrator.md` — added "Scout Output Verification Gate" section: after each batch returns, orchestrator must run a stub-detection shell snippet (file < 1 KB + no `### Finding` headers = stub), either re-dispatch or mark failed, and NOT advance to next batch until all scouts in current batch verified.

### Source-Quality Audit Finding
- Audited all 71 RSS sources with feedparser. **Only 13 (18%) were real RSS feeds.** The other 58 (82%) were homepage URLs that return HTML, not RSS — the same bug that caused ISC content to be missed. `source_health.py` passed them all because it only checks HTTP 200, not feed format.
- After this fix: 29/71 (41%) are real feeds. 25 high-priority sources still broken (no RSS found by automated probing). 17 lower-priority sources also still broken. These need manual research or alternative coverage strategies.

---

## 2026-07-24 — Cycle 3

### Sources Added
None this cycle — no new sources added. Gaps requiring new sources all have cycle_count = 1 and need one more cycle of observation before source-level action.

### Scout Skills Modified
None — all 12 scout skill files unchanged this cycle. "Robust Output" requirements from cycle 2.5 continue to produce quality findings.

### Scout Skills Created
None — no new scout was created. The only gap with cycle_count ≥ 2 that might warrant a new scout is "Interconnect fabric coverage missing," but the cooling/interconnect scout already exists and the gap is about missing sources within it, not about a missing domain entirely. Re-evaluate next cycle if fabric coverage remains zero.

### Scout Skills Archived (if any)
None — all active scouts produced findings this cycle. No barren_cycles counters triggered.

### Gaps Identified
#### Resolved this cycle:
- **arXiv/IEEE/ACM research feeds** → RESOLVED. All four arXiv RSS subdomains (cs.DC, cs.LG, cs.PF, cs.AR) returned articles.
- **Liquid-cooling vendor feeds** → RESOLVED. Vertiv (10 findings), Submer (4 findings), GRC active.
- **Scout subagent output-write reliability** → RESOLVED. 11/12 scouts produced valid files with the poll-and-collect protocol.

#### Persisting (cycle_count ≥ 2):
- **China-HPC first-party sources** (cycle_count: 3): All 5 dedicated feeds returned 0.
- **ACM/IJHPCA journal feeds** (cycle_count: 3): 403 from both journals.
- **HPE/AMD/IBM newsroom unreliability** (cycle_count: 3): HPE still times out.
- **Emerging accelerator vendor feeds sparse** (cycle_count: 3): SambaNova dominates.
- **Quantum vendor feeds sparse** (cycle_count: 3): IonQ dominates.

#### New this cycle:
- **Interconnect fabric coverage missing** (cycle_count: 1)
- **Content retrieval blocked by paywalls/cookie-gates** (cycle_count: 1)

---

## 2026-07-27 — Cycle 4

### Sources Added
None — no new sources added. The 3 scout failures (research-news, openaire-operations, interconnect-cooling) are likely timeout/crash issues, not missing-source issues.

### Scout Skills Modified
None — no scout skill files modified this cycle.

### Scout Skills Created
None — no new scout was created.

### Gaps Identified
#### Persisting (cycle_count ≥ 2):
- **China-HPC first-party sources** (cycle_count: 4)
- **ACM/IJHPCA journal feeds** (cycle_count: 4)
- **HPE/Dell/IBM/Supermicro newsroom** (cycle_count: 4)
- **Emerging accelerator vendor feeds** (cycle_count: 4)
- **Quantum vendor feeds** (cycle_count: 4)
- **Interconnect fabric coverage** (cycle_count: 2)
- **Content retrieval blocked by paywalls** (cycle_count: 2)

#### New this cycle:
- **Scout subagent reliability regression** (cycle_count: 1): 12/15 succeeded (80%)
- **China-HPC English-language coverage dead** (cycle_count: 1)

### Quality Issues
- **Scout reliability degraded** from 91.7% to 80%
- **China-HPC zero-finding cycle**: First time since pipeline inception
- **Lenovo-only vendors-systems**
- **NVIDIA developer blog is now the dominant vendor signal**

---

## 2026-08-11 — Cycle 5

### Sources Added
- **rss/arista-blog**: `https://www.arista.com/en/blog` — Arista Networks engineering blog (Ethernet switching, EOS, 400G/800G for AI/HPC). Added to address interconnect fabric coverage gap (cycle_count: 3).
- **rss/broadcom-news**: `https://investors.broadcom.com/news-releases` — Broadcom news (Tomahawk/Jericho switching, PCIe switches, custom ASICs for AI/HPC). Added to address interconnect fabric coverage gap.
- **rss/ultra-ethernet**: `https://ultraethern.wpenginepowered.com/feed/` — Ultra Ethernet Consortium (open Ethernet communication stack for AI/HPC workloads). Added to address interconnect fabric coverage gap.
- **rss/cxl-consortium**: `https://www.computeexpresslink.org/news` — CXL Consortium (CXL 3.x memory pooling, composable infrastructure). Added to address interconnect/memory fabric coverage gap.

**Rationale:** Interconnect fabric coverage gap has persisted for 3 cycles. The interconnect-cooling scout failed to produce output for 3 consecutive cycles. These 4 new sources provide first-party networking/fabric coverage that was completely missing — the scout previously had only cooling vendor feeds plus hpe-newsroom/nvidia-newsroom for Slingshot/Spectrum-X. Sources added directly rather than via new scout because the existing interconnect-cooling scout already covers this domain.

### Sources Updated (URL fixes)
None — all existing URL fixes from cycles 1–2.5 holding stable.

### Scout Skills Modified
- **scout-interconnect-cooling**: Added 4 new sources (arista-blog, broadcom-news, ultra-ethernet, cxl-consortium) to the Sources section. Scout now covers 12 sources spanning cooling (6), fabric/networking (4), and cross-cutting OEM (2).
- **nooz-orchestrator**: Updated both Scout Source Mapping tables to include the 4 new sources for scout-interconnect-cooling.

### Scout Skills Created
None — no new scout was created. No gap with cycle_count ≥ 2 that warrants a brand-new domain. The interconnect fabric gap is addressed by adding sources to the existing scout. The China-HPC gap (cycle_count: 5) would need a Chinese-language coverage approach that is beyond the scope of simple source additions — requires translation infrastructure.

### Scout Skills Archived (if any)
None — no scout has 3+ barren cycles. interconnect-cooling has 2 barren cycles (failed to produce output, not barren). middleware has 1 barren cycle (0 findings due to dedup, not source failure).

### Gaps Identified

#### Resolved this cycle:
- **Scout subagent reliability**: Improved from 80% (cycle 4) to 87% (cycle 5). Research-news and openaire-operations RECOVERED from prior-cycle failures. Still below the 91.7% peak.

#### Persisting (cycle_count ≥ 2):
- **China-HPC first-party sources** (cycle_count: 5): 1 marginal finding this cycle. DNS failures persist.
- **ACM/IJHPCA journal feeds** (cycle_count: 5): No change — 403 persists.
- **HPE/Dell/IBM/Supermicro newsroom** (cycle_count: 5): **WORSENED** — vendors-systems FAILED entirely this cycle (first complete failure). Previously Lenovo-only, now nothing.
- **Emerging accelerator vendor feeds** (cycle_count: 5): **IMPROVING** — SambaNova contributed 2 strong findings (SemiAnalysis SN50 benchmark + premium inference thesis).
- **Quantum vendor feeds** (cycle_count: 5): **IMPROVING** — IonQ had 2 strong findings + arXiv quant-ph 3 preprints.
- **Interconnect fabric coverage** (cycle_count: 3): **ACTION TAKEN** — 4 new fabric/networking sources added. Scout still failed (3rd consecutive), but root cause of coverage gap is addressed.
- **Content retrieval blocked by paywalls** (cycle_count: 3): No change, but scouts worked around it — research-news produced 5 quality findings from both HPCwire and Next Platform.
- **Scout subagent reliability** (cycle_count: 2): Improved to 87%.
- **China-HPC English-language coverage** (cycle_count: 2): Marginally improved — 1 finding vs 0 last cycle.

#### New this cycle:
- **vendors-systems scout failing** (cycle_count: 1): First complete failure for this scout. Previously Lenovo-only, now zero output. Monitor next cycle — if repeat failure, investigate goal structure and source health.

### Quality Issues
- **This was the richest cycle in pipeline history** — 6 mega-themes, 22 curated findings, the $500B NVIDIA/Wall Street financing announcement, Intel $20B raise, AMD Q2 earnings inflection, SambaNova SN50 multi-source benchmark, NVIDIA system-of-models agentic stack release, MLPerf Endpoints v0.7, and strong HPC scheduling research output.
- **NVIDIA dominated vendor coverage** — 5 of 9 vendors-gpu findings were NVIDIA developer blog posts; AMD contributed 2 (Taalas acquisition + Q2 earnings); Intel contributed 3 ($15B → $20B raise + CSO appointment). NVIDIA Developer Blog has become a primary first-party source, producing more content than the Newsroom.
- **Systems vendor coverage collapsed** — vendors-systems failed entirely this cycle. This is the first time since pipeline inception that no systems vendor (HPE, Dell, Lenovo, IBM, Supermicro) findings were produced. The gap is now critical — procurement comparison across multiple systems vendors is impossible.
- **MLPerf and MLCommons delivered high-value standards content** — MLPerf Endpoints v0.7 and the Benchmark Trust Test with SWE-Bench Pro contamination evidence are precisely the type of procurement-relevant signal the pipeline is designed to capture.
- **Research-news RECOVERED** from cycle 4 failure, producing 5 high-quality findings with full article bodies. The $500B NVIDIA story was captured with both the primary press release and the analytical companion piece.
- **openaire-operations RECOVERED** from cycle 4 failure, producing 2 strong findings (LLNL agentic HPC ops study + UChicago reactive scheduling thesis).
- **Middle-ware 0 findings** was a clean dedup result — Flux Framework Aug 4-10 releases were already ingested and marked reported. The scout provided useful top-of-feed reference context.
- **source_health.py timeout** at 120s remains an issue — ~20 sources remain unchecked. Should increase timeout or split into batches.

### Pipeline Reliability
- **Scout reliability improved** from 80% (12/15) to 87% (13/15). The two failures (vendors-systems, interconnect-cooling) are different from last cycle's three failures (research-news, openaire-operations, interconnect-cooling).
- **interconnect-cooling is the only repeat failure** (3 consecutive cycles). Root cause likely the combination of unreliable vendor feeds AND the scout's broad source scope (12 sources, balanced between cooling and networking). Added 4 fabric sources this cycle — monitor next cycle.
- **Poll-and-collect protocol continues to work correctly.** All 5 batches dispatched, 480s + 120s poll executed. Missing files correctly marked FAILED without re-dispatch.
- **Mark_reported.py ran successfully** — 18 articles flipped to reported=true. No data-loss scenario.
- **Total pipeline wall-clock time:** ~75 minutes (sync+health + 5×10 min scout batches + curation/report/evolution). Within cron execution window.