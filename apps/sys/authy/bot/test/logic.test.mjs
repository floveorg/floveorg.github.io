import test from 'node:test';
import assert from 'node:assert/strict';
import { parseStart, parseStartCommand, claimFromUpdate, risaFromUpdate, isFresh, publicClaim, TTL_MS } from '../logic.mjs';

const nonce = '0123456789abcdef';

function update(text, over = {}) {
  return {
    update_id: 1,
    message: {
      text,
      from: { id: 42, username: 'marc' },
      chat: { id: 42, type: 'private' },
      ...over
    }
  };
}

test('parseStart reads a claim nonce', () => {
  assert.deepEqual(parseStart(`/start claim_${nonce}`), { nonce });
  assert.deepEqual(parseStart(`/start claim_${nonce}@AuthyTgBot`), { nonce });
  assert.deepEqual(parseStart('/start'), { nonce: null });
  assert.equal(parseStart('hello'), null);
  assert.equal(parseStart('/start claim_xyz'), null);
});

test('claimFromUpdate only accepts private claim DMs', () => {
  assert.equal(claimFromUpdate(update('/start')), null);
  const c = claimFromUpdate(update(`/start claim_${nonce}`), 1_700_000_000_000);
  assert.equal(c.nonce, nonce);
  assert.equal(c.level, 'verified');
  assert.equal(c.telegram.id, 42);
  assert.equal(c.at, '2023-11-14T22:13:20.000Z');
  assert.equal(claimFromUpdate(update(`/start claim_${nonce}`, { chat: { id: 1, type: 'group' } })), null);
});

test('risa claim links a public risa key to Telegram presence', () => {
  const key = '84559b7a1e80ec172569aee2eb97d9f5b2f5c643268b5814c8c1c3c176369d0c';
  assert.deepEqual(parseStartCommand(`/start risa_${key}`), { kind: 'risa', key });
  const c = risaFromUpdate(update(`/start risa_${key}`), 1_700_000_000_000);
  assert.equal(c.key, key);
  assert.equal(c.level, 'presence');
  assert.equal(c.telegram.id, 42);
  assert.equal(risaFromUpdate(update(`/start risa_${key}`, { chat: { id: 1, type: 'group' } })), null);
});

test('isFresh enforces the TTL', () => {
  const c = claimFromUpdate(update(`/start claim_${nonce}`), 1_000_000);
  assert.equal(isFresh(c, 1_000_000), true);
  assert.equal(isFresh(c, 1_000_000 + TTL_MS), true);
  assert.equal(isFresh(c, 1_000_000 + TTL_MS + 1), false);
});

test('publicClaim never leaks Telegram identity', () => {
  const c = claimFromUpdate(update(`/start claim_${nonce}`), 1_000_000);
  assert.deepEqual(publicClaim(c), { ok: true, level: 'verified', at: c.at });
  assert.deepEqual(publicClaim(null), { ok: false });
});
