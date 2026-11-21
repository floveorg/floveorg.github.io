#!/usr/bin/env python3
"""Static check for the flove-portrait/1 protocol surface.

Verifies that every app in tools/routing.json that has a source file carries the
common storage/net layer and its embedded flove-fields manifest, and that the
reference adapter (Souls) exposes the full portrait API.

Usage: python3 tools/dev/check-portrait-protocol.py
Exit 0 = ok, 1 = missing pieces.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROUTING = os.path.join(ROOT, "tools", "routing.json")

COMMON = ["window.floveStore", "window.floveFields", "flove-fields"]
ADAPTER = ["window.flovePortrait", "window.flovePort", "validatePortrait", "consult(", "merge(", "selfTest"]
# Apps whose routing URL is a field-source variant; the adapter lives in the runnable file.
RUNNABLE = {"keys": "apps/puzzy/keys/keys-advanced.html"}


def main():
    with open(ROUTING, encoding="utf-8") as fh:
        routing = json.load(fh)
    errors = []
    checked = 0
    for app in routing.get("apps", []):
        url = app.get("url") or ""
        if not url:
            continue
        path = os.path.join(ROOT, url)
        if not os.path.exists(path):
            continue
        checked += 1
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        for token in COMMON:
            if token not in text:
                errors.append(f"{app['id']}: missing {token}")
        if app["id"] in ("souls", "goddy", "realy", "inventary", "myfamily", "pracsys", "keys", "crafty", "worthing", "lovy"):
            adapter_text = text
            if app["id"] in RUNNABLE:
                with open(os.path.join(ROOT, RUNNABLE[app["id"]]), encoding="utf-8", errors="ignore") as af:
                    adapter_text = af.read()
            for token in ADAPTER:
                if token not in adapter_text:
                    errors.append(f"{app['id']}: missing {token}")
        if app["id"] == "souls":
            m = re.search(
                r'<script[^>]*id="flove-fields"[^>]*>(.*?)</script>', text, re.S
            )
            if not m:
                errors.append("souls: no flove-fields JSON block")
            else:
                try:
                    data = json.loads(m.group(1))
                    if not isinstance(data.get("fields"), list) or not data["fields"]:
                        errors.append("souls: flove-fields has no fields")
                except Exception as exc:
                    errors.append(f"souls: invalid flove-fields JSON ({exc})")
    print(f"checked {checked} app files")
    if errors:
        for e in errors:
            print("  -", e)
        print(f"FAIL: {len(errors)} missing protocol piece(s)")
        return 1
    print("ok: portrait protocol surface present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
