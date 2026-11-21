#!/usr/bin/env python3
"""jsony_check.py — keep flove's JSON backbone aligned after apps/ commits.

Checks:
  - apps/**/*.html flove-fields manifests against tools/routing.json
  - tools/routing.json app URLs against the filesystem
  - apps/appy/index.html APP_ROUTING snapshot against routing
  - the flove-portrait/flove-profile envelope in appy-basic
  - debates/common.json against milestones.json (every live and archived task)

Pending, not checked: tools/puzzy.json apps{} vs routing. The registry has no
runtime consumer and its sync script is parked.

Default: write tools/jsony-pending.md and .json, exit 1 when critical drift.
Hook:    --changed --soft (only when HEAD touched apps/, never blocks).

Usage:
  python3 development/scripts/jsony_check.py
  python3 development/scripts/jsony_check.py --changed --soft
  python3 development/scripts/jsony_check.py --no-write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import register_projection as projection
import procedures_source

ROOT = Path(__file__).resolve().parents[2]
ROUTING = ROOT / "tools/routing.json"
APPY = ROOT / "apps/appy/index.html"
PENDING_MD = ROOT / "tools/jsony-pending.md"
PENDING_JSON = ROOT / "tools/jsony-pending.json"
STATE = ROOT / "tools/jsony-state.json"
MILESTONES = ROOT / "development/standards/debates/milestones.json"
COMMON = ROOT / "development/standards/debates/common.json"
INDEX = ROOT / "development/index.html"
MOVES = ROOT / "development/standards/debates/work-moves.json"

# Documented exceptions to the export contract — one set, no variants here.
# The variants (own HTML export · no standard summary · page outside the
# contract) are listed in development/standards/frontend/export.md and
# frontend/summary.md; each page's type is in the app table under
# development/index.html → Web → Apps (#web-apps). Change the docs, then this.
EXPORT_EXCEPTIONS = {
    "blogy", "browsy", "chacrikun", "electrorchestra", "fivy", "frotis",
    "loly", "nety", "profily", "puzzy", "questy", "rewardy",
    "sety", "vizy", "vizy2", "wizy",
}

MANIFEST_RE = re.compile(
    r'<script[^>]*id=["\']flove-fields["\'][^>]*>(.*?)</script>',
    re.S | re.I,
)
APPY_RE = re.compile(r"const\s+APP_ROUTING\s*=\s*\{(.*?)\n\};", re.S)
APPY_ITEM_RE = re.compile(
    r'"([^"]+)"\s*:\s*\{\s*id:\s*"([^"]+)"\s*,\s*category:\s*"([^"]+)"'
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


CATEGORY_ALIASES = {
    "ling": "ling",
    "ling / words": "ling",
    "ling/words": "ling",
    "linguistics": "ling",
    "inside": "inside",
    "mating": "mating",
    "social": "social",
    "economy": "economy",
}


def norm_category(value) -> str:
    key = str(value or "").strip().lower()
    return CATEGORY_ALIASES.get(key, key)


def scan_app_manifests() -> list[dict]:
    apps = []
    for path in sorted((ROOT / "apps").rglob("*.html")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        match = MANIFEST_RE.search(text)
        if not match:
            continue
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            apps.append({
                "id": None,
                "path": rel(path),
                "error": f"invalid flove-fields JSON: {exc}",
                "fields": 0,
                "portrait": False,
            })
            continue
        app_id = data.get("app")
        if not app_id:
            continue
        apps.append({
            "id": str(app_id),
            "path": rel(path),
            "fields": len(data.get("fields") or []),
            "status": data.get("status"),
            "portrait": ("flovePortrait" in text or "flovePort" in text),
            "error": None,
        })
    return apps


def scan_appy_snapshot(text: str) -> dict:
    match = APPY_RE.search(text)
    if not match:
        return {}
    snapshot = {}
    for name, app_id, category in APPY_ITEM_RE.findall(match.group(1)):
        snapshot[app_id] = {"name": name, "category": category}
    return snapshot


BRIDGE_MARKER = "flove-appy.js · app → Appy profile bridge"


def check_appy_bridge() -> dict:
    """Advisory: the Publish bridge is inlined per app, so copies can drift.

    Kept out of the hard distro gate on purpose — this reports the variants and
    never fails a build.
    """
    copies = []
    for path in sorted((ROOT / "apps").rglob("*.html")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if BRIDGE_MARKER not in text:
            continue
        at = text.find(BRIDGE_MARKER)
        start = text.rfind("<script", 0, at)
        end = text.find("</script>", at)
        if start == -1 or end == -1:
            continue
        block = re.sub(r"\s+", " ", text[start:end])
        digest = hashlib.sha256(block.encode("utf-8")).hexdigest()[:12]
        copies.append({"path": rel(path), "hash": digest})
    groups: dict[str, list[str]] = {}
    for item in copies:
        groups.setdefault(item["hash"], []).append(item["path"])
    variants = [{"hash": h, "files": files} for h, files in sorted(groups.items())]
    return {"copies": len(copies), "variants": variants, "drift": len(variants) > 1}


# Regexes, not substrings: a JSON-only save control is the standard, and the
# word "copy" or "insight" may legitimately appear in display content.
SUMMARY_PATTERNS = {
    "views": (r"view-axial|view-bars|view-vertical|view-spider|action-row--views",),
    "publish": (r"data-flove-publish",),
    "update": (r"data-flove-update",),
    "insight": (r'id="insightBtn"|insight-panel|insight-cycle',),
    "copy": (r'data-action="copy"|class="[^"]*\bcopy-btn\b',),
    "formats": (r'save-fmt-(?!json)|data-fmt="(?!json)|data-flove-save="(?!json)',),
}


def check_moves(register: dict, live: set, archived: set) -> list[str]:
    """A committed export is a review item: it must be applicable, not stale."""
    if not MOVES.exists():
        return []
    try:
        patch = read_json(MOVES)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{rel(MOVES)}: cannot read the export: {exc}"]
    errors = []
    if patch.get("schema") != "flove-work-moves/1":
        errors.append(f"{rel(MOVES)}: schema {patch.get('schema')!r}, expected 'flove-work-moves/1'")
    moves = patch.get("moves") or []
    ids = [m.get("id") for m in moves]
    if not ids or len(ids) != len(set(ids)):
        errors.append(f"{rel(MOVES)}: moves must be a non-empty list of unique ids")
    owner = {t.get("id"): t.get("hito_id")
             for m in register.get("sections", [])
             for b in m.get("subsections", [])
             for h in b.get("milestones", [])
             for t in (h.get("tasks") or [])}
    for m in moves:
        tid = m.get("id")
        if tid in archived or tid not in live:
            errors.append(f"{rel(MOVES)}: {tid} is not a live task (already applied?)")
        elif m.get("hito_id") and m["hito_id"] != owner.get(tid):
            errors.append(f"{rel(MOVES)}: {tid} has the wrong hito_id")
    for r in patch.get("replacements") or []:
        if r.get("id") in live or r.get("id") in archived:
            errors.append(f"{rel(MOVES)}: replacement {r.get('id')} already exists")
        if not (r.get("en") or "").strip() or not (r.get("es") or "").strip():
            errors.append(f"{rel(MOVES)}: replacement {r.get('id')} needs en/es titles")
        if not ((r.get("evidence") or {}).get("gaps") or [""])[0].strip():
            errors.append(f"{rel(MOVES)}: replacement {r.get('id')} needs a done criterion")
        if (r.get("evidence") or {}).get("by") != "optimizy":
            errors.append(f"{rel(MOVES)}: replacement {r.get('id')} needs evidence.by = optimizy")
    moves_by_hito: dict[str, int] = {}
    for m in moves:
        moves_by_hito[m.get("hito_id")] = moves_by_hito.get(m.get("hito_id"), 0) + 1
    repl_by_hito: dict[str, int] = {}
    for r in patch.get("replacements") or []:
        repl_by_hito[r.get("hito_id")] = repl_by_hito.get(r.get("hito_id"), 0) + 1
    if moves_by_hito != repl_by_hito:
        errors.append(f"{rel(MOVES)}: PROC-09 needs one replacement per move, per hito")
    return errors


def check_common() -> dict:
    """Join + embedded Work block must list every live/archived task in the register."""
    if not COMMON.exists():
        return {"errors": [f"missing {rel(COMMON)}"], "counts": {}, "moves": []}
    try:
        common = read_json(COMMON)
        register = read_json(MILESTONES)
    except (OSError, json.JSONDecodeError) as exc:
        return {"errors": [f"cannot read the join or register: {exc}"], "counts": {}, "moves": []}
    hitos = projection.hitos(register)
    live = set(projection.live_tasks(register))
    archived = {t.get("id") for t in (register.get("tasks_archive") or [])}
    counts = projection.counts(register)
    errors = []
    task_set = register.get("taskSet") or {}
    if task_set.get("live") != counts["live_tasks"] or task_set.get("archived") != counts["archived_tasks"]:
        errors.append(f"taskSet counts {task_set.get('live')}/{task_set.get('archived')} "
                      f"!= register {counts['live_tasks']}/{counts['archived_tasks']}")
    moves = check_moves(register, live, archived)
    if common.get("schema") != "flove-common/1":
        errors.append(f"{rel(COMMON)}: schema {common.get('schema')!r}, expected 'flove-common/1'")
    if common.get("counts") != counts:
        errors.append(f"{rel(COMMON)}: counts {common.get('counts')} != {counts}")
    by_id = {h.get("id"): h for h in (common.get("hitos") or [])}
    if set(by_id) != {m.get("id") for m in hitos}:
        errors.append(f"{rel(COMMON)}: hito ids differ from the register")
    for m in hitos:
        h = by_id.get(m.get("id"))
        if not h:
            continue
        want = {t.get("id") for t in (m.get("tasks") or [])}
        got = {t.get("id") for t in (h.get("tasks") or [])}
        if want != got:
            errors.append(f"{m.get('id')}: task ids differ "
                          f"(missing {sorted(want - got)}, extra {sorted(got - want)})")
        spec = h.get("spec") or {}
        for key in ("deliverable", "done", "decision"):
            if not str(spec.get(key) or "").strip():
                errors.append(f"{m.get('id')}: empty spec.{key}")
    if set(common.get("tasks") or {}) != live:
        missing = sorted(live - set(common.get("tasks") or {}))
        extra = sorted(set(common.get("tasks") or {}) - live)
        errors.append(f"{rel(COMMON)}: task index differs "
                      f"(missing {missing[:5]}, extra {extra[:5]})")
    if {a.get("id") for a in (common.get("archive") or [])} != archived:
        errors.append(f"{rel(COMMON)}: archive summary differs from tasks_archive")
    # The embedded Work block is the offline fallback for the same archive and
    # queue policy; it must not drift from the register either.
    try:
        page = INDEX.read_text(encoding="utf-8")
        m = re.search(r'<script type="application/json" id="work-data">(.*?)</script>',
                      page, re.S)
        embedded = json.loads(m.group(1)) if m else {}
    except (OSError, json.JSONDecodeError) as exc:
        embedded = {}
        errors.append(f"{rel(INDEX)}: cannot read embedded Work data: {exc}")
    if embedded:
        if {a.get("id") for a in (embedded.get("archive") or [])} != archived:
            errors.append(f"{rel(INDEX)}: embedded Work archive differs from tasks_archive")
        want_policy = projection.queue_policy(register)
        if (embedded.get("queuePolicy") or {}) != want_policy:
            errors.append(f"{rel(INDEX)}: embedded queuePolicy differs from taskSet")
    # The PROC policy has one source: AGENTS.md. Both projections must match it.
    want_procs = procedures_source.load()
    if register.get("procedures"):
        errors.append(f"{rel(MILESTONES)}: procedures block must live in AGENTS.md")
    if (common.get("procedures") or []) != want_procs:
        errors.append(f"{rel(COMMON)}: procedures differ from AGENTS.md")
    if embedded and (embedded.get("procedures") or []) != want_procs:
        errors.append(f"{rel(INDEX)}: embedded procedures differ from AGENTS.md")
    # PROC-08: a state move needs a machine-readable evidence pointer.
    for section in register.get("sections", []):
        for box in section.get("subsections", []):
            for h in box.get("milestones", []):
                for t in (h.get("tasks") or []):
                    if t.get("state") not in ("hecha", "parcial"):
                        continue
                    ptr = (t.get("evidence") or {}).get("pointer") or {}
                    if (ptr.get("kind") not in ("command", "anchor", "state")
                            or not str(ptr.get("value") or "").strip()):
                        errors.append(
                            f"{rel(MILESTONES)}: {t.get('id')} needs evidence.pointer "
                            f"{{kind, value}} for state {t.get('state')}")
    return {"errors": errors, "counts": counts, "moves": moves}


def markup_only(text: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.S | re.I)
    return re.sub(r"<style\b[^>]*>.*?</style>", "", text, flags=re.S | re.I)


def style_only(text: str) -> str:
    """Real page CSS only — a marker inside a JS template string is not scoped."""
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.S | re.I)
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", text, flags=re.S | re.I))


def summary_features(text: str) -> list[str]:
    text = markup_only(text)
    return [name for name, pats in SUMMARY_PATTERNS.items()
            if any(re.search(p, text) for p in pats)]


NARROW_MARKER = re.compile(r"standard summary buttons", re.I)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class SummaryShape(HTMLParser):
    """Read the summary row's shape from markup only: Magic, Share, and whether
    every Save control sits inside a Share container (Goddy model)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.skip = 0
        self.magic = 0
        self.share = 0
        self.save = 0
        self.save_in_share = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        if self.skip:
            return
        a = dict(attrs)
        cls = (a.get("class") or "").lower()
        _id = (a.get("id") or "").lower()
        is_magic = ("magic" in cls or "magic" in _id)
        is_share = (("share" in cls and "btn" in cls)
                    or ("share" in _id and ("btn" in _id or "summary" in _id))
                    or "data-flove-share" in a
                    or "data-flove-share-menu" in a
                    or a.get("data-cycle-toggle") == "share")
        is_save = (a.get("data-action") == "save"
                   or a.get("data-share") == "save"
                   or a.get("data-group") == "save"
                   or a.get("data-action") == "download"
                   or a.get("data-fmt") == "json"
                   or a.get("data-act") == "save"
                   or "data-flove-save" in a
                   or ("save" in _id and ("btn" in _id or "json" in _id))
                   or ("save" in cls and "btn" in cls))
        is_container = any(k in cls for k in ("summary", "action-row", "action-grid",
                                             "result-actions", "btn-popup-wrap", "btn-with-subs",
                                             "share-wrap", "cycle-row"))
        in_summary = any(f["summary"] for f in self.stack) or is_container
        if is_magic:
            self.magic += 1
            if self.stack:                      # its immediate action row
                self.stack[-1]["summary"] = True
            in_summary = True
        if is_share and in_summary:
            self.share += 1
            for frame in self.stack:
                frame["share"] = True
        if is_save and in_summary:
            self.save += 1
            if any(f["share"] for f in self.stack):
                self.save_in_share += 1
            for frame in self.stack:
                frame["saves"] += 1               # resolved when a frame closes
        if tag not in VOID_TAGS:
            self.stack.append({"share": False, "summary": in_summary, "saves": 0})

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            if self.skip:
                self.skip -= 1
            return
        if self.skip:
            return
        if self.stack:
            frame = self.stack.pop()
            # a Share trigger and its Save can be siblings in either order
            if frame["share"] and frame["saves"]:
                self.save_in_share += frame["saves"]


