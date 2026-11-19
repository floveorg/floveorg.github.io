#!/usr/bin/env bash
# serve-dev.sh — serve the REPO ROOT on localhost so the local preview uses the
# exact same URL layout as flove.org: /index.html, /apps/, /docs/…
#
# It runs tools/serve-edit.py, which also enables the in-browser editor for the
# dev wiki at /development/standards/ (an "Edit page" button appears on
# localhost; saving writes the .md into the repo, with a backup).
#
# One canonical root in every run mode (live, localhost, download package,
# file://) means a relative link is written once and never rewritten. Serving
# The old script served apps/ as a third layout and produced dead routes.
# Ctrl-C to stop.
#
#   ./serve-dev.sh            # start the server + open the home
#   ./serve-dev.sh install    # create a clickable "flove · dev" launcher icon
#   PORT=9000 ./serve-dev.sh  # use a different port (default 8642)
#
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"   # repo root
PORT="${PORT:-8642}"
HOST="${HOST:-127.0.0.1}"
URL="http://$HOST:$PORT/index.html"

open_browser(){
  ( sleep "${1:-0}"
    if command -v firefox >/dev/null; then firefox "$URL"
    elif command -v xdg-open >/dev/null; then xdg-open "$URL"; fi
  ) >/dev/null 2>&1 &
}

install_launcher(){
  local apps="$HOME/.local/share/applications"
  local desktop="$apps/flove-dev.desktop"
  mkdir -p "$apps"
  cat > "$desktop" <<EOF
[Desktop Entry]
Type=Application
Name=flove · dev
Comment=Serve the flove repo root on localhost with the same routes as flove.org
Exec=$ROOT/tools/serve-dev.sh
Icon=$ROOT/addons/media/dev-icon.png
Terminal=true
Categories=Development;Documentation;
EOF
  chmod +x "$desktop"
  if [ -d "$HOME/Desktop" ]; then
    cp "$desktop" "$HOME/Desktop/flove-dev.desktop" 2>/dev/null || true
    chmod +x "$HOME/Desktop/flove-dev.desktop" 2>/dev/null || true
    gio set "$HOME/Desktop/flove-dev.desktop" metadata::trusted true 2>/dev/null || true
  fi
  update-desktop-database "$apps" 2>/dev/null || true
  echo "🌱 installed launcher → $desktop"
  echo "   Find 'flove · dev' in your app menu (pin it / drag to the taskbar)."
  echo "   For a Firefox toolbar icon: run the server, open $URL, then Ctrl+D to bookmark it."
}

if [ "${1:-}" = "install" ]; then install_launcher; exit 0; fi

# Already running on this port? Just open the browser.
if curl -s -o /dev/null --max-time 2 "http://$HOST:$PORT/" 2>/dev/null; then
  if curl -s --max-time 2 "http://$HOST:$PORT/__edit/ping" 2>/dev/null | grep -q '"ok"'; then
    echo "🌱 server already up on :$PORT (editor enabled) — opening $URL"
  else
    echo "⚠  something without the editor is already on :$PORT."
    echo "   Stop it (Ctrl-C in its terminal) and run this script again to enable"
    echo "   the in-browser wiki editor. Opening the plain preview anyway…"
  fi
  open_browser 0
  exit 0
fi

echo "🌱 flove (repo root mirror of flove.org) → $URL"
echo "   apps → http://$HOST:$PORT/apps/     (Ctrl-C to stop)"
echo "   wiki editor → Edit page button in /development/standards/"
open_browser 1
cd "$ROOT"
exec python3 "$ROOT/tools/serve-edit.py" --root "$ROOT" --port "$PORT"
