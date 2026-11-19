#!/usr/bin/env python3
"""check-keyboard.py — keyboard walk-through per app (Chrome headless).

For every control the app hands keyboard duties to — a `label[for][tabindex]`,
or a non-button carrying `role=button/menuitem/tab` — the shared harness focuses
it, presses Enter and Space, and expects the delegated handler to fire a click.
Native `<button>`/`<input>` are the browser's job and are skipped.

Usage:
    python3 tools/check-keyboard.py                 # every routing app
    python3 tools/check-keyboard.py --app wisy      # one app
    python3 tools/check-keyboard.py --json out.json
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "development/standards/scripts/keyboard-harness.html"
CHROME = "google-chrome"
RESULT_RE = re.compile(r'<pre id="result">(.*?)</pre>', re.S)

REMOTE = re.compile(r'https?://')
LINK_REMOTE = re.compile(r'<link\b[^>]*href="https?://[^"]*"[^>]*>', re.I)
SRC_REMOTE = re.compile(r'(\bsrc=")https?://[^"]*(")', re.I)
POSTER_REMOTE = re.compile(r'(\bposter=")https?://[^"]*(")', re.I)
CSS_REMOTE = re.compile(r"url\(['\"]?https?://[^)]*\)", re.I)
ANY_REMOTE = re.compile(r'https?://(?!www\.w3\.org/)[^\s"\'<>)]+')


def apps(only: str | None) -> list[tuple[str, Path]]:
    routing = json.loads((ROOT / "tools/routing.json").read_text(encoding="utf-8"))
    out = []
    for app in routing.get("apps", []):
        if only and app.get("id") != only:
            continue
        if not app.get("url", "").startswith("apps/"):
            continue
        path = ROOT / app["url"]
        if path.is_file():
            out.append((app["id"], path))
    return out


def local_copy(path: Path) -> tuple[Path, Path | None]:
    """Remote assets keep `load` pending offline; audit a neutralised sibling."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not REMOTE.search(text):
        return path, None
    cooked = LINK_REMOTE.sub("", text)
    cooked = SRC_REMOTE.sub(r"\1data:,\2", cooked)
    cooked = POSTER_REMOTE.sub(r"\1\2", cooked)
    cooked = CSS_REMOTE.sub("url(data:)", cooked)
    cooked = ANY_REMOTE.sub("data:,", cooked)
    tmp = path.with_name(".__kb-" + path.name)
    tmp.write_text(cooked, encoding="utf-8")
    return tmp, tmp


def run(path: Path) -> tuple[dict | None, str | None]:
    profile = tempfile.mkdtemp()
    try:
        proc = subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--allow-file-access-from-files", "--disable-web-security",
             f"--user-data-dir={profile}", "--virtual-time-budget=12000",
             "--dump-dom", f"{HARNESS.as_uri()}?target={path.as_uri()}"],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout"
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    match = RESULT_RE.search(proc.stdout)
    if not match:
        return None, "no harness output"
    raw = html.unescape(match.group(1)).strip()
    if raw in ("pending", "loaded") or raw.startswith("ERR"):
        return None, raw
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        return None, "unreadable harness output"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app")
    ap.add_argument("--json")
    args = ap.parse_args()

    results, failures = [], 0
    for app_id, path in apps(args.app):
        audit_path, cleanup = local_copy(path)
        try:
            data, error = run(audit_path)
        finally:
            if cleanup is not None:
                cleanup.unlink(missing_ok=True)
        row = {"app": app_id, "error": error, "total": 0, "ok": 0, "fail": []}
        if data:
            row.update(data)
        results.append(row)
        if error:
            print(f"{app_id:14s} {error}", file=sys.stderr)
        else:
            flag = "ok" if not row["fail"] else f"{len(row['fail'])} fail"
            print(f"{app_id:14s} {row['ok']}/{row['total']} {flag}", file=sys.stderr)
            failures += len(row["fail"])
    print(f"\n{len(results)} apps · {failures} keyboard failure(s)", file=sys.stderr)
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
