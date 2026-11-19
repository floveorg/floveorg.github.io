#!/usr/bin/env node
// Authy Telegram claim bot + verifier.
//
//   TELEGRAM_BOT_TOKEN=... node apps/sys/authy/bot/server.mjs
//
// It long-polls Telegram getUpdates (no public webhook needed), accepts
// `/start claim_<nonce>` in a private chat, stores the claim for 10 minutes,
// and serves it at GET /claim?nonce=… for the Authy page to poll.
//
// Env: TELEGRAM_BOT_TOKEN (required), PORT=8787, CLAIMS_FILE=./claims.json
// No dependencies. Node 18+.

import http from 'node:http';
import https from 'node:https';
import { readFileSync } from 'node:fs';
import { readFile, writeFile } from 'node:fs/promises';
import { claimFromUpdate, risaFromUpdate, isFresh, publicClaim, TTL_MS } from './logic.mjs';

const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
if (!TOKEN) {
  console.error('TELEGRAM_BOT_TOKEN is required (create the bot with @BotFather).');
  process.exit(1);
}
const PORT = Number(process.env.PORT || 8787);
const HOST = process.env.HOST || '0.0.0.0';
const PUBLIC_URL = String(process.env.PUBLIC_URL || '').replace(/\/+$/, '');
const TLS_KEY = process.env.TLS_KEY || '';
const TLS_CERT = process.env.TLS_CERT || '';
const CLAIMS_FILE = process.env.CLAIMS_FILE || new URL('./claims.json', import.meta.url).pathname;

const api = `https://api.telegram.org/bot${TOKEN}/`;
const claims = new Map();
const risaClaims = new Map();
let offset = 0;
let lastUpdate = null;

async function load() {
  try {
    const data = JSON.parse(await readFile(CLAIMS_FILE, 'utf8'));
    Object.entries(data.claims || {}).forEach(([nonce, claim]) => {
      if (isFresh(claim)) claims.set(nonce, claim);
    });
    Object.entries(data.risa || {}).forEach(([key, claim]) => risaClaims.set(key, claim));
    offset = Number(data.offset || 0);
  } catch (_) {}
}
async function persist() {
  const now = Date.now();
  const data = { offset, claims: {}, risa: {} };
  claims.forEach((claim, nonce) => { if (isFresh(claim, now)) data.claims[nonce] = claim; });
  risaClaims.forEach((claim, key) => { data.risa[key] = claim; });
  try { await writeFile(CLAIMS_FILE, JSON.stringify(data, null, 2)); } catch (_) {}
}

async function call(method, body) {
  const res = await fetch(api + method, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body || {})
  });
  const json = await res.json();
  if (!json.ok) throw new Error(`${method}: ${JSON.stringify(json)}`);
  return json.result;
}

async function reply(chatId, text) {
  try { await call('sendMessage', { chat_id: chatId, text }); } catch (_) {}
}

async function poll() {
  for (;;) {
    try {
      const updates = await call('getUpdates', {
        offset, timeout: 25, allowed_updates: ['message']
      });
      for (const update of updates) {
        offset = update.update_id + 1;
        lastUpdate = { at: new Date().toISOString(), id: update.update_id, kind: update.message ? 'message' : 'other' };
        const claim = claimFromUpdate(update);
        if (claim) {
          if (claims.has(claim.nonce)) {
            await reply(update.message.chat.id, 'That claim nonce was already used. Generate a new one in Authy.');
            continue;
          }
          claims.set(claim.nonce, claim);
          console.log('claim received', claim.nonce.slice(0, 4) + '…');
          await persist();
          await reply(update.message.chat.id, 'Verified — level 4. Return to Authy; it will pick this up.');
          setTimeout(() => { claims.delete(claim.nonce); persist(); }, TTL_MS);
          continue;
        }
        const risa = risaFromUpdate(update);
        if (risa) {
          risaClaims.set(risa.key, risa);
          await persist();
          await reply(update.message.chat.id, 'Telegram linked to your risa profile — L3 presence. Return to Appy.');
          continue;
        }
        const msg = update.message;
        if (msg && msg.chat && msg.chat.type === 'private' && /^\/start/.test(msg.text || '')) {
          const hasClaim = /^\/start\s+claim_/i.test(String(msg.text || '').trim());
          const hasRisa = /^\/start\s+risa_/i.test(String(msg.text || '').trim());
          await reply(msg.chat.id, hasClaim
            ? 'That claim link is invalid or the nonce is incomplete. Generate a new one in Authy and use the full deep link.'
            : hasRisa
              ? 'That risa link is incomplete. Open Appy and use Link Telegram again.'
              : 'Authy bot. Open Authy, generate a claim nonce, then use the deep link it gives you.');
        }
      }
      if (updates.length) await persist();
    } catch (err) {
      console.error('poll error:', err.message, err.cause && (err.cause.code || err.cause.message) || '');
      await new Promise(r => setTimeout(r, 3000));
    }
  }
}

async function handle(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  res.setHeader('access-control-allow-origin', '*');
  res.setHeader('access-control-allow-methods', 'GET, POST, OPTIONS');
  res.setHeader('access-control-allow-headers', 'content-type');
  res.setHeader('cache-control', 'no-store');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (url.pathname === '/health') {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ ok: true, protocol: secure ? 'https' : 'http', publicUrl: PUBLIC_URL || null, claims: claims.size, risaClaims: risaClaims.size, offset, lastUpdate }));
    return;
  }
  if (url.pathname === '/claim') {
    const risaKey = String(url.searchParams.get('risa') || '').toLowerCase();
    if (risaKey) {
      const rc = risaClaims.get(risaKey);
      res.writeHead(rc ? 200 : 404, { 'content-type': 'application/json' });
      res.end(JSON.stringify(rc ? { ok: true, level: 'presence', at: rc.at } : { ok: false }));
      return;
    }
    const nonce = String(url.searchParams.get('nonce') || '').toLowerCase();
    const claim = claims.get(nonce);
    const ok = claim && isFresh(claim);
    res.writeHead(ok ? 200 : 404, { 'content-type': 'application/json' });
    res.end(JSON.stringify(publicClaim(ok ? claim : null)));
    return;
  }
  res.writeHead(404, { 'content-type': 'application/json' });
  res.end(JSON.stringify({ ok: false }));
}

let server;
const secure = !!(TLS_KEY && TLS_CERT);
if (secure) {
  server = https.createServer(
    { key: readFileSync(TLS_KEY), cert: readFileSync(TLS_CERT) },
    handle
  );
} else {
  server = http.createServer(handle);
}

await load();
server.listen(PORT, HOST, () => {
  const proto = secure ? 'https' : 'http';
  const shown = PUBLIC_URL || `${proto}://localhost:${PORT}`;
  console.log(`authy bot verifier on ${shown}/claim (${proto}, ${HOST}:${PORT})`);
});
poll();
