#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed per-app accent colour + field into fields-colours.json from apps-full.

Source of truth for the accents: development/central/apps/apps-full.html's
launcher tiles — top-level tiles wear their category colour; the Dealy-family
child tiles carry their own polished accent (--c-cur). Field comes from the
tiles' sub-* classes (currently only Inside apps are grouped: Metaphysics sub-meta
and Psychology sub-psy). Apps with no apps-full tile yet (offer, minioffer, wisy,
wizy, fity, questy, loly, browsy) and aliased anchors map as below.

One-way extract: only ADDS colour/field when absent; never overwrites an
existing value, so the table stays canonical once it diverges from apps-full.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "fields-colours.json")

# id → (accent hex from the apps-full launcher tiles, field)
ACCENTS = {
    # Mating — yellow tile
    "daty": ("#ffd84d", ""), "varyy": ("#ffd84d", ""), "trusty": ("#ffd84d", ""),
    "crumbly": ("#ffd84d", ""), "evily": ("#ffd84d", ""), "maty": ("#ffd84d", ""),
    "myfamily": ("#ffd84d", ""), "parenty": ("#ffd84d", ""),
    # Inside — orange tile, grouped by field (sub-meta / sub-psy)
    "astry": ("#ff9b5e", "Metaphysics"), "goddy": ("#ff9b5e", "Metaphysics"),
    "willy": ("#ff9b5e", "Metaphysics"), "cathy": ("#ff9b5e", "Metaphysics"),
    "hacky": ("#ff9b5e", "Psychology"), "diesafe": ("#ff9b5e", "Psychology"),
    "pracsys": ("#ff9b5e", "Psychology"), "sensy": ("#ff9b5e", "Psychology"),
    "souls": ("#ff9b5e", "Psychology"), "profily": ("#ff9b5e", "Psychology"),
    # Ling / Words — green tile
    "keys": ("#6ed089", ""), "fivy": ("#6ed089", ""), "puzzy": ("#6ed089", ""),
    # Social — blue tile
    "socy": ("#5ea4e6", ""), "realy": ("#5ea4e6", ""), "blogy": ("#5ea4e6", ""),
    "nety": ("#5ea4e6", ""), "shareful": ("#5ea4e6", ""),  # shareful = 'Shary' child, blue
    # Economy — indigo tile for the family, distinct accents for Dealy children
    "crafty": ("#6b6bd9", ""), "worthing": ("#6b6bd9", ""), "lowy": ("#6b6bd9", ""),
    "dealy": ("#ffd84d", ""),     # Dealy child accent (yellow)
    "inventary": ("#ff8a8a", ""),  # polished 2026-09-10: red (was blue #2f7fd6)
    "wanty": ("#ff9b5e", ""),      # child accent orange
    "freed": ("#6ed089", ""),      # child accent green
    "rewardy": ("#6b6bd9", ""),    # child accent indigo
    # lovy: apps-full 'Loves' tile is yellow + sub-psy, though its home is Economy
    # (the deep multi-category review is still open — colour/field kept as-is)
    "lovy": ("#ffd84d", "Psychology"),
    # Later tiles (apps-full marks present): accents from tile-rb colour classes
    "wisy": ("#6ed089", ""),     # tile-rb-g (also child --c-cur:#6ed089)
    "wizy": ("#5ea4e6", ""),     # tile-rb-b
    "browsy": ("#5ea4e6", ""),   # tile-rb-b
    "loly": ("#6ed089", ""),     # tile-rb-g
    "fity": ("#ff9b5e", ""),     # tile-rb-o (field stays Biology per catalog)
    "questy": ("#ff9b5e", ""),   # tile-rb-o
    # Solo apps with no central tile yet — Economy family indigo like crafty/worthing
    "offer": ("#6b6bd9", ""),
    "minioffer": ("#6b6bd9", ""),
}

def main():
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    changed = 0
    for app in data["apps"]:
        if "colour" not in app:
            got = ACCENTS.get(app["id"])
            if got and got[0]:
                app["colour"] = got[0]
                if got[1]:
                    app["field"] = got[1]
                elif not app.get("field"):
                    app.pop("field", None)
                changed += 1
    note = data.get("note", "")
    if "accent hex" not in note:
        data["note"] = (note.rstrip() +
                        " Each app also carries its accent hex (colour) and, when "
                        "grouped, a field (Inside = Metaphysics/Psychology), taken from "
                        "the apps-full launcher tiles. Regenerate the ODS after edits.")
    with open(DATA, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    missing = [a["id"] for a in data["apps"] if "colour" not in a]
    print(f"colours+fields applied: {changed} · still uncoloured: {len(missing)} "
          f"({', '.join(missing)})")
    return 0

if __name__ == "__main__":
    sys.exit(main())