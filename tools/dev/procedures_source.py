#!/usr/bin/env python3
"""procedures_source — the canonical PROC chapter lives in development/AGENTS.md.

Nine `### PROC-nn — title` blocks carry one field per line:

    - Checker: jsony
    - Standard: https://flove.org/...
    - Definition of done: ...
    - Advice: ...
    - Inputs: ...
    - Outputs: ...
    - Gates: ...

An indented line continues the previous field. tasky, common.json, the embedded
Work block and every gate call `load()` here, so no other file holds a second
copy of the policy. `milestones.json` owns only hitos and tasks.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "development"
SOURCE = ROOT / "AGENTS.md"

HEADING = re.compile(r"^###\s+(PROC-\d{2})\s+[—–-]\s+(.+?)\s*$")
LABEL = re.compile(r"^-\s+([^:]+):\s*(.*)$")
FIELDS = {
    "Checker": "checker",
    "Standard": "standard",
    "Definition of done": "definition_of_done",
    "Advice": "advice",
    "Inputs": "inputs",
    "Outputs": "outputs",
    "Gates": "gates",
}


def load(path: Path | None = None) -> list[dict]:
    """Read the ten PROC blocks from AGENTS.md, in document order."""
    text = (path or SOURCE).read_text(encoding="utf-8")
    rows: list[dict] = []
    current: dict | None = None
    last: str | None = None
    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading:
            current = {"id": heading.group(1), "title": heading.group(2).strip()}
            rows.append(current)
            last = None
            continue
        if line.startswith("#"):
            current = None
            last = None
            continue
        if current is None:
            continue
        field = LABEL.match(line)
        if field and field.group(1).strip() in FIELDS:
            last = FIELDS[field.group(1).strip()]
            current[last] = field.group(2).strip()
        elif line.startswith(("  ", "\t")) and last:
            current[last] += " " + line.strip()
    return rows
