#!/usr/bin/env python3
"""Verify the archived partitions and their checksums.

Usage:
  python3 tools/dev/checks/check-archive.py --check

`old/` is the archived pre-cutover snapshot. Dated sibling partitions hold
material archived later. Both are verified with the same rules; neither is an
owner or a live destination.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "development/port-ledger.json"
ARCHIVE = ROOT / "development/archive"
LEGACY_ROOTS = {"development/wiki/archive/old": "development/archive/old"}
REGISTRY_NAMES = ("manifest.json", "SHA256SUMS")


def partitions() -> list[tuple[Path, Path, Path, bool]]:
    """(root, manifest, checksums, legacy) for each archive partition."""
    out = [(ARCHIVE / "old", ARCHIVE / "manifest.json",
            ARCHIVE / "SHA256SUMS", True)]
    for path in sorted(p for p in ARCHIVE.iterdir()
                       if p.is_dir() and p.name != "old"):
        out.append((path, path / "manifest.json", path / "SHA256SUMS", False))
    return out


def check_partition(root: Path, manifest_path: Path, sha_path: Path,
                    legacy: bool) -> list[str]:
    errors: list[str] = []
    label = root.relative_to(ARCHIVE).as_posix()
    if not root.exists():
        return [f"archive partition missing: {label}"]
    if not sha_path.exists():
        if legacy:
            print(f"WARN: archive present, no SHA256SUMS yet")
            return []
        return [f"missing {sha_path.relative_to(ROOT)}"]
    if not manifest_path.exists():
        return [f"missing archive manifest: {manifest_path.relative_to(ROOT)}"]

    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != "flove-archive/1":
        return [f"{manifest_path.relative_to(ROOT)} schema is not flove-archive/1"]
    expected = root.relative_to(ROOT).as_posix()
    declared = manifest.get("root")
    legacy = ("development/wiki/archive/"
              + expected[len("development/archive/"):]
              if expected.startswith("development/archive/") else None)
    if declared != expected and declared != legacy:
        return [f"{manifest_path.relative_to(ROOT)} root does not match {label}"]

    entries = manifest.get("files") or []
    listed_paths = [entry.get("path") for entry in entries]
    actual_paths = sorted(p.relative_to(ARCHIVE).as_posix()
                          for p in root.rglob("*")
                          if p.is_file() and p.name not in REGISTRY_NAMES)
    if sorted(listed_paths) != actual_paths:
        extra = sorted(set(listed_paths) - set(actual_paths))
        missing_in_manifest = sorted(set(actual_paths) - set(listed_paths))
        errors.append(
            f"{label}: manifest does not match the tree "
            f"({len(listed_paths)} listed, {len(actual_paths)} on disk)")
        for path in (extra + missing_in_manifest)[:20]:
            errors.append(f"  - {path}")

    bad_entries = []
    for entry in entries:
        if entry.get("status") != "archived" or entry.get("live") is not False \
                or entry.get("owner") is not None:
            bad_entries.append(entry.get("path"))
        digest = entry.get("sha256")
        rel = entry.get("path")
        if digest and rel:
            path = ARCHIVE / rel
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                bad_entries.append(rel)
    for path in bad_entries[:20]:
        errors.append(f"{label}: bad archive entry: {path}")

    listed: dict[str, str] = {}
    for line in sha_path.read_text().splitlines():
        if "  " not in line:
            continue
        digest, rel = line.split("  ", 1)
        listed[rel] = digest.strip()
    if not listed:
        errors.append(f"{sha_path.relative_to(ROOT)} has no checksum entries")
    bad = []
    for rel, digest in listed.items():
        path = ARCHIVE / rel
        if not path.exists():
            bad.append((rel, "missing"))
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append((rel, "checksum mismatch"))
    for rel, why in bad[:20]:
        errors.append(f"{label}: {rel}: {why}")

    unlisted = sorted(set(actual_paths) - set(listed))
    for rel in unlisted[:20]:
        errors.append(f"{label}: file missing from SHA256SUMS: {rel}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.error("--check is required")

    data = json.loads(LEDGER.read_text())
    expected = [f["archive"] for f in data.get("files", []) if f.get("archive")]
    parts = partitions()
    old_root = parts[0][0]
    missing = [p for p in expected if not (ROOT / p).exists()]
    if not old_root.exists():
        print(f"FAIL: archive root missing: {old_root.relative_to(ROOT)} "
              f"({len(expected)} files expected)")
        return 1
    if missing:
        print(f"FAIL: {len(missing)} of {len(expected)} archived files are missing")
        for p in missing[:20]:
            print("  -", p)
        return 1

    errors: list[str] = []
    verified = 0
    for root, manifest_path, sha_path, legacy in parts:
        part_errors = check_partition(root, manifest_path, sha_path, legacy)
        errors.extend(part_errors)
        if not part_errors:
            verified += len([1 for line in sha_path.read_text().splitlines()
                             if "  " in line])

    # Legacy ledger sources must still be listed in the old checksum file.
    old_listed = set()
    for line in parts[0][2].read_text().splitlines():
        if "  " in line:
            old_listed.add(line.split("  ", 1)[1])
    unlisted = [p for p in expected
                if (ROOT / p).relative_to(ARCHIVE).as_posix() not in old_listed]
    for p in unlisted[:20]:
        errors.append(f"ledger source missing from SHA256SUMS: {p}")

    if errors:
        print(f"FAIL: {len(errors)} archive error(s)")
        for err in errors[:30]:
            print("  -", err)
        return 1
    print(f"OK: archive present, {len(parts)} partitions, {verified} files, "
          f"checksums verified ({len(expected)} ledger sources)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
