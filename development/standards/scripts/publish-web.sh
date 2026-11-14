#!/usr/bin/env bash
# publish-web.sh — publish flove.org via GitHub Pages (the updaty-web path).
#
# Gitea (origin) tracks the FULL dev workspace; the public web is a FILTERED
# subset of it. This script builds the filtered deploy tree from committed HEAD
# and force-pushes it to floveorg/floveorg.github.io (serves flove.org).
#
# Stripped for the public site (Gitea-only paths):
#   - root build/launcher artifacts, editor/OS noise, python caches
#   - embedded-repo gitlinks (nety) — replaced by its single landing index.html
#   - apk build dirs (flove-apk) — published separately via updaty-apk
#   - development/addons/ (937M, Godot binary > GitHub's 100 MB limit)
#   - submodule content (risa, ama, liberada.net) — published to their own
#     GitHub Pages repos with custom domains via publish-*.sh scripts
# Kept (GitHub keep list): development/skills + standards/skills, decentral/
# web part, development/blog (built output committed in place), package.json / package-lock.json.
# Project subdomain deploys (own repos, own domains):
#   risa → floveorg/risa (risa.liberada.net)
#   ama → floveorg/ama (ama.liberada.net)
#   liberada.net → floveorg/liberada (liberada.net)
#   lowai → LowAiorg/web (lowai.org)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../../.." && pwd)"
GH_REPO="floveorg/floveorg.github.io"
TOKEN_FILE="$HOME/agents/token-github-flove.md"

command -v git >/dev/null || { echo "need 'git'"; exit 1; }

TOKEN=$(grep -oP 'github_pat_\S+|ghp_\S+' "$TOKEN_FILE" 2>/dev/null | head -1)
[ -n "${TOKEN:-}" ] || { echo "no GitHub token in $TOKEN_FILE"; exit 1; }

# Enforce the Solo distro before publishing anything. Hard failures (entry,
# self-containment, single shared-images folder, dead local refs) abort the publish; warnings
# (stale routing / sw.js) are printed but do not block. updaty-web is the quick
# page-push path; the heavy release skill (upgrady) refreshes sw.js and packages.
"$REPO_ROOT/tools/check-distro.sh" || {
  echo "publish aborted: distro check failed" >&2
  exit 1
}

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
rm -rf "$STAGE/apps/flove-apk" "$STAGE/tools/flove-apk"

# development/addons/ (937M, Godot 132 MB > GitHub's 100 MB limit) — Gitea-only.
rm -rf "$STAGE/development/addons"

# nety: embedded repo — the web ships only its landing index.html
rm -rf "$STAGE/decentral/nety"
mkdir -p "$STAGE/decentral/nety"
cp "$REPO_ROOT/decentral/nety/index.html" "$STAGE/decentral/nety/index.html"

# Music apps live only under whole/linguistics/music/. Their short URLs
# (flove.org/frotis, /chacrikun, /electrorchestra) are served by the 404.html
# mote map; never ship duplicate copies at the repo root.
rm -rf "$STAGE/frotis" "$STAGE/chacrikun" "$STAGE/electrorchestra"

# Kept as-is: development/skills, standards/skills, decentral/ web part,
# development/blog (built output committed in place), package.json / package-lock.json.
# Project subdomain deploys are handled by publish-*.sh in each project dir — not here,
# because each has its own GitHub Pages repo with a custom domain.

# Safety: this is a force-push, so anything that exists only on github/main is
# deleted. Refuse to touch the sensitive landing pages when the live branch has
# a version the staged tree does not reproduce (e.g. a page added straight on
# GitHub).
if git -C "$REPO_ROOT" fetch -q github main 2>/dev/null; then
  for f in index.html apps/index.html development/index.html; do
    if git -C "$REPO_ROOT" cat-file -e "github/main:$f" 2>/dev/null; then
      if [ ! -f "$STAGE/$f" ] || ! cmp -s <(git -C "$REPO_ROOT" show "github/main:$f") "$STAGE/$f"; then
        # It differs. That is safe to replace when the live blob is already in
        # local main's history (a normal dev edit). Refuse only when the live
        # version exists ONLY on github/main — e.g. a page added straight on
        # GitHub, which a force-push would silently delete.
        LIVE_BLOB="$(git -C "$REPO_ROOT" rev-parse "github/main:$f")"
        if [ -n "$(git -C "$REPO_ROOT" log -1 --format=%H --find-object="$LIVE_BLOB" main 2>/dev/null)" ]; then
          echo "note: $f changed in dev (live blob is in main history) — updating it."
        else
          echo "refusing to publish: github/main has $f and the staged tree differs." >&2
          echo "  force-push would overwrite a page that exists only on GitHub." >&2
          exit 1
        fi
      fi
    fi
  done
fi

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
