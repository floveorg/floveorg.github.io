#!/usr/bin/env bash
# build-flove-zip.sh — builds flove.zip, the runnable local package that the
# "Download / Go local" button on the home page hands out.
#
# Source of truth = the COMMITTED site (git archive HEAD), so the package is
# exactly what flove.org serves: no .git, no .claude worktrees, no gitignored
# dev cruft. Commit your changes BEFORE running this, then commit flove.zip.
#
# The packaged copy gets a portable launcher: the .desktop icon is rewritten to
# a relative filename so the classical flove icon shows wherever it's unzipped.
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "$ROOT"

command -v zip >/dev/null || { echo "need 'zip' installed"; exit 1; }

STAGE="$(mktemp -d)"
TARGET="$STAGE/flove"
mkdir -p "$TARGET"

# Exactly the tracked files at HEAD (mirrors the deployed site).
git archive --format=tar HEAD | tar -x -C "$TARGET"

# Things that make no sense inside a downloaded local copy.
rm -f  "$TARGET/flove.zip" "$TARGET/build-flove-zip.sh" \
       "$TARGET/.gitignore" "$TARGET/.gitlab-ci.yml" "$TARGET/.gitmodules" \
       "$TARGET/.htmlvalidate.json" "$TARGET/CNAME" "$TARGET/.nojekyll"

# Portable launcher icon: reference the svg sitting beside the .desktop, so the
# classical flove icon shows on the user's machine (not Marc's absolute path).
if [ -f "$TARGET/flove-localhost.desktop" ]; then
  sed -i 's#^Icon=.*#Icon=flove-icon.svg#' "$TARGET/flove-localhost.desktop"
fi

rm -f "$ROOT/flove.zip"
( cd "$STAGE" && zip -rqX "$ROOT/flove.zip" flove )
rm -rf "$STAGE"

echo "built $ROOT/flove.zip ($(du -h "$ROOT/flove.zip" | cut -f1))"
