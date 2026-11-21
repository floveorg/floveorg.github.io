#!/usr/bin/env python3
"""Shared projections of milestones.json for Work, common.json and jsony.

`milestones.json` is the only authority. Every consumer that needs the archive,
the queue policy or the register counts calls this module so a new field can be
added once. Generated files never invent these values locally.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONES = ROOT / "standards/debates/milestones.json"


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
