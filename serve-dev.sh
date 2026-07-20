#!/usr/bin/env bash
# serve-dev.sh — serve flove locally so the docsify docs actually work.
#
# The docsify docs (apps/dev, docs/theory) fetch their markdown at runtime, which
# the file:// protocol blocks — so double-clicking index.html shows a "404". This
# runs a tiny local http server so those fetches succeed, then opens the dev docs
# in your browser. Ctrl-C to stop.
#
#   ./serve-dev.sh            # start the server + open the dev docs
#   ./serve-dev.sh install    # create a clickable "flove · dev docs" launcher icon
#   PORT=9000 ./serve-dev.sh  # use a different port (default 8642)
#
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PORT="${PORT:-8642}"
URL="http://localhost:$PORT/apps/dev/"

open_browser(){
  ( sleep "${1:-0}"
    if command -v firefox >/dev/null; then firefox "$URL"
    elif command -v xdg-open >/dev/null; then xdg-open "$URL"; fi
  ) >/dev/null 2>&1 &
}

install_launcher(){
  local apps="$HOME/.local/share/applications"
  local desktop="$apps/flove-dev-docs.desktop"
  mkdir -p "$apps"
  cat > "$desktop" <<EOF
[Desktop Entry]
Type=Application
Name=flove · dev docs
Comment=Serve flove locally and open the dev docs (standards · backend · agent search)
Exec=$ROOT/serve-dev.sh
Icon=$ROOT/images/dev-icon.png
Terminal=true
Categories=Development;Documentation;
EOF
  chmod +x "$desktop"
  if [ -d "$HOME/Desktop" ]; then
    cp "$desktop" "$HOME/Desktop/flove-dev-docs.desktop" 2>/dev/null || true
    chmod +x "$HOME/Desktop/flove-dev-docs.desktop" 2>/dev/null || true
    gio set "$HOME/Desktop/flove-dev-docs.desktop" metadata::trusted true 2>/dev/null || true
  fi
  update-desktop-database "$apps" 2>/dev/null || true
  echo "✺ installed launcher → $desktop"
  echo "   Find 'flove · dev docs' in your app menu (pin it / drag to the taskbar)."
  echo "   For a Firefox toolbar icon: run the server, open $URL, then Ctrl+D to bookmark it."
}

if [ "${1:-}" = "install" ]; then install_launcher; exit 0; fi

# Already running on this port? Just open the browser.
if curl -s -o /dev/null --max-time 2 "http://localhost:$PORT/" 2>/dev/null; then
  echo "✺ server already up on :$PORT — opening $URL"
  open_browser 0
  exit 0
fi

echo "✺ flove dev docs → $URL"
echo "   theory → http://localhost:$PORT/docs/theory/     (Ctrl-C to stop)"
open_browser 1
cd "$ROOT"
exec python3 -m http.server "$PORT"
