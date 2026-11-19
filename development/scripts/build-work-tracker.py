#!/usr/bin/env python3
"""Canonical Work tracker block for development/index.html.

  --build  regenerate the JSON block from the real Gitea snapshot (pendings.md)
  --check  validate the block embedded in development/index.html

The HTML block is canonical: the page renders it as a custom mirror of the
snapshot. There is no live fetch and no third copy of the rows. MD/wiki stays
external via ↗ links. `fields[]` is never inferred — it is manual only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
PEND = ROOT / "standards/debates/pendings.md"
BEGIN = "<!-- WORK-DATA:BEGIN -->"
END = "<!-- WORK-DATA:END -->"
SCRIPT_OPEN = '<script type="application/json" id="work-data">'
SCRIPT_CLOSE = "</script>"

TABS = ["backend", "frontend", "ai", "data", "infra", "ux", "community", "roadmap"]
PHASES = ["F0", "F1", "F2", "F3", "F4", "F5", "Next"]
LEVELS = {
    "S1": "Planned & specified",
    "S2": "In build",
    "S3": "In quality",
    "S4": "Documented",
    "S5": "Delivered & operating",
}
GLYPH = {"S1": "\u00b7", "S2": "+", "S3": "-", "S4": "+", "S5": "\u2713",
         "done": "\u2713", "na": "\u2014"}

# Explicit classification: ID prefix -> (category, domain, type, phase, field).
PREFIX = {
    "VARIOUS_Q": ("roadmap", "decisions", "question", "Next", "decisions"),
    "QUESTYDEMO": ("ux", "interview", "demo", "Next", "questy"),
    "BR": ("community", "risa", "community", "F5", "risa"),
    "GH": ("infra", "git", "infra", "F0", "git"),
    "N": ("frontend", "nety", "app", "F2", "nety"),
    "NF": ("frontend", "nety", "app", "F2", "nety"),
    "ARCH": ("infra", "architecture", "infra", "F3", "architecture"),
    "V": ("ux", "voice", "design", "Next", "voice"),
    "A11Y": ("ux", "a11y", "standard", "F1", "a11y"),
    "UX": ("ux", "experience", "design", "F1", "ux"),
    "VOCAB": ("data", "vocabulary", "standard", "F1", "vocabulary"),
    "W": ("backend", "workflow", "backend", "F0", "workflow"),
    "T": ("data", "taxonomy", "data", "F1", "taxonomy"),
    "PZ": ("roadmap", "puzzy", "plan", "F5", "puzzy"),
    "DS": ("frontend", "desk", "design", "F4", "desk"),
    "BUI": ("ux", "build", "demo", "F1", "build"),
    "NUI": ("ux", "interface", "demo", "F2", "nety"),
    "RC": ("community", "curators", "community", "F5", "nety"),
    "RISADNS": ("community", "risa", "community", "F5", "risa"),
    "BACKY": ("data", "backup", "infra", "F0", "backup"),
    "LANG": ("ux", "i18n", "standard", "F1", "i18n"),
    "PEN": ("roadmap", "pending", "question", "Next", "tracker"),
    "REV": ("ux", "review", "review", "F1", "review"),
    "CB_S": ("backend", "solo", "backend", "F3", "solo"),
    "EXP": ("data", "export", "standard", "F1", "export"),
    "FIELDS": ("data", "fields", "standard", "F1", "fields"),
}

# Keyword overrides applied to the title (first match wins).
KEYWORDS = [
    (("ai", "model", "llm", "lora", "fine-tun"), ("ai", "models", "ai", "Next", "ai")),
    (("infra", "pwa", "install", "deploy", "r2", "build", "release", "git", "ci"),
     ("infra", "delivery", "infra", "F0", "infra")),
    (("json", "field", "schema", "export", "portrait", "vocab", "taxonom"),
     ("data", "data-model", "standard", "F1", "data")),
    (("a11y", "accessible", "theme", "onboard", "i18n", "translat", "footer", "design", "docs"),
     ("ux", "experience", "standard", "F1", "ux")),
    (("community", "curator", "moderat", "risa", "linguist", "social"),
     ("community", "community", "community", "F5", "community")),
    (("browsy", "crypto", "permission", "keys", "login", "encrypt", "cubes", "visibility", "cross-link"),
     ("backend", "trust", "backend", "F3", "backend")),
]


def classify(rid, title):
    """Return (category, domain, type, phase, field, state, subcategory, labels)."""
    low = title.lower()
    cats = ""
    if " \u00b7 " in title:
        head, tail = title.split(" \u00b7 ", 1)
        cats = tail.split(" \u2014 \u25c7")[0]
        title = head
    labels = [c.strip() for c in cats.split(",") if c.strip()]

    base = None
    for key in sorted(PREFIX, key=len, reverse=True):
        if rid.startswith(key):
            base = PREFIX[key]
            break
    # A specific ID prefix wins; generic ones (VARIOUS_Q, PEN) use keyword rules.
    generic = base is None or rid.startswith(("VARIOUS_Q", "PEN"))

    def has(needle):
        # Short tokens need word boundaries ("ai" must not match "maintained").
        if len(needle) <= 4:
            return re.search(r"\b" + re.escape(needle) + r"\b", low) is not None
        return needle in low

    if generic:
        for needles, mapped in KEYWORDS:
            if any(has(n) for n in needles):
                base = mapped
                break
    if base is None:
        base = ("roadmap", "general", "question", "Next", "tracker")

    category, domain, typ, phase, field = base
    # VARIOUS_Q rows carry a real domain in their cats; keep it.
    if rid.startswith("VARIOUS_Q") and labels:
        domain = labels[0]
        field = labels[0]

    state = "S1"
    if "live demo" in low or "hecho" in low or "\u2705" in low:
        state = "S5"
    elif "partly live" in low or "in build" in low:
        state = "S2"
    elif "revisi" in low or "review" in low:
        state = "S3"

    return category, domain, typ, phase, field, state, state, labels


def build_rows():
    text = PEND.read_text(encoding="utf-8")
    rows = []
    seen = set()
    for line in text.splitlines():
        m = re.match(r"^- \*\*([A-Z0-9_]+(?: [A-Za-z][A-Za-z0-9 ]*)?)\*\* (.+)$", line)
        if not m:
            continue
        bold, rest = m.group(1), m.group(2).strip()
        # "REV01 Tours" → id REV01, title "Tours — …"
        if " " in bold:
            rid, tail = bold.split(" ", 1)
            title = tail + " \u2014 " + rest.lstrip("\u2014 ").strip()
        else:
            rid, title = bold, rest
        if rid in seen:
            continue
        # Retired / resolved items are out of scope for the tracker.
        if title.startswith("~~") or "\u2705" in title or re.search(
                r"\b(hecho|retirado|done)\b", title, re.I):
            continue
        seen.add(rid)
        category, domain, typ, phase, field, state, subcat, labels = classify(rid, title)
        rows.append({
            "id": rid,
            "title": title,
            "state": state,
            "labels": labels or [domain],
            "milestone": phase,
            "field": field,
            "source": "standards",
            "updated": "2026-11-19",
            "phase": phase,
            "category": category,
            "domain": domain,
            "type": typ,
            "subcategory": subcat,
            "fields": [],
            "refs": [{"label": "pendings.md#" + rid,
                      "url": "standards/debates/pendings.md"}],
        })
    rows.sort(key=lambda r: r["id"])
    return rows


def canonical():
    return {
        "schema": "flove-work/1",
        "generated": "2026-11-19",
        "snapshot": "Gitea flove · development/standards/debates/pendings.md",
        "tabs": TABS,
        "phases": PHASES,
        "levels": LEVELS,
        "glyphs": GLYPH,
        "groups": ["state", "phase", "field", "source", "category", "domain",
                   "type", "subcategory"],
        "rows": build_rows(),
    }


def extract_block(html):
    i = html.find(BEGIN)
    j = html.find(END, i + len(BEGIN))
    if i < 0 or j < 0:
        return None, None
    inner = html[i + len(BEGIN):j].strip()
    if not inner.startswith(SCRIPT_OPEN) or not inner.endswith(SCRIPT_CLOSE):
        return None, None
    raw = inner[len(SCRIPT_OPEN):-len(SCRIPT_CLOSE)]
    return (i, j + len(END)), raw


def do_build():
    data = canonical()
    body = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
    block = BEGIN + "\n" + SCRIPT_OPEN + "\n" + body + "\n" + SCRIPT_CLOSE + "\n" + END
    html = HTML.read_text(encoding="utf-8")
    span, _ = extract_block(html)
    if span:
        html = html[:span[0]] + block + html[span[1]:]
    else:
        anchor = '<div data-webpanel-content="work" id="home-work" hidden>'
        if anchor not in html:
            sys.exit("work panel anchor not found")
        html = html.replace(anchor, anchor + "\n" + block, 1)
    HTML.write_text(html, encoding="utf-8")
    print("built %d rows into %s" % (len(data["rows"]), HTML.relative_to(ROOT.parent)))


def do_check():
    html = HTML.read_text(encoding="utf-8")
    span, raw = extract_block(html)
    if not span:
        sys.exit("FAIL: canonical block not found in " + str(HTML))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit("FAIL: invalid JSON: %s" % e)
    errors = []
    if data.get("schema") != "flove-work/1":
        errors.append("bad schema")
    if data.get("tabs") != TABS:
        errors.append("tabs must be the 8 canonical names")
    if data.get("phases") != PHASES:
        errors.append("phases must be F0-F5 + Next")
    if set(data.get("levels", {})) != set(LEVELS):
        errors.append("levels must be S1-S5")
    rows = data.get("rows", [])
    if not rows:
        errors.append("no rows")
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    required = ["id", "title", "state", "labels", "milestone", "field", "source",
                "updated", "phase", "category", "domain", "type", "subcategory",
                "fields", "refs"]
    for r in rows:
        rid = r.get("id", "?")
        for k in required:
            if k not in r:
                errors.append("%s: missing %s" % (rid, k))
        if r.get("category") not in TABS:
            errors.append("%s: bad category %r" % (rid, r.get("category")))
        if r.get("phase") not in PHASES:
            errors.append("%s: bad phase %r" % (rid, r.get("phase")))
        if r.get("subcategory") not in LEVELS:
            errors.append("%s: bad subcategory %r" % (rid, r.get("subcategory")))
        if not isinstance(r.get("fields"), list):
            errors.append("%s: fields[] must be a list" % rid)
    if errors:
        for e in errors[:40]:
            print("FAIL:", e)
        sys.exit("%d validation error(s)" % len(errors))
    print("OK: %d rows, %d tabs, %d groups, schema %s"
          % (len(rows), len(TABS), len(data["groups"]), data["schema"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true", help="regenerate the canonical block")
    g.add_argument("--check", action="store_true", help="validate the embedded block")
    args = ap.parse_args()
    do_build() if args.build else do_check()
