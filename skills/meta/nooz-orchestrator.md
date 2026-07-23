---
name: nooz-orchestrator
description: "Weekly HPC/AI intelligence pipeline orchestrator. Runs scouts in parallel, curates findings, generates report, then evolves the system."
version: 1.2.0
category: meta
---

# NOOZ Orchestrator: Weekly HPC Intelligence Pipeline

You are the orchestrator for the NOOZ weekly HPC/AI intelligence pipeline. Your job is to execute the full pipeline end-to-end: verify sources, run scouts in parallel, curate findings, generate a report, mark articles as reported, then run the evolution step.

## Pipeline Overview

```
1. Source Health Check     → verify all sources reachable
2. Scout Phase (parallel)  → spawn scout subagents via delegate_task
3. Curation                → dedup, prioritize, theme-group
4. Report Generation       → synthesize weekly report
5. Mark Reported           → flip seen-items to reported=true (prevents data loss on crash)
6. Evolution               → autonomous system improvement (separate skill)
```

## Phase 0: Sync Models (cron only)

If running as a cron job, first sync models:

```bash
python3 scripts/sync-models.py
```

Then verify no :free models leaked in:

```bash
python3 scripts/verify_no_free_models.py
```

## Phase 1: Source Health Check

Run the health check script:

```bash
python scripts/source_health.py
```

Review the output. Note any sources that are inactive or are not real feeds (HTTP 200 but HTML pages). Do not block the pipeline for inactive sources — just note them in the report's source credibility section.

## Phase 2: Scout Phase (Parallel)

Spawn all scout subagents in parallel using delegate_task in batch mode. Each scout is a separate subagent that:
- Loads its scout skill
- Runs the fetch script **with the `-s` flag to fetch ONLY its own sources**
- Fetches full content for relevant articles
- Produces structured findings

### Scout Source Mapping

Each scout fetches ONLY its assigned sources (not all 74). Use the `-s` flag:

| Scout | Source Keys (pass with `-s`) |
|-------|------------------------------|
| scout-research | rss/arxiv-cs.dc rss/arxiv-cs.lg rss/arxiv-cs.pf rss/arxiv-cs.ar rss/hpcwire rss/nextplatform rss/ieee-tpds rss/acm-taco rss/ijhpca rss/usenix-osdi-atc |
| scout-slurm | repos/slurm-schedmd repos/slurm-(schedmd) rss/hpcwire rss/nextplatform rss/flux-framework rss/openhpc |
| scout-vendors | rss/nvidia-newsroom rss/nvidia-developer-blog rss/amd-newsroom rss/amd-rocm-blog rss/intel-newsroom rss/hpe-newsroom rss/hpe-developer rss/dell-newsroom rss/lenovo-press rss/ibm-newsroom rss/supermicro-news rss/qualcomm-news |
| scout-sovereign-ai | rss/nchc-taiwan rss/eurohpc-ju rss/riken-r-ccs rss/kisti rss/pawsey rss/nscc-singapore rss/nsc-shenzhen rss/doe-office-of-science rss/nsf |
| scout-china-hpc | rss/nsc-shenzhen rss/sugon-english rss/inspur-english rss/phytium-english rss/hisilicon rss/hpcwire rss/nextplatform |
| scout-middleware | repos/slurm-schedmd repos/slurm-(schedmd) repos/rocm rss/lustre rss/open-mpi rss/openhpc rss/apptainer rss/flux-framework |
| scout-interconnect-cooling | rss/vertiv-newsroom rss/submer-blog rss/coolit-systems rss/grc rss/asetek rss/uptime-institute rss/hpe-newsroom rss/nvidia-newsroom |
| scout-conference-standards | rss/sc rss/isc rss/top500 rss/green500 rss/hpcg rss/graph500 rss/mlperf |
| scout-emerging-accelerators | rss/hpcwire rss/nextplatform rss/intel-newsroom rss/qualcomm-news rss/cerebras-blog rss/groq-blog rss/sambanova-blog rss/quix-quantum |
| scout-quantum-hpc | rss/ibm-quantum rss/ionq rss/ionq-blog rss/quantinuum-news rss/pasqal-news rss/rigetti-news rss/quera-blog rss/arxiv-quant-ph rss/hpcwire rss/nextplatform |

### Scouts to Spawn

Spawn these scout subagents (up to 3 at a time due to concurrency limits, so batch them):

**Batch 1:**
- scout-research (academic papers, arXiv)
- scout-slurm (schedulers, workload management)
- scout-vendors (vendor announcements, hardware)

**Batch 2:**
- scout-sovereign-ai (national HPC programs)
- scout-china-hpc (Chinese HPC ecosystem)
- scout-middleware (HPC software stack releases)

