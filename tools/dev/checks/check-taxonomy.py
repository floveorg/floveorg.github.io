#!/usr/bin/env python3
"""Permanent validator for the flove Work taxonomy.

Runs from any cwd and from any location under the repository (it is meant to be
promoted to tools/dev/checks/check-taxonomy.py). It imports
build-work-tracker.py with importlib and only calls canonical(): the generator's
`if __name__ == "__main__"` block never runs, so this check never rebuilds or
writes the embedded block.

Usage:
  python3 tools/dev/checks/check-taxonomy.py [--strict-paths]
"""
from __future__ import annotations

import argparse
import importlib.util
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
GEN = ROOT / "tools/dev/tasks/build-work-tracker.py"
REG = ROOT / "development/tasks/milestones.json"
HTML = ROOT / "development/index.html"
CANON_TABS = ["tracker", "data", "backend", "frontend"]
CANON_MAX_DEPTH = 5
SCRIPT_RE = re.compile(
    r'<script type="application/json" id="tasks-data">(.*?)</script>', re.S)


def load_generator():
    spec = importlib.util.spec_from_file_location("flove_work_tracker_taxonomy", GEN)
    if spec is None or spec.loader is None:
        raise SystemExit("FAIL: cannot import %s" % GEN.relative_to(ROOT))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(GEN.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(GEN.parent))
    return mod


def read_tree(sections: list, errors: list[str]):
    """Return (valid paths, node ids, max depth) across all parent Sections."""
    valid: dict[str, set] = {}
    ids: dict[str, set] = {}
    deepest = 0
    for section in sections:
        parent = section.get("slug") or section.get("id")
        if not parent:
            errors.append("tree: section without slug")
            continue
        paths, seen, parent_deep = {parent}, set(), 0

        def rec(nodes, prefix: tuple, depth: int):
            nonlocal parent_deep
            for node in nodes or []:
                nid = node.get("id")
                if not isinstance(nid, str) or not nid:
                    errors.append("tree %s: node without id" % parent)
                    continue
                path = prefix + (nid,)
                if path in paths:
                    errors.append("tree %s: duplicate path %s"
                                  % (parent, "/".join(path)))
                    continue
                paths.add(path)
                seen.add(nid)
                parent_deep = max(parent_deep, depth)
                rec(node.get("subsubsections") or [], path, depth + 1)

        rec(section.get("subsections") or [], (parent,), 1)
        valid[parent] = paths
        ids[parent] = seen
        deepest = max(deepest, parent_deep)
    return valid, ids, deepest


