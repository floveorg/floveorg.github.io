#!/usr/bin/env python3
"""
extract_vocab.py — scan a single-file flove HTML/CSS/JS app and emit a vocabulary
inventory as JSON: every candidate internal name AND every translatable display string,
all the lines each appears on, whether a CSS-only-nav selector keys on a name
(load-bearing), the resolved UI label / en+es translation when one can be found, a
preliminary Safe/Nav-risk bucket, and any legacy markers / nested data objects.

This is the deterministic "discover" half of the /vocaby skill. The model then
reviews, classifies the dubious cases, and decides renames — it does not re-grep by hand.
It is a heuristic scanner, not a full parser: treat its buckets as a strong default, not
gospel. Stdlib only.

It extracts TWO layers on purpose (a deep pass as complete as possible without touching
load-bearing features):

  * MACHINE names — class / id / input-name / data-attr / i18n-key / semantic key.
    These live in selectors and JS; a name a state selector keys on is flagged
    `load_bearing` (Nav-risk by default). Renaming those needs care.
  * DISPLAY strings — every visible, translatable field: translaty `.en`/`.es` spans,
    `data-aria-*` / `data-ph-*` / `placeholder` / `aria-label` / `title` and the inner
    text of headings, buttons, labels and options. These are what the UI shows and the
    "to translate" candidate set; they are presentational and Safe to edit/translate.

Usage:
    python extract_vocab.py <file.html> [--out inventory.json]
    python extract_vocab.py <file.html> --summary           # human-readable counts only
    python extract_vocab.py <file.html> --labeled           # high-signal slice for review
    python extract_vocab.py <file.html> --deep-json OUT     # display inventory only
"""
import argparse
import json
import re
import sys
from collections import defaultdict

# ---- block segmentation -----------------------------------------------------------------

def find_blocks(text, tag):
    spans = []
    for m in re.finditer(rf"<{tag}\b[^>]*>", text, re.I):
        end = re.search(rf"</{tag}\s*>", text[m.end():], re.I)
        if end:
            spans.append((m.end(), m.end() + end.start()))
    return spans

def line_of(text, idx):
    return text.count("\n", 0, idx) + 1

def clean_txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")
    s = s.replace("{", " ").replace("}", " ")   # drop template braces, they hide JS
    return re.sub(r"\s+", " ", s).strip()

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

# ---- nested data objects (deck -> items, incl. i18n titles) -----------------------------

DECK_RE = re.compile(
    r"\{\s*id\s*:\s*['\"](?P<id>[^'\"]+)['\"]\s*,\s*"
    r"title\s*:\s*['\"](?P<title>[^'\"]+)['\"]"
    r"(?:[^{}]*?items\s*:\s*\[(?P<items>[^\]]*)\])?", re.S)
I18N_TITLE_RE = re.compile(
    r"titleI18n\s*:\s*\{\s*en\s*:\s*['\"]([^'\"]+)['\"]\s*,\s*es\s*:\s*['\"]([^'\"]+)['\"]\s*\}")

def find_data_objects(text):
    out = []
    for m in DECK_RE.finditer(text):
        items = []
        if m.group("items"):
            items = [s.strip().strip("'\"") for s in m.group("items").split(",")
                     if s.strip().strip("'\"")]
        seg = text[m.end():m.end() + 500]
        i18n = I18N_TITLE_RE.search(seg)
        out.append({
            "line": line_of(text, m.start()),
            "id": m.group("id"),
            "title": m.group("title"),
            "items": items,
            "title_en": i18n.group(1) if i18n else None,
            "title_es": i18n.group(2) if i18n else None,
        })
    return out

# ---- label resolution: <label for="id">text</label> , aria-label, title, placeholder ---

def resolve_labels(text):
    labels = {}
    for m in re.finditer(r"<label\b[^>]*\bfor\s*=\s*['\"]([^'\"]+)['\"][^>]*>(.*?)</label>",
                         text, re.I | re.S):
        txt = clean_txt(m.group(2))
        if txt and m.group(1) not in labels:
            labels[m.group(1)] = txt[:80]
    for m in re.finditer(
            r"\bid\s*=\s*['\"]([^'\"]+)['\"][^>]*\b(?:aria-label|title|placeholder)\s*=\s*(['\"])(.*?)\2",
            text, re.I):
        labels.setdefault(m.group(1), m.group(3)[:80])
    return labels

# ---- display (translatable) layer -------------------------------------------------------

ARIA_PH_RE = re.compile(
    r"\b(data-(?:aria|ph|label)-(en|es))\s*=\s*['\"]([^'\"]*)['\"]", re.I)
