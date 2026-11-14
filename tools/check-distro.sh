#!/usr/bin/env bash
# check-distro.sh — the single localhost-distro gate.
#
# Run before committing or publishing:
#   tools/check-distro.sh            report; exit 1 on hard breakage
#   tools/check-distro.sh --strict   warnings also fail
#   tools/check-distro.sh --build    also rebuild the downloadable zip
#
# Hard checks (always fail):
#   1. entry pages exist (root index, tools/start.html, manifest, apps/index.html)
#   2. no apps/shared code tree and no page points at shared css/js
#   2b. no root-absolute internal links (they break in the package / a subpath)
#   3. shared images live only in central/shared/media/images (no images/ mirror)
#   4. every local href/src resolves (known unbuilt apps allowlisted)
#   7. every skill's YAML frontmatter parses and has name/description
# Soft checks (warn; fail under --strict):
#   5. routing.json parses and its entry count is reported against app pages
#   6. sw.js matches the tracked tree (must be regenerated after a commit)
set -uo pipefail

HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
APPS="$ROOT/apps"
IMAGES="$ROOT/images"
TOOLS="$HERE"
IMAGES_SRC="$ROOT/central/shared/media/images"

STRICT=0
BUILD=0
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    --build)  BUILD=1 ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

FAIL=0
WARN=0
ok()   { printf '  \033[32mok\033[0m   %s\n' "$*"; }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$*"; FAIL=$((FAIL+1)); }
warn() { printf '  \033[33mwarn\033[0m %s\n' "$*"; WARN=$((WARN+1)); }

echo "🌱 localhost distro check — apps/ + tools/"

# ── 1. entry pages ─────────────────────────────────────────────────────────
echo "· entry"
for f in "$ROOT/index.html" "$TOOLS/start.html" "$TOOLS/manifest.webmanifest" "$APPS/index.html"; do
  [ -f "$f" ] && ok "present: ${f#$ROOT/}" || bad "missing: ${f#$ROOT/}"
