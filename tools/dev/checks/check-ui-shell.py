#!/usr/bin/env python3
"""Validate the Work shell DOM contract in development/index.html.

The page must be the 4-toptab shell, not the old 6-section one:
  - 4 Top-tab buttons (Tracker / Data / Backend / Frontend)
  - the filter bar carries stage / effort / impact + an archived checkbox
  - the hierarchical section filter (4 Sections -> Subsections -> Subsubsections presented as chapters)
  - the Plans section-tree producer and its consumers agree on the `subsubsections` key
  - canonical URL scheme #<tab>?stage=&effort=&impact=&q= (plus #tasks for the
    Tasks register; archived is a transient checkbox, never a URL param)
  - zero legacy `#work?` refs

Usage:
  python3 tools/dev/checks/check-ui-shell.py [--strict]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HTML = ROOT / "development/index.html"

CANON_TABS = ["tracker", "data", "backend", "frontend"]
CANON_LABELS = ["Tracker", "Data", "Backend", "Frontend"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="also require the legacy #work? route resolver to be absent")
    args = ap.parse_args()
    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Four toptab buttons, in order.
    for tab, label in zip(CANON_TABS, CANON_LABELS):
        if not re.search(r'href="#' + tab + r'" data-section="' + tab + r'"[^>]*>' + label + r'<', text):
            errors.append("missing Top-tab button #%s (%s)" % (tab, label))

    # 2. Filter bar groups.
    for g in ("stage", "effort", "impact"):
        if ('data-filter="%s"' % g) not in text:
            errors.append("missing filter group %s" % g)
    if 'id="work-archived"' not in text:
        errors.append("missing archived checkbox (#work-archived)")

    # 3. Hierarchical section filter machinery.
    for marker in ("function renderSections", "SEC_TREE", "LEAVES", "PORT_MAP",
                   "function nodeCount"):
        if marker not in text:
            errors.append("missing section-filter marker %r" % marker)

    # 3a. Producer/consumer shape contract in the Plans view. A rename once left
    #     planSubTree emitting `children` while degreeHTML read `subsubsections`;
    #     that threw on every plain load and left only the bare shell rendered.
    if "subsubsections:kids" not in text:
        errors.append("planSubTree must emit the subsubsections key")
    if "p.subsubsections.map" not in text:
        errors.append("degreeHTML must consume the subsubsections key")
    if "children:kids" in text:
        errors.append("stale children key in the Plans section tree")

    # 3b. The #tasks route (Tasks register) must exist in parseHash.
    if "tab==='tasks'" not in text:
        errors.append("missing #tasks route in parseHash")

    # 4. Canonical URL scheme: #<tab>?stage=&effort=&impact=&q= (archived is a
    #    transient checkbox, never a URL param).
    for param in ("p.getAll('stage')", "p.getAll('effort')", "p.getAll('impact')",
                  "p.get('q')"):
        if param not in text:
            errors.append("missing URL param handler %r" % param)
    if 'p.get("archived")' in text or "p.get('archived')" in text:
        errors.append("archived is still a URL param (should be a transient checkbox)")

    # 5. Zero legacy #work? refs.
    work_refs = re.findall(r'#work\?[^"\' )]*', text)
    if work_refs:
        errors.append("%d legacy #work? refs remain" % len(work_refs))

    # 6. Strict: the legacy route resolver must be gone (Fase 6).
    if args.strict and re.search(r"indexOf\('work'\)===0|#work\?tab=", text):
        errors.append("legacy #work route resolver still present")

    if errors:
        for e in errors:
            print("FAIL:", e)
        print("FAIL: check-ui-shell (%d error(s))" % len(errors))
        return 1
    print("OK: check-ui-shell — 4 toptabs, filters stage/effort/impact/archived, "
          "hierarchical section filter, canonical URL, 0 #work?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