ATTR_RE = re.compile(
    r"\b(aria-label|placeholder|title)\s*=\s*['\"]([^'\"]{1,120})['\"]", re.I)

def find_display_strings(text):
    """Translatable, presentational strings: dual-span, aria/ph attrs, and visible text
    in buttons / headings / labels / options / summaries."""
    out = []
    seen = set()

    def push(rec):
        k = (rec.get("en"), rec.get("es"), rec.get("attr"))
        if k in seen:
            return
        seen.add(k)
        out.append(rec)

    # dual-span translaty: <span class="en">EN</span><span class="es">ES</span>
    for m in re.finditer(
            r'<span[^>]*class=["\'][^"\']*\ben\b[^"\']*["\'][^>]*>(.*?)</span>\s*'
            r'<span[^>]*class=["\'][^"\']*\bes\b[^"\']*["\'][^>]*>(.*?)</span>',
            text, re.I | re.S):
        en_raw, es_raw = m.group(1), m.group(2)
        en, es = clean_txt(en_raw), clean_txt(es_raw)
        if en in ("${en}", "${es}", "$ en", "$ es", "${es","${en") or es in ("${en}", "${es}", "$ en", "$ es", "${en}", "${es}"):
            continue
        if en and en not in ("${en}", "${es}"):
            push({"kind": "display", "en": en, "es": es or None,
                  "line": line_of(text, m.start())})

    # translatable ARIA / placeholder / data-* language attributes + plain aria/title/placeholder
    for m in ARIA_PH_RE.finditer(text):
        lang, val = m.group(2), m.group(3)
        if val and lang in ("en",):
            push({"kind": "attr", "attr": m.group(1), "lang": lang, "en": clean_txt(val),
                  "line": line_of(text, m.start())})
        elif val:
            push({"kind": "attr", "attr": m.group(1), "lang": lang, "es": clean_txt(val),
                  "line": line_of(text, m.start())})
    for m in ATTR_RE.finditer(text):
        val = clean_txt(m.group(2))
        if val:
            push({"kind": "attr", "attr": m.group(1), "en": val, "lang": "en",
                  "line": line_of(text, m.start())})

    # visible text: inside controls/headings/options/summaries
    for m in re.finditer(
            r'<(?:button|h[1-4]|summary|option|label)\b[^>]*>(.*?)</(?:button|h[1-4]|summary|option|label)>',
            text, re.I | re.S):
        txt = clean_txt(m.group(1))
        if txt and len(txt) >= 2 and not txt.endswith(":") and not txt.endswith("…"):
            push({"kind": "display", "en": txt, "es": None,
                  "line": line_of(text, m.start())})
    return out

# ---- i18n key / dictionary --------------------------------------------------------------

def find_lang_dict(text):
    """Return {key: {en, es}} for an I18N.strings dictionary, if present."""
    m = re.search(r"strings\s*:\s*\{\s*en\s*:\s*\{(.*?)\},\s*es\s*:\s*\{(.*?)\}", text, re.S)
    if not m:
        return {}
    def parse(body):
        return {k: clean_txt(v) for k, v in re.findall(r'["\']?([\w][\w.]*)["\']?\s*:\s*["\']([^"\']*)["\']', body)}
    en, es = parse(m.group(1)), parse(m.group(2))
    keys = set(en) | set(es)
    return {k: {"en": en.get(k), "es": es.get(k)} for k in keys}

def find_i18n_keys(text):
    keys = set()
    for km in re.finditer(r"tKey\(\s*['\"]([^'\"]+)['\"]", text):
        keys.add(km.group(1))
    return keys

# ---- machine-name collection ------------------------------------------------------------

STATE_RE = re.compile(r":checked|:target|:has\(|:focus-within|:focus-visible")

def collect(text):
    sites = defaultdict(list)
    selector_sites = defaultdict(list)
    state_names = set()
    kinds = {}

    def add(kind, name, idx, selector=False):
        key = (kind, name)
        ln = line_of(text, idx)
        if ln not in sites[key]:
            sites[key].append(ln)
        kinds[key] = kind
        if selector and ln not in selector_sites[key]:
            selector_sites[key].append(ln)

    for m in re.finditer(r"\bclass\s*=\s*['\"]([^'\"]+)['\"]", text):
        for cls in m.group(1).split():
            if re.fullmatch(r"[A-Za-z_][\w-]*", cls):
                add("class", cls, m.start())
    for m in re.finditer(r"\bid\s*=\s*['\"]([A-Za-z_][\w-]*)['\"]", text):
        add("id", m.group(1), m.start())
    for a, b in find_blocks(text, "style"):
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
    for m in re.finditer(r"\bname\s*=\s*['\"]([A-Za-z_][\w-]*)['\"]", text):
        add("input-name", m.group(1), m.start())
    for m in re.finditer(r"\b(data-[a-z][\w-]*)\s*=", text):
        add("data-attr", m.group(1), m.start())
    lang_dict = find_lang_dict(text)
    i18n_keys = find_i18n_keys(text)
    for k in i18n_keys:
        sites[("i18n-key", k)] += [0] if not sites[("i18n-key", k)] else []
        kinds[("i18n-key", k)] = "i18n-key"
    return sites, selector_sites, state_names, kinds, i18n_keys, lang_dict

