#!/usr/bin/env python3
"""Validate that the legacy `#work` hash alias (Via A) is REMOVED (Fase 6).

After CLN-01 the read-only `#work` adapter is gone:
  - no `#work` branch in parseHash
  - zero `#work?` refs in index.html
  - no `legacy` key in the tasks-data block
  - migration/legacy-routes.json deleted
  - the 4 canonical toptabs remain

Usage:
  python3 tools/dev/checks/check-legacy-routes.py [--strict]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def find_root() -> Path:
    p = Path(__file__).resolve()
    for d in (p.parent,) + tuple(p.parents):
        if ((d / "tools/dev/tasks/build-work-tracker.py").exists()
                and (d / "development/index.html").exists()):
            return d
    raise SystemExit("FAIL: cannot locate the flove repository root")


ROOT = find_root()
HTML = ROOT / "development/index.html"
LEGACY_ROUTES = ROOT / "migration" / "legacy-routes.json"
CANON_TABS = ["tracker", "data", "backend", "frontend"]
WORK_DATA_RE = re.compile(
    r'<script type="application/json" id="tasks-data">(.*?)</script>', re.S)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="(kept for the Fase 5 gate; same check)")
    args = ap.parse_args()

    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []

    # The 4 canonical toptabs must always exist.
    for tab in CANON_TABS:
        if 'data-section="%s"' % tab not in text:
            errors.append("canonical toptab %s missing" % tab)

    # Legacy adapter must be gone.
    if re.search(r"tab\s*===?\s*'work'", text):
        errors.append("legacy `#work` branch still present in parseHash")
    work_refs = re.findall(r"#work\?", text)
    if work_refs:
        errors.append("%d legacy `#work?` refs remain" % len(work_refs))

    # Legacy table must be gone from tasks-data.
    m = WORK_DATA_RE.search(text)
    if m:
        try:
            if "legacy" in json.loads(m.group(1)):
                errors.append("`legacy` table still embedded in tasks-data")
        except json.JSONDecodeError:
            errors.append("tasks-data block is not valid JSON")
    else:
        errors.append("tasks-data block not found")

    if LEGACY_ROUTES.exists():
        errors.append("migration/legacy-routes.json still present")

    if errors:
        for e in errors:
            print("FAIL:", e)
        print("FAIL: check-legacy-routes (%d error(s))" % len(errors))
        return 1
    print("OK: check-legacy-routes — legacy #work alias removed; canonical toptabs intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
