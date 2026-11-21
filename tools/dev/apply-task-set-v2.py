#!/usr/bin/env python3
"""Apply the third-view task set to milestones.json.

Shape: 1 seed + 3 infant + 3 mature (+1 generalist) per open hito.
Closed hitos (`on`) keep their hito row and move their tasks to tasks_archive.
Mature band: .3 publish (keeps id and edges), .3b verify, .3c decision.

  --dry-run  (default) report the diff, write nothing
  --write    back up milestones.json and apply
  --force    re-apply over an already migrated register

The register stays canonical. Run build-common.py --build afterwards.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "development"
FILE = ROOT / "wiki/work/milestones.json"
TODAY = date.today().isoformat()
VERSION = "v2-third-view"

SPEC_RE = re.compile(
    r"Deliverable:\s*(?P<deliverable>.*?)\s*"
    r"(?P<done_marker>Done when|Done \(generated from [^)]+\)):?\s*"
    r"(?P<done>.*?)\s*Decision:\s*(?P<decision>.*)$",
    re.S,
)


def clean(s: str) -> str:
    return (s or "").strip().rstrip(".").strip()


def parse_notes(notes: str) -> dict:
    m = SPEC_RE.match((notes or "").strip())
    if not m:
        raise ValueError("note does not match the three-line spec: %r" % notes[:120])
    marker = m.group("done_marker")
    source = ""
    if marker.startswith("Done (generated from"):
        source = re.search(r"generated from ([^)]+)\)", marker).group(1)
    return {
        "deliverable": clean(m.group("deliverable")),
        "done": clean(m.group("done")),
        "decision": clean(m.group("decision")),
        "source": source,
    }


def render_note(spec: dict) -> str:
    source = (" · Source: " + spec["source"]) if spec.get("source") else ""
    return ("Deliverable: %s. Done when %s%s. Decision: %s."
            % (spec["deliverable"], spec["done"], source, spec["decision"]))


def gap(task: dict, text: str) -> None:
    ev = task.setdefault("evidence", {})
    ev["by"] = "optimizy"
    ev["apps"] = list(ev.get("apps") or [])
    ev["gaps"] = [text]


def task_id(m: dict, suffix: str) -> str:
    return "%s.%s" % (m["id"], suffix)


def new_task(m: dict, suffix: str, stage: str, effort: str,
             en: str, es: str, criterion: str) -> dict:
    return {
        "id": task_id(m, suffix),
        "en": en,
        "es": es,
        "stage": stage,
        "effort": effort,
        "state": "pendiente",
        "evidence": {"by": "optimizy", "apps": [], "gaps": [criterion]},
        "depends_on": [],
    }


def seed_criterion(title: str) -> str:
    return ("Done when the local definition of %s states its Deliverable, "
            "its Done-when and its Decision, and the Decision is recorded "
            "with an owner." % title)


def publish_criterion(title: str, doc: str) -> str:
    where = doc or "its owner MD"
    return ("Done when %s is published once in the canonical index at %s "
            "and the entry links back to its owner." % (title, where))


def verify_criterion(title: str, done: str) -> str:
    return ("Done when the published %s satisfies its done criterion: %s."
            % (title, done or "its Done-when line"))


def decision_criterion(title: str, decision: str) -> str:
    return ("Done when the decision for %s is recorded with its owner: %s."
            % (title, decision or "the accepted decision"))


def generalist_criterion(title: str, section: str, done: str) -> str:
    return ("Done when %s is implemented across %s and its done criterion "
            "holds: %s." % (title, section, done or "its Done-when line"))


def reshape(data: dict) -> tuple[dict, dict]:
    if (data.get("taskSet") or {}).get("version") == VERSION:
        raise SystemExit("already migrated to %s; pass --force to re-apply" % VERSION)
    archive: list[dict] = []
    dropped: list[tuple[str, str]] = []
    stats = {"open": 0, "closed": 0, "live": 0, "archived": 0,
             "seed": 0, "infant": 0, "mature": 0, "generalist": 0}
    for section in data.get("sections", []):
        for box in section.get("subsections", []):
            for m in box.get("milestones", []):
                spec = parse_notes(m.get("notes", ""))
                m["notes"] = render_note(spec)
                tasks = list(m.get("tasks") or [])
                if m.get("state") == "on":
                    stats["closed"] += 1
                    for t in tasks:
                        a = copy.deepcopy(t)
                        a["hito_id"] = m["id"]
                        a["closed_reason"] = "hito state on; archived by task-set-plan v2"
                        a["closed_on"] = TODAY
                        archive.append(a)
                        stats["archived"] += 1
                    m["tasks"] = []
                    continue
                stats["open"] += 1
                by_suffix = {t["id"].split(".")[-1]: t for t in tasks}
                seed = by_suffix.get("1b") or by_suffix.get("1a")
                if not seed:
                    seed = new_task(m, "1b", "seed", "easy",
                                    "%s — write the local definition and decision" % m["en"],
                                    "%s — escribir la definición local y la decisión" % m["es"],
                                    seed_criterion(m["en"]))
                else:
                    seed["en"] = "%s — write the local definition and decision" % m["en"]
                    seed["es"] = "%s — escribir la definición local y la decisión" % m["es"]
                    seed["stage"] = "seed"
                    gap(seed, seed_criterion(m["en"]))
                infants = []
                for suffix in ("2a", "2b", "2c"):
                    t = by_suffix.get(suffix)
                    if t:
                        if not (t.get("evidence", {}).get("gaps")):
                            gap(t, "Done when the basic-flow case for %s is verified "
                                   "and linked to its owner." % m["en"])
                        infants.append(t)
                mature = by_suffix.get("3")
                if not mature:
                    mature = new_task(m, "3", "mature", "hard",
                                      "%s — publish in the canonical index" % m["en"],
                                      "%s — publicar en el índice canónico" % m["es"],
                                      publish_criterion(m["en"], m.get("source", "")))
                else:
                    mature["en"] = "%s — publish in the canonical index" % m["en"]
                    mature["es"] = "%s — publicar en el índice canónico" % m["es"]
                    gap(mature, publish_criterion(m["en"], m.get("source", "")))
                verify = new_task(
                    m, "3b", "mature", "hard",
                    "%s — verify the published result against its done criterion" % m["en"],
                    "%s — verificar el resultado publicado contra su criterio de hecho" % m["es"],
                    verify_criterion(m["en"], spec["done"]))
                decision = new_task(
                    m, "3c", "mature", "easy",
                    "%s — record the decision and its owner" % m["en"],
                    "%s — registrar la decisión y su dueño" % m["es"],
                    decision_criterion(m["en"], spec["decision"]))
                generalist = by_suffix.get("4")
                if generalist:
                    gap(generalist, generalist_criterion(
                        m["en"], section.get("section", ""), spec["done"]))
                m["tasks"] = [seed] + infants + [mature, verify, decision]
                if generalist:
                    m["tasks"].append(generalist)
                stats["seed"] += 1
                stats["infant"] += len(infants)
                stats["mature"] += 3
                stats["generalist"] += 1 if generalist else 0
                stats["live"] += len(m["tasks"])

    # Drop task edges that pointed at archived tasks (all 15 have a hito edge).
    live_ids = {t["id"] for s in data.get("sections", [])
                for b in s.get("subsections", [])
                for m in b.get("milestones", [])
                for t in (m.get("tasks") or [])}
    for s in data.get("sections", []):
        for b in s.get("subsections", []):
            for m in b.get("milestones", []):
                for t in (m.get("tasks") or []):
                    deps = list(t.get("depends_on") or [])
                    kept = [d for d in deps if d in live_ids]
                    if kept != deps:
                        for d in deps:
                            if d not in live_ids:
                                dropped.append((t["id"], d))
                        t["depends_on"] = kept

    data["tasks_archive"] = sorted(archive, key=lambda t: t["id"])
    data["taskSet"] = {
        "version": VERSION,
        "date": TODAY,
        "shape": "1 seed + 3 infant + 3 mature (+1 generalist) per open hito",
        "live": stats["live"],
        "archived": stats["archived"],
        "cap": stats["live"],
        "archive_policy": "closed hito keeps its row; its tasks move to tasks_archive",
    }
    return data, {"stats": stats, "dropped": dropped}


def validate(data: dict) -> list[str]:
    errors = []
    hitos = [m for s in data.get("sections", [])
             for b in s.get("subsections", [])
             for m in b.get("milestones", [])]
    live = [t for m in hitos for t in (m.get("tasks") or [])]
    archive = list(data.get("tasks_archive") or [])
    ids = [t["id"] for t in live]
    aids = [t["id"] for t in archive]
    if len(hitos) != 326:
        errors.append("expected 326 hitos, got %d" % len(hitos))
    if len(live) != 1559:
        errors.append("expected 1559 live tasks, got %d" % len(live))
    if len(archive) != 805:
        errors.append("expected 805 archived tasks, got %d" % len(archive))
    if len(ids) != len(set(ids)):
        errors.append("duplicate live task ids")
    if len(aids) != len(set(aids)):
        errors.append("duplicate archived task ids")
    if set(ids) & set(aids):
        errors.append("live and archived ids overlap")
    for m in hitos:
        tasks = m.get("tasks") or []
        if m.get("state") == "on":
            if tasks:
                errors.append("%s is closed but has %d tasks" % (m["id"], len(tasks)))
        else:
            want = 8 if m.get("stage") in ("grown", "full") else 7
            if len(tasks) != want:
                errors.append("%s has %d tasks, expected %d" % (m["id"], len(tasks), want))
        note = m.get("notes", "")
        for marker in ("Deliverable:", "Done when", "Decision:"):
            if note.count(marker) != 1:
                errors.append("%s: %s appears %d times" % (m["id"], marker, note.count(marker)))
        for t in tasks:
            if not (t.get("evidence", {}).get("gaps") or [""])[0].strip():
                errors.append("%s: empty criterion" % t["id"])
            for d in t.get("depends_on") or []:
                if d not in ids:
                    errors.append("%s: dangling task dependency %s" % (t["id"], d))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="apply the reshape")
    ap.add_argument("--force", action="store_true",
                    help="re-apply from the newest milestones.json.bak-* backup")
    args = ap.parse_args()
    source = FILE
    if (json.loads(FILE.read_text(encoding="utf-8")).get("taskSet") or {}).get("version") == VERSION:
        if not args.force:
            raise SystemExit("already migrated; pass --force to re-apply from the backup")
        backups = sorted(FILE.parent.glob(FILE.name + ".bak-*"))
        if not backups:
            raise SystemExit("already migrated and no backup found; refusing to re-apply")
        source = backups[-1]
        print("re-applying from", source.name)
    data = json.loads(source.read_text(encoding="utf-8"))
    out, report = reshape(copy.deepcopy(data))
    errors = validate(out)
    s = report["stats"]
    print("open %d · closed %d · live %d · archived %d"
          % (s["open"], s["closed"], s["live"], s["archived"]))
    print("seed %d · infant %d · mature %d · generalist %d"
          % (s["seed"], s["infant"], s["mature"], s["generalist"]))
    print("dropped %d archived task edges:" % len(report["dropped"]))
    for src, dep in report["dropped"]:
        print("  %s -> %s" % (src, dep))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("validation OK")
    if not args.write:
        print("dry run — pass --write to apply")
        return 0
    backup = FILE.with_name(FILE.name + ".bak-" + TODAY)
    if not backup.exists():
        shutil.copy2(FILE, backup)
        print("backup:", backup.name)
    FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print("wrote", FILE.relative_to(ROOT.parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
