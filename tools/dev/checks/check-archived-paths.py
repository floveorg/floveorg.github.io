#!/usr/bin/env python3
"""Fail on archived-away paths in live files.

This is not check-archive.py: that one verifies archive checksums; this one
fails when a live file still references a path whose content was archived away.
`archived` is the only lifecycle label; older prose said `retired` or `frozen`.

Usage: python3 tools/dev/checks/check-archived-paths.py --check
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARCHIVED_PATHS = [
    "development/wiki/",
    "tools/dev/wiki/",
    "tools/dev/work/",
    "standards/AI/",
    "standards/Frontend/",
    "standards/Backend/",
    "standards/Community/",
    "standards/Data/",
    "development/standards/debates/",
    "development/standards/apps/",
    "development/standards/backend.md",
    "development/standards/adoption.md",
    "development/standards/worldview.md",
    "development/scripts/",
    "development/standards/scripts/",
    "docs/development/INDEX.md",
    "standards/debates/",
    "standards/apps/",
    "standards/backend.md",
    "standards/adoption.md",
    "standards/worldview.md",
]
SUFFIXES = {".md", ".html", ".json", ".py", ".sh", ".mjs", ".yml", ".yaml"}
SKIP = {
    "development/standards/AI",
    "development/standards/Backend",
    "development/standards/Community",
    "development/standards/Data",
    "development/standards/Frontend",
    "apps",
    "whole",
    "docs",
    "projects",
    "kb",
    "development/addons",
    "development/blog",
    "404.html",
    "tools/apps/v1/build-aliases.mjs",
    "tools/dev/checks/check-archive.py",
    "tools/dev/checks/check-doc-paths.py",
    "tools/dev/checks/check-paths.py",
    "tools/dev/checks/check-urls.py",
    "development/standards/vocabulary.html",
    "migration",
    "development/archive",
    "development/standards/debates",
    "development/standards/apps",
    "development/archive/old/docs-wiki-migration-plan.md",
    "development/archive/old/docs-migration-baseline.md",
    "development/register-path-inventory.json",
    "development/port-ledger.json",
    "tools/dev/checks/check-archived-paths.py",
    "development/pages.json",
    "tools/dev/checks/page-inventory.py",
    "tools/dev/checks/page-resolve.py",
    "development/standards/backend.md",
    "development/standards/adoption.md",
    "development/standards/worldview.md",
}
# Hidden/build/vendor trees are never live documentation; prune them so the
# walk never descends into .git, caches, node_modules or packaged vendor copies.
PRUNE_DIRS = {
    "__pycache__", "build", "dist", "vendor", "node_modules", "venv", ".venv",
    "site-packages", "target", "coverage", ".cache", ".mypy_cache",
    ".pytest_cache", ".tox", ".next", ".idea", ".vscode",
}


def live_files():
    """Yield live files, pruning hidden/build/vendor directories in place."""
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=True):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith(".") and d not in PRUNE_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix in SUFFIXES and path.is_file():
                yield path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    hits = []
    counts = Counter()
    for path in live_files():
        rel = path.relative_to(ROOT).as_posix()
        if any(rel == s or rel.startswith(s + "/") for s in SKIP):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Provenance fields keep old paths by design; they are not live links.
        text = re.sub(r'"(?:owner_origin|origin|migrated_from)"\s*:\s*"[^"]*"', '', text)
        for old in ARCHIVED_PATHS:
            n = text.count(old)
            if n:
                hits.append((rel, old, n))
                counts[old] += n

    if hits:
        print(f"FAIL: {sum(counts.values())} archived-path references in {len(hits)} file(s)")
        for old, n in counts.most_common():
            print(f"  {n:4} {old}")
        for rel, old, n in hits[:20]:
            print(f"  {rel}: {n} × {old}")
        return 1
    print("OK: no archived-away paths in live files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
