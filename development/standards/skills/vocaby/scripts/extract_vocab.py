#!/usr/bin/env python3
"""
extract_vocab.py — scan a single-file flove HTML/CSS/JS app and emit a vocabulary
inventory as JSON: every candidate internal name, all the lines it appears on, whether a
CSS-only-nav selector keys on it (load-bearing), its resolved UI label when one can be
found, a preliminary Safe/Nav-risk bucket, and any legacy markers / nested data objects.

This is the deterministic "discover" half of the /vocaby skill. The model then
reviews, classifies the dubious cases, and decides renames — it does not re-grep by hand.
It is a heuristic scanner, not a full parser: treat its buckets as a strong default, not
gospel. Stdlib only.

Usage:
    python extract_vocab.py <file.html> [--out inventory.json]
    python extract_vocab.py <file.html> --summary      # human-readable counts only
"""
import argparse
import json
import re
import sys
from collections import defaultdict

# ---- block segmentation -----------------------------------------------------------------

def find_blocks(text, tag):
    """Yield (start_idx, end_idx) char spans of <tag>...</tag> (case-insensitive)."""
    spans = []
    for m in re.finditer(rf"<{tag}\b[^>]*>", text, re.I):
        end = re.search(rf"</{tag}\s*>", text[m.end():], re.I)
        if end:
            spans.append((m.end(), m.end() + end.start()))
    return spans

def line_of(text, idx):
    return text.count("\n", 0, idx) + 1

def in_spans(idx, spans):
    return any(a <= idx < b for a, b in spans)

# ---- legacy / rename markers ------------------------------------------------------------

LEGACY_RE = re.compile(
    r"(renamed from|deferred class rename|legacy|deprecated|dead code|no longer|"
    r"\bold name\b|\balias\b|was ['\"]?)", re.I)

def find_legacy(text):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if LEGACY_RE.search(line):
            out.append({"line": i, "text": line.strip()[:160]})
    return out

# ---- nested data objects (deck -> items, etc.) ------------------------------------------

DECK_RE = re.compile(
    r"\{\s*id\s*:\s*['\"](?P<id>[^'\"]+)['\"]\s*,\s*"
    r"title\s*:\s*['\"](?P<title>[^'\"]+)['\"]"
    r"(?:[^{}]*?items\s*:\s*\[(?P<items>[^\]]*)\])?",
    re.S)

def find_data_objects(text):
    out = []
    for m in DECK_RE.finditer(text):
        items = []
        if m.group("items"):
            items = [s.strip().strip("'\"") for s in m.group("items").split(",")
                     if s.strip().strip("'\"")]
        out.append({
            "line": line_of(text, m.start()),
            "id": m.group("id"),
            "title": m.group("title"),
            "items": items,
        })
    return out

# ---- label resolution: <label for="id">text</label> and aria-label ----------------------

def resolve_labels(text):
    """id -> shown label, from `<label for=...>text</label>` and `aria-label`."""
    labels = {}
    for m in re.finditer(r"<label\b[^>]*\bfor\s*=\s*['\"]([^'\"]+)['\"][^>]*>(.*?)</label>",
                         text, re.I | re.S):
        fid, inner = m.group(1), m.group(2)
        # strip nested tags, collapse whitespace
        txt = re.sub(r"<[^>]+>", " ", inner)
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt and fid not in labels:
            labels[fid] = txt[:80]
    for m in re.finditer(r"\bid\s*=\s*['\"]([^'\"]+)['\"][^>]*\baria-label\s*=\s*['\"]([^'\"]+)['\"]",
                         text, re.I):
        labels.setdefault(m.group(1), m.group(2)[:80])
    return labels

# ---- name collection --------------------------------------------------------------------

# tokens that make a selector state/navigation-driven (the load-bearing tell). Plain
# styling selectors (`.foo{...}`) are NOT load-bearing — only state ones are.
STATE_RE = re.compile(r":checked|:target|:has\(|:focus-within|:focus-visible")

