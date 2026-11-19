#!/usr/bin/env python3
"""build-depth-md.py — sync the Data depth table into backend.md.

Reads the canonical table in development/index.html (Data → Data) and rewrites
the marked copy in development/standards/backend.md. `--check` reports drift
without writing; `updaty4` runs it before packaging.

    python3 development/scripts/build-depth-md.py            # rewrite
    python3 development/scripts/build-depth-md.py --check    # exit 1 on drift
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "development/index.html"
DST = ROOT / "development/standards/backend.md"
START = "<!-- depth:start -->"
END = "<!-- depth:end -->"
COLS = ["Level", "Name", "What it covers", "Commands"]


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def table() -> str:
    src = SRC.read_text(encoding="utf-8")
    match = re.search(
        r'<table class="atype-table depth-table">(.*?)</table>', src, re.S
    )
    if not match:
        raise SystemExit("depth table not found in development/index.html")
    rows = []
    for tr in re.findall(r"<tr>(.*?)</tr>", match.group(1), re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(cells) == 4:
            rows.append([clean(c) for c in cells])
    if not rows:
        raise SystemExit("depth table has no rows")
    out = ["| " + " | ".join(COLS) + " |", "|" + "|".join(["---"] * 4) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def main() -> int:
    check = "--check" in sys.argv
    body = table()
    dst = DST.read_text(encoding="utf-8")
    if START not in dst or END not in dst:
        raise SystemExit(f"markers {START} / {END} missing in {DST}")
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        START + "\n" + body + "\n" + END,
        dst,
        flags=re.S,
    )
    if check:
        if new != dst:
            print("Data depth table STALE — run python3 development/scripts/build-depth-md.py")
            return 1
        print(f"Data depth table OK ({len(body.splitlines()) - 2} rows)")
        return 0
    if new != dst:
        DST.write_text(new, encoding="utf-8")
        print(f"Data depth table synced → {DST.relative_to(ROOT)}")
    else:
        print("Data depth table already in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
