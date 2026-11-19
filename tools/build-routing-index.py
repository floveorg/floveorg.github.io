#!/usr/bin/env python3
"""Build a flat, colour-free index of routing fields for consumers.

The authored source stays tools/routing.json. This read model makes it easy to
combine fields across apps without walking every tree:

  tools/routing-index.json

It intentionally carries no colours (pending). Use it for lookups, cross links,
field pickers and future database import.

Usage:
  python3 tools/build-routing-index.py            # write the index
  python3 tools/build-routing-index.py --check    # exit 1 if stale
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "tools" / "routing.json"
INDEX = ROOT / "tools" / "routing-index.json"


def flatten(app, nodes, parent=""):
    out = []
    for f in nodes or []:
        if not isinstance(f, dict) or not f.get("id"):
            continue
        fid = str(f["id"])
        path = fid if not parent or fid.startswith(parent + ".") else parent + "." + fid
        item = {
            "app": app.get("id"),
            "appName": app.get("name"),
            "category": app.get("category"),
            "path": path,
            "id": fid,
            "label": f.get("label", ""),
            "type": f.get("type", ""),
            "parent": parent or None,
        }
        if f.get("options"):
            item["options"] = f["options"]
        out.append(item)
        if f.get("type") == "group":
            out += flatten(app, f.get("fields", []), path)
        if f.get("type") == "repeat":
            out += flatten(app, (f.get("item") or {}).get("fields", []), path)
    return out


def build():
    raw = ROUTING.read_bytes()
    data = json.loads(raw)
    fields = []
    for app in data.get("apps", []):
        fields += flatten(app, app.get("fields", []))
    fields.sort(key=lambda x: (x["app"] or "", x["path"] or ""))
    return {
        "schema": "flove-routing-index/1",
        "source": "tools/routing.json",
        "sourceVersion": data.get("version"),
        "sourceHash": hashlib.sha256(raw).hexdigest(),
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "colors": "pending",
        "count": len(fields),
        "fields": fields,
    }


def main() -> int:
    index = build()
    text = json.dumps(index, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if "--check" in sys.argv:
        if not INDEX.exists():
            print("routing-index.json is missing — run tools/build-routing-index.py", file=sys.stderr)
            return 1
        current = INDEX.read_text(encoding="utf-8")
        # generatedAt is not part of freshness; compare the substantive payload.
        try:
            a = json.loads(current)
            b = json.loads(text)
            a.pop("generatedAt", None)
            b.pop("generatedAt", None)
            if a != b:
                print("routing-index.json is stale — run tools/build-routing-index.py", file=sys.stderr)
                return 1
        except Exception:
            print("routing-index.json is invalid — run tools/build-routing-index.py", file=sys.stderr)
            return 1
        print(f"ok: routing-index.json matches {index['count']} fields")
        return 0
    INDEX.write_text(text, encoding="utf-8")
    print(f"wrote tools/routing-index.json ({index['count']} fields)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