def summary_shape(text: str) -> SummaryShape:
    scan = SummaryShape()
    try:
        scan.feed(text)
    except Exception:
        pass
    return scan


def audit_summary() -> int:
    """List apps whose summary still carries legacy features (doc: summary.md)."""
    routing = read_json(ROUTING)
    legacy = []
    exceptions = []
    narrowed = 0
    for app in routing.get("apps", []):
        app_id = str(app.get("id") or "")
        url = str(app.get("url") or "")
        if not app_id or not url.endswith(".html") or not url.startswith("apps/"):
            continue
        path = ROOT / url
        if not path.exists():
            continue
        if app_id in EXPORT_EXCEPTIONS:
            exceptions.append(app_id)
            continue          # documented: frontend/export.md · summary.md
        text = path.read_text(encoding="utf-8")
        if NARROW_MARKER.search(style_only(text)):
            # controls stay in the DOM for their displays/listeners but are
            # hidden by scoped CSS under the standard-buttons marker
            narrowed += 1
            continue
        feats = summary_features(text)
        shape = summary_shape(text)
        if not shape.magic:
            feats.append("no Magic")
        if not shape.share:
            feats.append("no Share")
        if not shape.save:
            feats.append("no Save in Share")
        elif shape.save_in_share < shape.save:
            feats.append("separate Save")
        if feats:
            legacy.append((app_id, url, feats))
    print(f"jsony: summary standard — {len(legacy)} app(s) with legacy features, "
          f"{narrowed} narrowed by CSS, {len(exceptions)} documented exception(s)")
    for app_id, url, feats in legacy:
        print(f"  {app_id:14} {url:42} {', '.join(feats)}")
    if exceptions:
        print("  exceptions: listed in frontend/summary.md · frontend/export.md "
              "· development/index.html → Web → Apps")
    print("  rule: development/standards/frontend/summary.md § Summary standard")
    return 0


