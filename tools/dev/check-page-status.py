#!/usr/bin/env python3
"""Fail when a live owner is still a draft or a phase-1 skeleton.

Usage:
  python3 tools/dev/check-page-status.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "development/wiki/wiki.json"
REGISTER = ROOT / "development/wiki/work/milestones.json"
STATUS = re.compile(r"^status:\s*(\w+)", re.M)
SKELETON = re.compile(r"Phase 1 skeleton|Do not cite it as an owner yet", re.I)
SCAFFOLD = re.compile(r"^## Migration$|Pilot migration \(phase 2\)", re.M)
ARCHIVE_LINK = re.compile(r"\]\([^)]*archive/old")


def declared_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = STATUS.search(text)
    return match.group(1).strip().lower() if match else "missing"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    wiki = json.loads(WIKI.read_text())
    errors: list[str] = []

    pages = [p for p in wiki.get("pages", []) if p.get("kind") in {"topic", "map"}]
    plans = wiki.get("plans", [])
    for entry in pages + plans:
        path = ROOT / entry["path"]
        if not path.exists():
            errors.append(f"missing page: {entry['path']}")
            continue
        if entry["path"] == "development/wiki/plans/debates/README.md":
            continue  # convention-only tray note, never an owner
        status = declared_status(path)
        allowed = {"stable", "live"}
        if entry.get("kind") == "map" or entry["path"].endswith("plans/conflicts.md"):
            allowed = {"stable", "live", "active", "missing"}
        if status not in allowed:
            errors.append(f"{entry['path']}: status is {status!r}, expected {'/'.join(sorted(allowed))}")
        text = path.read_text(encoding="utf-8", errors="replace")
        if SKELETON.search(text):
            errors.append(f"{entry['path']}: still carries a Phase 1 skeleton banner")
        if entry.get("kind") in {"topic", "map"} and SCAFFOLD.search(text):
            errors.append(f"{entry['path']}: still carries migration scaffolding")
        if entry.get("kind") == "topic" and ARCHIVE_LINK.search(text):
            errors.append(f"{entry['path']}: stable page links to archive/old")

    draft_owners: dict[str, int] = {}
    register = json.loads(REGISTER.read_text())
    for section in register.get("sections", []):
        for box in section.get("subsections", []):
            for hito in box.get("milestones", []):
                for task in hito.get("tasks", []):
                    owner = (task.get("owner") or "").split("#")[0]
                    if not owner or not owner.endswith(".md"):
                        continue
                    path = ROOT / owner
                    if path.exists() and declared_status(path) not in {"stable", "live"}:
                        draft_owners[owner] = draft_owners.get(owner, 0) + 1
    for owner, count in sorted(draft_owners.items()):
        errors.append(f"{count} task(s) point at a draft owner: {owner}")

    if errors:
        print(f"FAIL: {len(errors)} page-status error(s)")
        for error in errors[:40]:
            print(f"  - {error}")
        return 1
    print(f"OK: {len(pages)} live pages and {len(plans)} plans checked; no task owns a draft page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
