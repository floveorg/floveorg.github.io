#!/usr/bin/env bash
# publish-ama.sh — publish projects/liberada/ama → GitHub floveorg/ama → ama.liberada.net.
#
# Source of truth = flove/projects/liberada/ama (you edit it here, in the flove
# repo). This script syncs the folder's content into floveorg/ama, PRESERVING the
# repo's meta (CNAME, .github, README.md, .gitignore) and skipping this script itself,
# then commits + pushes. GitHub Pages serves it at ama.liberada.net.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../../.." && pwd)"
SRC="$REPO_ROOT/projects/liberada/ama"
TOKEN=$(grep -oP 'github_pat_\S+|ghp_\S+' "$HOME/agents/token-github-ama.md" 2>/dev/null | head -1)
[ -n "${TOKEN:-}" ] || { echo "no GitHub token in ~/agents/token-github-ama.md"; exit 1; }
command -v rsync >/dev/null || { echo "need 'rsync'"; exit 1; }
[ -d "$SRC" ] || { echo "no existe $SRC"; exit 1; }

STAGE="$(mktemp -d)"
git clone -q "https://x-access-token:${TOKEN}@github.com/floveorg/ama.git" "$STAGE"

rsync -a --delete \
  --exclude='.git' --exclude='.github/' --exclude='CNAME' --exclude='README.md' --exclude='.gitignore' \
  --exclude='publish-ama.sh' \
  "$SRC/" "$STAGE/"

cd "$STAGE"
git add -A
if git diff --cached --quiet; then
  echo "ama: sin cambios que publicar"
else
  git -c user.name='Marc' -c user.email='marc@futbolia.org' commit -q -m "publish ama from flove/projects/liberada/ama"
  git push -q origin main
  echo "published → ama.liberada.net (floveorg/ama)"
fi
rm -rf "$STAGE"
