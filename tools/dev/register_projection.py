#!/usr/bin/env python3
"""Shared projections of milestones.json for Work, common.json and jsony.

`milestones.json` is the only authority. Every consumer that needs the archive,
the queue policy or the register counts calls this module so a new field can be
added once. Generated files never invent these values locally.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "development"
MILESTONES = ROOT / "wiki/work/milestones.json"


def load_register(path: Path | None = None) -> dict:
    return json.loads((path or MILESTONES).read_text(encoding="utf-8"))


def hitos(register: dict) -> list[dict]:
    return [m for area in register.get("sections", [])
            for box in area.get("subsections", [])
            for m in box.get("milestones", [])]


def live_tasks(register: dict) -> dict[str, dict]:
    return {t.get("id"): t for m in hitos(register) for t in (m.get("tasks") or [])}


def reason_code(reason: str | None) -> str:
    """Short taxonomy label for a free-text closed_reason."""
    r = (reason or "").lower()
    if r.startswith("hito state on") or "archived by task-set-plan" in r:
        return "closed_hito"
    if "supersed" in r:
        return "superseded"
    if "done" in r or "apply-moves" in r:
        return "done"
    return "other"


def archive_projection(register: dict, detailed: bool = False) -> list[dict]:
    """Compact archive rows; `detailed` adds the fields only Work renders."""
    owner = {}
    for area in register.get("sections", []):
        for box in area.get("subsections", []):
            for m in box.get("milestones", []):
                owner[m.get("id")] = area.get("section")
    out = []
    for t in register.get("tasks_archive") or []:
        row = {
            "id": t.get("id"),
            "hito_id": t.get("hito_id"),
            "stage": t.get("stage"),
            "state": t.get("state"),
            "effort": t.get("effort"),
            "title": t.get("en"),
            "closed_reason": t.get("closed_reason"),
            "closed_on": t.get("closed_on"),
            "reason_code": reason_code(t.get("closed_reason")),
        }
        if detailed:
            ev = t.get("evidence") or {}
            row.update({
                "section": owner.get(t.get("hito_id"), ""),
                "title_es": t.get("es"),
                "criterion": (ev.get("gaps") or [""])[0],
            })
        out.append(row)
    return out


def queue_policy(register: dict) -> dict:
    return dict((register.get("taskSet") or {}).get("queuePolicy") or {})


def counts(register: dict) -> dict:
    ms = hitos(register)
    return {
        "hitos": len(ms),
        "open": sum(1 for m in ms if m.get("state") != "on"),
        "closed": sum(1 for m in ms if m.get("state") == "on"),
        "live_tasks": len(live_tasks(register)),
        "archived_tasks": len(register.get("tasks_archive") or []),
    }


# PROC-10: choice_weight is orthogonal to effort. It scores how consequential a
# decision is, so tasky knows how much to ask and Work can filter by it. Never
# changes a stage, a state or the PROC-07 order — it only adds a question depth.
CHOICE_CLASSES = ("directo", "ramificado", "estructurante")
CHOICE_DEPTH = {"directo": 0, "ramificado": 1, "estructurante": 3}
DECISION_KEYWORDS = ("vs", "or", "which", "who")
CANONICAL_OWNERS = (
    (r"(^|/)routing\.json$", "route"),
    (r"(^|/)frontend\.md$", "route"),
    (r"(^|/)vocabulary\.html$", "route"),
    (r"flove-[a-z0-9-]+|flove-fields|common\.json|milestones\.json|work-moves\.json",
     "envelope"),
    (r"(^|/)(INDEX|README)\.md$|(^|/)index\.md$", "index"),
    (r"(^|/)backend\.md$|(^|/)export\.md$|(^|/)schema", "schema"),
)


def canonical_owner(path: str) -> str:
    """Kind of canonical artefact an owner path edits, or '' for a local doc."""
    for pattern, kind in CANONICAL_OWNERS:
        if re.search(pattern, path or "", re.I):
            return kind
    return ""


def decision_of(hito: dict) -> str:
    notes = hito.get("notes") or ""
    return notes.split(" Decision: ", 1)[1].strip() if " Decision: " in notes else ""


def decision_options(decision: str) -> tuple[str, str]:
    """A = owner default, B = the explicit alternative or the open question."""
    text = (decision or "").strip().rstrip(".")
    parts = re.split(r"\s+(?:vs|or)\s+", text, flags=re.I)
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    if text:
        return text, "Resolve “%s” in the owner doc and record the answer in the hito Decision" % text
    return "", ""


def unlocked_by(register: dict) -> Counter:
    """Open hitos depending on each open hito — the PROC-07 unlock rank."""
    open_h = [m for m in hitos(register) if m.get("state") != "on"]
    open_ids = {m["id"] for m in open_h}
    return Counter(dep for m in open_h for dep in (m.get("depends_on") or [])
                   if dep in open_ids)


class ChoiceIndex:
    """Precomputed graph signals behind PROC-10; one instance per command/build."""

    def __init__(self, register: dict):
        self.register = register
        all_hitos = hitos(register)
        self.open = [m for m in all_hitos if m.get("state") != "on"]
        live = live_tasks(register)
        self.unlock = unlocked_by(register)
        # g = dependencies this task generates: other live tasks naming it.
        self.generated = Counter(
            dep for t in live.values() for dep in (t.get("depends_on") or [])
            if dep in live)
        # fan-out = open hitos that reference the artefact as source, standard
        # or task owner (counted once per hito).
        fan = Counter()
        for m in self.open:
            paths = set()
            if m.get("source"):
                paths.add(m["source"])
            for u in (m.get("standards") or []):
                paths.add(u.replace("https://flove.org/", "").split("#")[0])
            for t in (m.get("tasks") or []):
                if t.get("owner"):
                    paths.add(t["owner"])
            for path in paths:
                fan[path] += 1
        self.fanout = fan

    def weight(self, hito: dict, task: dict | None = None) -> dict:
        t = task or {}
        u = self.unlock[hito["id"]]
        g = self.generated.get(t.get("id"), 0)
        owner = t.get("owner") or hito.get("source") or ""
        fan = self.fanout[owner]
        canon = canonical_owner(owner)
        decision = decision_of(hito)
        keywords = [k for k in DECISION_KEYWORDS
                    if re.search(r"\b" + re.escape(k) + r"\b", decision, re.I)]
        structural = []
        branched = []
        if u >= 3:
            structural.append("u≥3 (%d)" % u)
        if fan >= 10:
            structural.append("fan-out≥10 (%d)" % fan)
        if canon:
            structural.append("canonical %s" % canon)
        if g >= 2:
            structural.append("g≥2 (%d)" % g)
        if u == 2:
            branched.append("u=2")
        if 3 <= fan <= 9:
            branched.append("fan-out 3–9 (%d)" % fan)
        if keywords:
            branched.append("Decision: " + "/".join(keywords))
        score = 3 * len(structural) + 2 * len(branched)
        kind = ("estructurante" if structural
                else "ramificado" if branched else "directo")
        override = t.get("choice_override")
        reason = t.get("choice_reason") or ""
        if override in CHOICE_CLASSES:
            kind = override
            reason = reason or "user override"
        return {
            "class": kind,
            "score": score,
            "depth": CHOICE_DEPTH[kind],
            "unlock": u,
            "generated": g,
            "fanout": fan,
            "canonical": canon,
            "decision": decision,
            "reasons": structural + branched,
            "override": override if override in CHOICE_CLASSES else None,
            "choice_reason": reason,
        }

    def hito_class(self, hito: dict) -> str:
        """A hito carries its most consequential task's class (Work filter)."""
        tasks = hito.get("tasks") or []
        classes = [self.weight(hito, t)["class"] for t in tasks]
        if not classes:
            classes = [self.weight(hito)["class"]]
        return max(classes, key=CHOICE_CLASSES.index)
