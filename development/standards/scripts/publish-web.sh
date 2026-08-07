#!/usr/bin/env bash
# publish-web.sh — publish flove.org via GitHub Pages (the updaty-web path).
#
# Gitea (origin) tracks the FULL dev workspace; the public web is a FILTERED
# subset of it. This script builds the filtered deploy tree from committed HEAD
# and force-pushes it to floveorg/floveorg.github.io (serves flove.org).
#
# Stripped for the public site (Gitea-only paths):
#   - root build/launcher artifacts, editor/OS noise, python caches (1-10)
#   - embedded-repo gitlinks (nety) — replaced by its single landing index.html
#   - apk build dirs (flove-apk) — published separately via updaty-apk
#   - development/addons/ (Gitea-only, 937M): Godot binary is 132 MB, over
#     GitHub's 100 MB per-file push limit, so addons never leaves Gitea.
# Kept (GitHub keep list): development/skills + standards/skills, decentral/
# web part, development/blog (built output committed in place), package.json / package-lock.json.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../../.." && pwd)"
GH_REPO="floveorg/floveorg.github.io"
TOKEN_FILE="$HOME/agents/token-github-flove.md"

command -v git >/dev/null || { echo "need 'git'"; exit 1; }

TOKEN=$(grep -oP 'github_pat_\S+|ghp_\S+' "$TOKEN_FILE" 2>/dev/null | head -1)
[ -n "${TOKEN:-}" ] || { echo "no GitHub token in $TOKEN_FILE"; exit 1; }

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# The tracked tree at HEAD (mirrors Gitea), then strip the Gitea-only paths.
git -C "$REPO_ROOT" archive --format=tar HEAD | tar -x -C "$STAGE"

# Root build / launcher artifacts
rm -rf "$STAGE/public"
rm -f  "$STAGE/.hugo_build.lock"
rm -f  "$STAGE/start-flove.sh" "$STAGE/flove-localhost.desktop"

# Editor / OS noise + python caches
find "$STAGE" -name .DS_Store -o -name Thumbs.db -o -name '*.swp' -o -name '*.swo' \
     -o -name '*.kate-swp' -o -name '*.log' | xargs -r rm -f
find "$STAGE" -type d \( -name .idea -o -name .vscode -o -name __pycache__ \) -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" -name '*.pyc' -delete 2>/dev/null || true

# APK builds (published separately via updaty-apk)
rm -rf "$STAGE/solo/apps/flove-apk" "$STAGE/solo/flove-apk"

# development/addons/ (937M, Godot 132 MB > GitHub's 100 MB limit) — Gitea-only.
rm -rf "$STAGE/development/addons"

# nety: embedded repo — the web ships only its landing index.html
rm -rf "$STAGE/decentral/nety"
mkdir -p "$STAGE/decentral/nety"
cp "$REPO_ROOT/decentral/nety/index.html" "$STAGE/decentral/nety/index.html"

# Kept as-is: development/skills, standards/skills, decentral/ web part,
# development/blog (built output committed in place), package.json / package-lock.json.

( cd "$STAGE"
  git init -q -b main
  git add -A
  git -c user.name='Marc' -c user.email='marc@futbolia.org' commit -q -m "publish flove.org (filtered from flove main)"
  # Large filtered tree → GitHub's dumb-HTTP can 408 on the plain push; bump the
  # post buffer, force HTTP/1.1 and skip pack compression so the upload lands.
  git -c http.postBuffer=2147483648 -c http.version=HTTP/1.1 \
      -c core.compression=0 -c pack.compression=0 \
      push -f "https://x-access-token:${TOKEN}@github.com/${GH_REPO}.git" main >/dev/null )

echo "published → https://flove.org/ (via $GH_REPO, filtered)"
