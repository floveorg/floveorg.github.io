#!/usr/bin/env bash
# Sync the plugin (and its Turndown vendor) into the public demo at
# addons/docsify-edit/. Run from anywhere.
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
DEST="$ROOT/addons/docsify-edit"
WIKI_VENDOR="$ROOT/development/standards/vendor"

mkdir -p "$DEST/vendor"
cp "$HERE/src/docsify-edit.js" "$DEST/docsify-edit.js"
cp "$HERE/vendor/turndown.min.js" "$HERE/vendor/turndown-plugin-gfm.min.js" "$DEST/vendor/"

# Keep the demo's docsify core in step with the wiki when it is present.
if [ -f "$WIKI_VENDOR/docsify.min.js" ]; then
  cp "$WIKI_VENDOR/docsify.min.js" "$WIKI_VENDOR/vue.css" "$DEST/vendor/"
fi

echo "docsify-edit demo → $DEST"