def collect(text):
    style_spans = find_blocks(text, "style")
    script_spans = find_blocks(text, "script")

    sites = defaultdict(list)          # (kind, name) -> [lines]
    selector_sites = defaultdict(list) # (kind, name) -> [lines] where any selector keys on it
    state_names = set()                # (kind, name) used in a :checked/:has/:target selector
    kinds = {}

    def add(kind, name, idx, selector=False):
        key = (kind, name)
        ln = line_of(text, idx)
        if ln not in sites[key]:
            sites[key].append(ln)
        kinds[key] = kind
        if selector and ln not in selector_sites[key]:
            selector_sites[key].append(ln)

    # class="a b c" in markup
    for m in re.finditer(r"\bclass\s*=\s*['\"]([^'\"]+)['\"]", text):
        for cls in m.group(1).split():
            if re.fullmatch(r"[A-Za-z_][\w-]*", cls):
                add("class", cls, m.start())
    # id="name" in markup
    for m in re.finditer(r"\bid\s*=\s*['\"]([A-Za-z_][\w-]*)['\"]", text):
        add("id", m.group(1), m.start())
    # CSS selectors — walk rule by rule so we know whether each selector is state-driven
    for a, b in style_spans:
        css = text[a:b]
        for rule in re.finditer(r"([^{}]+)\{", css):
            sel = rule.group(1)
            sel_start = a + rule.start(1)
            is_state = bool(STATE_RE.search(sel))
            for m in re.finditer(r"([.#])([A-Za-z_][\w-]*)", sel):
                kind = "class" if m.group(1) == "." else "id"
                add(kind, m.group(2), sel_start + m.start(), selector=True)
                if is_state:
                    state_names.add((kind, m.group(2)))
    # input name="..." — radio/checkbox groups are CSS-only-nav state by nature
    for m in re.finditer(r"\bname\s*=\s*['\"]([A-Za-z_][\w-]*)['\"]", text):
        add("input-name", m.group(1), m.start())
    # data-* attribute keys
    for m in re.finditer(r"\b(data-[a-z][\w-]*)\s*=", text):
        add("data-attr", m.group(1), m.start())
    # i18n keys: tKey('a.b.c')
    for m in re.finditer(r"tKey\(\s*['\"]([^'\"]+)['\"]", text):
        add("i18n-key", m.group(1), m.start())

    return sites, selector_sites, state_names, kinds, style_spans, script_spans

# ---- load-bearing references (for=, :has(#id), aria-controls, etc.) ----------------------

def referenced_ids(text):
    """ids that a navigation/relationship selector points AT -> set of ids."""
    ids = set()
    for pat in (r"\bfor\s*=\s*['\"]([^'\"]+)['\"]",
                r":has\(\s*#([\w-]+)",
                r"\baria-(?:controls|labelledby|describedby)\s*=\s*['\"]([^'\"]+)['\"]"):
        for m in re.finditer(pat, text, re.I):
            ids.update(m.group(1).split())
    return ids

# ---- assemble ---------------------------------------------------------------------------

def build(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    sites, selector_sites, state_names, kinds, style_spans, script_spans = collect(text)
    ref_ids = referenced_ids(text)
    labels = resolve_labels(text)
    legacy = find_legacy(text)
    legacy_lines = {d["line"] for d in legacy}

    terms = []
    for key in sites:
        kind, name = key
        sel = sorted(selector_sites.get(key, []))
        # load-bearing = a state selector keys on it, an id is targeted by for=/:has()/aria-*,
        # or it's an input-name (radio/checkbox group state). Plain styling is NOT load-bearing.
        load_bearing = (key in state_names
                        or (kind in ("id", "input-name") and name in ref_ids)
                        or kind == "input-name")
        label = labels.get(name)
        near_legacy = any(abs(ln - L) <= 1 for ln in sites[key] for L in legacy_lines)
        bucket = "nav-risk" if load_bearing else "safe"
        terms.append({
            "name": name,
            "kind": kind,
            "sites": sorted(sites[key]),
            "selector_sites": sel,
            "load_bearing": load_bearing,
            "label": label,
            "bucket": bucket,
            "maybe_legacy": near_legacy,
        })

    # deterministic order, then number
    terms.sort(key=lambda t: (t["kind"], t["name"]))
    for i, t in enumerate(terms, 1):
        t["id"] = i
    for t in terms:  # put id first for readability
        t_keys = ["id", "name", "kind", "label", "bucket", "load_bearing",
                  "maybe_legacy", "sites", "selector_sites"]
        for k in list(t):
            if k not in t_keys:
                t_keys.append(k)

    return {
        "file": path,
        "summary": {
            "terms": len(terms),
            "load_bearing": sum(t["load_bearing"] for t in terms),
            "with_label": sum(t["label"] is not None for t in terms),
            "maybe_legacy": sum(t["maybe_legacy"] for t in terms),
            "by_kind": {k: sum(1 for t in terms if t["kind"] == k)
                        for k in sorted({t["kind"] for t in terms})},
        },
        "legacy_markers": legacy,
        "data_objects": find_data_objects(text),
        "terms": terms,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    ap.add_argument("--summary", action="store_true", help="print counts only")
    ap.add_argument("--labeled", action="store_true",
                    help="keep only the high-signal terms (a resolved UI label or a legacy "
                         "marker) — the seed for the numbered review table")
    a = ap.parse_args()
    inv = build(a.file)
    if a.labeled:
        inv["terms"] = [t for t in inv["terms"] if t["label"] or t["maybe_legacy"]]
        inv["summary"]["shown"] = len(inv["terms"])
    if a.summary:
        print(json.dumps(inv["summary"], indent=2, ensure_ascii=False))
        return
    out = json.dumps(inv, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
        print(f"wrote {a.out}: {inv['summary']['terms']} terms "
              f"({inv['summary']['load_bearing']} load-bearing)", file=sys.stderr)
    else:
        print(out)

if __name__ == "__main__":
    main()
