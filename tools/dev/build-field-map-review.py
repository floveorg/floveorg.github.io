#!/usr/bin/env python3
"""Build a field-map review report from the phase-0 register inventory.

This is a review artifact, not a migration step. It groups the 801
`needs_review` rows by the 28 hito fields so the owner can accept or override
one mapping per field instead of reviewing one task at a time.

Usage:
  python3 tools/dev/build-field-map-review.py --write
  python3 tools/dev/build-field-map-review.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "development/wiki/register-path-inventory.json"
OUT_JSON = ROOT / "development/wiki/field-map-review.json"
OUT_MD = ROOT / "development/wiki/field-map-review.md"

# The proposed field map is also in wiki.json; duplicate it here so the report
# is readable without opening the manifest.
FIELD_MAP = {
    "docs/map": "development/standards/plan.md",
    "docs/plan": "development/standards/plan.md",
    "docs/work": "development/standards/work.md",
    "backend/contracts": "development/standards/systems.md",
    "backend/delivery": "development/standards/scripts.md",
    "backend/storage": "development/standards/storage.md",
    "backend/systems": "development/standards/systems.md",
    "backend/mynet": "development/standards/mynet.md",
    "frontend/a11y": "development/standards/accessibility.md",
    "frontend/levels": "development/standards/experience.md",
    "frontend/quality": "development/standards/experience.md",
    "frontend/shell": "development/standards/apps.md",
    "frontend/tours": "development/standards/experience.md",
    "frontend/tree": "development/standards/apps.md",
    "frontend/types": "development/standards/apps.md",
    "frontend/visual": "development/standards/apps.md",
    "ai/flows": "development/standards/flows.md",
    "ai/levels": "development/standards/models.md",
    "ai/models": "development/standards/models.md",
    "ai/skills": "development/standards/skills.md",
    "data/index": "development/standards/json.md",
    "data/json": "development/standards/json.md",
    "data/mds": "development/standards/mds.md",
    "data/schemas": "development/standards/schemas.md",
    "community/channels": "development/standards/channels.md",
    "community/docs": "development/standards/docs.md",
    "community/feedback": "development/standards/feedback.md",
    "community/language": "development/standards/language.md",
    "community/levels": "development/standards/language.md",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("choose --write or --check")

    inv = json.loads(INV.read_text())
    groups: dict[str, dict] = {}
    for field, target in FIELD_MAP.items():
        groups[field] = {
            "field": field,
            "target": target,
            "rows": 0,
            "needs_review": 0,
            "sources": Counter(),
            "targets": Counter(),
            "samples": [],
        }

    unknown = []
    for item in inv["items"]:
        key = f"{item.get('section')}/{item.get('hito_field')}"
        if key not in groups:
            if item["needs_review"]:
                unknown.append(item)
            continue
        g = groups[key]
        g["rows"] += 1
        if item["needs_review"]:
            g["needs_review"] += 1
        if item["base"]:
            g["sources"][item["base"]] += 1
        if item["target"]:
            g["targets"][item["target"].split("#")[0]] += 1
        if item["needs_review"] and len(g["samples"]) < 3:
            g["samples"].append(
                {
                    "record": item.get("record"),
                    "old": item["base"],
                    "target": item["target"],
                    "rule": item["rule"],
                }
            )

    rows = []
    for field in FIELD_MAP:
        g = groups[field]
        rows.append(
            {
                "field": field,
                "target": g["target"],
                "rows": g["rows"],
                "needs_review": g["needs_review"],
                "sources": [
                    {"source": s, "rows": n}
                    for s, n in g["sources"].most_common(8)
                ],
                "other_targets": [
                    {"target": t, "rows": n}
                    for t, n in g["targets"].most_common()
                    if t != g["target"]
                ],
                "samples": g["samples"],
                "action": "accept" if g["needs_review"] == 0 else "review",
            }
        )

    payload = {
        "schema": "flove-field-map-review/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_inventory": str(INV.relative_to(ROOT)),
        "fields": len(rows),
        "rows": sum(r["rows"] for r in rows),
        "needs_review": sum(r["needs_review"] for r in rows),
        "unknown_review_rows": len(unknown),
        "map": rows,
    }

    if args.check:
        if not OUT_JSON.exists():
            print(f"missing {OUT_JSON.relative_to(ROOT)}")
            return 1
        print(f"OK: {payload['fields']} fields, {payload['needs_review']} review rows")
        return 0

    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# Field-map review",
        "",
        f"> Generated from `{INV.relative_to(ROOT)}`.",
        f"> {payload['rows']} routed rows · {payload['needs_review']} need review · "
        f"{payload['unknown_review_rows']} outside the {payload['fields']} fields.",
        "",
        "The default rule is: **accept the target below for the whole field**. A",
        "row is only overridden when a task names a different owner in its title or",
        "`Decision:` clause. Accepting a field clears all of its review rows.",
        "",
        "| Field | Target | Rows | Review | Other targets |",
        "|---|---|---:|---:|---|",
    ]
    for r in rows:
        others = ", ".join(f"`{x['target']}`×{x['rows']}" for x in r["other_targets"][:2]) or "—"
        lines.append(
            f"| `{r['field']}` | `{r['target']}` | {r['rows']} | {r['needs_review']} | {others} |"
        )
    lines += [
        "",
        "## Review examples",
        "",
    ]
    for r in rows:
        if not r["samples"]:
            continue
        lines += [f"### `{r['field']}` → `{r['target']}`", ""]
        for s in r["samples"]:
            lines.append(
                f"- `{s['record']}`: `{s['old']}` → `{s['target']}` (`{s['rule']}`)"
            )
        lines.append("")
    lines += [
        "## Sign-off",
        "",
        "Reply with the field keys to accept, or the keys to override with a new",
        "target. Until then these rows stay `needs_review`.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(json.dumps({k: payload[k] for k in ("fields", "rows", "needs_review", "unknown_review_rows")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
