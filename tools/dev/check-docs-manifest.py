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
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "development/wiki/wiki.json"
HTML = ROOT / "development/index.html"
CONTEXT = re.compile(r"<!-- CONTEXT:BEGIN\n(.*?)\nCONTEXT:END -->", re.S)
STATUS = re.compile(r"^status:\s*(\w+)", re.M)
SIDEBAR = ROOT / "development/standards/_sidebar.md"
INDEX = ROOT / "development/wiki/INDEX.md"


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    found = set(re.findall(r'<a id="([^"]+)"', text))
    found.update(slug(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.*?)\s*$", text, re.M))
    return found


def declared_status(path: Path) -> str:
    match = STATUS.search(path.read_text(encoding="utf-8", errors="replace"))
    return match.group(1).strip().lower() if match else "missing"


def list_field(text: str, key: str) -> list[str]:
    match = re.search(rf"^{key}:\s*\n((?:  - .*\n)*)", text, re.M)
    if not match:
        return []
    return [line.strip()[2:] for line in match.group(1).splitlines()
            if line.strip().startswith("- ")]


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
    plans = m.get("plans", [])
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


    # Frontmatter must agree with the manifest, with the two documented plan
    # exceptions (active conflict tracker and the draft tray README).
    for entry in pages + plans:
        path = ROOT / entry["path"]
        if not path.exists():
            continue
        expected = entry.get("status")
        actual = declared_status(path)
        if actual == "missing":
            continue
        if expected and actual != expected:
            errors.append(f"status mismatch: {entry['path']} file={actual} manifest={expected}")

    # One owner string, one page.
    claims: dict[str, list[str]] = {}
    for entry in pages:
        for claim in entry.get("owns") or []:
            claims.setdefault(claim, []).append(entry["id"])
    for claim, owners in claims.items():
        if len(set(owners)) > 1:
            errors.append(f"ownership conflict: {claim!r} -> {sorted(set(owners))}")

    # Every read_next anchor and supersedes source must exist.
    for entry in pages:
        path = ROOT / entry["path"]
        text = path.read_text(encoding="utf-8", errors="replace")
        page_anchors = anchors(path)
        for ref in list_field(text, "read_next"):
            if ref.lstrip("#") not in page_anchors:
                errors.append(f"read_next anchor missing: {entry['path']} -> {ref}")
        supersedes = list_field(text, "supersedes")
        for source in supersedes:
            if not (ROOT / source).exists():
                errors.append(f"supersedes source missing: {entry['path']} -> {source}")
        for row in re.findall(r"^\| `(archive/old/[^`]+)` \| \d{4}-\d{2}-\d{2} \|", text, re.M):
            source = "development/wiki/" + row
            if source not in supersedes:
                errors.append(f"source map row not in supersedes: {entry['path']} -> {source}")

    # INDEX topic/plan tables and historical rows must match the manifest.
    index_text = INDEX.read_text(encoding="utf-8", errors="replace")
    section = lambda start, end: index_text.split(start, 1)[-1].split(end, 1)[0]
    topic_section = section("## 2. Topic grid", "## 3.")
    index_topics = dict(re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|", topic_section, re.M))
    manifest_topics = {p["id"]: p["path"] for p in topics}
    if index_topics != manifest_topics:
        errors.append("INDEX topic table differs from the manifest")
    plan_section = section("## 4. Plans", "## 5.")
    index_plans = dict(re.findall(r"^\| `([^`]+)` \| `[^`]+` \| (\w+) \|", plan_section, re.M))
    manifest_plans = {p["path"]: p.get("status") for p in m.get("plans", [])}
    if index_plans != manifest_plans:
        errors.append("INDEX plan table differs from the manifest")
    historical = section("## 7. Historical rows", "## 8.")
    hist_rows = re.findall(r"^\| \[[^\]]+\]\((archive/old/[^)]+)\) \|", historical, re.M)
    if len(hist_rows) != 33:
        errors.append(f"INDEX historical rows: expected 33, found {len(hist_rows)}")
    for target in hist_rows:
        if not (ROOT / "development/wiki" / target).exists():
            errors.append(f"INDEX historical row target missing: {target}")

    # The docsify sidebar must expose every topic page.
    sidebar = SIDEBAR.read_text(encoding="utf-8", errors="replace")
    for topic in topics:
        name = Path(topic["path"]).name
        if f"]({name})" not in sidebar:
            errors.append(f"sidebar missing topic page: {topic['path']}")
    for standing in [p for p in pages if p.get("kind") == "standing"]:
        rel = Path(standing["path"]).relative_to("development/standards").as_posix()
        if f"]({rel})" not in sidebar:
            errors.append(f"sidebar missing standing book: {standing['path']}")

    # Stable child plans should not carry the phase-1 undated placeholder.
    for plan in m.get("plans", []):
        text = (ROOT / plan["path"]).read_text(encoding="utf-8", errors="replace")
        if "undated" in text:
            errors.append(f"plan still has undated source sections: {plan['id']}")

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
