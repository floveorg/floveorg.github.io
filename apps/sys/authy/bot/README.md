# Authy Telegram bot

The bot behind **Authy L3 → L4**. It accepts `/start claim_<nonce>` in a private
Telegram chat and exposes the verified claim at `GET /claim?nonce=…`; the Authy
page polls it.

## 1. Create the bot (BotFather — human step)

1. Open **@BotFather** in Telegram.
2. `/newbot` → name **Authy** → username, e.g. **AuthyTgBot**.
3. Copy the token. Never commit it.

This is the only step a script cannot do: BotFather needs a Telegram account.

## 2. Run the verifier

```bash
export TELEGRAM_BOT_TOKEN='123456:ABC…'
node apps/sys/authy/bot/server.mjs
# authy bot verifier on http://localhost:8787/claim
```

No dependencies. Claims live in memory and `claims.json` (10 min TTL, one use).

### HTTPS

The bot long-polls Telegram, so **no webhook is required**. Only `/claim` needs
to be reachable from the Authy page; `http://localhost:8787` is enough for local
testing, but flove.org needs HTTPS.

**Quick tunnel (temporary URL):**

```bash
# terminal 1
node apps/sys/authy/bot/server.mjs
# terminal 2
apps/sys/authy/bot/https.sh
# → https://<random>.trycloudflare.com
```

Use `?verify=https://<random>.trycloudflare.com/claim`.

**Caddy with your own domain:**

```bash
caddy run --config apps/sys/authy/bot/Caddyfile.example
```

Point the domain at the machine running the bot; Caddy obtains the certificate.

**Direct TLS:** set `TLS_KEY` and `TLS_CERT` in `.env` to PEM paths. The server
then starts with HTTPS on `PORT`.

Set `PUBLIC_URL=https://your-domain.example` so `/health` reports the public
origin. `HOST` defaults to `0.0.0.0`; use `127.0.0.1` behind a local proxy.

## 3. Point Authy at it

Open Authy with the bot username and verifier URL:

```
apps/sys/authy/index.html?bot=AuthyTgBot&verify=http://localhost:8787/claim
```

The same values can be set in `apps/sys/authy/index.html`:

```js
var TELEGRAM = { bot: 'AuthyTgBot', verify: 'https://…/claim' };
```

## 4. Claim

1. Authy → **Generate claim nonce** → open the `t.me/<bot>?start=claim_…` link.
2. In Telegram, send `/start` (the deep link does it) → the bot replies
   “Verified — level 3”.
3. Authy polls the verifier and stores L4 in `flove:authy`.
4. Appy reads it (or receives the handoff) and unlocks publishing; MyNet was
   already available at L3.

## Production

Run `server.mjs` on any HTTPS host (Railway, Fly, a small VM, or behind Caddy /
Cloudflare Tunnel) and set `verify` to `https://…/claim`. Keep the bot token
only in the server env. The verifier returns `{ok, level, at}` — **no Telegram
id or username**.

## Security

- Nonce: 16 hex chars, 10 min TTL, single use.
- Private chats only; the bot stores nothing else.
- The public endpoint reveals only “this nonce was verified” and when.
- Revocation: delete the claim and write `verified:false` to Authy/Appy
  (Browsy attestation is the durable path — see the plan).
