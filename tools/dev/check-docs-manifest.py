#!/usr/bin/env python3
"""Validate the docs-wiki manifest and page contexts.

Usage:
  python3 tools/dev/check-docs-manifest.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "development/wiki/wiki.json"
HTML = ROOT / "development/index.html"
CONTEXT = re.compile(r"<!-- CONTEXT:BEGIN\n(.*?)\nCONTEXT:END -->", re.S)


def anchor_exists(name: str) -> bool:
    if not HTML.exists():
        return False
    return f'id="{name.lstrip("#")}"' in HTML.read_text(errors="ignore")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    errors = []
    try:
        m = json.loads(WIKI.read_text())
    except Exception as e:
        print("FAIL: manifest does not parse:", e)
        return 1

    if m.get("schema") != "flove-wiki-manifest/1":
        errors.append("schema is not flove-wiki-manifest/1")
    pages = m.get("pages", [])
    ids = [p.get("id") for p in pages]
    paths = [p.get("path") for p in pages]
    if len(ids) != len(set(ids)):
        errors.append("duplicate page id")
    if len(paths) != len(set(paths)):
        errors.append("duplicate page path")

    for p in pages:
        path = ROOT / p.get("path", "")
        if not path.exists():
            errors.append(f"missing page file: {p.get('path')}")
            continue
        if p.get("kind") == "topic":
            text = path.read_text(errors="ignore")
            match = CONTEXT.search(text)
            if not match:
                errors.append(f"missing CONTEXT: {p.get('path')}")
                continue
            try:
                c = yaml.safe_load(match.group(1))
            except Exception as e:
                errors.append(f"CONTEXT does not parse: {p.get('path')}: {e}")
                continue
            if c.get("id") != p.get("id"):
                errors.append(f"CONTEXT id mismatch: {p.get('path')}")
            for a in c.get("html_place", []):
                if not anchor_exists(a):
                    errors.append(f"HTML anchor missing: {a} ({p.get('id')})")

    topics = [p for p in pages if p.get("kind") == "topic"]
    if len(topics) != 19:
        errors.append(f"expected 19 topic pages, found {len(topics)}")

    for plan in m.get("plans", []):
        if not (ROOT / plan.get("path", "")).exists():
            errors.append(f"missing plan file: {plan.get('path')}")
        if plan.get("primary") and plan.get("primary") not in ids:
            errors.append(f"plan primary page missing: {plan.get('id')} -> {plan.get('primary')}")
        sources = plan.get("sources") or []
        if not sources:
            errors.append(f"plan has no archived sources: {plan.get('id')}")
        for source in sources:
            if not (ROOT / source).exists():
                errors.append(f"plan source missing: {plan.get('id')} -> {source}")

    for key, target in m.get("field_map", {}).items():
        if not (ROOT / target).exists():
            errors.append(f"field_map target missing: {key} -> {target}")

    if errors:
        print(f"FAIL: {len(errors)} manifest error(s)")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(pages)} pages, {len(topics)} topics, {len(m.get('plans', []))} plans")
    return 0


if __name__ == "__main__":
    sys.exit(main())
