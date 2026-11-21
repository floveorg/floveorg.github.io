#!/usr/bin/env python3
"""Verify the verbatim archive and its checksums.

Usage:
  python3 tools/dev/check-archive.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "development/wiki/port-ledger.json"
ARCHIVE = ROOT / "development/wiki/archive/old"
MANIFEST = ROOT / "development/wiki/archive/SHA256SUMS"
INDEX = ROOT / "development/wiki/archive/manifest.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    data = json.loads(LEDGER.read_text())
    expected = [f["archive"] for f in data.get("files", []) if f.get("archive")]
    missing = [p for p in expected if not (ROOT / p).exists()]
    if not ARCHIVE.exists():
        print(f"FAIL: archive root missing: {ARCHIVE.relative_to(ROOT)} ({len(expected)} files expected)")
        return 1
    if missing:
        print(f"FAIL: {len(missing)} of {len(expected)} archived files are missing")
        for p in missing[:20]:
            print("  -", p)
        return 1
    if not MANIFEST.exists():
        print(f"WARN: archive present, {len(expected)} files, no SHA256SUMS yet")
        return 0
    if not INDEX.exists():
        print(f"FAIL: missing archive manifest: {INDEX.relative_to(ROOT)}")
        return 1
    manifest = json.loads(INDEX.read_text())
    if manifest.get("schema") != "flove-archive/1":
        print(f"FAIL: {INDEX.relative_to(ROOT)} schema is not flove-archive/1")
        return 1
    entries = manifest.get("files") or []
    listed_paths = [entry.get("path") for entry in entries]
    actual_paths = sorted(p.relative_to(ARCHIVE.parent).as_posix()
                          for p in ARCHIVE.rglob("*") if p.is_file())
    if sorted(listed_paths) != actual_paths:
        extra = sorted(set(listed_paths) - set(actual_paths))
        missing_in_manifest = sorted(set(actual_paths) - set(listed_paths))
        print(f"FAIL: archive manifest does not match the tree "
              f"({len(listed_paths)} listed, {len(actual_paths)} on disk)")
        for path in (extra + missing_in_manifest)[:20]:
            print("  -", path)
        return 1
    bad_entries = []
    for entry in entries:
        if entry.get("status") != "archived" or entry.get("live") is not False \
                or entry.get("owner") is not None:
            bad_entries.append(entry.get("path"))
    if bad_entries:
        print(f"FAIL: {len(bad_entries)} archive entr(ies) are not marked non-live")
        for path in bad_entries[:20]:
            print("  -", path)
        return 1

    listed: dict[str, str] = {}
    for line in MANIFEST.read_text().splitlines():
        if "  " not in line:
            continue
        digest, rel = line.split("  ", 1)
        listed[rel] = digest.strip()
    if not listed:
        print(f"FAIL: {MANIFEST.relative_to(ROOT)} has no checksum entries")
        return 1

    bad = []
    for rel, digest in listed.items():
        path = ROOT / "development/wiki/archive" / rel
        if not path.exists():
            bad.append((rel, "missing"))
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append((rel, "checksum mismatch"))
    if bad:
        print(f"FAIL: {len(bad)} archived file(s) do not verify")
        for rel, why in bad[:20]:
            print(f"  - {rel}: {why}")
        return 1

    unlisted = [p for p in expected
                if (ROOT / p).relative_to(ARCHIVE.parent).as_posix() not in listed]
    if unlisted:
        print(f"FAIL: {len(unlisted)} ledger source(s) missing from SHA256SUMS")
        for p in unlisted[:20]:
            print("  -", p)
        return 1

    print(f"OK: archive present, {len(listed)} files, checksums verified "
          f"({len(expected)} ledger sources)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
