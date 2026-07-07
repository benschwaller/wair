#!/usr/bin/env python3
"""
sync-models.py — apply model-lists.yaml to hermes config.yaml.

Reads the curated weak/strong model lists and writes:
  - model.default             → first strong model
  - model.provider            → top-level `provider` (default: openrouter)
  - delegation.model          → first weak model
  - delegation.provider       → top-level `provider`
  - fallback_model            → ordered list of (strong[1:], weak[:])
                                tried on timeout / 429 / 529 / 503

Also enforces the hard rule: NO ":free" suffix, NO "openrouter/free".

Usage:
    python3 scripts/sync-models.py            # apply
    python3 scripts/sync-models.py --dry-run  # show what would change
    python3 scripts/sync-models.py --check    # CI mode: exit 1 if drift
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = Path.home() / ".hermes"
LISTS_FILE = PROJECT_ROOT / "model-lists.yaml"
CONFIG_FILE = HERMES_HOME / "config.yaml"

BANNED_SUFFIXES = (":free", ":extended", ":nitro")
BANNED_IDS = {"openrouter/free"}


def die(msg: str, code: int = 1) -> None:
    print(f"sync-models: error: {msg}", file=sys.stderr)
    sys.exit(code)


def load_lists(path: Path) -> dict[str, Any]:
    if not path.is_file():
        die(f"lists file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        die(f"{path}: top-level must be a mapping, got {type(data).__name__}")
    if "weak" not in data or "strong" not in data:
        die(f"{path}: must define both 'weak' and 'strong' lists")
    for key in ("weak", "strong"):
        if not isinstance(data[key], list) or not data[key]:
            die(f"{path}: '{key}' must be a non-empty list")
    return data


def validate_models(lists: dict[str, Any]) -> None:
    """Refuse to apply if any banned model id is present."""
    for tier in ("weak", "strong"):
        for entry in lists[tier]:
            model_id = entry if isinstance(entry, str) else entry.get("model", "")
            if model_id in BANNED_IDS:
                die(f"{tier} list contains banned id '{model_id}' (literal 'openrouter/free')")
            for suffix in BANNED_SUFFIXES:
                if model_id.endswith(suffix):
                    die(
                        f"{tier} list contains banned id '{model_id}' "
                        f"(suffix '{suffix}' is rate-limited / broken on OpenRouter)"
                    )


def entry_to_fb(entry: Any, default_provider: str) -> dict[str, str]:
    """Convert a list entry (str or dict) to a fallback_model dict."""
    if isinstance(entry, str):
        return {"provider": default_provider, "model": entry}
    if not isinstance(entry, dict) or "model" not in entry:
        die(f"malformed entry: {entry!r}")
    out = {"provider": entry.get("provider", default_provider), "model": entry["model"]}
    for key in ("base_url", "api_key", "api_mode"):
        if key in entry and entry[key]:
            out[key] = entry[key]
    return out


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        die(f"config file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)


def find_block(d: dict[str, Any], key: str) -> dict[str, Any]:
    """Return the sub-dict at d[key], creating it if missing."""
    if key not in d or d[key] is None:
        d[key] = {}
    if not isinstance(d[key], dict):
        die(f"config.yaml: '{key}' is not a mapping (got {type(d[key]).__name__})")
    return d[key]


def apply(
    lists: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    """Mutate `config` in place and return (config, changes)."""
    changes: list[str] = []
    provider = lists.get("provider", "openrouter")

    weak = lists["weak"]
    strong = lists["strong"]

    model_block = find_block(config, "model")
    if model_block.get("default") != strong[0]:
        changes.append(f"model.default: {model_block.get('default')!r} → {strong[0]!r}")
        model_block["default"] = strong[0]
    if model_block.get("provider") != provider:
        changes.append(f"model.provider: {model_block.get('provider')!r} → {provider!r}")
        model_block["provider"] = provider
    if not model_block.get("base_url"):
        model_block["base_url"] = "https://openrouter.ai/api/v1"
        changes.append("model.base_url: → 'https://openrouter.ai/api/v1' (default)")
    if not model_block.get("api_mode"):
        model_block["api_mode"] = "chat_completions"
        changes.append("model.api_mode: → 'chat_completions' (default)")

    del_block = find_block(config, "delegation")
    if del_block.get("model") != weak[0]:
        changes.append(f"delegation.model: {del_block.get('model')!r} → {weak[0]!r}")
        del_block["model"] = weak[0]
    if del_block.get("provider") != provider:
        changes.append(f"delegation.provider: {del_block.get('provider')!r} → {provider!r}")
        del_block["provider"] = provider

    fallback_chain = [entry_to_fb(e, provider) for e in (strong[1:] + weak)]
    if config.get("fallback_model") != fallback_chain:
        old = config.get("fallback_model")
        config["fallback_model"] = fallback_chain
        changes.append(
            f"fallback_model: {len(old) if isinstance(old, list) else '?'} entries "
            f"→ {len(fallback_chain)} entries"
        )

    return config, changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--dry-run", action="store_true", help="print changes, don't write")
    parser.add_argument("--check", action="store_true", help="exit 1 if config is out of sync")
    parser.add_argument("--lists", type=Path, default=LISTS_FILE)
    parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    args = parser.parse_args()

    lists = load_lists(args.lists)
    validate_models(lists)
    config = load_config(args.config)

    new_config, changes = apply(lists, config)

    if not changes:
        print("sync-models: config is already in sync with model-lists.yaml")
        return 0

    print("sync-models: planned changes:")
    for c in changes:
        print(f"  - {c}")

    if args.check:
        print("sync-models: --check set, exiting 1 (config out of sync)", file=sys.stderr)
        return 1

    if args.dry_run:
        print("sync-models: --dry-run set, not writing")
        return 0

    original_text = args.config.read_text(encoding="utf-8")
    new_text = dump_yaml(new_config)

    header_match = re.match(r"^#.*?(?=\n\w|\Z)", original_text, flags=re.DOTALL)
    header = header_match.group(0) if header_match else ""

    bak = args.config.with_suffix(args.config.suffix + ".bak")
    bak.write_text(original_text, encoding="utf-8")

    args.config.write_text(header + "\n" + new_text, encoding="utf-8")
    print(f"sync-models: wrote {args.config} (backup at {bak})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
