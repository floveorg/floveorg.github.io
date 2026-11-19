#!/usr/bin/env bash
# Copy the plugin from this package into the flove wiki's vendor/ folder.
set -euo pipefail
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
DEST="$ROOT/development/standards/vendor/docsify-edit.js"
cp "$HERE/src/docsify-edit.js" "$DEST"
echo "docsify-edit → $DEST"
