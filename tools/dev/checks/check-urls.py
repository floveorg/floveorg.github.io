#!/usr/bin/env python3
"""Count public URLs with the archived development prefix and enforce the baseline.

S0-S3 baseline mode: fail only above the recorded 198. From S4 run --strict.

  python3 tools/dev/checks/check-urls.py
  python3 tools/dev/checks/check-urls.py --strict
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "dev"))
import paths  # noqa: E402

OLD_PREFIX = "https://flove.org/development/wiki/"
BASELINE = 0


def candidates() -> list[Path]:
    return [
        paths.DEVELOPMENT / "index.html",
        paths.COMMON,
        paths.MILESTONES,
        paths.STANDARDS / "community" / "index.html",
        paths.AGENTS,
        ROOT / "tools" / "dev" / "skilly.py",
        paths.STANDARDS / "README.md",
        paths.STANDARDS / "contract.md",
        paths.STANDARDS / "data" / "ai" / "skills" / "questy" / "index.html",
        paths.STANDARDS / "data" / "ai" / "skills" / "jsony" / "SKILL.md",
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    old = OLD_PREFIX
    rows = []
    total = 0
    for path in candidates():
        if not path.exists():
            continue
        n = path.read_text(errors="ignore").count(old)
        if n:
            rows.append((path.relative_to(ROOT).as_posix(), n))
            total += n
    if args.strict and total:
        print(f"FAIL: {total} public URL(s) still point at the old prefix")
        for rel, n in rows[:20]:
            print(f"  {rel}: {n}")
        return 1
    if total > BASELINE:
        print(f"FAIL: {total} public URL(s) > baseline {BASELINE}")
        for rel, n in rows[:20]:
            print(f"  {rel}: {n}")
        return 1
    print(f"{'OK' if not args.strict else 'OK'}: {total} public URL(s) pending "
          f"(baseline {BASELINE}, strict={args.strict})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