done
if [ -f "$TOOLS/manifest.webmanifest" ]; then
  START_URL=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("start_url",""))' "$TOOLS/manifest.webmanifest" 2>/dev/null || true)
  TARGET="${START_URL%%[?#]*}"
  case "$TARGET" in
    /*) [ -f "$ROOT$TARGET" ] && ok "manifest start_url resolves: $START_URL" || bad "manifest start_url unresolved: $START_URL" ;;
    *)  [ -f "$TOOLS/$TARGET" ] && ok "manifest start_url resolves: $START_URL" || bad "manifest start_url unresolved: $START_URL" ;;
  esac
fi

# ── 2. self-contained apps ─────────────────────────────────────────────────
echo "· self-contained code"
if [ -d "$APPS/shared" ]; then
  bad "apps/shared exists — Solo pages must inline their CSS/JS (no shared code tree)"
else
  ok "no apps/shared code tree"
fi
SHARED_REFS=$(grep -rlaE '(src|href)="[^"]*(shared/(css|js)|\.\./shared/)' "$APPS" "$TOOLS" --include='*.html' 2>/dev/null || true)
if [ -n "$SHARED_REFS" ]; then
  bad "page(s) still call shared css/js:"
  printf '         %s\n' $SHARED_REFS
else
  ok "no page calls shared css/js"
fi

# ── 2b. portable links ─────────────────────────────────────────────────────
# A root-absolute internal link (/foo) works at the site root but not under a
# GitHub/Gitea Pages subpath (and is needlessly fragile in the package).
echo "· portable links"
ABS=$(grep -rnaE '(href|src)="/[^/]' "$APPS" "$TOOLS" --include='*.html' 2>/dev/null || true)
if [ -n "$ABS" ]; then
  bad "root-absolute internal link(s) — these break under a subpath:"
  printf '         %s\n' "$(printf '%s\n' "$ABS" | head -10)"
else
  ok "no root-absolute internal links"
fi

# ── 3. shared images (single canonical folder) ─────────────────────────────
echo "· shared images"
if [ -d "$IMAGES_SRC" ]; then
  ok "central/shared/media/images present ($(find "$IMAGES_SRC" -type f | wc -l) files)"
else
  bad "missing source: ${IMAGES_SRC#$ROOT/}"
fi
if [ -e "$IMAGES" ]; then
  bad "duplicate images/ folder exists — the canonical artwork lives only in central/shared/media/images"
else
  ok "no duplicate images/ mirror"
fi

# ── 4. local references ────────────────────────────────────────────────────
echo "· local references"
python3 - "$ROOT" "$APPS" "$TOOLS" <<'PY'
import os, re, sys, html
from collections import Counter

root, apps, tools = sys.argv[1:4]
# Apps not built yet — intentionally allowed until they are imported or hidden
# (owner decision, 2026-11-08). Keys are the URL strings as written.
KNOWN = {
    'wizardry.html',
    '../apps/hoty.html',
    'boty.html',
    'loves.html',
    'fuga/index.html',
    'clauses.html',
    'ranks/',
}
SPAN = re.compile(r'<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>', re.S | re.I)
REF  = re.compile(r'(?:href|src)="([^"#?]+)')

bad = []
for base in (apps, tools):
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git')]
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dirpath, f)
            s = open(p, encoding='utf-8', errors='ignore').read()
            spans = [m.span() for m in SPAN.finditer(s)]
            for m in REF.finditer(s):
                i = m.start()
                if any(a <= i < b for a, b in spans):
                    continue
                u = html.unescape(m.group(1)).strip()
                if not u or u.startswith(('http', 'mailto:', 'data:', 'javascript:', '//', 'tel:', '/')):
                    continue
                if '${' in u or "'+" in u or '{{' in u:
                    continue
                if u.endswith(('.zip', '.mp4')):   # per-app zips + stripped audio: planned
                    continue
                up = os.path.normpath(os.path.join(os.path.dirname(p), u))
                if not os.path.exists(up):
                    bad.append((os.path.relpath(p, root), u))

known = [x for x in bad if x[1] in KNOWN]
new   = [x for x in bad if x[1] not in KNOWN]
if known:
    c = Counter(u for _, u in known)
    print(f"  ok   known unbuilt-app links allowed: {len(known)} "
          f"({', '.join(f'{u}×{n}' for u, n in c.items())})")
if new:
    print(f"  \033[31mFAIL\033[0m {len(new)} new dead local reference(s):")
    for p, u in new:
        print(f"         {p} -> {u}")
    sys.exit(1)
print("  ok   every other local href/src resolves")
PY
[ $? -ne 0 ] && FAIL=$((FAIL+1))

# ── 5. routing ─────────────────────────────────────────────────────────────
echo "· routing"
if [ -f "$TOOLS/routing.json" ]; then
  ROUTING=$(python3 - "$TOOLS/routing.json" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    print(len(d.get('apps', [])), len(d.get('cross', {})))
except Exception as e:
    print('ERR', e)
PY
)
  case "$ROUTING" in
    ERR*) bad "routing.json does not parse: ${ROUTING#ERR }" ;;
    *)
      set -- $ROUTING; ENTRIES=$1; CROSS=$2
      PAGES=$(find "$APPS" -name '*.html' \
                -not -path '*/new/*' -not -path '*/dev/*' \
                -not -name 'index.html' | wc -l)
      if [ "$ENTRIES" -ge "$PAGES" ]; then
        ok "routing.json covers $ENTRIES app entries ($PAGES app pages, cross=$CROSS)"
      else
        warn "routing.json has $ENTRIES app entries for $PAGES app pages (stale registry)"
      fi
      ;;
  esac
else
  bad "missing: tools/routing.json"
fi

# ── 6. service worker ──────────────────────────────────────────────────────
echo "· service worker"
if command -v node >/dev/null; then
  SWLOG=$(mktemp)
  if node "$TOOLS/build-sw.mjs" --check >"$SWLOG" 2>&1; then
    ok "$(tail -1 "$SWLOG")"
  else
    warn "$(tail -1 "$SWLOG")"
  fi
  rm -f "$SWLOG"
else
  warn "node not installed — cannot verify sw.js"
fi
if git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  DIRTY=$(git -C "$ROOT" status --porcelain -- apps central/shared/media/images tools sw.js index.html | wc -l)
  if [ "$DIRTY" -gt 0 ]; then
    warn "$DIRTY uncommitted path(s) under apps/, central/shared/media/images, tools/ or sw.js — commit; the heavy upgrady release refreshes sw.js"
  else
    ok "distro working tree clean"
  fi
fi

# ── 7. skills frontmatter ──────────────────────────────────────────────────
echo "· skills frontmatter"
if python3 -c 'import yaml' 2>/dev/null; then
  SKILLOG=$(mktemp)
  if python3 "$TOOLS/check-skills.py" >"$SKILLOG" 2>&1; then
    ok "$(grep -E 'skills in' "$SKILLOG" | head -1)"
  else
    bad "check-skills.py found errors"
    grep -E 'ERROR|WARN' "$SKILLOG" | head -10
  fi
  rm -f "$SKILLOG"
else
  warn "PyYAML not installed — skills frontmatter check skipped"
fi

# ── 8. optional package build ──────────────────────────────────────────────
if [ "$BUILD" -eq 1 ]; then
  echo "· package build"
  ZIPLOG=$(mktemp)
  if bash "$TOOLS/build-flove-zip.sh" >"$ZIPLOG" 2>&1; then
    ok "$(tail -1 "$ZIPLOG")"
  else
    bad "build-flove-zip.sh failed"
    tail -5 "$ZIPLOG"
  fi
  rm -f "$ZIPLOG"
fi

# ── summary ────────────────────────────────────────────────────────────────
echo
if [ "$FAIL" -gt 0 ]; then
  echo "🌱 distro check FAILED — $FAIL hard error(s), $WARN warning(s)"
  exit 1
fi
if [ "$STRICT" -eq 1 ] && [ "$WARN" -gt 0 ]; then
  echo "🌱 distro check FAILED (--strict) — $WARN warning(s)"
  exit 1
fi
echo "🌱 distro check passed — 0 hard errors, $WARN warning(s)"
