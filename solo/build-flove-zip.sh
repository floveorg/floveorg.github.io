#!/usr/bin/env bash
# build-flove-zip.sh — builds flove-solo.zip, the runnable local package that the
# "Download / Go local" button on the solo home hands out.
#
# Source of truth = the COMMITTED site (git archive HEAD), so the package is
# exactly what flove.org serves: no .git, no CI config, no gitignored dev
# cruft. The package ships exactly two things, extracted from tracked HEAD:
#   - solo/    the app — renamed per flove-solo and FLATTENED: its content sits
#              directly in the flove-solo/ folder (start.html, apps/, index.html,
#              sw.js, … at the package root), not nested under solo/. NO shared
#              multimedia ships: audio/ and images/ are stripped, so the download
#              is fully self-contained text (no sounds, no captions, no icons).
#              The Android build dir solo/flove-apk/ never ships either — apk-only.
#   - docs/    a minimal reading library, kept as docs/: just index.html +
#              paradigms.html (the only two pages the site links to). The
#              embedded packs/backups docs/docs-files/ never ships — gitignored.
# Nothing else in the repo (central/, decentral/, development/, root index/404)
# lands in the download. The package-only launchers (START-FLOVE-LINUX.sh /
# -MAC.command / -WINDOWS.bat) are NOT tracked — they're GENERATED here and sit
# at the ZIP ROOT beside flove-solo/ (which holds the app and docs/).
# The Linux script creates its own menu/Desktop icon on first run (so no
# .desktop is shipped). Commit site changes BEFORE running this.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"     # repo root — git pathspecs are root-relative
cd "$ROOT"

command -v zip >/dev/null || { echo "need 'zip' installed"; exit 1; }

STAGE="$(mktemp -d)"
TARGET="$STAGE/flove-solo"   # package root inside the zip (solo renamed + flattened)
mkdir -p "$TARGET"

# Exactly the tracked files at HEAD (mirrors the deployed site), but only the
# three things the offline package ships.
git archive --format=tar HEAD solo   | tar -x --strip-components=1 -C "$TARGET"   # solo/ → flattened into flove-solo/
git archive --format=tar HEAD docs/index.html docs/paradigms.html | tar -x -C "$TARGET"   # minimal docs/: just the two linked pages
git archive --format=tar HEAD index.html | tar -x -C "$TARGET"   # the flove home, at the package root (flove-solo/index.html)

# The download is deliberately self-contained text — no shared multimedia: drop
# audio/ (sounds) and images/ (captions, logo animations, icons) so the package
# never carries or calls them. Apps keep their own inline/in-app assets only
# (e.g. the tiny per-app favicon SVGs their tab icons need).
rm -rf "$TARGET/audio" "$TARGET/images"

# The Android build dir is apk-only cruft (gradle, twa/ store_icon.png, keystore
# refs) — it must never ship in the offline package. The APK is a TWA wrapping
# the live site, so the download carries no android scaffolding.
rm -rf "$TARGET/flove-apk"

# docs/docs-files/ is an embedded packs/backups repo — never part of the download.
rm -rf "$TARGET/docs/docs-files"

# Things that make no sense inside a downloaded local copy.
rm -f  "$TARGET/flove.zip" "$TARGET/flove-solo.zip" \
       "$TARGET/build-flove-zip.sh" "$TARGET/build-sw.mjs" \
       "$TARGET/build-aliases.mjs" "$TARGET/404.html" \
       "$TARGET/.gitignore" "$TARGET/.htmlvalidate.json"

# The landing page keeps its name in the download (start.html) — one single
# localhost entrance, same file the live site and APK use. In the download the
# landing = the language selector on every launch: drop the "auto-skip to
# index.html when a language is remembered" line (live site keeps it).
if [ -f "$TARGET/start.html" ]; then
  sed -i "s|.*saved === 'en'.*return;.*|      // download: the language selector stays the landing (no auto-skip)|" "$TARGET/start.html"
fi

