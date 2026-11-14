#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drift gate for the questy-flove field pipeline (flove-hats/1).

THE gate (exit code): the matrix (vocabulary/index.html slotKinds) is the
authority; fields-colours.json must mirror it per app:

    matrix input slots (kind=="input")  ==  catalog app slots (slots keys)

Run by /vocaby at sync time (Q11 invariant of the flove workflow): a slot whose
kind flips input↔display in the matrix but not in the catalog is a silent
divergence — questy-flove would keep asking (or stop asking) about a field the
other side no longer treats as user data. Nothing crashes; it quietly ships a
stale questionnaire.

Also reports (advisory, never fail the gate):
  - matrix apps absent from the catalog (e.g. hoty, removed)
  - catalog apps absent from the matrix (expected: the signature-only extras)
  - questy-flove's hand-copied INPUT_FIELDS/CATEGORIES vs the catalog, when
    --with-consumers is given (the real drift this gate eventually removes)

Never edits anything: it surveys, prints, and exits 0/1. Regenerate-from-source
stays the rule — checking never mutates.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = os.path.dirname(HERE)
MATRIX = os.path.join(VOCAB, "index.html")
CATALOG = os.path.join(VOCAB, "fields-colours.json")
QF = os.path.join(VOCAB, "..", "skills", "questy-flove", "index.html")

