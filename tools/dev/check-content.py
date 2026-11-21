#!/usr/bin/env python3
"""Validate the port ledger: modes, destinations, anchors and sign-offs.

Usage:
  python3 tools/dev/check-content.py --check
  python3 tools/dev/check-content.py --check --allow-pending
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "development/wiki/port-ledger.json"


def slug(h: str) -> str:
    s = h.lower()
    s = re.sub(r"[^a-z0-9 \-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-")


def anchors(path: Path) -> set[str]:
    text = path.read_text(errors="ignore")
    out = set(re.findall(r'<a id="([^"]+)"', text))
    for line in text.splitlines():
        m = re.match(r"^#{1,4}\s+(.+?)\s*$", line)
        if m:
            out.add(slug(m.group(1)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--allow-pending", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    data = json.loads(LEDGER.read_text())
    errors = []
    pending = unsigned = 0
    for f in data.get("files", []):
        for h in f.get("headings", []):
            mode = h.get("mode")
            if mode == "pending":
                pending += 1
                continue
            if mode not in {"ported", "linked", "archive-only"}:
                errors.append(f"bad mode {mode}: {f['source']}#{h.get('heading')}")
                continue
            if mode in {"ported", "linked"} and not h.get("signoff"):
                unsigned += 1
            if mode == "archive-only":
                continue
            dest = h.get("destination")
            if not dest:
                errors.append(f"missing destination: {f['source']}#{h.get('heading')}")
                continue
            p = ROOT / dest
            if not p.exists():
                errors.append(f"missing destination file: {dest}")
                continue
            a = (h.get("destination_anchor") or "").lstrip("#")
            if a and a not in anchors(p):
                errors.append(f"missing destination anchor: {dest}#{a}")

    print(f"ledger: {data.get('summary', {}).get('headings', '?')} headings, {pending} pending, {unsigned} unsigned")
    if pending and not args.allow_pending:
        errors.append(f"{pending} pending heading(s)")
    if unsigned:
        errors.append(f"{unsigned} heading(s) without sign-off")
    if errors:
        print(f"FAIL: {len(errors)} content error(s)")
        for e in errors[:30]:
            print(" -", e)
        return 1
    print("OK: ledger complete and signed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
