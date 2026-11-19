// Pure Authy claim logic — no Telegram, no HTTP. Tested by test/logic.test.mjs.
export const NONCE_RE = /^[a-f0-9]{16}$/;
export const TTL_MS = 10 * 60 * 1000;

// `/start`, `/start claim_<16 hex>`, `/start risa_<16..64 hex>`.
export function parseStartCommand(text) {
  const t = String(text || '').trim();
  let m = /^\/start(?:@\w+)?\s+claim_([a-f0-9]{16})(?:@\w+)?\s*$/i.exec(t);
  if (m) return { kind: 'claim', nonce: m[1] };
  m = /^\/start(?:@\w+)?\s+risa_([a-f0-9]{16,64})(?:@\w+)?\s*$/i.exec(t);
  if (m) return { kind: 'risa', key: m[1].toLowerCase() };
  if (/^\/start(?:@\w+)?\s*$/i.test(t)) return { kind: 'start' };
  return null;
}

export function parseStart(text) {
  const c = parseStartCommand(text);
  return c && c.kind === 'claim' ? { nonce: c.nonce } : c && c.kind === 'start' ? { nonce: null } : null;
}

export function claimFromUpdate(update, now = Date.now()) {
  const msg = update && update.message;
  if (!msg || !msg.from || !msg.chat) return null;
  if (msg.chat.type !== 'private') return null;
  const parsed = parseStartCommand(msg.text);
  if (!parsed || parsed.kind !== 'claim') return null;
  return {
    nonce: parsed.nonce,
    level: 'verified',
    telegram: { id: msg.from.id, username: msg.from.username || '' },
    at: new Date(now).toISOString()
  };
}

export function risaFromUpdate(update, now = Date.now()) {
  const msg = update && update.message;
  if (!msg || !msg.from || !msg.chat) return null;
  if (msg.chat.type !== 'private') return null;
  const parsed = parseStartCommand(msg.text);
  if (!parsed || parsed.kind !== 'risa') return null;
  return {
    key: parsed.key,
    level: 'presence',
    telegram: { id: msg.from.id, username: msg.from.username || '' },
    at: new Date(now).toISOString()
  };
}

export function isFresh(claim, now = Date.now(), ttl = TTL_MS) {
  const at = Date.parse(claim && claim.at);
  return Number.isFinite(at) && now - at >= 0 && now - at <= ttl;
}

// Public verifier payload — no Telegram id, no username.
export function publicClaim(claim) {
  if (!claim) return { ok: false };
  return { ok: true, level: claim.level, at: claim.at };
}
