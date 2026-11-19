#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh the `love` snapshot embedded in apps/puzzy/love.html.

The full-view page is self-contained: its data block is a snapshot of
`tools/puzzy.json` -> `words.love`. This script keeps the snapshot honest.

Usage:
  python3 development/scripts/build-puzzy-demo.py            # report drift
  python3 development/scripts/build-puzzy-demo.py --apply    # rewrite the data block
  python3 development/scripts/build-puzzy-demo.py --check    # exit 1 when the snapshot is stale
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PUZZY = ROOT / "tools/puzzy.json"
PAGE = ROOT / "apps/puzzy/love.html"

BLOCK = re.compile(
    r'(<script type="application/json" id="love-data">)(.*?)(</script>)',
    re.S,
)


def snapshot() -> dict:
    love = json.loads(PUZZY.read_text(encoding="utf-8"))["words"]["love"]
    bundle = love["bundle"]
    return {
        "entry": bundle["entries"][0],
        "stubs": [
            {"id": e["id"], "lemma": e["lemma"], "gloss": e["senses"][0]["gloss"]}
            for e in bundle["entries"][1:]
        ],
        "frames": bundle["frames"],
        "annotation": bundle["annotations"][0],
        "wisy": love["views"]["wisy"],
    }


def render(page: str, data: dict) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=1)
    return BLOCK.sub(lambda m: m.group(1) + text + m.group(3), page, count=1)


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    data = snapshot()
    out = render(page, data)
    stale = out != page

    if "--apply" in sys.argv:
        PAGE.write_text(out, encoding="utf-8")
        print(f"wrote {PAGE.relative_to(ROOT)} ({len(data['entry']['senses'])} senses, {len(data['frames'])} frames)")
        return 0

    if "--check" in sys.argv:
        if stale:
            print("apps/puzzy/love.html is stale — run development/scripts/build-puzzy-demo.py --apply", file=sys.stderr)
            return 1
        print("ok: love.html snapshot matches tools/puzzy.json")
        return 0

    print("stale" if stale else "ok: love.html snapshot matches tools/puzzy.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
