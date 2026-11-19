#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep `tools/puzzy.json` in sync with the puzzy family in `tools/routing.json`.

PARKED 2026-11-17 — not wired anywhere. No runtime consumer reads `apps{}`, and
the distro build never calls this script. While parked, run it manually from the
repo root if the registry needs a refresh:

  python3 tools/pending/sync-puzzy.py --apply

`tools/puzzy.json` has two blocks:

  apps{}   generated — id, name, url, category, fields and fieldCount copied
           from routing.json for the puzzy launcher and its wings
  words{}  hand-authored — the showcase lexicon (default word: love) plus each
           app's view of it

Only `apps{}` is generated. `words{}` and any unknown top-level keys are
preserved verbatim, so the checker never eats hand-written data.

Usage:
  python3 tools/pending/sync-puzzy.py            # report drift
  python3 tools/pending/sync-puzzy.py --apply    # rewrite apps{} in tools/puzzy.json
  python3 tools/pending/sync-puzzy.py --check    # exit 1 when apps{} is stale
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTING = ROOT / "tools/routing.json"
PUZZY = ROOT / "tools/puzzy.json"

SCHEMA = "flove-puzzy-lexicon/1"
FAMILY = [
    "puzzy", "raty", "poly", "fivy", "vizy", "vizy2", "comby",
    "confluenty", "linky", "wisy", "sety", "keys", "loly",
]
COPIED = ("name", "url", "category", "fields", "fieldCount")


def registry(routing: dict) -> dict:
    by_id = {str(a.get("id")): a for a in routing.get("apps", []) if a.get("id")}
    apps = {}
    for app_id in FAMILY:
        app = by_id.get(app_id)
        if app is None:
            continue
        apps[app_id] = {key: app.get(key) for key in COPIED}
    return apps


def diff(expected: dict, current: dict) -> list[str]:
    lines = []
    for app_id, app in expected.items():
        got = current.get(app_id)
        if got is None:
            lines.append(f"  missing  {app_id}")
            continue
        for key in COPIED:
            if got.get(key) != app.get(key):
                lines.append(f"  drift    {app_id}.{key}")
    for app_id in current:
        if app_id not in expected:
            lines.append(f"  extra    {app_id}")
    return lines


def load() -> dict:
    if not PUZZY.exists():
        return {"schema": SCHEMA, "version": 1, "apps": {}, "words": {}}
    with PUZZY.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("schema") != SCHEMA:
        raise SystemExit(f"{PUZZY.name}: schema must be {SCHEMA}")
    return data


def render(data: dict, apps: dict) -> str:
    data["apps"] = apps
    data.setdefault("words", {})
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    expected = registry(routing)
    data = load()
    lines = diff(expected, data.get("apps", {}))

    if "--apply" in sys.argv:
        PUZZY.write_text(render(data, expected), encoding="utf-8")
        print(f"wrote {PUZZY.relative_to(ROOT)} ({len(expected)} apps, {len(data.get('words', {}))} words)")
        return 0

    if "--check" in sys.argv:
        if lines:
            print(f"{PUZZY.relative_to(ROOT)} is stale — run tools/pending/sync-puzzy.py --apply", file=sys.stderr)
            print("\n".join(lines), file=sys.stderr)
            return 1
        print(f"ok: {len(expected)} puzzy apps match routing.json")
        return 0

    if not PUZZY.exists():
        print(f"{PUZZY.relative_to(ROOT)} does not exist; run --apply to create it")
    elif lines:
        print("\n".join(lines))
        print(f"{len(lines)} drift(s); run --apply")
    else:
        print(f"ok: {len(expected)} puzzy apps match routing.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
