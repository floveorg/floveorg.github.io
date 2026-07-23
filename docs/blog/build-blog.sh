#!/usr/bin/env bash
# build-blog.sh — the flove blog (Hugo source; repo marc/blog, nested at flove/blog).
# The source of truth for posts + drafts lives HERE in Gitea (private). The built
# HTML is published to GitHub floveorg/blog, which serves https://flove.org/blog/.
# Drafts (draft:true) stay here and are never published.
#
#   ./build-blog.sh serve      # live preview incl. drafts → http://localhost:1313/
#   ./build-blog.sh build      # build ./public (production; drafts excluded)
#   ./build-blog.sh publish    # build + push HTML to floveorg/blog → live at flove.org/blog
#
# New post:  hugo new posts/my-article.md  → starts draft:true. Flip to draft:false to publish.
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
GH_REPO="floveorg/blog"
TOKEN_FILE="$HOME/Claude/token-github-flove.md"

command -v hugo >/dev/null || {
  echo "need 'hugo' (extended) — https://gohugo.io/installation/  (or: snap install hugo --channel=extended)"; exit 1; }

build() { rm -rf "$ROOT/public"; hugo --source "$ROOT" --minify; touch "$ROOT/public/.nojekyll"; }

case "${1:-build}" in
  serve)
    exec hugo server -D --source "$ROOT" ;;
  build)
    build; echo "built $ROOT/public ($(find "$ROOT/public" -type f | wc -l) files)" ;;
  publish)
    TOKEN=$(grep -oP 'github_pat_\S+' "$TOKEN_FILE" 2>/dev/null | head -1)
    [ -n "${TOKEN:-}" ] || { echo "no GitHub token in $TOKEN_FILE"; exit 1; }
    build
    # Push the built output as a fresh single commit to floveorg/blog (deploy repo).
    ( cd "$ROOT/public"
      git init -q -b main
      git add -A
      git -c user.name='Marc' -c user.email='marc@futbolia.org' commit -q -m "publish built blog"
      git push -f "https://x-access-token:${TOKEN}@github.com/${GH_REPO}.git" main >/dev/null
      rm -rf .git )
    echo "published → https://flove.org/blog/  (via $GH_REPO)" ;;
  *)
    echo "usage: build-blog.sh [serve|build|publish]"; exit 1 ;;
esac