LEGACY_FORMATS = (
    "toMd(", "toXml(", "toCsv(", "toHtml(", "renderJpg", "renderMatrixJPG",
    "buildPortraitHtml", "portraitCsv", "portraitXml", "buildSummaryDocHTML",
)


def audit_app(query: str) -> int:
    """Audit one app's export against the standard (Goddy is the model)."""
    routing = read_json(ROUTING)
    apps = routing.get("apps", [])
    q = query.strip().lower()
    app = next((a for a in apps if str(a.get("id", "")).lower() == q
                or str(a.get("name", "")).lower() == q), None)
    if not app:
        print(f"jsony: no app in routing.json matches {query!r}", file=sys.stderr)
        return 2
    app_id = str(app.get("id") or query)
    if app_id in EXPORT_EXCEPTIONS:
        print(f"jsony: app {app_id} — documented export exception "
              "(frontend/export.md · summary.md)")
        return 0
    status = str(app.get("status") or "complete")
    pending = status not in ("complete",)
    path = ROOT / str(app.get("url") or "")
    print(f"jsony: app {app_id} ({rel(path) if path.exists() else path})")
    if pending:
        print(f"  note  status {status} — portrait export not required yet")
    if not path.exists():
        print("  FAIL  file does not exist")
        return 1
    text = path.read_text(encoding="utf-8")
    critical = 0
    advisory = 0

    def ok(msg):
        print(f"  ok    {msg}")

    def warn(msg):
        nonlocal advisory
        advisory += 1
        print(f"  warn  {msg}")

    def bad(msg):
        nonlocal critical, advisory
        if pending:
            advisory += 1
            print(f"  warn  {msg} (app still {status})")
        else:
            critical += 1
            print(f"  FAIL  {msg}")

    if "flovePortrait" in text or "flovePort.get" in text:
        ok("portrait API")
    else:
        bad("no flovePortrait / flovePort API")
    if "flove-portrait/1" in text:
        ok("flove-portrait/1 schema")
    else:
        bad("no flove-portrait/1 schema")
    if re.search(r"portrait\.json", text):
        ok("<app>-portrait.json download")
    else:
        bad("no <app>-portrait.json filename")
    if re.search(r"\bphrase\s*:", text):
        ok("phrase in the envelope")
    else:
        warn("no phrase field (renderer shows rows only)")
    if re.search(r"\brows\s*:", text):
        ok("rows[]")
    else:
        warn("no rows[] found")
    legacy = [tok for tok in LEGACY_FORMATS if tok in text]
    if legacy:
        warn("legacy format serializer(s): " + ", ".join(legacy))
    if re.search(r"window\.floveAppy(?!\w)|app → Appy profile bridge", text):
        warn("legacy Publish/Appy bridge still present")
    if re.search(r"navigator\.share", text) and "canShare" not in text:
        warn("navigator.share without canShare guard")

    print(f"  {critical} critical · {advisory} advisory")
    return 1 if critical else 0


