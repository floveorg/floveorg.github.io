#!/usr/bin/env python3
"""Audit the live task queue for the docs-wiki rebuild.

Phase 2a: every live task gets its new page owner and a recycle action. The
current queue is scaffold-only (no evidence), so the default action is `respec`;
`keep` requires a real evidence pointer, and `archive` requires an owner reason.

Usage:
  python3 tools/dev/build-task-recycle.py --write
  python3 tools/dev/build-task-recycle.py --check
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
DEV = ROOT / "development"
REGISTER = DEV / "wiki/work/milestones.json"
MANIFEST = DEV / "wiki/wiki.json"
OUT_JSON = DEV / "wiki/task-recycle.json"
OUT_MD = DEV / "wiki/task-recycle.md"

SUFFIX = re.compile(r"\.([0-9]+[a-z]*)$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("choose --write or --check")

    data = json.loads(REGISTER.read_text())
    manifest = json.loads(MANIFEST.read_text())
    field_map = manifest["field_map"]
    pages = {p["id"]: p for p in manifest["pages"] if p["kind"] == "topic"}

    rows = []
    for section in data.get("sections", []):
        top = section.get("section", "")
        for sub in section.get("subsections", []):
            for hito in sub.get("milestones", []):
                field = f"{top}/{hito.get('section', '')}"
                page_path = field_map.get(field)
                page = next((p for p in pages.values() if p["path"] == page_path), None)
                if not page:
                    continue
                for task in hito.get("tasks", []):
                    evidence = task.get("evidence", {})
                    pointer = evidence.get("pointer", {})
                    has_evidence = bool(pointer.get("kind") and pointer.get("value"))
                    m = SUFFIX.search(task.get("id", ""))
                    suffix = m.group(1) if m else ""
                    if has_evidence:
                        action, reason = "keep", "evidence-present"
                    else:
                        action = "respec"
                        reason = "template-stage" if suffix else "no-evidence"
                    rows.append(
                        {
                            "id": task.get("id"),
                            "hito": hito.get("id"),
                            "title": task.get("en", ""),
                            "state": task.get("state", ""),
                            "effort": task.get("effort", ""),
                            "field": field,
                            "chapter": field.replace("/", "-"),
                            "owner_current": task.get("owner"),
                            "owner_new": page["path"],
                            "page": page["id"],
                            "suffix": suffix,
                            "action": action,
                            "reason": reason,
                            "has_evidence": has_evidence,
                            "evidence_kind": pointer.get("kind"),
                            "evidence_value": pointer.get("value"),
                        }
                    )

    by_page: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        by_page[r["page"]][r["action"]] += 1
        by_page[r["page"]]["total"] += 1
    actions = Counter(r["action"] for r in rows)
    payload = {
        "schema": "flove-task-recycle/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": str(REGISTER.relative_to(ROOT)),
        "counts": {
            "tasks": len(rows),
            "keep": actions["keep"],
            "respec": actions["respec"],
            "archive": actions["archive"],
            "no_evidence": sum(1 for r in rows if not r["has_evidence"]),
        },
        "by_page": {p: dict(c) for p, c in sorted(by_page.items())},
        "tasks": rows,
    }

    if args.check:
        if not OUT_JSON.exists():
            print(f"missing {OUT_JSON.relative_to(ROOT)}")
            return 1
        current = json.loads(OUT_JSON.read_text())
        if current.get("counts") != payload["counts"]:
            print("stale: task counts differ from the register")
            return 1
        print(f"OK: {payload['counts']}")
        return 0

    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# Task recycle audit",
        "",
        f"> Generated from `{REGISTER.relative_to(ROOT)}`.",
        f"> {payload['counts']['tasks']} live tasks · {payload['counts']['respec']} respec · "
        f"{payload['counts']['keep']} keep · {payload['counts']['archive']} archive.",
        "",
        f"The current queue is scaffold-only: every task is `pendiente`. "
        f"{payload['counts']['keep']} carry an `evidence.pointer` and "
        f"{payload['counts']['no_evidence']} do not. `respec` means PROC-08 supplies a "
        "concrete title, done criterion, page owner and `{kind, value}`; the task id "
        "and hito stay.",
        "",
        "| Page | Tasks | Respec | Keep | Archive |",
        "|---|---:|---:|---:|---:|",
    ]
    for p, c in sorted(by_page.items()):
        lines.append(
            f"| `{p}` | {c['total']} | {c['respec']} | {c['keep']} | {c['archive']} |"
        )
    lines += [
        "",
        "No task is marked done by this audit. Archiving needs the owner’s sign-off.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(json.dumps(payload["counts"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
