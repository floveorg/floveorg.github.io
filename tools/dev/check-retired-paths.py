#!/usr/bin/env python3
"""Fail on retired paths in live files.

Usage: python3 tools/dev/check-retired-paths.py --check
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RETIRED = [
    "development/standards/debates/",
    "development/standards/apps/",
    "development/standards/backend.md",
    "development/standards/adoption.md",
    "development/standards/worldview.md",
    "development/scripts/",
    "development/standards/scripts/",
    "development/standards/AGENTS.md",
    "standards/AGENTS.md",
    "docs/development/INDEX.md",
    "standards/debates/",
    "standards/apps/",
    "standards/backend.md",
    "standards/adoption.md",
    "standards/worldview.md",
]
SUFFIXES = {".md", ".html", ".json", ".py", ".sh", ".mjs", ".yml", ".yaml"}
SKIP = {
    "development/wiki/archive",
    "development/standards/debates",
    "development/standards/apps",
    "development/docs-wiki-migration-plan.md",
    "development/docs-migration-baseline.md",
    "development/wiki/register-path-inventory.json",
    "development/wiki/register-path-inventory.md",
    "development/wiki/register-path-inventory.baseline.json",
    "development/wiki/port-ledger.json",
    "development/wiki/port-ledger.skeleton.json",
    "development/wiki/task-recycle.json",
    "development/wiki/task-recycle.md",
    "development/wiki/chapter-map.json",
    "development/wiki/chapter-map.md",
    "development/wiki/field-map-review.json",
    "development/wiki/field-map-review.md",
    "development/wiki/register-path-migration.json",
    "tools/dev/check-retired-paths.py",
    "development/wiki/wiki.json",
    "tools/dev/wiki-inventory.py",
    "tools/dev/wiki-resolve.py",
    "tools/dev/port-ledger-mark.py",
    "tools/dev/apply-task-owners.py",
    "tools/dev/build-field-map-review.py",
    "tools/dev/build-task-recycle.py",
    "tools/dev/build-wiki-skeleton.py",
    "tools/dev/build-port-ledger.py",
    "development/standards/backend.md",
    "development/standards/adoption.md",
    "development/standards/worldview.md",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    hits = []
    counts = Counter()
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(rel == s or rel.startswith(s + "/") for s in SKIP):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        # Provenance fields keep old paths by design; they are not live links.
        text = re.sub(r'"(?:owner_origin|origin|migrated_from)"\s*:\s*"[^"]*"', '', text)
        for old in RETIRED:
            n = text.count(old)
            if n:
                hits.append((rel, old, n))
                counts[old] += n

    if hits:
        print(f"FAIL: {sum(counts.values())} retired-path references in {len(hits)} file(s)")
        for old, n in counts.most_common():
            print(f"  {n:4} {old}")
        for rel, old, n in hits[:20]:
            print(f"  {rel}: {n} × {old}")
        return 1
    print("OK: no retired paths in live files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
