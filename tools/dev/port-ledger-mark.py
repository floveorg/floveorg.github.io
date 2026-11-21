#!/usr/bin/env python3
"""Mark selected headings in the working port ledger.

Phase 2 helper. Copies `port-ledger.skeleton.json` to `port-ledger.json` on
first use, then applies a JSON map of exact heading text to destination fields.

Usage:
  python3 tools/dev/port-ledger-mark.py --source <source> --map <map.json>
  python3 tools/dev/port-ledger-mark.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "development/wiki"
SKELETON = WIKI / "port-ledger.skeleton.json"
LEDGER = WIKI / "port-ledger.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source")
    ap.add_argument("--map")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        if not LEDGER.exists():
            print(f"missing {LEDGER.relative_to(ROOT)}")
            return 1
        data = json.loads(LEDGER.read_text())
        pending = sum(
            1
            for f in data["files"]
            for h in f["headings"]
            if h["mode"] == "pending"
        )
        print(f"OK: {data['summary']['files']} files, {data['summary']['headings']} headings, {pending} pending")
        return 0

    if not (args.source and args.map):
        ap.error("--source and --map are required unless --check")

    if LEDGER.exists():
        data = json.loads(LEDGER.read_text())
    else:
        data = json.loads(SKELETON.read_text())

    mapping = json.loads(Path(args.map).read_text())
    source = args.source
    hit = 0
    for f in data["files"]:
        if f["source"] != source:
            continue
        for h in f["headings"]:
            if h["heading"] not in mapping:
                continue
            spec = mapping[h["heading"]]
            h.update(
                {
                    "mode": spec["mode"],
                    "destination": spec.get("destination"),
                    "destination_anchor": spec.get("destination_anchor"),
                    "provenance": spec.get("provenance"),
                    "signoff": spec.get("signoff"),
                    "summary_reason": spec.get("summary_reason"),
                }
            )
            hit += 1
    if hit != len(mapping):
        print(f"warning: applied {hit} of {len(mapping)} mappings for {source}")

    counts = {"pending": 0, "ported": 0, "linked": 0, "archive-only": 0}
    for f in data["files"]:
        for h in f["headings"]:
            counts[h["mode"]] = counts.get(h["mode"], 0) + 1
    data["schema"] = "flove-port-ledger/1"
    data["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data["summary"]["by_mode"] = counts
    data["summary"]["pending"] = counts["pending"]
    data["summary"]["completed"] = data["summary"]["headings"] - counts["pending"]
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {LEDGER.relative_to(ROOT)}; {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
