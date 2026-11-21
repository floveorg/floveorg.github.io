#!/usr/bin/env python3
"""Check narrative register counts against common.json.

Usage: python3 tools/dev/check-counts.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "development/wiki/work/common.json"
FILES = [
    ROOT / "development/standards/README.md",
    ROOT / "development/wiki/work/pendings.md",
    ROOT / "development/wiki/INDEX.md",
]
STALE = ["424 items", "312 milestones", "1,455 live", "76 rows", "425-item", "425 items"]
STALE_RX = [r"\b312\b", r"\b424\b", r"\b1,455\b", r"\b1455\b"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    c = json.loads(COMMON.read_text())["counts"]
    expected = {
        "hitos": c["hitos"],
        "live": c["live_tasks"],
        "archived": c["archived_tasks"],
        "features": c["hitos"] + 37 + 75,
    }
    hits = []
    for path in FILES:
        if not path.exists():
            continue
        text = path.read_text(errors="ignore")
        for s in STALE:
            if s in text:
                hits.append((path.relative_to(ROOT).as_posix(), s))
        for rx in STALE_RX:
            if re.search(rx, text):
                hits.append((path.relative_to(ROOT).as_posix(), rx))
    print("expected:", expected)
    if hits:
        print(f"FAIL: {len(hits)} stale narrative count(s)")
        for rel, s in hits:
            print(f"  {rel}: {s}")
        return 1
    print("OK: no stale narrative counts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