# The home (index.html) sits at the package root, and the whole solo/ tree is
# flattened — rewrite its internal "solo/" prefixed links to the package paths so
# the buttons, manifest, icon and service worker resolve inside the download. The
# root index.html also links the solo home at solo/apps/ → apps/. The Desktop zip /
# Mobile download buttons keep working online (the apk links straight to the
# GitHub release), so they're left pointing outward.
if [ -f "$TARGET/index.html" ]; then
  sed -i -e 's#solo/manifest.webmanifest#manifest.webmanifest#g' \
         -e 's#solo/apple-touch-icon.png#apple-touch-icon.png#g' \
         -e 's#solo/apps/#apps/#g' \
         -e 's#solo/sw.js#sw.js#g' \
         "$TARGET/index.html"
fi

# ── Package-only launchers (generated, not tracked), one per desktop OS, at the
# ZIP ROOT next to flove-solo/ and docs/. Each serves the folder on
# localhost:8642 and opens flove-solo/start.html. Each first stops anything
# already serving 8642 (an older download), so running a fresh download takes
# over — update behavior. Needs python3 (preinstalled on Linux & macOS).
cat > "$STAGE/START-FLOVE-LINUX.sh" <<'SH'
#!/usr/bin/env bash
# START-FLOVE-LINUX.sh — run this. Serves the folder beside this script and
# opens flove-solo/start.html at http://localhost:8642. It stops anything
# already serving 8642 (an older download) so this copy is the one that shows,
# and on first run drops a flove icon into your applications menu (and Desktop).
set -uo pipefail

SELF="$(readlink -f "$0")"
HERE="$(cd "$(dirname "$SELF")" && pwd)"
ROOT="$HERE/flove-solo"               # the package: flattened app + docs/
PORT=8642
ENTRY="start.html"
URL="http://localhost:${PORT}/${ENTRY}"

