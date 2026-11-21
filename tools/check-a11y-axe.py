#!/usr/bin/env python3
"""check-a11y-axe.py — real axe-core audit per app (Chrome headless).

Runs the shared harness (tools/dev/a11y-harness.html) once
per routing app and collects axe violations. This is the A11Y02 pass: the
static checks in check-a11y.py stay the cheap gate; this one needs a browser.

Usage:
    python3 tools/check-a11y-axe.py                 # every routing app
    python3 tools/check-a11y-axe.py --app goddy     # one app
    python3 tools/check-a11y-axe.py --md report.md  # write a Markdown report
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
HARNESS = ROOT / "tools/dev/a11y-harness.html"
CHROME = "google-chrome"
RESULT_RE = re.compile(r'<pre id="result">(.*?)</pre>', re.S)


def apps(only: str | None) -> list[tuple[str, Path]]:
    routing = json.loads((ROOT / "tools/routing.json").read_text(encoding="utf-8"))
    out = []
    for app in routing.get("apps", []):
        if only and app.get("id") != only:
            continue
        if not app.get("url", "").startswith("apps/"):
            continue          # flove apps only; project sites are out of scope
        path = ROOT / app["url"]
        if path.is_file():
            out.append((app["id"], path))
    return out


def run(app_id: str, path: Path) -> tuple[list[dict], str | None]:
    target = path.as_uri()
    profile = tempfile.mkdtemp()
    try:
        proc = subprocess.run(
            [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--allow-file-access-from-files", "--disable-web-security",
             f"--user-data-dir={profile}", "--virtual-time-budget=15000",
             "--dump-dom", f"{HARNESS.as_uri()}?target={target}"],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return [], "timeout"
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    match = RESULT_RE.search(proc.stdout)
    if not match:
        return [], "no harness output"
    raw = html.unescape(match.group(1)).strip()
    if raw == "pending" or raw.startswith("ERR"):
        return [], raw
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        return [], "unreadable harness output"



REMOTE = re.compile(r'https?://')
LINK_REMOTE = re.compile(r'<link\b[^>]*href="https?://[^"]*"[^>]*>', re.I)
SRC_REMOTE = re.compile(r'(\bsrc=")https?://[^"]*(")', re.I)
POSTER_REMOTE = re.compile(r'(\bposter=")https?://[^"]*(")', re.I)
CSS_REMOTE = re.compile(r"url\(['\"]?https?://[^)]*\)", re.I)
ANY_REMOTE = re.compile(r'https?://(?!www\.w3\.org/)[^\s"\'<>)]+')


def local_copy(path: Path) -> tuple[Path, Path | None]:
    """Pages that pull remote stylesheets or images keep `load` pending offline,
    so the harness never injects axe. Audit a sibling copy with those requests
    neutralised; local assets and all markup stay as they are."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not REMOTE.search(text):
        return path, None
    cooked = LINK_REMOTE.sub("", text)
    cooked = SRC_REMOTE.sub(r"\1data:,\2", cooked)
    cooked = POSTER_REMOTE.sub(r"\1\2", cooked)
    cooked = CSS_REMOTE.sub("url(data:)", cooked)
    cooked = ANY_REMOTE.sub("data:,", cooked)
    tmp = path.with_name(".__a11y-" + path.name)
    tmp.write_text(cooked, encoding="utf-8")
    return tmp, tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app")
    ap.add_argument("--md")
    ap.add_argument("--json")
    args = ap.parse_args()

    results = []
    for app_id, path in apps(args.app):
        audit_path, cleanup = local_copy(path)
        try:
            violations, error = run(app_id, audit_path)
        finally:
            if cleanup is not None:
                cleanup.unlink(missing_ok=True)
        results.append({"app": app_id, "violations": violations,
                        "error": error,
                        "nodes": sum(v["nodes"] for v in violations)})
        flag = error or f"{len(violations)} rules / {results[-1]['nodes']} nodes"
        print(f"{app_id:14s} {flag}", file=sys.stderr)

    ok = [r for r in results if not r.get("error")]
    skipped = [r["app"] for r in results if r.get("error")]
    total = sum(r["nodes"] for r in ok)
    print(f"\n{len(ok)} apps · {total} violation nodes"
          + (f" · skipped: {', '.join(skipped)}" if skipped else ""), file=sys.stderr)

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")
    if args.md:
        counts: dict[str, dict] = {}
        for r in ok:
            for v in r["violations"]:
                c = counts.setdefault(v["id"], {"rule": v["id"], "impact": v["impact"],
                                                "help": v["help"], "nodes": 0, "apps": set()})
                c["nodes"] += v["nodes"]
                c["apps"].add(r["app"])
        lines = [f"# Accessibility — axe-core audit ({len(ok)} apps)", "",
                 "Regenerate: `python3 tools/check-a11y-axe.py --md development/wiki/work/a11y-report.md`. "
                 "Chrome headless + axe 4.10.2; the static gate stays `tools/check-a11y.py`.", "",
                 f"{total} violation nodes across {len(counts)} rules."
                 + (f" Skipped (timeout): {', '.join(skipped)}." if skipped else "")]
        if counts:
            lines += ["", "| rule | impact | nodes | apps | help |", "|---|---|---:|---:|---|"]
            for c in sorted(counts.values(), key=lambda c: -c["nodes"]):
                lines.append(f"| `{c['rule']}` | {c['impact']} | {c['nodes']} | "
                             f"{len(c['apps'])} | {c['help']} |")
        Path(args.md).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"report → {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
