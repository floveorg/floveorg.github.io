#!/usr/bin/env bash
# publish-risa.sh — publish projects/liberada/risa → GitHub floveorg/risa → risa.liberada.net.
#
# Source of truth = flove/projects/liberada/risa (you edit it here, in the flove
# repo). This script syncs the folder's content into floveorg/risa, PRESERVING the
# repo's meta (CNAME, .github, README.md, .gitignore) and skipping this script itself,
# then commits + pushes. GitHub Pages serves it at risa.liberada.net.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/../../.." && pwd)"
SRC="$REPO_ROOT/projects/liberada/risa"
TOKEN=$(grep -oP 'github_pat_\S+|ghp_\S+' "$HOME/agents/token-github-risa.md" 2>/dev/null | head -1)
[ -n "${TOKEN:-}" ] || { echo "no GitHub token in ~/agents/token-github-risa.md"; exit 1; }
command -v rsync >/dev/null || { echo "need 'rsync'"; exit 1; }
[ -d "$SRC" ] || { echo "no existe $SRC"; exit 1; }

STAGE="$(mktemp -d)"
git clone -q "https://x-access-token:${TOKEN}@github.com/floveorg/risa.git" "$STAGE"

rsync -a --delete \
  --exclude='.git' --exclude='.github/' --exclude='CNAME' --exclude='README.md' --exclude='.gitignore' \
  --exclude='publish-risa.sh' \
  "$SRC/" "$STAGE/"

cd "$STAGE"
git add -A
if git diff --cached --quiet; then
  echo "risa: sin cambios que publicar"
else
  git -c user.name='Marc' -c user.email='marc@futbolia.org' commit -q -m "publish risa from flove/projects/liberada/risa"
  git push -q origin main
  echo "published → risa.liberada.net (floveorg/risa)"
fi
rm -rf "$STAGE"
