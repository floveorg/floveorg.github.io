#!/usr/bin/env python3
"""Page-facing join for development/index.html: hitos + tasks in one file.

  --build  write standards/debates/common.json from milestones.json
  --check  verify common.json is in sync with the register

`milestones.json` stays canonical for hitos and tasks; the PROC chapter is
canonical in `development/AGENTS.md` (see `procedures_source`). `common.json` is
a generated projection: every hito's info-box spec (Deliverable / Done when /
Decision), its plan/doc pointer, its live tasks, a flat task index, the archive
summary and the PROC mirror. Never hand-edit common.json; edit the owning source
and rebuild.

Schema: flove-common/1
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import register_projection as projection
import procedures_source

ROOT = Path(__file__).resolve().parents[1]
MILESTONES = ROOT / "standards/debates/milestones.json"
COMMON = ROOT / "standards/debates/common.json"
SCHEMA = "flove-common/1"

SPEC_RE = re.compile(
    r"Deliverable:\s*(?P<deliverable>.*?)\s*"
    r"(?P<done_marker>Done when|Done \(generated from [^)]+\)):?\s*"
    r"(?P<done>.*?)\s*Decision:\s*(?P<decision>.*)$",
    re.S,
)


def parse_spec(notes: str) -> dict:
    m = SPEC_RE.match(notes.strip())
    if not m:
        return {"deliverable": "", "done": "", "decision": "", "source": ""}
    marker = m.group("done_marker")
    source = ""
    if marker.startswith("Done (generated from"):
        source = re.search(r"generated from ([^)]+)\)", marker).group(1)
    return {
        "deliverable": m.group("deliverable").strip(),
        "done": m.group("done").strip(),
        "decision": m.group("decision").strip(),
        "source": source,
    }


def task_row(t: dict) -> dict:
    ev = t.get("evidence") or {}
    return {
        "id": t.get("id"),
        "stage": t.get("stage"),
        "state": t.get("state"),
        "effort": t.get("effort"),
        "title": t.get("en"),
        "title_es": t.get("es"),
        "criterion": (ev.get("gaps") or [""])[0],
        "apps": ev.get("apps") or [],
        "depends_on": list(t.get("depends_on") or []),
    }


def build() -> dict:
    data = json.loads(MILESTONES.read_text(encoding="utf-8"))
    hitos = []
    tasks: dict[str, dict] = {}
    plans: dict[str, list[str]] = {}
    counts = projection.counts(data)
    for section in data.get("sections", []):
        for box in section.get("subsections", []):
            for m in box.get("milestones", []):
                spec = parse_spec(m.get("notes", ""))
                doc = m.get("source") or ""
                plan = doc.split("#")[0] if doc else ""
                row = {
                    "id": m.get("id"),
                    "title": m.get("en"),
                    "title_es": m.get("es"),
                    "state": m.get("state"),
                    "stage": m.get("stage"),
                    "section": section.get("section"),
                    "field": m.get("section"),
                    "degree": box.get("degree"),
                    "ladder": box.get("ladder"),
                    "doc": doc,
                    "plan": plan,
                    "standards": list(m.get("standards") or []),
                    "depends_on": list(m.get("depends_on") or []),
                    "spec": spec,
                    "tasks": [],
                }
                for t in m.get("tasks") or []:
                    tr = task_row(t)
                    tr["hito_id"] = m.get("id")
                    row["tasks"].append(tr)
                    tasks[tr["id"]] = {
                        "hito_id": m.get("id"),
                        "stage": tr["stage"],
                        "state": tr["state"],
                        "effort": tr["effort"],
                    }
                hitos.append(row)
                if plan:
                    plans.setdefault(plan, []).append(m.get("id"))
    archive = projection.archive_projection(data)
    return {
        "schema": SCHEMA,
        "generated": date.today().isoformat(),
        "sources": {
            "register": "development/standards/debates/milestones.json",
            "plans": "development/standards/debates/plans/index.md",
            "page": "development/index.html",
        },
        "counts": counts,
        "plans": [
            {"path": p, "hitos": ids}
            for p, ids in sorted(plans.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        ],
        "hitos": hitos,
        "tasks": tasks,
        "archive": archive,
        "procedures": procedures_source.load(),
    }


def check() -> int:
    if not COMMON.exists():
        print("FAIL: missing " + str(COMMON))
        return 1
    got = json.loads(COMMON.read_text(encoding="utf-8"))
    want = build()
    if got.get("schema") != SCHEMA:
        print("FAIL: schema %r, expected %r" % (got.get("schema"), SCHEMA))
        return 1
    if got.get("counts") != want["counts"]:
        print("FAIL: counts %r, expected %r" % (got.get("counts"), want["counts"]))
        return 1
    if got.get("hitos") != want["hitos"]:
        print("FAIL: hito specs or tasks differ from the register")
        return 1
    if got.get("tasks") != want["tasks"]:
        print("FAIL: task index differs from the register")
        return 1
    if got.get("archive") != want["archive"]:
        print("FAIL: archive summary differs from the register")
        return 1
    if got.get("plans") != want["plans"]:
        print("FAIL: plan index differs from the register")
        return 1
    if got.get("procedures") != want["procedures"]:
        print("FAIL: procedures mirror differs from the register")
        return 1
    print("OK: common.json — %d hitos, %d live tasks, %d archived"
          % (want["counts"]["hitos"], want["counts"]["live_tasks"],
             want["counts"]["archived_tasks"]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true")
    g.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    data = build()
    COMMON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("built %s — %d hitos, %d live tasks, %d archived"
          % (COMMON.relative_to(ROOT.parent), data["counts"]["hitos"],
             data["counts"]["live_tasks"], data["counts"]["archived_tasks"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
