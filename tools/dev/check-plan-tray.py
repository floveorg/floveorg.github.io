#!/usr/bin/env python3
"""Validate the child-plan tray and plan frontmatter.

Usage: python3 tools/dev/check-plan-tray.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "development/wiki/plans"
REGISTER = ROOT / "development/wiki/work/milestones.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    errors = []
    tray = PLANS / "debates/README.md"
    if not tray.exists():
        errors.append("missing plans/debates/README.md")

    for path in PLANS.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        if path == tray or path.name in ("index.md", "conflicts.md"):
            continue
        text = path.read_text(errors="ignore")
        if not text.startswith("---\n"):
            errors.append(f"missing frontmatter: {rel}")
            continue
        for key in ("status:", "section:", "created:", "also:"):
            if key not in text.split("\n---", 1)[0]:
                errors.append(f"missing {key}: {rel}")

    data = json.loads(REGISTER.read_text())
    owners = set()
    for sec in data.get("sections", []):
        for sub in sec.get("subsections", []):
            for h in sub.get("milestones", []):
                for t in h.get("tasks", []):
                    if "plans/debates/" in str(t.get("owner", "")):
                        owners.add(t.get("id"))
    if owners:
        errors.append(f"tray used as owner by {len(owners)} task(s): {sorted(owners)[:5]}")

    if errors:
        print(f"FAIL: {len(errors)} plan-tray error(s)")
        for e in errors[:20]:
            print("  -", e)
        return 1
    print("OK: plan frontmatter and tray valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
