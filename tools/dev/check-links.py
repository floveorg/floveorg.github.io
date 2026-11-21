#!/usr/bin/env python3
"""Fail on broken local Markdown links or anchors in the live docs.

Usage:
  python3 tools/dev/check-links.py --check
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASES = [ROOT / "development/standards", ROOT / "development/wiki"]
EXTRA = [ROOT / "development/AGENTS.md"]
SKIP = (ROOT / "development/wiki/archive/old",)
LINK = re.compile(r"\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.M)
EXPLICIT_ID = re.compile(r'<a id="([^"]+)"')
LINK_START = ("http://", "https://", "mailto:", "#")


def slug(text: str) -> str:
    """The wiki's ## → anchor rule: lowercase, drop punctuation, hyphenate."""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


_cache: dict[Path, set[str]] = {}


def anchors(path: Path) -> set[str]:
    if path in _cache:
        return _cache[path]
    found: set[str] = set()
    if path.suffix == ".md":
        text = path.read_text(encoding="utf-8", errors="replace")
        found.update(EXPLICIT_ID.findall(text))
        found.update(slug(m.group(1)) for m in HEADING.finditer(text))
    _cache[path] = found
    return found


def source_files():
    seen: list[Path] = []
    for base in BASES:
        for path in base.rglob("*.md"):
            if any(path == p or p in path.parents for p in SKIP):
                continue
            seen.append(path)
    seen.extend(EXTRA)
    return seen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    missing: list[tuple[str, str]] = []
    bad_anchor: list[tuple[str, str]] = []
    for path in source_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in LINK.finditer(text):
            href = match.group(1)
            if href.startswith(LINK_START):
                continue
            target, _, anchor = href.partition("#")
            target = urllib.parse.unquote(target)
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                missing.append((rel, href))
            elif anchor and anchor not in anchors(resolved):
                bad_anchor.append((rel, href))

    if missing or bad_anchor:
        print(f"FAIL: {len(missing)} broken link(s), {len(bad_anchor)} broken anchor(s)")
        for rel, href in missing[:30]:
            print(f"  missing  {rel}: {href}")
        for rel, href in bad_anchor[:30]:
            print(f"  anchor   {rel}: {href}")
        return 1

    print(f"OK: {len(source_files())} live docs, no broken local links or anchors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
