#!/usr/bin/env bash
# build-blog.sh — the flove blog (Hugo source, flove repo: development/blog).
# The built HTML is committed INTO this directory's root (no /public segment)
# and ships with the main site via publish-web.sh → https://flove.org/development/blog/.
# Drafts (draft:true) stay here and are never built.
#
#   ./build-blog.sh serve      # live preview incl. drafts → http://localhost:1313/
#   ./build-blog.sh build      # build in place (production; drafts excluded)
#   ./build-blog.sh publish    # build + commit + push Gitea + publish-web.sh → live
#
# New post:  hugo new posts/my-article.md  → starts draft:true. Flip to draft:false to publish.
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"

command -v hugo >/dev/null || {
  echo "need 'hugo' (extended) — https://gohugo.io/installation/  (or: snap install hugo --channel=extended)"; exit 1; }

# Build into a temp dir, then rsync into $ROOT --delete, protecting the source
# files (content/, layouts/, themes/, archetypes/, config, scripts, README).
# 'public' is gone: the blog's own directory is the publish root.
build() {
  local tmp
  tmp="$(mktemp -d)"
  hugo --source "$ROOT" --destination "$tmp" --minify
  touch "$tmp/.nojekyll"
  rsync -a --delete "$tmp/" "$ROOT/" \
    --exclude 'content' --exclude 'layouts' --exclude 'themes' \
    --exclude 'archetypes' --exclude 'hugo.toml' --exclude 'build-blog.sh' \
    --exclude 'README.md' --exclude '.gitignore' --exclude 'resources' \
    --exclude '.hugo_build.lock'
  rm -rf "$tmp"
  echo "built $ROOT ($(find "$ROOT" -type f -not -path "$ROOT/content/*" -not -path "$ROOT/layouts/*" -not -path "$ROOT/themes/*" -not -path "$ROOT/archetypes/*" | wc -l) files)"
}

case "${1:-build}" in
  serve)
    exec hugo server -D --source "$ROOT" ;;
  build)
    build ;;
  publish)
    build
    git -C "$REPO_ROOT" add "$ROOT"
    git -C "$REPO_ROOT" commit -m "blog: publish built output"
    git -C "$REPO_ROOT" push origin main
    bash "$REPO_ROOT/development/standards/scripts/publish-web.sh"
    echo "published → https://flove.org/development/blog/" ;;
  *)
    echo "usage: build-blog.sh [serve|build|publish]"; exit 1 ;;
esac
