#!/usr/bin/env python3
"""
setup.py — bootstrap a fresh nooz-hermes clone.

This script links the project into your local hermes installation so that
the nooz pipeline can run.  It is safe to re-run – existing symlinks,
config, and cron jobs are never overwritten without confirmation.

What it does
------------
1. Ensures ``~/.hermes/.env`` has an ``OPENROUTER_API_KEY``.
2. Ensures ``~/.hermes/config.yaml`` exists (creates a minimal one if missing).
3. Applies model tiering from ``model-lists.yaml`` via ``sync-models.py``
   (writes to ``~/.hermes/config.yaml`` — does not own the whole file).
4. Creates the weekly cron job (skips if one with the same name already exists).
5. Verifies configuration with ``verify_no_free_models.py``.

Skills live in the repo (``skills/``), not in ``~/.hermes/skills/``.
The cron job's prompt tells the orchestrator to ``read_file`` the skill
markdown directly from the repo, so no symlink or skill installation is needed.

Usage
-----
    python3 scripts/setup.py          # interactive (prompts before destructive steps)
    python3 scripts/setup.py --yes    # non-interactive (assume yes to all prompts)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path.home() / ".hermes"
HERMES_BIN = "hermes"

CRON_JOB_NAME = "nooz-weekly-hpc-intelligence"
CRON_EXPR = "0 8 * * 1"
CRON_PROMPT = (
    "You are the NOOZ weekly HPC/AI intelligence pipeline orchestrator.\n\n"
    "The skill files live in the repo, not in ~/.hermes. Before doing anything "
    "else, read them:\n"
    "1. read_file: skills/meta/nooz-orchestrator.md  (the full pipeline instructions)\n"
    "2. read_file: skills/meta/nooz-evolution.md      (the evolution step)\n\n"
    "Then execute the full weekly pipeline as described in the orchestrator skill:\n\n"
    "0. Sync models: `python3 scripts/sync-models.py`\n"
    "1. Run source health check: `python3 scripts/source_health.py`\n"
    "2. Spawn scout subagents in parallel batches using delegate_task (up to 3 at a "
    "time). Each scout should run `python3 scripts/fetch_new_rss.py --limit 5`, "
    "filter articles for relevance to its mission, fetch full article content via "
    "web tools, and write structured findings to its output file in "
    "workspace/findings/.\n"
    "3. Read all findings files from workspace/findings/ and curate them (dedup, "
    "prioritize, theme-group, tag) — write to workspace/findings/curated.md\n"
    "4. Generate the weekly HPC intelligence report with full citations, "
    "credibility indicators, and technical depth. Write to "
    "workspace/reports/YYYY-MM-DD.md (today's date).\n"
    "5. Run the evolution step following the evolution skill: analyze coverage "
    "gaps, add new sources, modify scout skills cautiously, update "
    "evolution-state.md and evolution-log.md.\n\n"
    "CRITICAL: The orchestrator MUST NOT run fetch_new_rss.py, write fetch "
    "scripts, or fetch article content directly. Those are scout "
    "responsibilities. If you find yourself writing /tmp/fetch_*.py or calling "
    "web_search/read_file on article URLs, STOP — wait for the scout subagents "
    "instead. Doing scout work in parallel wastes tool-call budget and causes "
    "the pipeline to hit the iteration cap before curation/report.\n\n"
    "Use simple/fast models for scout subagents and the stronger model for "
    "curation/editing/evolution.\n"
    f"The project working directory is {PROJECT_ROOT}."
)


def green(s: str) -> str:
    return f"\033[32m{s}\033[0m" if sys.stdout.isatty() else s


def yellow(s: str) -> str:
    return f"\033[33m{s}\033[0m" if sys.stdout.isatty() else s


def blue(s: str) -> str:
    return f"\033[34m{s}\033[0m" if sys.stdout.isatty() else s


def check_call(cmd: list[str], desc: str) -> bool:
    print(f"  {desc} … ", end="", flush=True)
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=PROJECT_ROOT)
        print(green("OK"))
        return True
    except subprocess.CalledProcessError as exc:
        print(f"FAILED (code {exc.returncode})")
        if exc.stderr:
            for line in exc.stderr.strip().splitlines():
                print(f"    {line}")
        return False
    except FileNotFoundError:
        print(f"NOT FOUND ({cmd[0]})")
        return False


def confirm(prompt: str, *, default_yes: bool = False) -> bool:
    if default_yes:
        return True
    suffix = " [Yn] " if True else " [y/N] "
    resp = input(prompt + suffix).strip().lower()
    if not resp:
        return default_yes
    return resp.startswith("y")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--yes", action="store_true", help="non-interactive, assume yes")
    args = parser.parse_args()

    issues: list[str] = []

    # ── 0. Prerequisites ────────────────────────────────────────────────────
    print(blue("=== Prerequisites ==="))

    hermes_path = shutil.which(HERMES_BIN)
    if not hermes_path:
        issues.append(f"{HERMES_BIN} not found on PATH — install hermes-agent first")
    else:
        print(f"  hermes:    {hermes_path}")
    print(f"  api key:   ", end="")
    env_file = HERMES_HOME / ".env"
    if env_file.is_file():
        txt = env_file.read_text()
        if "OPENROUTER_API_KEY=" in txt:
            print(green("found OPENROUTER_API_KEY in ~/.hermes/.env"))
        else:
            print(yellow("OPENROUTER_API_KEY not found in ~/.hermes/.env"))
            issues.append("set OPENROUTER_API_KEY in ~/.hermes/.env (get one at https://openrouter.ai/keys)")
    else:
        print(yellow("~/.hermes/.env does not exist"))
        issues.append("create ~/.hermes/.env with OPENROUTER_API_KEY=<your-key>")

    if issues:
        print(f"\n{yellow('Cannot proceed until these are fixed:')}")
        for i in issues:
            print(f"  • {i}")
        return 1

    # ── 1. Config: ensure hermes config exists ───────────────────────────────
    print(f"\n{blue('=== Config ===')}")

    hermes_config = HERMES_HOME / "config.yaml"
    if hermes_config.is_file():
        print(f"  {green('~/.hermes/config.yaml found')}")
    else:
        print(f"  Generating minimal ~/.hermes/config.yaml …", end=" ", flush=True)
        hermes_config.parent.mkdir(parents=True, exist_ok=True)
        import yaml
        minimal = {
            "model": {
                "base_url": "https://openrouter.ai/api/v1",
                "default": "minimax/minimax-m3",
                "provider": "openrouter",
                "api_mode": "chat_completions",
            },
            "delegation": {
                "model": "google/gemini-3-flash-preview",
                "provider": "openrouter",
                "max_iterations": 50,
                "child_timeout_seconds": 600,
                "max_concurrent_children": 3,
                "max_async_children": 3,
            },
            "toolsets": ["hermes-cli", "web"],
            "agent": {"max_turns": 60},
        }
        hermes_config.write_text(yaml.safe_dump(minimal, sort_keys=False, allow_unicode=True))
        print(green("OK"))

    # ── 2. Apply model tiering ──────────────────────────────────────────────
    print(f"\n{blue('=== Model Tiering ===')}")
    ok = check_call([sys.executable, "scripts/sync-models.py"], "Applying model-lists.yaml")
    if not ok:
        issues.append("failed to apply model tiering with sync-models.py")

    # ── 3. Create cron job ──────────────────────────────────────────────────
    print(f"\n{blue('=== Cron Job ===')}")

    cron_file = HERMES_HOME / "cron" / "jobs.json"
    already_exists = False
    if cron_file.is_file():
        try:
            cron = json.loads(cron_file.read_text())
            for job in cron.get("jobs", []):
                if job.get("name") == CRON_JOB_NAME:
                    already_exists = True
                    print(f"  Cron job '{CRON_JOB_NAME}' already exists (id={job['id']})")
                    break
        except (json.JSONDecodeError, IOError):
            pass

    if not already_exists:
        print(f"  Creating cron job '{CRON_JOB_NAME}' ({CRON_EXPR}) …", end=" ", flush=True)
        try:
            result = subprocess.run(
                [HERMES_BIN, "cron", "create",
                 CRON_EXPR,
                 CRON_PROMPT,
                 "--name", CRON_JOB_NAME,
                 "--workdir", str(PROJECT_ROOT),
                 "--deliver", "local",
                 ],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                job_id = result.stdout.strip()
                print(green(f"OK (id={job_id})"))
            else:
                print(f"FAILED: {result.stderr.strip()}")
                issues.append("failed to create cron job — create it manually: hermes cron create ...")
        except FileNotFoundError:
            issues.append(f"{HERMES_BIN} not found — create cron job manually")
        except subprocess.TimeoutExpired:
            issues.append("cron creation timed out")

    # ── 4. Verify ───────────────────────────────────────────────────────────
    print(f"\n{blue('=== Verification ===')}")
    verify_script = PROJECT_ROOT / "scripts" / "verify_no_free_models.py"
    ok = check_call([sys.executable, str(verify_script)], "Checking for :free models")
    if not ok:
        issues.append("verify_no_free_models.py found issues — review output above")

    # ── Summary ─────────────────────────────────────────────────────────────
    print()
    if issues:
        print(f"{yellow('Setup complete with warnings:')}")
        for i in issues:
            print(f"  • {i}")
        return 1
    else:
        print(green("Setup complete! Run the pipeline with:"))
        print(f"  cd {PROJECT_ROOT}")
        print(f"  hermes chat -q \"Read skills/meta/nooz-orchestrator.md and execute the full weekly pipeline.\"")
        return 0


if __name__ == "__main__":
    sys.exit(main())
