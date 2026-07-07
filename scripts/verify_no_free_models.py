#!/usr/bin/env python3
"""Verify no OpenRouter :free model variants are in active use.

Checks:
  1. ~/.hermes/config.yaml  -> model.default and delegation.model
  2. ~/.hermes/cron/jobs.json -> model_snapshot / provider_snapshot
  3. repo + installed nooz skills -> no :free model refs (except explicit warnings)
  4. scout model != orchestrator model (tiering exists)

Exit 0 = pass, exit 1 = fail.
"""
import re
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # scripts/ → nooz-hermes/
HERMES = Path.home() / ".hermes"

FAIL = []

# --- 1. Hermes config ---
cfg = (HERMES / "config.yaml").read_text()
m_default = re.search(r'^model:\s*\n(?:\s+.*\n)*?\s+default:\s*(\S+)', cfg, re.M)
deleg_section = cfg[cfg.find('delegation:'):]
d_model = re.search(r'^\s+model:\s*(\S+)', deleg_section, re.M)

default_model = m_default.group(1) if m_default else None
deleg_model = d_model.group(1) if d_model else None

print(f"model.default         = {default_model}")
print(f"delegation.model      = {deleg_model}")

if default_model and ':free' in default_model.lower():
    FAIL.append(f"model.default contains :free: {default_model}")
if deleg_model and ':free' in deleg_model.lower():
    FAIL.append(f"delegation.model contains :free: {deleg_model}")
if not default_model:
    FAIL.append("model.default not found in config")
if not deleg_model:
    FAIL.append("delegation.model not found in config")

# --- 2. Cron job ---
cron_path = HERMES / "cron" / "jobs.json"
if cron_path.exists():
    cron = json.loads(cron_path.read_text())
    for job in cron.get('jobs', []):
        ms = job.get('model_snapshot', '')
        ps = job.get('provider_snapshot', '')
        print(f"cron model_snapshot   = {ms}")
        print(f"cron provider_snapshot= {ps}")
        if ':free' in str(ms).lower():
            FAIL.append(f"cron job {job['job_id']} model_snapshot is :free: {ms}")

# --- 3. Repo + installed skills: scan for :free (excluding explicit warning lines) ---
warn_substrings = (
    'Do NOT use', 'rate-limited', 'removed/broken', 'removed or broken',
    'e.g.', 'meta-llama/llama-3.3-70b-instruct:free', 'openai/gpt-4o-mini:free',
    'BANNED_SUFFIXES', 'BANNED_IDS', 'NO ":free"', 'HARD RULE',
    'in active use', 'no :free', 'contains :free', 'unexpected :free',
    'PASS: no :free', 'scan for :free',
    "':free'", '":free"', 'no `:free`', 'confirm no',
    'model_snapshot is :free', 'delimiter',
    'Hard rule', 'Checking for :free', 'literal `openrouter/free`',
)

check_files = []
if REPO.exists():
    for f in REPO.rglob('*'):
        if f.is_file() and f.suffix in ('.md', '.py', '.yaml', '.yml', '.json', '.toml'):
            check_files.append(f)
# Scanning the repo covers all skills/ and scripts/ files.

for f in check_files:
    for i, line in enumerate(f.read_text(errors='ignore').splitlines(), 1):
        if ':free' not in line.lower():
            continue
        if any(s in line for s in warn_substrings):
            continue
        rel = f.relative_to(REPO) if str(f).startswith(str(REPO)) else f
        FAIL.append(f"{rel}:{i}: unexpected :free ref: {line.strip()}")

# --- 4. Tiering: scout model should differ from orchestrator model ---
tiers_differ = bool(deleg_model and default_model and deleg_model != default_model)
print(f"\nScout tier (cheap)        : {deleg_model}")
print(f"Orchestrator tier (strong): {default_model}")
print(f"Tiers differ              : {tiers_differ}")
if default_model and deleg_model and not tiers_differ:
    FAIL.append(f"Scout model == orchestrator model ({default_model}) — no tiering")

# --- Result ---
if FAIL:
    print(f"\n=== FAIL ({len(FAIL)} issue(s)) ===")
    for f in FAIL:
        print(f"  {f}")
    sys.exit(1)
else:
    print("\n=== PASS: no :free models in active use, tiering intact ===")
    sys.exit(0)