def check_path(raw, parent: str, label: str, valid: dict[str, set], sections: list[str],
               errors: list[str], strict: bool) -> bool:
    path = tuple(p for p in (raw or []) if isinstance(p, str))
    if not path:
        errors.append("%s: empty path" % label)
        return False
    if path[0] in sections:
        full = path
        if path[0] != parent:
            errors.append("%s: path Section %s != parent %s" % (label, path[0], parent))
            return False
    else:
        full = (parent,) + path
        if strict:
            errors.append("%s: path must start with its parent Section: %s"
                          % (label, "/".join(full)))
            return False
    if full not in valid.get(parent, set()):
        errors.append("%s: subsection/subsubsection path %s does not exist in Section %s"
                      % (label, "/".join(full), parent))
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict-paths", action="store_true",
                    help="require literal parent Section prefixes in register paths")
    args = ap.parse_args()
    errors: list[str] = []

    try:
        mod = load_generator()
        canonical = mod.canonical()
    except Exception as exc:  # noqa: BLE001 - a broken generator is a hard fail
        print("FAIL: cannot evaluate build-work-tracker.canonical(): %s" % exc)
        return 1

    try:
        html = HTML.read_text(encoding="utf-8")
    except OSError as exc:
        print("FAIL: cannot read %s: %s" % (HTML.relative_to(ROOT), exc))
        return 1
    m = SCRIPT_RE.search(html)
    if not m:
        print("FAIL: #tasks-data JSON block not found")
        return 1
    try:
        embedded = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        print("FAIL: #tasks-data is not valid JSON (%s)" % exc)
        return 1

    # Canonical parity: the page block is a projection of canonical(), never a
    # second authority. Report the diverging top-level keys.
    if canonical != embedded:
        keys = sorted(set(canonical) | set(embedded))
        for key in keys:
            if canonical.get(key) != embedded.get(key):
                errors.append("tasks-data differs from canonical() at %r" % key)

    section_slugs = list(canonical.get("tabs") or [])
    if section_slugs != CANON_TABS:
        errors.append("Section slugs %r, expected %r" % (section_slugs, CANON_TABS))
    module_max = getattr(mod, "MAX_DEPTH", None)
    if module_max != CANON_MAX_DEPTH:
        errors.append("MAX_DEPTH %r, expected %d" % (module_max, CANON_MAX_DEPTH))
    if "max_depth" in canonical and canonical["max_depth"] != CANON_MAX_DEPTH:
        errors.append("tasks-data max_depth %r, expected %d"
                      % (canonical["max_depth"], CANON_MAX_DEPTH))

    sections = canonical.get("sections") or []
    valid, ids, deepest = read_tree(sections, errors)
    if deepest > CANON_MAX_DEPTH:
        errors.append("tree depth %d exceeds MAX_DEPTH %d"
                      % (deepest, CANON_MAX_DEPTH))
    if any(a.get("slug") not in CANON_TABS for a in sections):
        errors.append("Sections contain a non-canonical parent slug")

    checked = relative = 0
    # A retired chapter id is still written in the register; validate it against
    # the one chapter that presents it. The alias lives in the canonical builder.
    alias = getattr(mod, "SUBSUBSECTION_ALIAS", {}) or {}

    def record(raw, parent, label, subsubsection=None):
        nonlocal checked, relative
        before = len(errors)
        raw = [alias.get(p, p) for p in raw] if isinstance(raw, list) else raw
        if subsubsection is not None:
            subsubsection = alias.get(subsubsection, subsubsection)
        if isinstance(raw, list) and raw and raw[0] not in section_slugs:
            relative += 1
        if check_path(raw, parent, label, valid, section_slugs, errors, args.strict_paths):
            checked += 1
        if subsubsection is not None and parent in ids and subsubsection not in ids[parent]:
            errors.append("%s: subsubsection id %r is not in %s" % (label, subsubsection, parent))
        return len(errors) == before

    try:
        reg = json.loads(REG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append("cannot read register: %s" % exc)
        reg = {}
    for sec in reg.get("sections", []):
        parent = sec.get("section")
        for box in sec.get("subsections", []):
            for item in box.get("milestones", []):
                record(item.get("path"), parent,
                       "hilo %s" % (item.get("id") or item.get("es", "?")),
                       item.get("section"))
    for item in reg.get("new_tickets", []):
        record(item.get("path"), item.get("category"),
               "ticket %s" % (item.get("id") or "?"), item.get("section"))
    # Rows carry the canonical MD in `path`; their tree chapter comes from the
    # generated sectionMeta (the old row-level category/subtab keys are gone).
    section_meta = canonical.get("sectionMeta") or {}
    for row in canonical.get("rows", []):
        section = row.get("section")
        meta = section_meta.get(section) or {}
        parent = meta.get("parent")
        tree_path = [parent, meta.get("child")]
        if section != meta.get("child"):
            tree_path.append(section)
        record(tree_path, parent, "fila %s" % (row.get("id") or "?"), section)
        if not str(row.get("path") or "").startswith("development/"):
            errors.append("fila %s: bad canonical MD path %r"
                          % (row.get("id") or "?", row.get("path")))

    if errors:
        for e in errors:
            print("FAIL:", e)
        print("FAIL: check-taxonomy (%d error(s))" % len(errors))
        return 1
    nodes = sum(len(s) for s in ids.values())
    print("OK: check-taxonomy — %d parent Sections, %d nodos, profundidad %d/%d, "
          "%d rutas (%d relativas al padre), tasks-data == canonical()"
          % (len(section_slugs), nodes, deepest, CANON_MAX_DEPTH, checked, relative))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