def changed_apps() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line.strip() for line in out.splitlines() if line.strip().startswith("apps/")]


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def load_state() -> dict:
    if not STATE.exists():
        return {"lastCommit": None, "queue": []}
    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("state is not an object")
        data.setdefault("queue", [])
        data.setdefault("lastCommit", None)
        return data
    except (OSError, ValueError):
        return {"lastCommit": None, "queue": []}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_findings(changed: list[str]) -> dict:
    routing = read_json(ROUTING)
    apps = scan_app_manifests()
    appy_text = APPY.read_text(encoding="utf-8")
    appy = scan_appy_snapshot(appy_text)

    routing_by_id = {str(a.get("id")): a for a in routing.get("apps", []) if a.get("id")}
    bridge = check_appy_bridge()
    common = check_common()

    manifest_by_id = {}
    for app in apps:
        if app.get("id") and not app.get("error"):
            manifest_by_id.setdefault(app["id"], app)

    routing_missing = []
    for app_id, app in manifest_by_id.items():
        if app_id not in routing_by_id:
            routing_missing.append({
                "id": app_id,
                "path": app["path"],
                "fields": app["fields"],
            })
    for app in apps:
        if app.get("error"):
            routing_missing.append({
                "id": None,
                "path": app["path"],
                "error": app["error"],
            })

    routing_url_missing = []
    for app_id, app in routing_by_id.items():
        url = str(app.get("url") or "").strip()
        if not url or url.startswith(("http://", "https://")):
            continue
        target = ROOT / url
        if not target.exists():
            routing_url_missing.append({"id": app_id, "name": app.get("name"), "url": url})

    appy_missing = []
    appy_mismatch = []
    appy_extra = []
    for app_id, app in routing_by_id.items():
        if app_id not in appy:
            appy_missing.append({
                "id": app_id,
                "name": app.get("name"),
                "category": app.get("category"),
            })
        elif norm_category(appy[app_id].get("category")) != norm_category(app.get("category")):
            appy_mismatch.append({
                "id": app_id,
                "name": app.get("name"),
                "snapshot": appy[app_id].get("category"),
                "routing": app.get("category"),
            })
    for app_id, item in appy.items():
        if app_id not in routing_by_id:
            appy_extra.append({"id": app_id, "name": item.get("name"), "category": item.get("category")})

    export_appy = {
        "flove-profile": ("kind: 'flove-profile'" in appy_text or 'kind:"flove-profile"' in appy_text),
        "routing flove-routing/3": "flove-routing/3" in appy_text,
        "appsPlayed": "appsPlayed" in appy_text,
        "flove-portrait/1": "flove-portrait/1" in appy_text,
        "flovePort": "flovePort" in appy_text,
    }
    export_appy_missing = [k for k, ok in export_appy.items() if not ok]

    apps_without_portrait = [
        {"id": app["id"], "path": app["path"], "fields": app["fields"]}
        for app in apps
        if app.get("id") and not app.get("error") and app["fields"] > 0 and not app["portrait"]
    ]

    critical = (
        len(routing_missing) + len(routing_url_missing) + len(appy_missing)
        + len(appy_extra) + len(appy_mismatch) + len(export_appy_missing)
        + len(common["errors"]) + len(common["moves"])
    )
    advisory = len(apps_without_portrait) + (1 if bridge["drift"] else 0)

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "changed": changed,
        "routingMissing": routing_missing,
        "routingUrlMissing": routing_url_missing,
        "appyMissing": appy_missing,
        "appyExtra": appy_extra,
        "appyMismatch": appy_mismatch,
        "exportAppyMissing": export_appy_missing,
        "appsWithoutPortrait": apps_without_portrait,
        "appyBridge": bridge,
        "commonDrift": common["errors"],
        "movesDrift": common["moves"],
        "commonCounts": common["counts"],
        "critical": critical,
        "advisory": advisory,
    }


