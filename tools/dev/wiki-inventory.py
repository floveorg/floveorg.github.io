#!/usr/bin/env python3
"""Build the docs-wiki migration inventory from the live register.

Phase 0 tool for development/docs-wiki-migration-plan.md. It never edits
milestones.json: it only records every path occurrence, its target, the mapping
rule and whether an owner must review the mapping.

Usage:
  python3 tools/dev/wiki-inventory.py --write
  python3 tools/dev/wiki-inventory.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "development"
REGISTER = DEV / "wiki/work/milestones.json"
OUT_JSON = DEV / "wiki/register-path-inventory.json"
OUT_MD = DEV / "wiki/register-path-inventory.md"

PATH_RE = re.compile(r"(https://flove\.org/)?(development/[A-Za-z0-9_./#-]+)")

FIELD_MAP = {
    "docs/map": "plan",
    "docs/plan": "plan",
    "docs/work": "work",
    "backend/contracts": "systems",
    "backend/delivery": "scripts",
    "backend/storage": "storage",
    "backend/systems": "systems",
    "frontend/a11y": "accessibility",
    "frontend/levels": "experience",
    "frontend/quality": "experience",
    "frontend/shell": "apps",
    "frontend/tours": "experience",
    "frontend/tree": "apps",
    "frontend/types": "apps",
    "frontend/visual": "apps",
    "ai/flows": "flows",
    "ai/levels": "models",
    "ai/models": "models",
    "ai/skills": "skills",
    "data/index": "json",
    "data/json": "json",
    "data/mds": "mds",
    "data/schemas": "schemas",
    "community/channels": "channels",
    "community/docs": "docs",
    "community/feedback": "feedback",
    "community/language": "language",
    "community/levels": "language",
}

# Files that split. A task/fact is routed by the hito field map, then this
# default; every such row is flagged for owner review.
SPLIT_DEFAULT = {
    "development/standards/backend.md": "systems",
    "development/standards/adoption.md": "systems",
    "development/standards/worldview.md": "contract",
    "development/standards/debates/browsy/spec.md": "mynet",
    "development/standards/debates/browsy/browsy-questions.md": "work",
    "development/standards/debates/browsy/rationale.md": "mynet",
    "development/standards/debates/browsy/README.md": "systems",
    "development/standards/debates/browsy/TESTING.md": "systems",
    "development/standards/debates/browsy/port-nety.md": "systems",
    "development/standards/debates/plans/2026-11-21-app-database-stages.md": "storage",
    "development/standards/debates/plans/2026-11-17-appy-authy-mynet.md": "mynet",
    "development/standards/debates/plans/2026-11-20-appy-dashboard-redesign.md": "apps",
    "development/standards/debates/plans/central-backend.md": "systems",
    "development/standards/debates/plans/puzzy.md": "apps",
    "development/standards/debates/plans/standards.md": "work",
    "development/standards/debates/proposals/frontend-wizy.md": "apps",
    "development/standards/debates/bridges/oasis.md": "mynet",
    "development/standards/apps/README.md": "apps",
    "development/standards/apps/onboarding-copy.md": "experience",
    "development/standards/debates/questy-proposals.md": "skills",
    "development/standards/debates/standards.md": "mds",
    "development/standards/debates/UseCase-adv.md": "flows",
}

EXACT = {
    "development/standards/debates/INDEX.md": ("move", "development/wiki/INDEX.md", "index"),
    "development/standards/debates/pendings.md": ("move", "development/wiki/work/pendings.md", "pendings"),
    "development/standards/debates/task-set-plan.md": ("move", "development/wiki/work/measures.md", "measures"),
    "development/standards/debates/hitos-audit.md": ("move", "development/wiki/work/measures.md", "measures"),
    "development/standards/debates/plans/index.md": ("move", "development/standards/plan.md", "plans-index"),
    "development/standards/debates/plans/conflicts.md": ("move", "development/wiki/plans/conflicts.md", "conflicts"),
    "development/standards/debates/plans/standards.md": ("move", "development/wiki/work/pendings.md", "standards-decisions"),
    "development/standards/debates/plans/2026-11-19-authy-open-questions.md": ("move", "development/standards/work.md", "open-questions"),
    "development/standards/debates/plans/2026-11-14-app-tier-planned.md": ("move", "development/standards/apps.md", "app-tier"),
    "development/standards/debates/plans/2026-06-18-nety-frontend-build.md": ("move", "development/standards/apps.md", "nety-frontend"),
    "development/standards/debates/plans/2026-06-18-nety-frontend-build.md.bak-orig": ("archive", "development/wiki/archive/old/plans/2026-06-18-nety-frontend-build.md.bak-orig", "bak"),
    "development/standards/debates/proposals/frontend-tiers.md": ("move", "development/standards/apps.md", "frontend-tiers"),
    "development/standards/debates/a11y-report.md": ("move", "development/standards/accessibility.md", "a11y-report"),
    "development/standards/debates/others/flove-libs-insights.md": ("move", "development/standards/mds.md", "libs"),
    "development/standards/debates/research/vr_interfaces.md": ("move", "development/standards/experience.md", "vr"),
    "development/standards/debates/reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md": ("move", "development/standards/systems.md", "review"),
    "development/standards/debates/roadmap-2026-06.md": ("move", "development/standards/plan.md", "roadmap"),
    "development/standards/debates/proposals.md": ("move", "development/standards/plan.md", "proposals"),
        "development/standards/debates/browsy/pre-build/01-mvp.md": ("move", "development/standards/mynet.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/02-authy-levels.md": ("move", "development/standards/mynet.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/03-schemas.md": ("move", "development/standards/schemas.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/04-myfamily-profile.md": ("move", "development/standards/schemas.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/05-native-host.md": ("move", "development/standards/systems.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/06-bridge-threat-model.md": ("move", "development/standards/systems.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/07-lineage-tests.md": ("move", "development/standards/mynet.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/08-model-labels.md": ("move", "development/standards/experience.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/09-consult-agreements.md": ("move", "development/standards/schemas.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/11-ui-pending.md": ("move", "development/standards/experience.md", "prebuild"),
    "development/standards/debates/browsy/pre-build/README.md": ("move", "development/standards/plan.md", "prebuild-index"),
    "development/standards/debates/browsy/pre-build/open-issues.md": ("archive", "development/wiki/archive/old/browsy/pre-build/open-issues.md", "closed-log"),
}

ARCHIVE_FILES = {
    "development/standards/debates/agents.md",
    "development/standards/debates/skills-library.md",
    "development/standards/debates/archive.md",
    "development/standards/debates/a11y-development-index.md",
}

KEEP_PREFIXES = (
    "development/standards/frontend/",
    "development/standards/skills/",
    "development/standards/risaliberada/",
    "development/standards/workflow/",
    "development/standards/vendor/",
    "development/standards/puzzy/",
    "development/standards/apps/",  # README/onboarding are handled as split above
    "apps/",
    "projects/",
    "docs/",
    "development/media/",
    "development/addons/",
)
KEEP_FILES = {
    "development/standards/contract.md",
    "development/standards/puzzy.md",
    "development/standards/vocabulary.md",
    "development/standards/vocabulary.html",
    "development/standards/README.md",
    "development/standards/_sidebar.md",
    "development/standards/index.html",
    "development/AGENTS.md",
    "development/index.html",
}

MERGED = {
    "development/standards/AGENTS.md": ("merge", "development/AGENTS.md", "agents-merge"),
}

WORK_FILES = {
    "development/wiki/work/milestones.json": ("move", "development/wiki/work/milestones.json", "register"),
    "development/standards/debates/common.json": ("generated", "development/wiki/work/common.json", "generated"),
    "development/standards/debates/work-moves.json": ("generated", "development/wiki/work/work-moves.json", "inbox"),
}


def classify(path: str, meta: dict) -> dict:
    """Return action/target/rule/needs_review for one old path."""
    if path in WORK_FILES:
        action, target, rule = WORK_FILES[path]
        return dict(action=action, target=target, rule=rule, needs_review=False)
    if path in MERGED:
        action, target, rule = MERGED[path]
        return dict(action=action, target=target, rule=rule, needs_review=False)
    if path in EXACT:
        action, target, rule = EXACT[path]
        return dict(action=action, target=target, rule=rule, needs_review=False)
    if path in SPLIT_DEFAULT:
        topic = FIELD_MAP.get(f"{meta.get('section')}/{meta.get('field')}") or SPLIT_DEFAULT[path]
        return dict(
            action="move",
            target=f"development/standards/{topic}.md",
            rule="field_map" if f"{meta.get('section')}/{meta.get('field')}" in FIELD_MAP else "default",
            needs_review=True,
        )
    if path.startswith("development/scripts/"):
        return dict(action="move", target=f"tools/dev/{Path(path).name}", rule="script", needs_review=False)
    if path.startswith("development/standards/scripts/"):
        return dict(action="move", target=f"tools/dev/{Path(path).name}", rule="script", needs_review=False)
    if path in ARCHIVE_FILES or path.startswith("development/standards/debates/archive/"):
        rel = path.split("development/standards/debates/", 1)[1]
        return dict(action="archive", target=f"development/wiki/archive/old/{rel}", rule="archive", needs_review=False)
    if path in KEEP_FILES or path.startswith(KEEP_PREFIXES):
        return dict(action="keep", target=path, rule="keep", needs_review=False)
    if path.startswith("development/standards/debates/"):
        return dict(action="move", target=None, rule="unmapped", needs_review=True)
    if path.startswith("development/standards/apps/"):
        return dict(action="move", target="development/standards/apps.md", rule="apps-default", needs_review=True)
    return dict(action="keep", target=path, rule="keep", needs_review=False)


def scan_text(text: str, meta: dict) -> list[dict]:
    out = []
    for m in PATH_RE.finditer(text):
        is_url = bool(m.group(1))
        raw = m.group(2).rstrip(".,;:")
        base, _, anchor = raw.partition("#")
        cls = classify(base, meta)
        target = cls["target"]
        if target and anchor:
            target = f"{target}#{anchor}"
        if target and is_url:
            target = f"https://flove.org/{target}"
        out.append(
            {
                "old": raw,
                "base": base,
                "anchor": anchor or None,
                "kind": "url" if is_url else "path",
                "action": cls["action"],
                "target": target,
                "rule": cls["rule"],
                "needs_review": cls["needs_review"],
                "field": meta.get("field_path"),
                "record": meta.get("record"),
                "hito": meta.get("hito"),
                "section": meta.get("section"),
                "hito_field": meta.get("field"),
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the inventory files")
    ap.add_argument("--check", action="store_true", help="check the generated files are current")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("choose --write or --check")

    data = json.loads(REGISTER.read_text())
    items: list[dict] = []
    hito_meta: dict[str, dict] = {}

    def add_text(text, meta):
        if isinstance(text, str):
            items.extend(scan_text(text, meta))

    for section in data.get("sections", []):
        top = section.get("section", "")
        for sub in section.get("subsections", []):
            for hito in sub.get("milestones", []):
                hmeta = {
                    "section": top,
                    "field": hito.get("section", ""),
                    "hito": hito.get("id"),
                    "record": hito.get("id"),
                }
                hito_meta[hito.get("id")] = hmeta
                for key in ("source", "notes", "en", "es"):
                    add_text(hito.get(key), {**hmeta, "field_path": f"hitos[{hito.get('id')}].{key}"})
                for i, url in enumerate(hito.get("standards", [])):
                    add_text(url, {**hmeta, "field_path": f"hitos[{hito.get('id')}].standards[{i}]"})
                for i, url in enumerate(hito.get("docs", [])):
                    add_text(url, {**hmeta, "field_path": f"hitos[{hito.get('id')}].docs[{i}]"})
                for task in hito.get("tasks", []):
                    tmeta = {
                        "section": top,
                        "field": hito.get("section", ""),
                        "hito": hito.get("id"),
                        "record": task.get("id"),
                    }
                    add_text(task.get("owner"), {**tmeta, "field_path": f"tasks[{task.get('id')}].owner"})
                    for i, gap in enumerate(task.get("evidence", {}).get("gaps", [])):
                        add_text(gap, {**tmeta, "field_path": f"tasks[{task.get('id')}].evidence.gaps[{i}]"})

    for task in data.get("tasks_archive", []):
        base_meta = hito_meta.get(task.get("hito_id"), {})
        meta = {
            "section": base_meta.get("section", ""),
            "field": base_meta.get("field", ""),
            "hito": task.get("hito_id"),
            "record": task.get("id"),
        }
        for i, gap in enumerate(task.get("evidence", {}).get("gaps", [])):
            add_text(gap, {**meta, "field_path": f"tasks_archive[{task.get('id')}].evidence.gaps[{i}]"})

    for ticket in data.get("new_tickets", []):
        meta = {
            "section": ticket.get("category", ""),
            "field": ticket.get("section", ""),
            "record": ticket.get("id"),
        }
        for key in ("source", "notes", "origin"):
            add_text(ticket.get(key), {**meta, "field_path": f"new_tickets[{ticket.get('id')}].{key}"})

    add_text(data.get("taskSet", {}).get("moves_inbox"), {
        "section": "", "field": "", "record": "taskSet", "field_path": "taskSet.moves_inbox"
    })

    counts = {
        "occurrences": len(items),
        "move": sum(1 for x in items if x["action"] == "move"),
        "archive": sum(1 for x in items if x["action"] == "archive"),
        "generated": sum(1 for x in items if x["action"] == "generated"),
        "merge": sum(1 for x in items if x["action"] == "merge"),
        "keep": sum(1 for x in items if x["action"] == "keep"),
        "needs_review": sum(1 for x in items if x["needs_review"]),
    }
    counts["moving"] = counts["move"] + counts["archive"] + counts["generated"] + counts["merge"]
    by_field: dict[str, int] = {}
    for item in items:
        by_field[item["field"] or "?"] = by_field.get(item["field"] or "?", 0) + 1
    review_by_rule: dict[str, int] = {}
    review_by_field: dict[str, int] = {}
    mappings: dict[tuple[str, str], int] = {}
    for item in items:
        if item["needs_review"]:
            review_by_rule[item["rule"]] = review_by_rule.get(item["rule"], 0) + 1
            key = f"{item.get('section')}/{item.get('hito_field')}"
            review_by_field[key] = review_by_field.get(key, 0) + 1
        if item["action"] != "keep" and item["target"]:
            mappings[(item["base"], item["target"].split("#")[0])] = mappings.get((item["base"], item["target"].split("#")[0]), 0) + 1

    payload = {
        "schema": "flove-register-inventory/1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "baseline_commit": "170cfee3473b17fa1428ea64c5eeb186bb21491d",
        "source": str(REGISTER.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(REGISTER.read_bytes()).hexdigest(),
        "counts": counts,
        "by_field": dict(sorted(by_field.items())),
        "review_by_rule": dict(sorted(review_by_rule.items())),
        "review_by_field": dict(sorted(review_by_field.items())),
        "items": items,
    }

    if args.check:
        if not OUT_JSON.exists():
            print(f"missing {OUT_JSON.relative_to(ROOT)}")
            return 1
        current = json.loads(OUT_JSON.read_text())
        if current.get("source_sha256") != payload["source_sha256"]:
            print("inventory is stale: milestones.json changed")
            return 1
        print(f"OK: inventory has {len(items)} path occurrences")
        return 0

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# Register path inventory",
        "",
        f"> Generated from `{REGISTER.relative_to(ROOT)}` at `170cfee3`.",
        f"> {counts['occurrences']} occurrences · {counts['moving']} moving · "
        f"{counts['keep']} staying · {counts['needs_review']} need review.",
        "",
        "| Action | Count |",
        "|---|---:|",
        f"| move | {counts['move']} |",
        f"| archive | {counts['archive']} |",
        f"| generated | {counts['generated']} |",
        f"| merge | {counts['merge']} |",
        f"| keep | {counts['keep']} |",
        f"| needs review | {counts['needs_review']} |",
        "",
        "The JSON is the gate input; this table is a summary.",
        "",
        "## Review queue by field",
        "",
        "| Section/field | Rows |",
        "|---|---:|",
        *[f"| {k} | {v} |" for k, v in sorted(review_by_field.items(), key=lambda kv: -kv[1])],
        "",
        "## Top source → target mappings",
        "",
        "| Source | Target | Rows |",
        "|---|---|---:|",
        *[f"| `{s}` | `{t}` | {n} |" for (s, t), n in sorted(mappings.items(), key=lambda kv: -kv[1])[:30]],
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
