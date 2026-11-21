#!/usr/bin/env python3
"""Read-only restore drill for the Work archive (NEW-WORK-RESTORE-DRILL).

Reopens one closed hito on an in-memory copy of milestones.json and checks that
its tasks come back from tasks_archive with no id collision or row loss. Never
writes the register.

  python3 tools/dev/check-restore.py [--hito ID]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import register_projection as projection

ROOT = Path(__file__).resolve().parents[2] / "development"
REGISTER = ROOT / "wiki/work/milestones.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hito", help="closed hito id to reopen (default: first with archived tasks)")
    args = ap.parse_args()
    register = projection.load_register(REGISTER)
    hitos = {m.get("id"): m for m in projection.hitos(register)}
    archive = register.get("tasks_archive") or []
    candidates = [h for h in hitos.values()
                  if h.get("state") == "on"
                  and any(t.get("hito_id") == h.get("id") for t in archive)]
    if args.hito:
        hito = hitos.get(args.hito)
        if not hito or hito.get("state") != "on":
            print("FAIL: %s is not a closed hito" % args.hito)
            return 1
    else:
        if not candidates:
            print("FAIL: no closed hito has archived tasks")
            return 1
        hito = candidates[0]
    hid = hito["id"]
    owned = [t for t in archive if t.get("hito_id") == hid]
    if not owned:
        print("FAIL: %s has no archived tasks" % hid)
        return 1
    live = projection.live_tasks(register)
    restored_ids = [t.get("id") for t in owned]
    errors = []
    collided = sorted(set(restored_ids) & set(live))
    if collided:
        errors.append("id collision on reopen: " + ", ".join(collided))
    if len(restored_ids) != len(set(restored_ids)):
        errors.append("duplicate archived ids for " + hid)
    remaining = [t for t in archive if t.get("hito_id") != hid]
    if len(remaining) + len(owned) != len(archive):
        errors.append("archive row count changes on restore")
    if hito.get("tasks"):
        errors.append("closed hito already has live tasks")
    for t in owned:
        for key in ("id", "en", "es", "stage", "effort", "state", "evidence"):
            if key not in t:
                errors.append("%s lost %s" % (t.get("id"), key))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("OK: %s — %d task(s) restore cleanly; live %d, archive %d -> %d"
          % (hid, len(owned), len(live), len(archive), len(remaining)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