def referenced_ids(text):
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
    sites, selector_sites, state_names, kinds, i18n_keys, lang_dict = collect(text)
    ref_ids = referenced_ids(text)
    labels = resolve_labels(text)
    legacy = find_legacy(text)
    legacy_lines = {d["line"] for d in legacy}

    terms = []
    for key in sorted(sites):
        kind, name = key
        load_bearing = (key in state_names
                        or (kind in ("id", "input-name") and name in ref_ids)
                        or kind == "input-name")
        label = labels.get(name)
        near_legacy = any(abs(ln - L) <= 1 for ln in sites[key] for L in legacy_lines)
        bucket = "nav-risk" if load_bearing else "safe"
        term = {
            "name": name,
            "kind": kind,
            "sites": sorted(sites[key]),
            "selector_sites": sorted(selector_sites.get(key, [])),
            "load_bearing": load_bearing,
            "label": label,
            "bucket": bucket,
            "maybe_legacy": near_legacy,
        }
        if kind == "i18n-key" and name in lang_dict:
            term["en"] = lang_dict[name].get("en")
            term["es"] = lang_dict[name].get("es")
            term["label"] = term["en"] or term["es"]
        terms.append(term)

    terms.sort(key=lambda t: (t["kind"], t["name"]))
    for i, t in enumerate(terms, 1):
        t["id"] = i
    for t in terms:
        t_keys = ["id", "name", "kind", "label", "en", "es", "bucket", "load_bearing",
                  "maybe_legacy", "sites", "selector_sites"]
        for k in list(t):
            if k not in t_keys:
                t_keys.append(k)

    disp = find_display_strings(text)

    return {
        "file": path,
        "summary": {
            "terms": len(terms),
            "load_bearing": sum(t["load_bearing"] for t in terms),
            "with_label": sum(t["label"] is not None for t in terms),
            "maybe_legacy": sum(t["maybe_legacy"] for t in terms),
            "by_kind": {k: sum(1 for t in terms if t["kind"] == k)
                        for k in sorted({t["kind"] for t in terms})},
            "i18n_keys": len(i18n_keys),
            "lang_dict": len(lang_dict),
            "display_strings": len(disp),
        },
        "legacy_markers": legacy,
        "data_blocks": find_data_objects(text),
        "i18n_dict": lang_dict or None,
        "display": disp,
        "terms": terms,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    ap.add_argument("--summary", action="store_true", help="print counts only")
    ap.add_argument("--labeled", action="store_true",
        help="keep only the labelled/legacy/i18n terms (seeded review slice)")
    ap.add_argument("--deep-json", metavar="OUT",
        help="write ONLY the translatable/display inventory for the Deep-labels view")
    ap.add_argument("--no-display", action="store_true", help="drop the display layer")
    a = ap.parse_args()
    inv = build(a.file)
    if a.deep_json:
        deep = {
            "file": inv["file"],
            "approx": inv["summary"],
            "display": inv["display"],
            "i18n": inv.get("i18n_dict"),
            "data_blocks": inv["data_blocks"],
            "machine_count": len(inv["terms"]),
            "load_bearing": inv["summary"]["load_bearing"],
        }
        open(a.deep_json, "w", encoding="utf-8").write(json.dumps(deep, indent=2, ensure_ascii=False))
        print(f"wrote {a.deep_json}: {len(deep['display'])} display strings, "
              f"{len(deep['i18n'] or {})} dict entries", file=sys.stderr)
        return
    if a.no_display:
        inv["display"] = []
    if a.labeled:
        inv["terms"] = [t for t in inv["terms"] if t["label"] or t["maybe_legacy"] or t["kind"] == "i18n-key"]
        inv["summary"]["shown"] = len(inv["terms"]) + len(inv["display"])
    if a.summary:
        print(json.dumps(inv["summary"], indent=2, ensure_ascii=False))
        return
    out = json.dumps(inv, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
        print(f"wrote {a.out}: {inv['summary']['terms']} terms, "
              f"{inv['summary']['display_strings']} display strings "
              f"({inv['summary']['load_bearing']} load-bearing)", file=sys.stderr)
    else:
        print(out)

if __name__ == "__main__":
    main()