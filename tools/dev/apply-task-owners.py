#!/usr/bin/env python3
"""Apply the task-owner migration patch to milestones.json.

Phase 2b: every live task gets its new page owner from task-recycle.json. The
original value is kept in `owner_origin`. This does not respec titles or mark
anything done; the respec audit stays separate.

Usage:
  python3 tools/dev/apply-task-owners.py --plan
  python3 tools/dev/apply-task-owners.py --apply
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "development/wiki/work/milestones.json"
PATCH = ROOT / "development/wiki/task-recycle.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not (args.plan or args.apply):
        ap.error("choose --plan or --apply")

    data = json.loads(REGISTER.read_text())
    patch = json.loads(PATCH.read_text())
    by_id = {t["id"]: t for t in patch["tasks"]}

    seen = set()
    changes = 0
    missing = []
    for section in data.get("sections", []):
        for sub in section.get("subsections", []):
            for hito in sub.get("milestones", []):
                for task in hito.get("tasks", []):
                    row = by_id.get(task.get("id"))
                    if not row:
                        missing.append(task.get("id"))
                        continue
                    seen.add(task.get("id"))
                    old = task.get("owner")
                    new = row["owner_new"]
                    if old != new:
                        changes += 1
                        if args.apply:
                            if "owner_origin" not in task:
                                task["owner_origin"] = old
                            task["owner"] = new

    print(f"live tasks: {len(seen)}; changes: {changes}; missing: {len(missing)}")
    if missing:
        print("missing patch rows:", ", ".join(missing[:10]))
        return 1
    if args.plan:
        return 0
    REGISTER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"applied {changes} owner changes to {REGISTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
