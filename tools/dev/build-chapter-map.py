#!/usr/bin/env python3
"""Build the chapter map from the milestone spine.

Phase 2a: one chapter per milestone field, grouped under its owning topic page.
Counts (hitos/tasks/open/closed) come from the register; evidence sources come
from the phase-0 inventory. The map is the content order for phase 2.

Usage:
  python3 tools/dev/build-chapter-map.py --write
  python3 tools/dev/build-chapter-map.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "development"
REGISTER = DEV / "wiki/work/milestones.json"
MANIFEST = DEV / "wiki/wiki.json"
INV = DEV / "wiki/register-path-inventory.json"
OUT_JSON = DEV / "wiki/chapter-map.json"
OUT_MD = DEV / "wiki/chapter-map.md"

FIELD_TITLES = {
    "docs/map": "Map",
    "docs/plan": "Plan",
    "docs/work": "Work",
    "backend/contracts": "Contracts",
    "backend/delivery": "Delivery",
    "backend/storage": "Storage",
    "backend/systems": "Systems",
    "backend/mynet": "MyNet",
    "frontend/a11y": "Accessibility",
    "frontend/levels": "Levels",
    "frontend/quality": "Quality",
    "frontend/shell": "Shell",
    "frontend/tours": "Tours",
    "frontend/tree": "Tree",
    "frontend/types": "Types",
    "frontend/visual": "Visual",
    "ai/flows": "Flows",
    "ai/levels": "Levels",
    "ai/models": "Models",
    "ai/skills": "Skills",
    "data/index": "Data index",
    "data/json": "JSON",
    "data/mds": "MDs",
    "data/schemas": "Schemas",
    "community/channels": "Channels",
    "community/docs": "Docs",
    "community/feedback": "Feedback",
    "community/language": "Language",
    "community/levels": "Levels",
}


def slug(text: str) -> str:
    out = []
    for ch in text.lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join("".join(out).split("-")).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("choose --write or --check")

    data = json.loads(REGISTER.read_text())
    manifest = json.loads(MANIFEST.read_text())
    inv = json.loads(INV.read_text())
    field_map = manifest["field_map"]
    pages = {p["id"]: p for p in manifest["pages"] if p["kind"] == "topic"}

    chapters: dict[str, dict] = {}
    for field, page_path in field_map.items():
        page = next((p for p in pages.values() if p["path"] == page_path), None)
        if not page:
            continue
        cid = f"{page['id']}::{field}"
        chapters[cid] = {
            "id": cid,
            "field": field,
            "title": FIELD_TITLES.get(field, field.split("/")[-1].title()),
            "page": page["id"],
            "page_path": page["path"],
            "chapter_anchor": "#" + slug(FIELD_TITLES.get(field, field.split("/")[-1])),
            "hitos": [],
            "tasks": 0,
            "open_hitos": 0,
            "closed_hitos": 0,
            "task_states": {},
            "evidence_sources": set(),
            "milestone_only": True,
        }

    for section in data.get("sections", []):
        top = section.get("section", "")
        for sub in section.get("subsections", []):
            for hito in sub.get("milestones", []):
                key = f"{top}/{hito.get('section', '')}"
                page_path = field_map.get(key)
                if not page_path:
                    continue
                page = next((p for p in pages.values() if p["path"] == page_path), None)
                if not page:
                    continue
                cid = f"{page['id']}::{key}"
                c = chapters.get(cid)
                if not c:
                    continue
                tasks = hito.get("tasks", [])
                c["hitos"].append(
                    {
                        "id": hito.get("id"),
                        "title": hito.get("en", ""),
                        "state": hito.get("state", ""),
                    }
                )
                c["tasks"] += len(tasks)
                if hito.get("state") == "on":
                    c["closed_hitos"] += 1
                else:
                    c["open_hitos"] += 1
                for t in tasks:
                    c["task_states"][t.get("state", "?")] = c["task_states"].get(t.get("state", "?"), 0) + 1

    for item in inv["items"]:
        key = f"{item.get('section')}/{item.get('hito_field')}"
        page_path = field_map.get(key)
        if not page_path:
            continue
        page = next((p for p in pages.values() if p["path"] == page_path), None)
        if not page:
            continue
        cid = f"{page['id']}::{key}"
        if cid in chapters and item.get("base"):
            chapters[cid]["evidence_sources"].add(item["base"])

    rows = []
    for c in chapters.values():
        page = pages[c["page"]]
        c["page_sources"] = sorted(set(page.get("supersedes", [])))
        c["evidence_sources"] = sorted(set(c["evidence_sources"]) | set(c["page_sources"]))
        c["milestone_only"] = not c["evidence_sources"]
        rows.append(c)

    # Group by page.
    by_page: dict[str, list[dict]] = defaultdict(list)
    for c in rows:
        by_page[c["page"]].append(c)
    page_rows = []
    for page_id, cs in sorted(by_page.items()):
        page = pages[page_id]
        page_rows.append(
            {
                "page": page_id,
                "path": page["path"],
                "chapters": sorted(cs, key=lambda x: x["field"]),
                "hitos": sum(len(c["hitos"]) for c in cs),
                "tasks": sum(c["tasks"] for c in cs),
                "open_hitos": sum(c["open_hitos"] for c in cs),
                "closed_hitos": sum(c["closed_hitos"] for c in cs),
                "page_sources": sorted({s for c in cs for s in c["page_sources"]}),
            }
        )

    payload = {
        "schema": "flove-chapter-map/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": str(REGISTER.relative_to(ROOT)),
        "pages": page_rows,
        "totals": {
            "pages": len(page_rows),
            "chapters": len(rows),
            "hitos": sum(p["hitos"] for p in page_rows),
            "tasks": sum(p["tasks"] for p in page_rows),
            "open_hitos": sum(p["open_hitos"] for p in page_rows),
            "closed_hitos": sum(p["closed_hitos"] for p in page_rows),
        },
    }

    if args.check:
        if not OUT_JSON.exists():
            print(f"missing {OUT_JSON.relative_to(ROOT)}")
            return 1
        current = json.loads(OUT_JSON.read_text())
        if current.get("totals") != payload["totals"]:
            print("stale: chapter totals differ from the register")
            return 1
        print(f"OK: {payload['totals']['pages']} pages, {payload['totals']['chapters']} chapters")
        return 0

    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    # Reflect the chapter/work data in the manifest.
    manifest["pages"] = [
        {
            **page,
            "chapters": [
                {
                    "id": c["id"],
                    "field": c["field"],
                    "title": c["title"],
                    "hitos": len(c["hitos"]),
                    "tasks": c["tasks"],
                    "open_hitos": c["open_hitos"],
                    "closed_hitos": c["closed_hitos"],
                    "evidence_sources": len(c["evidence_sources"]),
                }
                for c in by_page.get(page["id"], [])
            ],
        }
        if page["kind"] == "topic"
        else page
        for page in manifest["pages"]
    ]
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    lines = [
        "# Chapter map",
        "",
        f"> Generated from `{REGISTER.relative_to(ROOT)}` and `wiki.json`.",
        f"> {payload['totals']['chapters']} chapters · {payload['totals']['hitos']} hitos · "
        f"{payload['totals']['tasks']} tasks · {payload['totals']['open_hitos']} open hitos.",
        "",
        "Each chapter is a milestone field. The page order is the topic grid; the",
        "chapter order is the field order below.",
        "",
    ]
    for p in page_rows:
        lines += [
            f"## {p['page']} — `{p['path']}`",
            "",
            f"{p['hitos']} hitos · {p['tasks']} tasks · {p['open_hitos']} open · {p['closed_hitos']} closed · {len(p['page_sources'])} page sources",
            "",
            "| Chapter | Field | Hitos | Tasks | Evidence |",
            "|---|---|---:|---:|---|",
        ]
        for c in p["chapters"]:
            ev = "milestone-only" if c["milestone_only"] else f"{len(c['evidence_sources'])} sources"
            lines.append(f"| {c['title']} | `{c['field']}` | {len(c['hitos'])} | {c['tasks']} | {ev} |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(json.dumps(payload["totals"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