# ── Phones: where to open flove ├────────────────────────────────────────────
# A phone can never reach this computer's "localhost". It must load the same
# package over the LAN (same Wi-Fi) — or over Tailscale if you have it (any
# network, and HTTPS, so offline/PWA works on the phone). We expose these in
# devices.json (read by the app's Settings ▸ Devices section to show/QR them).
lan_ips() { hostname -I 2>/dev/null | tr ' ' '\n' \
            | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' \
            | grep -v '^127\.' || true; }
tailscale_url() { command -v tailscale >/dev/null 2>&1 \
  && tailscale ip -4 2>/dev/null | head -1 | sed "s#^#http://#; s#\$#:$PORT#"; }
write_devices() {
  local out lan="[" ip ts fst=1
  for ip in $(lan_ips); do
    [ -n "$ip" ] || continue
    if [ "$fst" -eq 1 ]; then lan="$lan\"http://$ip:$PORT\""; fst=0; else lan="$lan, \"http://$ip:$PORT\""; fi
  done
  out="{\"port\":$PORT,\"localhost\":\"$URL\",\"lan\":$lan]"
  ts="$(tailscale_url)"; [ -n "$ts" ] && out="$out,\"tailscale\":\"$ts\""
  out="$out}"
  printf '%s\n' "$out" > "$ROOT/devices.json" 2>/dev/null || true
  echo "──────────────────────────────────────────────────────────"
  echo "  Open flove on a phone (ranked):"
  echo "    1 · Termux (this phone):      install Termux, copy this package to the"
  echo "                                  phone and run START-ANDROID.sh (no network)."
  [ -n "$ts" ] && echo "    2 · Tailscale (any network):  $ts/"
  for ip in $(lan_ips); do [ -n "$ip" ] && echo "    3 · same Wi-Fi:                       http://$ip:$PORT/"; done
  echo "    · this computer:               $URL"
  echo "  Phone wants a QR: open here ▸ Settings ▸ Devices (or scan on the same page)."
  echo "──────────────────────────────────────────────────────────"
}
write_devices

port_open() { (exec 3<>"/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null; }
opener() { xdg-open "$1" >/dev/null 2>&1 || open "$1" >/dev/null 2>&1 & }

# Take over the port: an older flove localhost (previous download) may already
# be serving 8642 — stop it so THIS folder is the one that shows. Update
# behavior. Older downloads predate this and can't take over the port, so they
# are superseded by the newest download — not backwards compatible.
stop_existing() {
  local pids=""
  if command -v lsof >/dev/null 2>&1; then
    pids="$(lsof -ti tcp:8642 2>/dev/null | tr '\n' ' ')"
  else
    pids="$(pgrep -f 'http.server 8642' 2>/dev/null | tr '\n' ' ')"
  fi
  [ -n "$pids" ] || return 0
  kill $pids 2>/dev/null || true
  sleep 0.3
  if command -v notify-send >/dev/null 2>&1; then
    notify-send "flove" "Actualizado: se detuvo un flove localhost anterior; esta copia es la activa."
  else
    echo "flove: actualizado — se reemplazó un flove localhost anterior." >&2
  fi
}

# Create a real menu/desktop icon that points back to this very script.
make_icon() {
  local apps="$HOME/.local/share/applications"
  mkdir -p "$apps" 2>/dev/null || return 0
  cat > "$apps/flove-localhost.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=flove (localhost)
Comment=Serve flove on localhost and open it
Exec="$SELF"
Icon=$ROOT/apple-touch-icon.png
Terminal=false
StartupNotify=true
Categories=Network;
EOF
  chmod +x "$apps/flove-localhost.desktop" 2>/dev/null || true
  update-desktop-database "$apps" >/dev/null 2>&1 || true
  if [ -d "$HOME/Desktop" ]; then
    cp "$apps/flove-localhost.desktop" "$HOME/Desktop/" 2>/dev/null || true
    chmod +x "$HOME/Desktop/flove-localhost.desktop" 2>/dev/null || true
    gio set "$HOME/Desktop/flove-localhost.desktop" metadata::trusted true 2>/dev/null || true
  fi
}
make_icon
stop_existing

if ! port_open; then
  cd "$ROOT" || { command -v notify-send >/dev/null && notify-send "flove" "No encuentro la carpeta flove-solo"; exit 1; }
  nohup python3 -m http.server "$PORT" >/tmp/flove-server.log 2>&1 &
  disown
  for _ in $(seq 1 20); do port_open && break; sleep 0.2; done
fi

if port_open; then
  opener "$URL"                          # localhost: reliable storage + secure context
else
  command -v notify-send >/dev/null && notify-send "flove" \
    "Sin servidor local — abriendo el fichero directo (file://), modo degradado."
  opener "$ROOT/${ENTRY}"
fi
SH
chmod +x "$STAGE/START-FLOVE-LINUX.sh"

# macOS double-click launcher (.command opens in Terminal). readlink -f isn't
# portable on macOS, so locate the folder the simple way; use `open`.
cat > "$STAGE/START-FLOVE-MAC.command" <<'CMD'
#!/usr/bin/env bash
# START-FLOVE-MAC.command — macOS: serves the folder beside this file and opens
# flove-solo/start.html at http://localhost:8642. Stops anything already serving
# 8642 (an older download) so this copy wins. Double-click it (needs python3).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$HERE/flove-solo"
PORT=8642
ENTRY="start.html"
URL="http://localhost:${PORT}/${ENTRY}"
lan_ips() { ipconfig getifaddr en0 2>/dev/null; ipconfig getifaddr en1 2>/dev/null; }
ts_url() { command -v tailscale >/dev/null 2>&1 && tailscale ip -4 2>/dev/null | head -1 | sed "s#^#http://#; s#\$#:$PORT#"; }
write_devices() {
  local out lan="[" ip ts fst=1
  for ip in $(lan_ips); do
    [ -n "$ip" ] || continue
    if [ "$fst" -eq 1 ]; then lan="$lan\"http://$ip:$PORT\""; fst=0; else lan="$lan, \"http://$ip:$PORT\""; fi
  done
  out="{\"port\":$PORT,\"localhost\":\"$URL\",\"lan\":$lan]"
  ts="$(ts_url)"; [ -n "$ts" ] && out="$out,\"tailscale\":\"$ts\""
  printf '%s\n' "$out" > "$ROOT/devices.json" 2>/dev/null || true
}
port_open() { (exec 3<>"/dev/tcp/127.0.0.1/${PORT}") 2>/dev/null; }
stop_existing() {
  local pids=""
  if command -v lsof >/dev/null 2>&1; then
    pids="$(lsof -ti tcp:8642 2>/dev/null | tr '\n' ' ')"
  else
    pids="$(pgrep -f 'http.server 8642' 2>/dev/null | tr '\n' ' ')"
  fi
  [ -n "$pids" ] || return 0
  kill $pids 2>/dev/null || true
  sleep 0.3
  osascript -e 'display notification "Se reemplazó un flove localhost anterior; esta copia es la activa." with title "flove"' 2>/dev/null || \
    echo "flove: actualizado — se reemplazó un flove localhost anterior." >&2
}
stop_existing
write_devices
if ! port_open; then
  cd "$ROOT" || exit 1
  if command -v python3 >/dev/null; then
    nohup python3 -m http.server "$PORT" >/tmp/flove-server.log 2>&1 &
    for _ in $(seq 1 20); do port_open && break; sleep 0.2; done
  fi
fi
if port_open; then open "$URL"; else open "$ROOT/start.html"; fi
CMD
chmod +x "$STAGE/START-FLOVE-MAC.command"

# Windows launcher. Tries python / py; if neither, opens the file directly.
cat > "$STAGE/START-FLOVE-WINDOWS.bat" <<'BAT'
@echo off
REM START-FLOVE-WINDOWS.bat - serves the flove-solo folder and opens start.html on localhost:8642
REM Update behavior: stops anything already serving 8642 (a previous download) so this copy wins.
setlocal
cd /d "%~dp0flove-solo"
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r ":8642 .*LISTENING"') do (
  taskkill /F /PID %%a >nul 2>nul
  set "REPLACED=1"
)
if defined REPLACED echo Updated: replaced an older flove localhost; this copy is now active.
echo For a phone: open http://<this-PC-LAN-IP>:8642/ from the same Wi-Fi. Scan the QR in the app (Settings > Devices).
where python >nul 2>nul
if %errorlevel%==0 (
  start "flove server" /min python -m http.server 8642
  timeout /t 1 >nul
  start "" http://localhost:8642/start.html
  goto :eof
)
where py >nul 2>nul
if %errorlevel%==0 (
  start "flove server" /min py -m http.server 8642
  timeout /t 1 >nul
  start "" http://localhost:8642/start.html
  goto :eof
)
echo Python not found - opening the file directly ^(some features may be limited^).
start "" start.html
BAT

# Android/Termux launcher. Termux = the Android shell; run START-ANDROID.sh there
# and it serves the package beside it on the phone's OWN localhost:8642.
# Phone-localhost is a secure context, so the service worker / offline / PWA
# install work on the phone with NO shared Wi-Fi and NO Tailscale — the package
# is simply run where it lives. Get Termux + python first: 'pkg install python'.
cat > "$STAGE/START-ANDROID.sh" <<'SH'
#!/usr/bin/env bash
# START-ANDROID.sh — run inside Termux on the phone.
# Serves the flove-solo folder beside this script and opens start.html on your
# phone's own http://localhost:8642 (localhost on the phone = secure context, so
# the offline service worker works). No shared Wi-Fi or network needed.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$HERE/flove-solo"
PORT=8642
ENTRY="start.html"
URL="http://localhost:${PORT}/${ENTRY}"

command -v python3 >/dev/null 2>&1 || python3 --version 2>/dev/null || {
  echo "Termux needs python: run  pkg install python  in Termux first."
  exit 1
}

# Stop anything already serving 8642 so this copy wins.
if command -v lsof >/dev/null 2>&1; then
  PIDS="$(lsof -ti tcp:8642 2>/dev/null | tr '\n' ' ')"
elif command -v pgrep >/dev/null 2>&1; then
  PIDS="$(pgrep -f 'http.server 8642' 2>/dev/null | tr '\n' ' ')"
else
  PIDS=""
fi
[ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true

cd "$ROOT" || { echo "No encuentro la carpeta flove-solo"; exit 1; }
nohup python3 -m http.server "$PORT" >/tmp/flove-server.log 2>&1 &
sleep 1

# Open in the phone's browser (start is Termux's tool). Fall back gracefully.
if command -v termux-open-url >/dev/null 2>&1; then
  termux-open-url "$URL"
else
  echo "flove listo → abrelo en tu navegador: $URL"
fi
echo "flove serving locally on this phone at $URL"
SH
chmod +x "$STAGE/START-ANDROID.sh"

rm -f "$ROOT/solo/flove-solo.zip"
( cd "$STAGE" && zip -rqX "$ROOT/solo/flove-solo.zip" \
    START-FLOVE-LINUX.sh START-FLOVE-MAC.command START-FLOVE-WINDOWS.bat START-ANDROID.sh \
    flove-solo )
rm -rf "$STAGE"

echo "built $ROOT/solo/flove-solo.zip ($(du -h "$ROOT/solo/flove-solo.zip" | cut -f1))"
