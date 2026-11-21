#!/usr/bin/env python3
"""Resolve old register paths to the new wiki pages.

Reads `development/wiki/register-path-inventory.json` (the phase-0/current
inventory) and rewrites the register fields it covers. Owners are already
migrated; this tool handles sources, standards URLs, gaps, notes, tickets, docs
and the moves inbox.

Usage:
  python3 tools/dev/wiki-resolve.py --plan
  python3 tools/dev/wiki-resolve.py --write
  python3 tools/dev/wiki-resolve.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "development/wiki/work/milestones.json"
INV = ROOT / "development/wiki/register-path-inventory.json"
REPORT = ROOT / "development/wiki/register-path-migration.json"

FIELDS = {"owner", "source", "notes", "standards", "docs", "gaps", "moves_inbox"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.plan or args.write or args.check):
        ap.error("choose --plan, --write or --check")

    inv = json.loads(INV.read_text())
    items = inv["items"]

    by_old: dict[str, Counter] = defaultdict(Counter)
    by_field: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        if item["action"] == "keep" or not item["target"]:
            continue
        old = item["old"]
        by_old[old][item["target"]] += 1
        by_field[item["field"].split(".")[-1].split("[")[0]].append(item)

    mapping: dict[str, str] = {}
    ambiguous = []
    for old, counter in by_old.items():
        target, n = counter.most_common(1)[0]
        mapping[old] = target
        if len(counter) > 1:
            ambiguous.append({"old": old, "chosen": target, "alternatives": dict(counter)})

    olds = sorted(mapping, key=len, reverse=True)
    changes = 0
    by_kind = Counter()

    def rewrite(text: str) -> tuple[str, int]:
        if not isinstance(text, str):
            return text, 0
        count = 0
        for old in olds:
            if old and old in text:
                count += text.count(old)
                text = text.replace(old, mapping[old])
        return text, count

    data = json.loads(REGISTER.read_text())

    def walk(node):
        nonlocal changes
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if k in ("owner_origin", "origin", "provenance"):
                    continue
                if isinstance(v, str):
                    new, n = rewrite(v)
                    if n:
                        node[k] = new
                        changes += n
                        by_kind[k] += n
                elif isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                if isinstance(v, str):
                    new, n = rewrite(v)
                    if n:
                        node[i] = new
                        changes += n
                        by_kind["list"] += n
                elif isinstance(v, (dict, list)):
                    walk(v)

    if args.check:
        moving = 0
        for item in items:
            if item["action"] != "keep":
                moving += 1
        print(f"inventory: {inv['counts']['occurrences']} occurrences, {moving} moving")
        if moving:
            print("FAIL: moving paths remain; use --write")
            return 1
        print("OK: no moving paths remain")
        return 0

    walk(data)
    report = {
        "schema": "flove-register-path-migration/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inventory": str(INV.relative_to(ROOT)),
        "changes": changes,
        "by_field": dict(sorted(by_kind.items())),
        "ambiguous": ambiguous[:50],
        "ambiguous_count": len(ambiguous),
    }

    if args.plan:
        print(json.dumps({"changes": changes, "by_field": dict(by_kind), "ambiguous": len(ambiguous)}, indent=2))
        for a in ambiguous[:10]:
            print("ambiguous:", a["old"], "->", a["chosen"], "| alternatives", len(a["alternatives"]))
        return 0

    REGISTER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {REGISTER.relative_to(ROOT)}; {changes} replacements")
    print(json.dumps(report["by_field"], indent=2))
    if ambiguous:
        print(f"warning: {len(ambiguous)} ambiguous old paths used the majority target")
    return 0


if __name__ == "__main__":
    sys.exit(main())