**Batch 3:**
- scout-interconnect-cooling (networking, thermal)
- scout-conference-standards (Top500, ISC, SC)
- scout-emerging-accelerators (non-NVIDIA/AMD accelerators)

**Batch 4:**
- scout-quantum-hpc (quantum-HPC convergence)

### How to Spawn Each Scout

For each scout, use delegate_task with:
- goal: "Execute the scout mission defined in your loaded skill. Run `python scripts/fetch_new_rss.py -s <SOURCE_KEYS> --limit 5` to get new articles (use the source keys from the Scout Source Mapping table above), filter for relevant ones, fetch full content, and write structured findings to the specified output file."
- context: The project directory path, the scout skill name, and instructions to fetch article content via web tools.
- toolsets: ['terminal', 'file', 'web']
- Load the scout skill via the `skills` parameter

**Scout delegation goal — full text** (use this exact string in `delegate_task goal=`, substituting <NAME>, <PROJECT_ROOT>, <SOURCE_KEYS>, and <OUTPUT_FILE>):

```
You are scout "<NAME>". Execute the mission defined in your loaded scout skill.

Working directory: <PROJECT_ROOT>

Hard requirements:
1. Run `python scripts/fetch_new_rss.py -s <SOURCE_KEYS> --limit 5` to get new articles.
   - Use ONLY the source keys from the Scout Source Mapping table. Do NOT fetch all sources.
   - Example: for scout-research, use `-s rss/arxiv-cs.dc rss/arxiv-cs.lg rss/arxiv-cs.pf rss/arxiv-cs.ar rss/hpcwire rss/nextplatform rss/ieee-tpds rss/acm-taco rss/ijhpca rss/usenix-osdi-atc`
2. Filter for articles relevant to your mission.
3. For each relevant article, fetch full content via web tools.
4. WRITE STRUCTURED FINDINGS TO THE OUTPUT FILE FIRST.
   - The output file path is in your scout skill ("File Output" section).
   - Write each finding with the full template from your scout skill: ### Title, Summary, Source URL, Published Date, Source Credibility, Tags, Importance, Operational Impact, Why This Matters.
   - Every finding MUST include the source URL and a published date (or "Unknown").
   - Use write_file (full overwrite) — do not append incrementally.
   - Do NOT summarize or compress findings into a header-only stub.
5. Verify the file yourself before exiting:
   - Run `wc -l <output-file>` and `wc -c <output-file>`.
   - The file must be > 2 KB OR contain an explicit "No findings this cycle" section with reasons (sources unreachable / no new articles after dedup).
   - If < 2 KB and no explicit "no findings" explanation, REWRITE the file with the missing detail. Do not exit with a stub.
6. Return ONLY a one-line summary in your final response, e.g.:
   "Scout <NAME>: <N> findings written to <path> (<KB> KB). <One sentence on what the top finding is>."

Do not do orchestrator work (curation, reporting, evolution). Do not modify files outside workspace/findings/<your-file>.
```

### Scout Output Verification Gate (REQUIRED — per batch)

After each batch's delegates return, BEFORE dispatching the next batch, verify each scout wrote a real file. For each scout in the batch:

```bash
for f in workspace/findings/scout-*.md; do
  size=$(stat -c %s "$f")
  lines=$(wc -l < "$f")
  echo "$f  $size bytes  $lines lines"
  # Stub detection: < 1 KB and no "Finding" headers
  if [ "$size" -lt 1024 ] && ! grep -q "^### Finding" "$f"; then
    echo "  STUB: $f needs rewrite or respawn"
  fi
done
```

