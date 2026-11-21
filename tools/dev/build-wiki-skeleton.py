#!/usr/bin/env python3
"""Create the phase-1 docs-wiki skeleton.

Writes:
  development/wiki/wiki.json
  development/wiki/INDEX.md
  development/standards/<topic>.md          (19 draft topic pages)
  development/wiki/plans/<category>/<topic>.md
  development/wiki/plans/conflicts.md
  development/wiki/plans/debates/README.md
  development/wiki/work/.gitkeep
  development/wiki/archive/.gitkeep

It never rewrites an existing page or touches a live pointer. Run once for
phase 1; phase 2 replaces the draft bodies with migrated content.

Usage:
  python3 tools/dev/build-wiki-skeleton.py --write
  python3 tools/dev/build-wiki-skeleton.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "development"
STD = DEV / "standards"
WIKI = DEV / "wiki"
INV = WIKI / "register-path-inventory.json"
TODAY = "2026-11-21"

# trunk, topic, html places, owns
TOPICS = [
    ("docs", "plan", ["#plan-maps"], ["Plan map", "roadmap", "stage aliases"]),
    ("docs", "work", ["#work-tracker"], ["Open questions", "status", "acceptance tests"]),
    ("backend", "scripts", ["#localhost"], ["Script homes", "distro", "tooling"]),
    ("backend", "systems", ["#p2p"], ["Architecture", "bridge", "permissions"]),
    ("backend", "mynet", ["#p2p", "#messenger"], ["MyNet L1–L5", "flove-auth/1", "BSP acceptance"]),
    ("backend", "storage", ["#data-database"], ["Storage", "Web-of-Trust budget", "persistence"]),
    ("frontend", "apps", ["#apps"], ["App rollout", "tiers", "frontend build"]),
    ("frontend", "accessibility", ["#apps"], ["a11y baseline", "axe report"]),
    ("frontend", "experience", ["#apps"], ["UX tiers", "model labels", "pending surfaces"]),
    ("ai", "models", ["#ai"], ["Models", "AI levels"]),
    ("ai", "skills", ["#ai"], ["Skill library", "questy decisions"]),
    ("ai", "flows", ["#ai-note-wizy"], ["Wizy derivation", "use cases"]),
    ("data", "mds", ["#data"], ["MD sources", "library insights"]),
    ("data", "json", ["#data-json"], ["flovePortrait/1", "routing index", "data index"]),
    ("data", "schemas", ["#data"], ["Schemas", "storage keys", "flove-auth"]),
    ("community", "docs", ["#md-sources"], ["Docs navigation", "privacy-first docs"]),
    ("community", "feedback", ["#md-sources"], ["Feedback channels"]),
    ("community", "language", ["#md-sources"], ["Language", "onboarding copy"]),
    ("community", "channels", ["#messenger"], ["Chatland", "messenger"]),
]

STANDING = [
    ("standing", "puzzy", "puzzy.md", ["#data"], ["Puzzy extended definitions", "D0–D5 ladder"], True, "md"),
    ("standing", "frontend", "frontend/frontend.md", ["#apps"], ["Frontend catalogue", "§13 conventions"], True, "md"),
    ("standing", "skills", "skills/README.md", ["#ai"], ["Skill library", "standing rules"], False, "md"),
    ("standing", "risaliberada", "risaliberada/risaliberada.md", ["#apps"], ["Risa project book"], False, "md"),
    ("standing", "vocabulary", "vocabulary.md", ["#data"], ["Vocabulary matrix"], False, "md"),
    ("standing", "workflow", "workflow/workflow.html", [], ["Workflow demos"], False, "html"),
    ("governance", "contract", "contract.md", [], ["Values", "the floor"], False, "md"),
]

MAP_PAGES = [
    ("map", "index", "INDEX.md", ["wiki index", "plans map", "data-index map"]),
    ("map", "conflicts", "plans/conflicts.md", ["cross-plan conflicts"]),
    ("map", "debates-tray", "plans/debates/README.md", ["raw draft tray convention"]),
]

PLAN_TOPICS = [(trunk, topic) for trunk, topic, *_ in TOPICS]

TOPIC_TITLES = {
    "plan": "Plan", "work": "Work", "scripts": "Scripts", "systems": "Systems",
    "mynet": "MyNet", "storage": "Storage", "apps": "Apps",
    "accessibility": "Accessibility", "experience": "Experience", "models": "Models",
    "skills": "Skills", "flows": "Flows", "mds": "MD sources", "json": "JSON",
    "schemas": "Schemas", "docs": "Docs", "feedback": "Feedback",
    "language": "Language", "channels": "Channels",
}

# Old source -> primary/also topic pages. Used for the manifest supersedes graph.
D = "development/standards/debates/"
SOURCE_TOPICS = {
    "development/standards/backend.md": ["plan", "systems", "mds", "schemas", "json", "apps", "storage", "scripts", "mynet", "channels"],
    "development/standards/adoption.md": ["systems", "storage", "experience", "apps", "scripts"],
    "development/standards/worldview.md": ["plan", "contract"],
    "development/standards/apps/README.md": ["scripts", "apps", "plan", "skills"],
    "development/standards/apps/onboarding-copy.md": ["experience", "apps", "language"],
    D + "browsy/spec.md": ["mynet", "systems", "schemas", "apps", "experience", "plan", "flows", "work"],
    D + "browsy/browsy-questions.md": ["mynet", "experience", "work", "mds", "systems", "flows", "channels", "docs", "schemas"],
    D + "browsy/rationale.md": ["mynet", "docs", "plan", "systems", "schemas", "flows", "json", "mds", "work"],
    D + "browsy/README.md": ["systems", "mynet"],
    D + "browsy/TESTING.md": ["systems", "mynet"],
    D + "browsy/port-nety.md": ["systems", "mynet"],
    D + "plans/2026-11-21-app-database-stages.md": ["plan", "work", "json", "apps", "storage", "mynet"],
    D + "plans/2026-11-17-appy-authy-mynet.md": ["mynet", "systems", "schemas", "apps", "experience", "storage", "work", "plan"],
    D + "plans/2026-11-20-appy-dashboard-redesign.md": ["apps", "experience", "plan", "json"],
    D + "plans/central-backend.md": ["systems", "storage", "mynet", "mds", "experience"],
    D + "plans/puzzy.md": ["apps", "work"],
    D + "plans/2026-06-18-nety-frontend-build.md": ["apps", "experience", "scripts", "plan"],
    D + "plans/2026-11-14-app-tier-planned.md": ["apps"],
    D + "plans/2026-11-19-authy-open-questions.md": ["work"],
    D + "proposals/frontend-wizy.md": ["apps", "flows", "work", "experience"],
    D + "proposals/frontend-tiers.md": ["apps"],
    D + "bridges/oasis.md": ["mynet", "systems", "schemas", "work", "mds"],
    D + "a11y-report.md": ["accessibility"],
    D + "others/flove-libs-insights.md": ["mds", "contract"],
    D + "research/vr_interfaces.md": ["experience"],
    D + "reviews/2026-07-25-browsy-fastapi-libsql-performance-review.md": ["systems"],
    D + "roadmap-2026-06.md": ["plan"],
    D + "proposals.md": ["plan"],
    D + "questy-proposals.md": ["skills", "flows", "mds"],
    D + "standards.md": ["skills", "flows", "mds"],
    D + "UseCase-adv.md": ["flows"],
    D + "browsy/pre-build/01-mvp.md": ["mynet"],
    D + "browsy/pre-build/02-authy-levels.md": ["mynet", "schemas"],
    D + "browsy/pre-build/03-schemas.md": ["schemas", "json"],
    D + "browsy/pre-build/04-myfamily-profile.md": ["schemas", "mynet", "experience"],
    D + "browsy/pre-build/05-native-host.md": ["systems"],
    D + "browsy/pre-build/06-bridge-threat-model.md": ["systems"],
    D + "browsy/pre-build/07-lineage-tests.md": ["mynet"],
    D + "browsy/pre-build/08-model-labels.md": ["experience"],
    D + "browsy/pre-build/09-consult-agreements.md": ["schemas", "mynet"],
    D + "browsy/pre-build/11-ui-pending.md": ["experience"],
    D + "browsy/pre-build/README.md": ["plan", "work", "mds"],
}


def archive_for(src: str) -> str | None:
    """Archive path for an old standards source, or None when it stays."""
    if src == "development/standards/contract.md":
        return None
    if src.startswith("development/standards/debates/"):
        return "development/wiki/archive/old/" + src.split("development/standards/debates/", 1)[1]
    if src.startswith("development/standards/apps/"):
        return "development/wiki/archive/old/apps/" + Path(src).name
    if src in {
        "development/standards/backend.md",
        "development/standards/adoption.md",
        "development/standards/worldview.md",
        "development/standards/AGENTS.md",
    }:
        return "development/wiki/archive/old/root/" + Path(src).name
    return None


def context(page: dict) -> str:
    def flow(values):
        return json.dumps(values, ensure_ascii=False)

    lines = [
        "<!-- CONTEXT:BEGIN",
        "schema: flove-page/1",
        f"id: {page['id']}",
        f"path: {page['path']}",
        f"trunk: {page['trunk']}",
        f"topic: {page['topic']}",
        f"kind: {page['kind']}",
        f"status: {page['status']}",
        f"html_place: {flow(page['html_place'])}",
        f"owns: {flow(page['owns'])}",
        f"updated: {page['updated']}",
        "read_next: []",
    ]
    if page.get("supersedes"):
        lines.append("supersedes:")
        lines.extend(f"  - {x}" for x in page["supersedes"])
    else:
        lines.append("supersedes: []")
    lines.append(f"heavy: {'true' if page.get('heavy') else 'false'}")
    lines.append("CONTEXT:END -->")
    return "\n".join(lines)


def topic_body(page: dict) -> str:
    return "\n".join(
        [
            context(page),
            "",
            f"# {TOPIC_TITLES.get(page['topic'], page['topic'])}",
            "",
            "> **Phase 1 skeleton.** This page exists so the manifest, resolver and gates",
            "> can be built. Phase 2 writes the migrated content here. Do not cite it as",
            "> an owner yet.",
            "",
            "## Migration",
            "",
            f"- Registered as `{page['id']}` in `development/wiki/wiki.json`.",
            "- Source rows: `development/wiki/port-ledger.skeleton.json`.",
            "- Child plan: see `development/wiki/plans/`.",
            "",
        ]
    )


def manifest() -> dict:
    inv = json.loads(INV.read_text())
    pages = []

    pages.append(
        {
            "id": "map/index",
            "path": "development/wiki/INDEX.md",
            "trunk": "map",
            "topic": "index",
            "kind": "map",
            "status": "draft",
            "html_place": [],
            "owns": ["wiki index", "plans map", "data-index map"],
            "updated": TODAY,
            "supersedes": [],
            "heavy": False,
        }
    )

    for trunk, topic, html, owns in TOPICS:
        path = f"development/standards/{topic}.md"
        supersedes = {
            archive_for(item["base"])
            for item in inv["items"]
            if item["target"]
            and item["target"].split("#")[0] == path
            and item["base"].startswith("development/standards/")
            and archive_for(item["base"])
        }
        for src, topics in SOURCE_TOPICS.items():
            if topic in topics:
                arc = archive_for(src)
                if arc:
                    supersedes.add(arc)
        supersedes = sorted(x for x in supersedes if x)
        pages.append(
            {
                "id": f"{trunk}/{topic}",
                "path": path,
                "trunk": trunk,
                "topic": topic,
                "kind": "topic",
                "status": "draft",
                "html_place": html,
                "owns": owns,
                "updated": TODAY,
                "supersedes": supersedes,
                "heavy": False,
            }
        )

    for trunk, topic, rel, html, owns, heavy, fmt in STANDING:
        pages.append(
            {
                "id": f"{trunk}/{topic}",
                "path": f"development/standards/{rel}",
                "trunk": trunk,
                "topic": topic,
                "kind": "standing",
                "format": fmt,
                "status": "active",
                "html_place": html,
                "owns": owns,
                "updated": TODAY,
                "supersedes": [],
                "heavy": heavy,
            }
        )

    pages.extend(
        {
            "id": f"map/{topic}",
            "path": f"development/wiki/{rel}",
            "trunk": "map",
            "topic": topic,
            "kind": "map",
            "status": "draft",
            "html_place": [],
            "owns": owns,
            "updated": TODAY,
            "supersedes": [],
            "heavy": False,
        }
        for trunk, topic, rel, owns in MAP_PAGES
        if topic != "index"
    )

    redirects: dict[str, str] = {}
    aliases: dict[str, str] = {}
    grouped: dict[str, list[dict]] = {}
    for item in inv["items"]:
        grouped.setdefault(item["base"], []).append(item)

    for base, items in grouped.items():
        targets = {i["target"].split("#")[0] for i in items if i["target"] and not i["target"].startswith("development/wiki/archive/")}
        if base.startswith("development/standards/") and len(targets) == 1 and not any(i["needs_review"] for i in items):
            target = next(iter(targets))
            if target:
                redirects[base] = target
        arch = archive_for(base)
        if arch:
            aliases[base] = arch
        elif len(targets) == 1 and next(iter(targets)) != base:
            aliases[base] = next(iter(targets))

    field_map = {
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

    plans = [
        {
            "id": f"{trunk}/{topic}",
            "path": f"development/wiki/plans/{trunk}/{topic}.md",
            "primary": f"{trunk}/{topic}",
            "sources": [],
            "status": "draft",
        }
        for trunk, topic in PLAN_TOPICS
    ]

    return {
        "schema": "flove-wiki-manifest/1",
        "roots": {
            "wiki": "development/wiki",
            "pages": "development/standards",
            "archive": "development/wiki/archive/old",
        },
        "pages": pages,
        "chapter_map": "development/wiki/chapter-map.json",
        "task_recycle": "development/wiki/task-recycle.json",
        "plans": plans,
        "redirects": dict(sorted(redirects.items())),
        "aliases": dict(sorted(aliases.items())),
        "field_map": field_map,
        "excluded_live": [
            "development/wiki/work/milestones.json",
            "development/wiki/work/common.json",
        ],
        "labels": {
            "standards": "development/standards/mds.md",
            "owner": "development/standards/work.md",
            "proposals": "development/standards/plan.md",
            "conflicts": "development/wiki/plans/conflicts.md",
            "pendings": "development/wiki/work/pendings.md",
        },
    }


def index_body(m: dict) -> str:
    topics = [p for p in m["pages"] if p["kind"] == "topic"]
    standing = [p for p in m["pages"] if p["kind"] == "standing"]
    lines = [
        "# flove development wiki — index",
        "",
        "> **Phase 1 skeleton.** The single index. Phase 2 fills the historical rows and",
        "> the plan detail; §8 is generated from the register.",
        "",
        "## 1. How to read this wiki",
        "",
        "Topic pages own the migrated facts. Standing books stay canonical and are",
        "linked. `plans/conflicts.md` is the only cross-plan conflict tracker.",
        "",
        f"## 2. Topic grid ({len(topics)})",
        "",
        "| Topic | Page | HTML place |",
        "|---|---|---|",
        *[f"| `{p['id']}` | `{p['path']}` | {' / '.join(p['html_place']) or '—'} |" for p in topics],
        "",
        f"## 3. Standing books and governance ({len(standing)})",
        "",
        "| Book | Page |",
        "|---|---|",
        *[f"| `{p['id']}` | `{p['path']}` |" for p in standing],
        "",
        f"## 4. Plans ({len(m['plans'])})",
        "",
        "| Plan | Primary page | Status |",
        "|---|---|---|",
        *[f"| `{p['path']}` | `{p['primary']}` | {p['status']} |" for p in m["plans"]],
        "",
        "## 5. Data index and routing",
        "",
        "Canonical detail: `development/standards/json.md#data-index-and-routing`.",
        "",
        "## 6. Conflicts",
        "",
        "`development/wiki/plans/conflicts.md` — one table, one home.",
        "",
        "## 7. Historical rows (33)",
        "",
        "Ported in phase 2 from the old `debates/INDEX.md` into archive links. No",
        "authority; no duplicate facts.",
        "",
        "## 8. Register counts and gates",
        "",
        "326 hitos · 37 debate tickets · 75 pendings rows = **438** features;",
        "1,559 live tasks · 805 archived. Generated from `common.json`; never",
        "hand-typed at cutover.",
        "",
    ]
    return "\n".join(lines)


def plan_body(trunk: str, topic: str) -> str:
    return "\n".join(
        [
            "---",
            "status: draft",
            f"section: {trunk}/{topic}",
            f"created: {TODAY}",
            "also: []",
            "---",
            "",
            f"# {trunk}/{topic} plan",
            "",
            "> **Phase 1 skeleton.** Phase 2 adds the dated `## <source> — <date>`",
            "> sections. The stable page is the only owner; this file is a child plan.",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite skeleton files")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("choose --write or --check")

    m = manifest()
    expected = [WIKI / "wiki.json", WIKI / "INDEX.md"]
    expected += [STD / f"{t}.md" for _, t, *_ in TOPICS]
    expected += [WIKI / "plans" / trunk / f"{topic}.md" for trunk, topic in PLAN_TOPICS]
    expected += [WIKI / "plans/conflicts.md", WIKI / "plans/debates/README.md"]

    if args.check:
        missing = [str(p.relative_to(ROOT)) for p in expected if not p.exists()]
        if missing:
            print("missing:", *missing, sep="\n  ")
            return 1
        print(f"OK: {len(expected)} skeleton files present")
        return 0

    conflicts = [p for p in expected if p.exists()]
    if conflicts and not args.force:
        print("refusing to overwrite:", *[str(p.relative_to(ROOT)) for p in conflicts], sep="\n  ")
        return 1

    WIKI.mkdir(parents=True, exist_ok=True)
    (WIKI / "wiki.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    (WIKI / "INDEX.md").write_text(index_body(m))
    for page in m["pages"]:
        if page["kind"] == "topic":
            (STD / f"{page['topic']}.md").write_text(topic_body(page))
    for trunk, topic in PLAN_TOPICS:
        p = WIKI / "plans" / trunk / f"{topic}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(plan_body(trunk, topic))
    (WIKI / "plans/debates").mkdir(parents=True, exist_ok=True)
    (WIKI / "work").mkdir(parents=True, exist_ok=True)
    (WIKI / "archive").mkdir(parents=True, exist_ok=True)
    (WIKI / "work/.gitkeep").write_text("")
    (WIKI / "archive/.gitkeep").write_text("")
    (WIKI / "plans/conflicts.md").write_text(
        "# Cross-plan conflicts\n\n"
        "> **Phase 1 skeleton.** Phase 2 moves the live conflict register here.\n\n"
        "## Open\n\n## Closed\n"
    )
    (WIKI / "plans/debates/README.md").write_text(
        "# Debates tray\n\n"
        "Drop on-the-fly draft plans here. No facts, not an owner.\n\n"
        "```md\n---\nstatus: draft\nsection: backend/mynet\ncreated: 2026-11-21\n---\n```\n\n"
        "Promote with `git mv` to `plans/<category>/<topic>.md`, then port the facts.\n"
    )
    print(f"wrote {len(expected)} skeleton files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
