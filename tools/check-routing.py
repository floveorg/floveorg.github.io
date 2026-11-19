#!/usr/bin/env python3
"""Validate tools/routing.json without changing it.

Checks:
  - schema/version and required top-level keys
  - unique app ids and urls
  - categories referenced by apps
  - field tree shape, unique ids, allowed types, options, fieldCount
  - cross links point at known apps/fields
  - routing stays colour-free (colours are a separate pending map)
  - apps with no fields are reported as warnings

Usage:
  python3 tools/check-routing.py
  python3 tools/check-routing.py --strict   # warnings become errors
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "tools" / "routing.json"
TYPES = {"text", "text[]", "number", "file", "date", "time", "boolean", "pick", "multi", "unknown", "group", "repeat"}
COLOR_KEYS = {"color", "colour", "colors", "colours", "palette"}


def field_count(nodes):
    n = 0
    for f in nodes or []:
        t = f.get("type")
        if t == "repeat":
            n += (f.get("max") or f.get("min") or 1) * field_count((f.get("item") or {}).get("fields", []))
        elif t == "group":
            n += field_count(f.get("fields", []))
        else:
            n += 1
    return n


def flatten(nodes, parent=""):
    out = []
    for f in nodes or []:
        if not isinstance(f, dict) or not f.get("id"):
            continue
        fid = str(f["id"])
        path = fid if not parent or fid.startswith(parent + ".") else parent + "." + fid
        out.append(path)
        if f.get("type") == "group":
            out += flatten(f.get("fields", []), path)
        if f.get("type") == "repeat":
            out += flatten((f.get("item") or {}).get("fields", []), path)
    return out


def main() -> int:
    errors = []
    warnings = []
    try:
        data = json.loads(ROUTING.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"routing.json does not parse: {exc}", file=sys.stderr)
        return 1

    for key in ("schema", "version", "apps", "categories", "cross", "consumers", "pending"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if data.get("schema") != "flove-routing/3":
        errors.append(f"unexpected schema: {data.get('schema')!r}")

    apps = data.get("apps", [])
    categories = data.get("categories", {})
    ids = {}
    urls = {}
    for app in apps:
        app_id = app.get("id")
        url = app.get("url")
        if not app_id:
            errors.append("app without id")
            continue
        if app_id in ids:
            errors.append(f"duplicate app id: {app_id}")
        ids[app_id] = app
        if not url:
            errors.append(f"{app_id}: missing url")
        elif url in urls:
            errors.append(f"duplicate app url: {url} ({app_id}, {urls[url]})")
        else:
            urls[url] = app_id
        cat = app.get("category")
        if cat and cat not in categories:
            errors.append(f"{app_id}: unknown category {cat!r}")

        def walk(nodes, where):
            seen = set()
            for f in nodes or []:
                if not isinstance(f, dict):
                    errors.append(f"{where}: field is not an object")
                    continue
                fid = f.get("id")
                label = f.get("label")
                typ = f.get("type")
                if not fid or not label:
                    errors.append(f"{where}: field missing id/label")
                    continue
                if fid in seen:
                    errors.append(f"{app_id}.{fid}: duplicate field id")
                seen.add(fid)
                if typ not in TYPES:
                    errors.append(f"{app_id}.{fid}: unknown type {typ!r}")
                if typ in ("pick", "multi") and not f.get("options"):
                    errors.append(f"{app_id}.{fid}: {typ} needs options")
                if typ == "group":
                    walk(f.get("fields", []), f"{app_id}.{fid}")
                if typ == "repeat":
                    item = f.get("item")
                    if not isinstance(item, dict):
                        errors.append(f"{app_id}.{fid}: repeat needs item")
                    else:
                        walk(item.get("fields", []), f"{app_id}.{fid}")

        walk(app.get("fields", []), app_id)
        if app.get("fieldCount") != field_count(app.get("fields", [])):
            errors.append(f"{app_id}: fieldCount {app.get('fieldCount')} != {field_count(app.get('fields', []))}")
        if not app.get("fields") and not app.get("displayOnly"):
            warnings.append(f"{app_id}: no fields declared")

    # colour-free router
    for app in apps:
        for f in app.get("fields", []) or []:
            for k in COLOR_KEYS & set(f.keys()):
                errors.append(f"{app.get('id')}: field {f.get('id')} carries {k}; colours belong in the separate map")
    for cat, meta in categories.items():
        for k in COLOR_KEYS & set(meta.keys()):
            errors.append(f"category {cat}: carries {k}; colours belong in the separate map")

    # cross links
    for cross in data.get("cross", []):
        src = (cross.get("source") or {}).get("app")
        tgt = (cross.get("target") or {}).get("app")
        if src and src != "*" and src not in ids:
            errors.append(f"cross {cross.get('id')}: unknown source app {src}")
        if tgt and tgt != "*" and tgt not in ids:
            errors.append(f"cross {cross.get('id')}: unknown target app {tgt}")
        for field in (cross.get("target") or {}).get("fields", []) or []:
            if tgt in ids and field not in flatten(ids[tgt].get("fields", [])):
                warnings.append(f"cross {cross.get('id')}: target field {tgt}.{field} not found")

    # pending apps
    for item in data.get("pending", []):
        for app_id in item.get("apps", []) or []:
            if app_id not in ids:
                warnings.append(f"pending {item.get('kind')}: unknown app {app_id}")

    for warning in warnings:
        print(f"warn  {warning}")
    for error in errors:
        print(f"error {error}", file=sys.stderr)

    if errors or (warnings and "--strict" in sys.argv):
        print(f"routing check failed: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"ok: {len(apps)} apps, {len(data.get('cross', []))} cross, {len(data.get('pending', []))} pending, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