If a scout produced a stub (< 1 KB with no `### Finding` headers), do ONE of:
- **Re-dispatch** the same scout with goal prefix "REWRITE: Your previous run produced only a stub. Rewrite the output file with full finding detail. The articles to process are already in seen-items.jsonl — re-run fetch_new_rss.py with the same -s source keys to see what's available, then write complete findings. Do NOT exit until the file is > 2 KB with ### Finding sections."
- **Mark as failed** and continue (record in the report's Coverage Notes that the scout produced a stub after re-dispatch).

Do NOT advance to the next batch until the current batch's scouts have either real files or are explicitly marked failed. This prevents the iteration-cap truncation that caused Scout 3 to lose its 11 findings on 2026-07-06.

### After All Scouts Complete

Read all files in workspace/findings/ to collect the scout results. If a scout produced no findings (empty file or file not found), note it but continue.

## Phase 3: Curation

You are now the Curator. Read all findings files and perform:

1. **Merge duplicates** — If multiple findings cover the same story, keep the most detailed one
2. **Remove weak findings** — Remove findings that:
   - Lack proper source citations
   - Are too vague or lack technical detail
   - Are just marketing/PR content
3. **Prioritize operational relevance** — HPC admin impact should be paramount
4. **Identify major themes** — Group related findings together
5. **Ensure all findings have sources** — Mark any finding without a source URL as [UNVERIFIED]
6. **Flag emerging trends** — Identify findings representing new developments

Write the curated output to `workspace/findings/curated.md`.

## Phase 4: Report Generation

You are now the Editor. Generate a comprehensive, sourced HPC intelligence report.

### Report Structure

```
# HPC Intelligence Report

Date: [today's date]

## Executive Summary
[2-3 paragraph overview of the most important findings this week]

## Major Themes
[Deep dives into the top 3-4 themes, each with multiple sourced paragraphs]

## Important Updates
[Itemized updates with proper citations, organized by topic area]

## Emerging Topics
[New technologies, trends, or developments worth watching]

## Source Credibility Summary
[Summary of sources used and their credibility assessment]

## Coverage Notes
[Which scouts produced findings, which didn't, any source health issues]
```

### Critical Requirements

1. **Every claim MUST have a source citation** in format: `([Source Name](URL), Date)`
2. **Include URLs for all sources** — do not leave any finding unsourced
3. **Credibility indicators**: [High Credibility], [Medium Credibility], [Verify]
4. **Technical depth**: version numbers, dates, configurations, performance metrics
5. **No marketing language** — use technical, precise language
6. **Traceability**: every section traceable to specific findings

Write the report to: `workspace/reports/YYYY-MM-DD.md` (use today's date).

## Phase 5: Mark Articles as Reported

Once the report file is successfully written to disk, run:

```bash
python scripts/mark_reported.py
```

This flips `reported: true` on all entries in `workspace/memory/seen-items.jsonl`.
If this step is skipped (e.g., pipeline crashes before this point), next cycle's
fetch will re-encounter the same articles and treat them as new — no data loss.

**Always run this AFTER the report is saved, never before.** The report is the
canonical record; the seen-items registry is just a dedup cache.

## Phase 6: Evolution

After the report is saved and `mark_reported.py` has run, load and follow the `nooz-evolution` skill to run the autonomous evolution step. The evolution step will:
- Analyze the report and curated findings for coverage gaps
- Add new sources freely
- Cautiously create/modify scout skills (max 1 new per cycle, gap must persist 2+ cycles)
- Update evolution log and state files

## Model Tiering (important)

The pipeline uses two model tiers, configured in Hermes:

- **Scouts** (delegated subagents): the `delegation.model` setting — a cheap/fast
  model, since scouts do high-volume, simpler analysis. Default: `openai/gpt-4o-mini`.
- **Orchestrator / Curator / Editor / Evolution**: the `model.default` setting — a
  stronger model for synthesis, curation, and autonomous evolution. Default:
  `z-ai/glm-5.2`.

Do NOT use OpenRouter `:free` variants (e.g. `openai/gpt-4o-mini:free`,
`meta-llama/llama-3.3-70b-instruct:free`). They are rate-limited, unreliable, and
have been removed/broken on OpenRouter. Always use the paid (non-`:free`) model ID.
If you change a model, verify it resolves as a paid model on OpenRouter first.

## Important Notes

- The fetch_new_rss.py script handles dedup automatically via seen-items.jsonl
- Articles are marked `reported: false` at fetch time and only become `reported: true`
  after the report is saved and `mark_reported.py` runs. This prevents data loss
  from mid-cycle crashes.
- If a scout finds no new articles, that's fine — note it and continue
- The pipeline should complete end-to-end without user interaction

## CRITICAL: Do Not Do Scout Work Yourself

The orchestrator MUST NOT run `fetch_new_rss.py`, write fetch scripts, or fetch
article content directly. Those are scout responsibilities. The orchestrator's
job is strictly:

1. Run `source_health.py` (health check only — no article fetching)
2. `delegate_task` to spawn scouts (they fetch, filter, and write findings)
3. Read the findings files the scouts produced
4. Curate, report, run `mark_reported.py`, evolve

If you find yourself writing a `/tmp/fetch_*.py` script or calling `web_search`/
`read_file` on an article URL, STOP — you are doing scout work. Wait for the
scout subagents to return their findings instead. Doing scout work in parallel
with the scouts wastes tool-call budget and causes the pipeline to hit the
iteration cap before curation/report.

## Model Verification

A verification script is provided at `scripts/verify_no_free_models.py` — run it
after any model config change to confirm no `:free` variants have crept in and
that the two-tier structure (scout != orchestrator) is still intact:

```bash
python3 scripts/verify_no_free_models.py
```