CONSUMER_ALIASES = {"MoralY": "cathy", "Crumbly": "crumbly"}  # display name → canonical id (Q5)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def brace_block(text, start):
    """Return the brace-balanced text starting at `start` (the opening brace)."""
    i = text.index("{", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    raise ValueError("unbalanced braces")


def parse_app_id_list(text, const_name):
    m = re.search(rf"const\s+{const_name}\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        return []
    return re.findall(r'"([^"]+)"', m.group(1))


def parse_kinds(text):
    block = brace_block(text, text.index("const slotKinds ="))
    kinds = {}
    for m in re.finditer(r'"?([A-Za-z][\w ]*)"?\s*:\s*\{', block):
        app = m.group(1)
        styles = re.findall(r'"([^"]+)"\s*:\s*"(input|display|action|nav)"', block[m.end():])
        kinds[app] = {s: k for s, k in styles}
        for s, k in styles:
            if s == "Menu" and k == "nav":
                pass
        start = block.find("}", block.index("{", m.start() + 1))
    # Brace-split per app is unreliable with the regex above; fall back to a
    # proper scan: walk depth-1 entries and read each object fully.
    return kinds


def parse_slot_kinds(text):
    start = text.index("const slotKinds =")
    block = brace_block(text, text.index("{", start))
    i = 0
    kinds = {}
    while i < len(block):
        m = re.match(r'\s*"?([\w ]+)"?\s*:\s*\{', block[i:])
        if m:
            obj_start = i + len(m.group(0)) - 1  # point at the opening brace
            body = brace_block(block, obj_start)
            app = m.group(1)
            styles = dict(re.findall(r'"([^"]+)"\s*:\s*"(input|display|action|nav)"', body))
            kinds[app] = styles
            i = obj_start + len(body)
        else:
            i += 1
    return kinds


def parse_consumer_inputs(text):
    """Parse questy-flove's INPUT_FIELDS and CATEGORIES (depth-1 consts)."""
    fields, cats = {}, []
    for cname, out in (("INPUT_FIELDS", fields),):
        m = re.search(rf"const\s+{cname}\s*=\s*\{{", text)
        if not m:
            continue
        start = text.index("{", m.start())
        block = brace_block(text, start)
        i = 0
        while i < len(block):
            mm = re.match(r'\s*(?:["\'])?([\w ]+)(?:["\'])?\s*:\s*\[', block[i:])
            if mm:
                arr_start = i + len(mm.group(0)) - 1
                body = block[arr_start:block.index("]", arr_start) + 1]
                out[mm.group(1)] = re.findall(r'["\']([^"\']+)["\']', body)
                i = arr_start + len(body)
            else:
                i += 1
    catm = re.search(r"const\s+CATEGORIES\s*=\s*\[(.*?)\];", text, re.S)
    if catm:
        block = catm.group(1)
        for m in re.finditer(r"apps:\s*\[(.*?)\]", block, re.S):
            cats += re.findall(r"[\"']([^\"']+)[\"']", m.group(1))
    return fields, cats


def catalog_apps(data):
    return {a["id"]: a for a in data["apps"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-consumers", action="store_true",
                    help="also survey questy-flove's hand-copied consts (advisory)")
    args = ap.parse_args()

    matrix_text = read(MATRIX)
    catalog = json.loads(read(CATALOG))
    matrix_apps = parse_app_id_list(matrix_text, "APPS")
    slot_kinds = parse_slot_kinds(matrix_text)
    apps = catalog_apps(catalog)
    cat_order = [c["name"] for c in catalog["categories"]]

    problems = []
    advisory = []

    matrix_inputs = {a: {s for s, k in slot_kinds.get(a, {}).items() if k == "input"}
                     for a in matrix_apps if a in slot_kinds}
    catalog_inputs = {a: set(slots.keys()) for a, slots in
                      ((a["id"], a.get("slots", {})) for a in catalog["apps"])}

    for app in sorted(catalog_inputs):
        if app not in matrix_apps:
            advisory.append(f"catalog-only app not in matrix APPS: {app}")
            continue
        mi = set(slot_kinds.get(app, {}))
        ci = catalog_inputs[app]
        only_matrix = {s for s in mi if slot_kinds.get(app, {}).get(s) == "input"} - ci
        only_catalog = ci - {s for s, k in slot_kinds.get(app, {}).items() if k == "input"}
        if only_matrix or only_catalog:
            problems.append(
                f"slot-set drift in {app}: matrix-input-only {sorted(only_matrix)} · "
                f"catalog-only {sorted(only_catalog)}")

    for app in sorted(matrix_apps):
        if app not in catalog_inputs:
            if slot_kinds.get(app):
                problems.append(f"matrix app {app} missing from catalog (has {len(slot_kinds[app])} slots)")
            else:
                advisory.append(f"matrix app with no slotKinds entry: {app}")

    if args.with_consumers:
        try:
            qf_text = read(QF)
            qf_fields, qf_cats = parse_consumer_inputs(qf_text)
        except OSError:
            qf_fields, qf_cats = {}, []
            advisory.append("questy-flove/index.html not found — consumer survey skipped")
        missing = []
        titles = set()
        for a in qf_cats:
            cid = CONSUMER_ALIASES.get(a, a.lower())
            titles.add(cid)
            if cid not in catalog_inputs:
                missing.append(a)
        if missing:
            advisory.append(f"questy-flove CATEGORIES apps not in catalog: {sorted(set(missing))}")
        not_askable = sorted(t for t in titles if t not in slot_kinds)
        in_catalog_only = sorted(a for a in catalog_inputs
                                 if a not in titles
                                 and a not in ("hoty",))
        if not_askable:
            advisory.append(f"questy-flove picker includes matrix-less apps: {not_askable}")
        if in_catalog_only:
            advisory.append(f"catalog apps with input slots not in questy-flove picker: {in_catalog_only}")
        for cname, slots in qf_fields.items():
            cid = CONSUMER_ALIASES.get(cname, cname.lower())
            if cid not in catalog_inputs:
                continue
            want = sorted(s for s, k in slot_kinds.get(cid, {}).items() if k == "input")
            have = sorted(slots)
            if set(have) != set(want):
                advisory.append(f"questy-flove INPUT_FIELDS[{cname}] drifts from catalog: "
                                f"has {have} · catalog {want}")

    print(f"matrix apps: {len(matrix_apps)} · catalog apps: {len(apps)} · "
          f"catalog input slots: {sum(len(v) for v in catalog_inputs.values())}")
    print(f"gate (matrix inputs == catalog slots): {'CLEAN' if not problems else 'DRIFT'}")
    for p in problems:
        print(f"  DRIFT  {p}")
    for a in advisory:
        print(f"  note   {a}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())