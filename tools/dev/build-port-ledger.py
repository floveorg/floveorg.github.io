#!/usr/bin/env python3
"""Build the source-heading ledger for the docs-wiki migration.

Phase 0 writes only the skeleton: every source heading with mode `pending`.
Phase 2 fills destination, mode, provenance and sign-off. The file is never
hand-edited.

Usage:
  python3 tools/dev/build-port-ledger.py --skeleton
  python3 tools/dev/build-port-ledger.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "development"
DEBATES = DEV / "standards/debates"
APPS = DEV / "standards/apps"
OUT = DEV / "wiki/port-ledger.skeleton.json"

ROOT_FILES = [
    DEV / "standards/backend.md",
    DEV / "standards/adoption.md",
    DEV / "standards/worldview.md",
    DEV / "standards/contract.md",
    DEV / "standards/AGENTS.md",
]

ARCHIVE_ONLY = {
    "agents.md",
    "skills-library.md",
    "archive.md",
    "a11y-development-index.md",
    "browsy/pre-build/open-issues.md",
    "plans/2026-06-18-nety-frontend-build.md.bak-orig",
}

HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(ref: str, fallback: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", f"{ref}^{{commit}}"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return fallback


def headings(path: Path) -> list[dict]:
    out: list[dict] = []
    fence = False
    for lineno, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        out.append(
            {
                "level": len(m.group(1)),
                "heading": m.group(2).strip(),
                "line": lineno,
                "mode": "pending",
                "destination": None,
                "destination_anchor": None,
                "provenance": None,
                "signoff": None,
                "summary_reason": None,
            }
        )
    return out


def archive_for(source: Path) -> str | None:
    rel = source.relative_to(DEV / "standards")
    if source == DEV / "standards/contract.md":
        return None
    if source.parent == APPS:
        return f"development/wiki/archive/old/apps/{source.name}"
    if source.parent == DEV / "standards" and source.name in {
        "backend.md", "adoption.md", "worldview.md", "AGENTS.md"
    }:
        return f"development/wiki/archive/old/root/{source.name}"
    if DEBATES in source.parents:
        rel_debates = source.relative_to(DEBATES)
        return f"development/wiki/archive/old/{rel_debates}"
    return f"development/wiki/archive/old/{rel}"


def treatment(source: Path) -> str:
    if source == DEV / "standards/contract.md":
        return "keep"
    if source == DEV / "standards/AGENTS.md":
        return "merge"
    rel = str(source.relative_to(DEBATES)) if DEBATES in source.parents else source.name
    if rel in ARCHIVE_ONLY or rel.startswith("archive/making-of/"):
        return "archive-only"
    return "port+archive"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skeleton", action="store_true", help="write the skeleton ledger")
    ap.add_argument("--check", action="store_true", help="validate the skeleton against the tree")
    args = ap.parse_args()
    if not (args.skeleton or args.check):
        ap.error("choose --skeleton or --check")

    sources = sorted(DEBATES.rglob("*.md")) + sorted(APPS.glob("*.md")) + ROOT_FILES
    files = []
    total_headings = 0
    by_level: dict[str, int] = {}
    by_group: dict[str, int] = {}
    for source in sources:
        hs = headings(source)
        total_headings += len(hs)
        for h in hs:
            by_level[str(h["level"])] = by_level.get(str(h["level"]), 0) + 1
        rel = source.relative_to(ROOT)
        if DEBATES in source.parents:
            group = "debates"
        elif source.parent == APPS:
            group = "apps"
        else:
            group = "root"
        by_group[group] = by_group.get(group, 0) + 1
        files.append(
            {
                "source": str(rel),
                "group": group,
                "treatment": treatment(source),
                "archive": archive_for(source),
                "source_sha256": sha256(source),
                "archive_sha256": None,
                "headings": hs,
            }
        )

    payload = {
        "schema": "flove-port-ledger/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "baseline_commit": git_commit("docs-migration-baseline", "170cfee3473b17fa1428ea64c5eeb186bb21491d"),
        "summary": {
            "files": len(files),
            "headings": total_headings,
            "by_level": dict(sorted(by_level.items())),
            "by_group": dict(sorted(by_group.items())),
            "archive_only_files": sum(1 for f in files if f["treatment"] == "archive-only"),
            "keep_files": sum(1 for f in files if f["treatment"] == "keep"),
            "merge_files": sum(1 for f in files if f["treatment"] == "merge"),
        },
        "files": files,
    }

    if args.check:
        if not OUT.exists():
            print(f"missing {OUT.relative_to(ROOT)}")
            return 1
        current = json.loads(OUT.read_text())
        if current.get("summary", {}).get("files") != len(files):
            print(f"stale: {current.get('summary', {}).get('files')} files, tree has {len(files)}")
            return 1
        if current.get("summary", {}).get("headings") != total_headings:
            print(f"stale: {current.get('summary', {}).get('headings')} headings, tree has {total_headings}")
            return 1
        print(f"OK: {len(files)} files, {total_headings} headings")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(json.dumps(payload["summary"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
