# NOOZ-Hermes: HPC/AI Intelligence Pipeline

This project is a multi-agent HPC/AI intelligence pipeline built on Hermes Agent.
It replaces the original nooz Python pipeline with Hermes-native primitives:
cron scheduling, skill loading, delegate_task subagents, and autonomous evolution.

## Project Rules

- Python scripts live in `scripts/`. They handle RSS/GitHub fetching with dedup.
- Scout skills live in `skills/scouts/`. Each scout monitors a domain.
- Meta skills (orchestrator, evolution) live in `skills/meta/`.
- Source definitions live in `sources/rss/` and `sources/repos/` as markdown files.
- All output goes to `workspace/` (reports, findings, memory).
- The pipeline is driven by a weekly cron job whose prompt instructs the
  orchestrator to `read_file` the skill markdown directly from `skills/`.
  No `~/.hermes/skills/` installation or symlink is needed — the repo is
  self-contained.

## Running the Pipeline

```bash
# Manual run (from this directory):
hermes chat -q "Read skills/meta/nooz-orchestrator.md and execute the full weekly pipeline."

# The cron job handles this automatically on schedule.
```

## Model Configuration

Model tiering is managed via `model-lists.yaml` at the project root. Edit the
weak/strong lists there, then apply to the hermes config:

```bash
python3 scripts/sync-models.py
```

The weekly cron job automatically runs `sync-models.py` as step 0 of every
pipeline execution, so cron snapshots are refreshed from `model-lists.yaml`
before any scraping or spending occurs. Manual runs should do the same.

If the cron job fails with a "config drifted" error, the snapshot is stale.
Run `sync-models.py` first, then either re-pin the job via the edit command
shown in the error or delete and recreate it:

To verify no `:free` variants or `openrouter/free` leaked in:

```bash
python3 scripts/verify_no_free_models.py
```

**Hard rule:** never use `:free` suffixes or the literal `openrouter/free` model ID.

## Dependencies

```bash
pip install feedparser requests trafilatura
```

## Key Files

- `model-lists.yaml` — Weak/strong model lists; edit this to change models
- `scripts/fetch_new_rss.py` — RSS + GitHub release fetcher with dedup
- `scripts/source_health.py` — Source health checker
- `scripts/sync-models.py` — Apply model-lists.yaml to ~/.hermes/config.yaml
- `scripts/setup.py` — Bootstrap a fresh clone (syncs models, creates cron)
- `scripts/verify_no_free_models.py` — Check no `:free` models leaked in
- `skills/meta/nooz-orchestrator.md` — Pipeline orchestrator
- `skills/meta/nooz-evolution.md` — Autonomous evolution with guardrails
- `skills/scouts/*.md` — Scout skill files (one per domain)
- `workspace/memory/seen-items.jsonl` — Dedup registry (auto-populated)
- `workspace/memory/evolution-state.md` — Persistent gap tracking
- `workspace/memory/evolution-log.md` — Change log for all autonomous modifications