def fmt_list(items: list[dict], columns: tuple[str, ...]) -> list[str]:
    lines = []
    for item in items:
        parts = [str(item.get(col, "") or "").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(parts) + " |")
    return lines


def markdown_report(f: dict) -> str:
    lines = [
        "# jsony pending — JSON backbone",
        "",
        f"Generated: `{f['generatedAt']}`",
        "",
    ]
    if f["changed"]:
        lines += ["Changed in HEAD:", ""]
        lines += [f"- `{p}`" for p in f["changed"]]
        lines.append("")
    lines += [
        f"**Critical:** {f['critical']} · **Advisory:** {f['advisory']}",
        "",
    ]
    if f["critical"] == 0 and f["advisory"] == 0:
        lines += ["## Status", "", "All checked files are aligned. No pending update.", ""]
        return "\n".join(lines)

    if f["routingMissing"]:
        lines += [
            "## Critical — app manifests missing from routing.json",
            "",
            "| app id | file | fields |",
            "|---|---|---|",
        ]
        lines += fmt_list(f["routingMissing"], ("id", "path", "fields"))
        lines += ["", "Propose a routing entry (category needs an owner decision):", ""]
        for item in f["routingMissing"]:
            if item.get("id"):
                lines.append(
                    f"- `{item['id']}` → `{item['path']}` — "
                    f"`{{\"id\":\"{item['id']}\",\"name\":\"TODO\",\"category\":\"TODO\",\"url\":\"{item['path']}\"}}`"
                )
        lines.append("")

    if f["routingUrlMissing"]:
        lines += [
            "## Critical — routing URLs that do not resolve",
            "",
            "| app id | name | url |",
            "|---|---|---|",
        ]
        lines += fmt_list(f["routingUrlMissing"], ("id", "name", "url"))
        lines.append("")

    if f["appyMissing"] or f["appyExtra"] or f["appyMismatch"]:
        lines += [
            "## Critical — appy-basic APP_ROUTING snapshot",
            "",
        ]
        if f["appyMissing"]:
            lines += ["Missing in appy:", "", "| id | name | category |", "|---|---|---|"]
            lines += fmt_list(f["appyMissing"], ("id", "name", "category"))
            lines.append("")
        if f["appyExtra"]:
            lines += ["Extra in appy:", "", "| id | name | category |", "|---|---|---|"]
            lines += fmt_list(f["appyExtra"], ("id", "name", "category"))
            lines.append("")
        if f["appyMismatch"]:
            lines += ["Category mismatch:", "", "| id | name | snapshot | routing |", "|---|---|---|---|"]
            lines += fmt_list(f["appyMismatch"], ("id", "name", "snapshot", "routing"))
            lines.append("")

    if f["exportAppyMissing"]:
        lines += [
            "## Critical — appy-basic export envelope",
            "",
        ]
        lines += [f"- missing: `{key}`" for key in f["exportAppyMissing"]]
        lines.append("")

    if f.get("commonDrift"):
        lines += [
            "## Critical — common.json drift",
            "",
            f"`common.json` must list the actual {f.get('commonCounts', {}).get('live_tasks', '?')} live "
            f"tasks and {f.get('commonCounts', {}).get('archived_tasks', '?')} archived tasks.",
            "",
        ]
        lines += [f"- {e}" for e in f["commonDrift"]]
        lines += ["", "Rebuild with `python3 development/scripts/build-common.py --build`.", ""]

    if f.get("movesDrift"):
        lines += [
            "## Critical — exported Work moves",
            "",
            f"`{rel(MOVES)}` is a review item; apply or discard it before publishing.",
            "",
        ]
        lines += [f"- {e}" for e in f["movesDrift"]]
        lines.append("")

    if f["appsWithoutPortrait"]:
        lines += [
            "## Advisory — apps without a flovePortrait envelope",
            "",
        ]
        lines += [f"- `{item['id']}` (`{item['path']}`, {item['fields']} fields)" for item in f["appsWithoutPortrait"]]
        lines.append("")

    if f.get("appyBridge", {}).get("drift"):
        bridge = f["appyBridge"]
        lines += [
            "## Advisory — embedded Publish bridge differs across apps",
            "",
            f"{bridge['copies']} app(s) inline the bridge in {len(bridge['variants'])} variant(s).",
            "This never fails a build; copy one variant into the others when convenient.",
            "",
            "| variant | apps |",
            "|---|---|",
        ]
        for variant in bridge["variants"]:
            lines.append(f"| `{variant['hash']}` | " + ", ".join(f"`{p}`" for p in variant["files"]) + " |")
        lines.append("")

    lines += [
        "## Apply, in order",
        "",
        "1. Review every critical item; add routing entries or fix URLs.",
        "2. Run `python3 development/scripts/build-common.py --build` after any register change.",
        "3. Run `python3 tools/extract-fields.py --apply` for field-tree updates.",
        "4. Update the appy-basic `APP_ROUTING` snapshot (id + category).",
        "5. Run `/exporty <app>` on the changed apps.",
        "6. Re-run `jsony_check.py --strict` until clean; delete the pending files.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check flove's JSON backbone.")
    parser.add_argument("--record", action="store_true", help="append HEAD's apps/ changes to the queue (hook mode)")
    parser.add_argument("--changed", action="store_true", help="process the queued apps/ changes")
    parser.add_argument("--soft", action="store_true", help="always exit 0 (for hooks)")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any critical drift")
    parser.add_argument("--no-write", action="store_true", help="do not write pending files")
    parser.add_argument("--app", metavar="APP", help="audit one app's export against the standard")
    parser.add_argument("--summary", action="store_true", help="list summaries with legacy features")
    parser.add_argument("--quiet", action="store_true", help="summary only")
    args = parser.parse_args()
    if args.app:
        return audit_app(args.app)
    if args.summary:
        return audit_summary()

    missing = [p for p in (ROUTING, APPY) if not p.exists()]
    if missing:
        for p in missing:
            print(f"jsony: missing {rel(p)}", file=sys.stderr)
        return 1

    state = load_state()

    if args.record:
        changed = changed_apps()
        if not changed:
            if not args.quiet:
                print("jsony: HEAD did not touch apps/ — nothing queued")
            return 0
        head = git_head()
        state.setdefault("queue", []).append({
            "commit": head,
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "files": changed,
        })
        save_state(state)
        if not args.quiet:
            print(f"jsony: queued {len(changed)} app change(s) at {head[:8] or 'unknown'}")
        return 0

    if args.changed:
        queue = state.get("queue") or []
        changed = sorted({f for item in queue for f in item.get("files", [])})
        if not changed:
            if not args.quiet:
                print("jsony: no queued apps/ changes — skip")
            return 0
        last = queue[-1].get("commit") if queue else state.get("lastCommit")
    else:
        changed = []
        last = None

    findings = build_findings(changed)

    if not args.quiet:
        print(f"jsony: critical={findings['critical']} advisory={findings['advisory']} changed={len(changed)}")
        if findings["routingMissing"]:
            print("  routing missing:", ", ".join(str(x.get("id") or x.get("path")) for x in findings["routingMissing"]))
        if findings["routingUrlMissing"]:
            print("  routing urls missing:", ", ".join(x["id"] for x in findings["routingUrlMissing"]))
        if findings["appyMissing"]:
            print("  appy missing:", ", ".join(x["id"] for x in findings["appyMissing"]))
        if findings["appyExtra"]:
            print("  appy extra:", ", ".join(x["id"] for x in findings["appyExtra"]))
        if findings["appyMismatch"]:
            print("  appy mismatch:", ", ".join(x["id"] for x in findings["appyMismatch"]))
        if findings["exportAppyMissing"]:
            print("  appy envelope missing:", ", ".join(findings["exportAppyMissing"]))
        if findings["appsWithoutPortrait"]:
            print("  apps without portrait:", len(findings["appsWithoutPortrait"]))
        if findings.get("commonDrift"):
            print("  common.json drift:", len(findings["commonDrift"]))
        if findings.get("movesDrift"):
            print("  exported moves:", len(findings["movesDrift"]))

    if not args.no_write:
        PENDING_MD.write_text(markdown_report(findings), encoding="utf-8")
        PENDING_JSON.write_text(json.dumps(findings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.changed:
            state = load_state()
            if last:
                state["lastCommit"] = last
            state["lastRun"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            state["queue"] = []
            save_state(state)
        if not args.quiet:
            print(f"  pending: {rel(PENDING_MD)} · {rel(PENDING_JSON)}")

    if args.soft:
        return 0
    if findings["critical"]:
        return 1
    if args.strict and findings["advisory"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
