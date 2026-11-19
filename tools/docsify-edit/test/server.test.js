'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const fsp = fs.promises;
const os = require('node:os');
const path = require('node:path');
const { createServer } = require('../server/node/server.js');

async function boot(opts = {}) {
  const tmp = await fsp.mkdtemp(path.join(os.tmpdir(), 'docsify-edit-'));
  const root = path.join(tmp, 'site');
  const editable = path.join(root, 'docs');
  await fsp.mkdir(editable, { recursive: true });
  await fsp.writeFile(path.join(editable, 'page.md'), '# Title\n\nBody.\n');
  const server = createServer({
    root,
    editable: 'docs',
    backupDir: path.join(tmp, 'backs'),
    token: opts.token
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  const base = `http://127.0.0.1:${port}`;
  return {
    tmp, root, editable, server, port, base,
    page: path.join(editable, 'page.md'),
    async close() {
      await new Promise((resolve) => server.close(resolve));
      await fsp.rm(tmp, { recursive: true, force: true });
    }
  };
}

function save(base, payload, { origin = true, token } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (origin) headers.Origin = base;
  if (token) headers['X-Edit-Token'] = token;
  return fetch(`${base}/__edit/save`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload)
  });
}

test('ping', async () => {
  const app = await boot();
  try {
    const res = await fetch(`${app.base}/__edit/ping`);
    const j = await res.json();
    assert.equal(res.status, 200);
    assert.equal(j.ok, true);
    assert.equal(j.api, 1);
    assert.equal(j.auth, 'none');
  } finally { await app.close(); }
});

test('save writes, backs up and returns a base hash', async () => {
  const app = await boot();
  try {
    const res = await save(app.base, { path: 'page.md', markdown: '# Changed\n\nNew.\n' });
    const j = await res.json();
    assert.equal(res.status, 200, JSON.stringify(j));
    assert.equal(await fsp.readFile(app.page, 'utf8'), '# Changed\n\nNew.\n');
    assert.ok(fs.existsSync(j.backup));
    assert.equal((await fsp.readFile(j.backup, 'utf8')), '# Title\n\nBody.\n');
    assert.match(j.base, /^[0-9a-f]{64}$/);
  } finally { await app.close(); }
});

test('refuses cross-origin saves', async () => {
  const app = await boot();
  try {
    const res = await save(app.base, { path: 'page.md', markdown: 'x' }, { origin: false });
    assert.equal(res.status, 403);
    assert.equal(await fsp.readFile(app.page, 'utf8'), '# Title\n\nBody.\n');
  } finally { await app.close(); }
});

test('rejects traversal, non-md and missing files', async () => {
  const app = await boot();
  try {
    for (const rel of ['../page.md', '../../etc/passwd', 'sub/../../page.md']) {
      const res = await save(app.base, { path: rel, markdown: 'x' });
      assert.ok([400, 403, 404].includes(res.status), `${rel}: ${res.status}`);
    }
    let res = await save(app.base, { path: 'page.html', markdown: 'x' });
    assert.ok([400, 403].includes(res.status));
    res = await save(app.base, { path: 'missing.md', markdown: 'x' });
    assert.equal(res.status, 404);
  } finally { await app.close(); }
});

test('409 on a stale base', async () => {
  const app = await boot();
  try {
    const res = await save(app.base, { path: 'page.md', markdown: 'x', base: '0'.repeat(64) });
    const j = await res.json();
    assert.equal(res.status, 409);
    assert.equal(j.code, 'conflict');
    assert.equal(await fsp.readFile(app.page, 'utf8'), '# Title\n\nBody.\n');
  } finally { await app.close(); }
});

test('dryRun does not write', async () => {
  const app = await boot();
  try {
    const res = await save(app.base, { path: 'page.md', markdown: 'x', dryRun: true });
    assert.equal(res.status, 200);
    assert.equal(await fsp.readFile(app.page, 'utf8'), '# Title\n\nBody.\n');
  } finally { await app.close(); }
});

test('preserves CRLF and BOM', async () => {
  const app = await boot();
  try {
    await fsp.writeFile(app.page, Buffer.from('# T\r\n\r\nB.\r\n'));
    await save(app.base, { path: 'page.md', markdown: '# C\n\nN.\n' });
    assert.equal(await fsp.readFile(app.page, 'utf8'), '# C\r\n\r\nN.\r\n');

    await fsp.writeFile(app.page, Buffer.from([0xef, 0xbb, 0xbf, ...Buffer.from('# T\n')]));
    await save(app.base, { path: 'page.md', markdown: '# C\n' });
    const bytes = await fsp.readFile(app.page);
    assert.deepEqual([...bytes.slice(0, 3)], [0xef, 0xbb, 0xbf]);
  } finally { await app.close(); }
});

test('token is required when configured', async () => {
  const app = await boot({ token: 's3cret' });
  try {
    let res = await save(app.base, { path: 'page.md', markdown: 'x' });
    assert.equal(res.status, 403);
    res = await save(app.base, { path: 'page.md', markdown: '# T\n' }, { token: 's3cret' });
    assert.equal(res.status, 200);
    res = await save(app.base, { path: 'page.md', markdown: 'x' }, { token: 'wrong' });
    assert.equal(res.status, 403);
  } finally { await app.close(); }
});

test('serves static files and 404s outside the root', async () => {
  const app = await boot();
  try {
    await fsp.writeFile(path.join(app.root, 'index.html'), '<h1>hi</h1>');
    let res = await fetch(`${app.base}/`);
    assert.equal(res.status, 200);
    assert.match(await res.text(), /hi/);
    res = await fetch(`${app.base}/../package.json`);
    assert.equal(res.status, 404);
  } finally { await app.close(); }
});
