#!/usr/bin/env bash
# Quick public HTTPS for the Authy verifier using a Cloudflare quick tunnel.
# The bot itself keeps polling Telegram; only /claim needs to be reachable.
set -euo pipefail

PORT="${PORT:-8787}"
if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared is required: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" >&2
  exit 1
fi

echo "Starting a temporary HTTPS tunnel to http://localhost:${PORT} ..." >&2
exec cloudflared tunnel --url "http://localhost:${PORT}"
