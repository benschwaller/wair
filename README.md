# NOOZ-Hermes

A multi-agent HPC/AI intelligence pipeline built on [Hermes Agent](https://hermes-agent.nousresearch.com/).

Replaces the original `nooz` Python pipeline with Hermes-native primitives:
cron scheduling, skill loading, `delegate_task` subagents, and autonomous evolution.

## What It Does

Every week, automatically:

1. **Verifies sources** — Health-checks all 79 sources (76 RSS feeds + 3 GitHub release pages).
2. **Runs scouts in parallel** — 15 scout subagents each fetch from their assigned sources,
   filter for new articles (deduped against a seen-items registry), and produce structured findings.
3. **Curates** — Deduplicates, prioritizes, theme-groups, and tags findings.
4. **Generates a report** — Synthesizes a weekly HPC/AI intelligence report with citations,
   credibility indicators, and technical depth.
5. **Evolves** — Analyzes coverage gaps and autonomously:
   - Adds new sources (unlimited)
   - Modifies existing scout skills (unlimited, low-risk)
   - Creates new scout skills (max 1/cycle, gap must persist 2+ cycles)
   - Archives unproductive scouts (3 barren cycles → archived)

## Quick Start (first-time setup)

**Prerequisites:**
- [Hermes Agent](https://hermes-agent.nousresearch.com/) installed and on PATH
- An [OpenRouter API key](https://openrouter.ai/keys) (or other provider)
- Python 3.10+ with `pip install feedparser requests trafilatura`

```bash
# 1. Set your API key
echo 'OPENROUTER_API_KEY=sk-or-v1-...' > ~/.hermes/.env

# 2. Let hermes generate a default config (only needed on first hermes run)
hermes config show

# 3. Run the setup script — links skills into your hermes installation,
#    applies model tiering to your global hermes config, and creates the cron job
python3 scripts/setup.py
```

The setup script is safe to re-run — it won't overwrite existing config without asking.

**After setup**, run the pipeline:

```bash
hermes chat -q "Read skills/meta/nooz-orchestrator.md and execute the full weekly pipeline."
```

## Configuration

### Model Tiering

Models are managed by `model-lists.yaml` at the project root. It defines two lists:

| Tier | Used for | First model (primary) | Falls back through |
|------|----------|-----------------------|--------------------|
| `strong` | Orchestrator, curator, editor, evolution | `minimax/minimax-m3` | strong[1:] + weak[:] |
| `weak` | Scout subagents (delegated) | `google/gemini-3-flash-preview` | strong[1:] + weak[:] (inherits from parent) |

Edit the lists and reorder them to change which models are tried first.
Run `python3 scripts/sync-models.py` to apply changes to your hermes config
(``~/.hermes/config.yaml`` — only the model-related sections are touched).

**Hard rule:** never use `:free` suffixes or the literal `openrouter/free` model ID.
Run `python3 scripts/verify_no_free_models.py`
to audit the current configuration.

### Cron Job

```bash
hermes cron list                      # list all cron jobs
hermes cron run <job-id>              # trigger the pipeline now
hermes cron edit <job-id>             # change schedule or delivery
```

## How It Works

```
nooz-hermes/
├── AGENTS.md                           # Project context (auto-loaded by Hermes)
├── README.md                           # This file
├── model-lists.yaml                    # Weak/strong model lists — edit to change models
├── scripts/
│   ├── setup.py                        # Bootstrap a fresh clone
│   ├── sync-models.py                  # Apply model-lists.yaml to ~/.hermes/config.yaml
│   ├── fetch_new_rss.py                # RSS + GitHub fetcher with dedup
│   └── source_health.py                # Source health checker
├── skills/                             # Scout + meta skills (read directly by the orchestrator)
│   ├── scouts/                         # Scout skills (one per domain)
│   └── meta/                           # Pipeline orchestration skills
├── sources/
│   ├── rss/                            # 76 RSS source definitions
│   └── repos/                          # 3 GitHub release sources
└── workspace/
    ├── reports/                        # Weekly reports (YYYY-MM-DD.md)
    ├── findings/                       # Scout output (per-scout .md files)
    └── memory/
        ├── seen-items.jsonl            # Dedup registry (auto-populated)
        ├── evolution-state.md          # Persistent gap tracking
        └── evolution-log.md            # Change log for autonomous modifications
```

## Source Coverage

79 sources monitored across:

- Vendor newsrooms (NVIDIA, AMD, Intel, HPE, Dell, Lenovo, IBM, Supermicro, Qualcomm)
- National HPC programs (EuroHPC, RIKEN, NCHC Taiwan, KISTI, Pawsey, NSCC, NSC, DoE, NSF)
- Chinese vendors (Sugon, Inspur, Phytium, HiSilicon)
- HPC software projects (Slurm, Lustre, Open MPI, ROCm, Apptainer, Flux, OpenHPC)
- Conferences & benchmarks (SC, ISC, Top500, Green500, HPCG, Graph500, MLPerf)
- Academic (arXiv cs.DC/cs.LG/cs.PF/cs.AR, OpenAIRE open-access publications across 6 HPC-admin topic queries, US DOE labs (NERSC, ORNL, LBNL, Sandia), EU HPC centers (CSC Finland/LUMI, BSC Barcelona/MareNostrum))
- Cooling & infrastructure (Vertiv, Submer, CoolIT, Asetek, GRC, Uptime Institute)
- Quantum (IBM Quantum, IonQ)
- Trade press (HPCwire, The Next Platform, Phoronix, LWN, AnandTech)

## Evolution Guardrails

The evolution step can autonomously:
- **Add sources freely** — New RSS/GitHub sources without restriction
- **Modify scout skills freely** — Prompt refinements, source additions, topic expansion
- **Create new scouts cautiously** — Max 1 per cycle, gap must persist 2+ cycles
- **Archive unproductive scouts** — 3 barren cycles → archived

The evolution step CANNOT:
- Delete the orchestrator or evolution skills
- Remove sources that produced findings in the current cycle
- Create more than 1 new scout per cycle
- Create a scout without a documented persistent gap

## Reading the Output

After the pipeline runs, the report is at:
```
workspace/reports/YYYY-MM-DD.md
```

Other outputs:
- `workspace/findings/` — Individual scout findings (per-scout .md files)
- `workspace/findings/curated.md` — Curated/deduplicated findings
- `workspace/memory/evolution.md` — Human-readable evolution report
- `workspace/memory/evolution-log.md` — Full log of autonomous modifications
- `workspace/memory/evolution-state.md` — Persistent gap tracking
