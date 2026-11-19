#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract embedded app field manifests into tools/routing.json.

Every self-contained app can declare its full field tree in an inert JSON
script:

    <script type="application/json" id="flove-fields">
    {"schema":"flove-fields/1","app":"goddy","status":"complete","fields":[...]}
    </script>

The manifest is part of the app (no external file, no runtime dependency).
This extractor scans apps/**/*.html, validates each manifest, and copies its
fields / status / fieldCount into the matching routing.json app.

Usage:
  python3 tools/extract-fields.py            # report only
  python3 tools/extract-fields.py --apply    # write routing.json
  python3 tools/extract-fields.py --check    # exit 1 if routing is stale
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTING = os.path.join(ROOT, "tools", "routing.json")
APP_ROOTS = [os.path.join(ROOT, "apps"), os.path.join(ROOT, "central", "apps"),
              os.path.join(ROOT, "decentral"), os.path.join(ROOT, "development", "standards", "skills")]

MANIFEST_RE = re.compile(
    r'<script[^>]*\bid=["\']flove-fields["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
TYPES = {"text", "text[]", "number", "file", "date", "time", "boolean", "pick", "multi", "unknown", "group", "repeat"}


def field_count(nodes: list) -> int:
    n = 0
    for f in nodes:
        t = f.get("type")
        if t == "repeat":
            mult = f.get("max") or f.get("min") or 1
            n += mult * field_count(f.get("item", {}).get("fields", []))
        elif t == "group":
            n += field_count(f.get("fields", []))
        else:
            n += 1
    return n


def validate_puzzy(pz, where: str) -> None:
    """Validate the optional `puzzy` annotability block (standards/puzzy.md §8.13.1).

    Absent means not annotable. The block is copied verbatim into routing.json so
    downstream consumers (questy, appy) can read it; this gate keeps typos from
    becoming silent drift.
    """
    if pz is None:
        return
    if not isinstance(pz, dict):
        raise ValueError(f"{where}.puzzy: must be an object")
    for key in ("annotate", "free", "auto"):
        if key in pz and not isinstance(pz[key], bool):
            raise ValueError(f"{where}.puzzy.{key}: must be a boolean")
    if pz.get("auto"):
        raise ValueError(f"{where}.puzzy.auto: reserved — must be false in flove-puzzy/1")
    if "free" in pz and "annotate" not in pz:
        raise ValueError(f"{where}.puzzy: `free` is only meaningful with `annotate`")
    kinds = pz.get("kinds")
    if kinds is not None:
        if not isinstance(kinds, list) or not all(isinstance(k, str) for k in kinds):
            raise ValueError(f"{where}.puzzy.kinds: must be an array of strings")
        allowed = {"word", "concept", "act", "person", "app", "place", "frame"}
        bad = sorted(set(kinds) - allowed)
        if bad:
            raise ValueError(f"{where}.puzzy.kinds: unknown {bad}")


def validate(nodes: list, where: str) -> None:
    if not isinstance(nodes, list):
        raise ValueError(f"{where}: fields must be an array")
    if not nodes:
        return
    seen = set()
    for f in nodes:
        if not isinstance(f, dict):
            raise ValueError(f"{where}: field is not an object")
        fid, label, typ = f.get("id"), f.get("label"), f.get("type")
        if not fid or not label:
            raise ValueError(f"{where}: field missing id/label: {f!r}")
        if fid in seen:
            raise ValueError(f"{where}: duplicate field id {fid!r}")
        seen.add(fid)
        if typ not in TYPES:
            raise ValueError(f"{where}.{fid}: unknown type {typ!r}")
        validate_puzzy(f.get("puzzy"), f"{where}.{fid}")
        if typ in ("pick", "multi"):
            opts = f.get("options")
            if not isinstance(opts, list) or not opts:
                raise ValueError(f"{where}.{fid}: {typ} needs options")
        if typ == "group":
            validate(f.get("fields", []), f"{where}.{fid}")
        if typ == "repeat":
            item = f.get("item")
            if not isinstance(item, dict):
                raise ValueError(f"{where}.{fid}: repeat needs item")
            validate(item.get("fields", []), f"{where}.{fid}.item")


def app_dirs(routing: dict) -> list[str]:
    """Directories that hold a routed app — a manifest can live outside the main roots
    (repo-root stubs, `projects/…`, a skill folder)."""
    dirs = set(APP_ROOTS)
    for app in routing.get("apps", []):
        url = app.get("url") or ""
        if url and os.path.exists(os.path.join(ROOT, url)):
            dirs.add(os.path.join(ROOT, os.path.dirname(url)))
    # drop any root nested inside another, or its files would be scanned twice
    kept = []
    for d in sorted(dirs):
        if not any(d == k or d.startswith(k + os.sep) for k in kept):
            kept.append(d)
    return kept


def manifests(routing: dict | None = None) -> list[tuple[str, dict]]:
    found = []
    for root in app_dirs(routing or {}):
      for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git"}]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            match = MANIFEST_RE.search(text)
            if not match:
                continue
            rel = os.path.relpath(path, ROOT)
            try:
                data = json.loads(match.group(1))
            except Exception as exc:  # noqa: BLE001
                raise ValueError(f"{rel}: invalid manifest JSON: {exc}") from exc
            if data.get("schema") != "flove-fields/1":
                raise ValueError(f"{rel}: schema must be flove-fields/1")
            if not data.get("app"):
                raise ValueError(f"{rel}: manifest missing app id")
            validate(data.get("fields", []), rel)
            found.append((rel, data))
    return found


def apply_manifest(routing: dict, rel: str, data: dict) -> None:
    app_id = data["app"]
    app = next((a for a in routing.get("apps", []) if a.get("id") == app_id), None)
    if not app:
        raise ValueError(f"{rel}: app {app_id!r} is not in routing.json")
    app["fields"] = data["fields"]
    app["fieldCount"] = field_count(data["fields"])
    app["status"] = data.get("status", "complete")
    app["fieldsSource"] = rel
    if data.get("displayOnly"):
        app["displayOnly"] = True
    else:
        app.pop("displayOnly", None)


def main() -> int:
    routing = json.load(open(ROUTING, encoding="utf-8"))
    found = manifests(routing)
    routed = {a["id"]: a for a in routing.get("apps", [])}
    by_app = {}
    for rel, data in found:
        if data["app"] in by_app:
            # Two files declare the same app (e.g. an app moved and the old copy kept
            # its manifest). The one routing points at wins; the other is left alone.
            keep = by_app[data["app"]]
            url = (routed.get(data["app"]) or {}).get("url") or ""
            if rel == url and keep != url:
                print(f"  note  {data['app']}: using {rel} (routing URL); {keep} is stale")
                by_app[data["app"]] = rel
                apply_manifest(routing, rel, data)
            else:
                print(f"  note  {data['app']}: ignoring stale manifest in {rel}")
            continue
        by_app[data["app"]] = rel
        apply_manifest(routing, rel, data)

    routed = {a["id"]: a for a in routing.get("apps", [])}
    missing = sorted(set(routed) - set(by_app))
    unknown = sorted(set(by_app) - set(routed))
    for app_id in missing:
        print(f"  warn  {app_id}: no flove-fields manifest ({routed[app_id].get('url')})")
    for app_id in unknown:
        print(f"  warn  {app_id}: manifest has no routing entry")

    text = json.dumps(routing, ensure_ascii=False, indent=2) + "\n"
    if "--apply" in sys.argv:
        open(ROUTING, "w", encoding="utf-8").write(text)
        print(f"wrote {os.path.relpath(ROUTING, ROOT)} ({len(found)} manifests)")
        return 0
    if "--check" in sys.argv:
        current = open(ROUTING, encoding="utf-8").read()
        if current != text:
            print("routing.json is stale — run tools/extract-fields.py --apply", file=sys.stderr)
            return 1
        print(f"ok: {len(found)} manifests match routing.json")
        return 0

    print(f"{len(found)} manifests found; run --apply to write routing.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
