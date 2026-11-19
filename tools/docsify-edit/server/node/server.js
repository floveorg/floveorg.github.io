#!/usr/bin/env node
/* docsify-edit — static docs server + save API (zero dependencies).
 *
 *   node server.js [--port 8642] [--host 127.0.0.1] [--root .]
 *                  [--editable docs] [--token secret]
 *
 * The API is the same as the Python reference server:
 *
 *   GET  /__edit/ping
 *   POST /__edit/save  {path, markdown, base?, dryRun?}
 *
 * Safety: loopback by default, same-origin POSTs, optional token, .md files
 * only inside --editable, atomic writes, per-path lock, backups, CRLF/BOM
 * preservation and a SHA-256 base conflict check.
 */
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const fsp = fs.promises;
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');

const API_VERSION = 1;
const SERVER_VERSION = '1.0.0';
const MAX_BODY = 4 * 1024 * 1024;
const MAX_BACKUPS = 200;
const DEFAULT_BACKUP_DIR = path.join(os.homedir(), '.cache', 'docsify-edit');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.mp3': 'audio/mpeg',
  '.mp4': 'video/mp4',
  '.webmanifest': 'application/manifest+json'
};

class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

function sha256(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function sendJson(res, status, payload) {
  const body = Buffer.from(JSON.stringify(payload));
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': body.length,
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY) {
        reject(new ApiError(413, 'too_large', `body larger than ${MAX_BODY} bytes`));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function sameOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return false;
  const host = req.headers.host || '';
  return origin === `http://${host}` || origin === `https://${host}`;
}

async function realInside(root, candidate) {
  try {
    const real = await fsp.realpath(candidate);
    if (real === root) return real;
    return real.startsWith(root + path.sep) ? real : null;
  } catch (err) {
    return null;
  }
}

function safeRelative(rel) {
  if (typeof rel !== 'string' || !rel || rel.includes('\0') || rel.includes('\\')) return null;
  if (rel.startsWith('/') || rel.startsWith('..')) return null;
  return rel;
}

function createServer(options = {}) {
  const rootArg = path.resolve(options.root || process.cwd());
  const editableArg = path.resolve(rootArg, options.editable || 'docs');
  const token = options.token || null;
  const backupDir = path.resolve(options.backupDir || DEFAULT_BACKUP_DIR);
  const locks = new Map();
  let realRoot = null;
  let realEditable = null;

  function withLock(key, fn) {
    const previous = locks.get(key) || Promise.resolve();
    const next = previous.then(fn, fn);
    locks.set(key, next.catch(() => {}));
    return next;
  }

  async function ensureRoots() {
    if (realRoot) return;
    realRoot = await fsp.realpath(rootArg);
    realEditable = await fsp.realpath(editableArg);
  }

  async function pruneBackups() {
    try {
      const names = await fsp.readdir(backupDir);
      const stats = await Promise.all(names.map(async (name) => {
        const full = path.join(backupDir, name);
        try { return { full, mtime: (await fsp.stat(full)).mtimeMs }; }
        catch { return null; }
      }));
      const files = stats.filter(Boolean).sort((a, b) => b.mtime - a.mtime);
      await Promise.all(files.slice(MAX_BACKUPS).map((f) => fsp.unlink(f.full).catch(() => {})));
    } catch { /* no cache dir yet */ }
  }

  async function save(payload) {
    const rel = safeRelative(payload.path);
    if (!rel || !rel.toLowerCase().endsWith('.md')) {
      throw new ApiError(403, 'path', 'only .md files inside the editable directory can be written');
    }
    if (typeof payload.markdown !== 'string') {
      throw new ApiError(400, 'input', 'path and markdown (strings) are required');
    }
    if (payload.base != null && typeof payload.base !== 'string') {
      throw new ApiError(400, 'input', 'base must be a SHA-256 string');
    }
    await ensureRoots();

    const candidate = path.resolve(realEditable, rel);
    if (candidate !== realEditable && !candidate.startsWith(realEditable + path.sep)) {
      throw new ApiError(403, 'path', 'outside the editable directory');
    }
    let stat;
    try { stat = await fsp.stat(candidate); }
    catch { throw new ApiError(404, 'missing', 'file not found'); }
    if (!stat.isFile()) throw new ApiError(403, 'path', 'not a regular file');
    const target = await realInside(realEditable, candidate);
    if (!target) throw new ApiError(403, 'path', 'outside the editable directory');

    return withLock(target, async () => {
      const original = await fsp.readFile(target);
      if (payload.base && sha256(original) !== payload.base) {
        throw new ApiError(409, 'conflict', 'the file changed on disk since you opened the editor');
      }

      let text = payload.markdown.replace(/\r\n/g, '\n');
      const crlf = original.includes(Buffer.from('\r\n'));
      if (crlf) text = text.replace(/\n/g, '\r\n');
      let data = Buffer.from(text, 'utf8');
      const bom = original.length >= 3 && original[0] === 0xef && original[1] === 0xbb && original[2] === 0xbf;
      if (bom && !(data[0] === 0xef && data[1] === 0xbb && data[2] === 0xbf)) {
        data = Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), data]);
      }

      let backup = null;
      if (!payload.dryRun) {
        await fsp.mkdir(backupDir, { recursive: true });
        const stamp = new Date().toISOString().replace(/[:.]/g, '-');
        backup = path.join(backupDir, `${stamp}--${rel.replace(/\//g, '__')}`);
        await fsp.copyFile(target, backup);
        await pruneBackups();

        const tmp = path.join(path.dirname(target), `.${path.basename(target)}.${process.pid}.${Date.now()}.tmp`);
        try {
          await fsp.writeFile(tmp, data);
          await fsp.rename(tmp, target);
        } catch (err) {
          await fsp.unlink(tmp).catch(() => {});
          throw new ApiError(500, 'write', `write failed: ${err.message}`);
        }
      }

      const next = await fsp.stat(target);
      return {
        ok: true,
        path: rel,
        bytes: data.length,
        base: sha256(data),
        backup,
        mtime: next.mtimeMs / 1000,
        dryRun: Boolean(payload.dryRun)
      };
    });
  }

  async function serveStatic(req, res, pathname) {
    if (!['GET', 'HEAD'].includes(req.method)) {
      res.writeHead(405, { Allow: 'GET, HEAD' });
      res.end('Method Not Allowed');
      return;
    }
    if (pathname === '/') pathname = '/index.html';
    let decoded;
    try { decoded = decodeURIComponent(pathname); }
    catch { res.writeHead(400); res.end('Bad Request'); return; }

    let file = path.resolve(realRoot, '.' + decoded);
    let real = await realInside(realRoot, file);
    if (!real) { res.writeHead(404); res.end('Not found'); return; }
    let stat = await fsp.stat(real).catch(() => null);
    if (stat && stat.isDirectory()) {
      real = await realInside(realRoot, path.join(real, 'index.html'));
      if (!real) { res.writeHead(404); res.end('Not found'); return; }
      stat = await fsp.stat(real).catch(() => null);
    }
    if (!stat || !stat.isFile()) { res.writeHead(404); res.end('Not found'); return; }

    const type = MIME[path.extname(real).toLowerCase()] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': type,
      'Content-Length': stat.size,
      'Cache-Control': 'no-store'
    });
    if (req.method === 'HEAD') { res.end(); return; }
    fs.createReadStream(real).pipe(res);
  }

  async function handle(req, res) {
    await ensureRoots().catch(() => {});
    const url = new URL(req.url, 'http://localhost');
    const pathname = url.pathname;

    if (pathname === '/__edit/ping') {
      const authOk = !token || req.headers['x-edit-token'] === token;
      sendJson(res, 200, {
        ok: true,
        api: API_VERSION,
        version: SERVER_VERSION,
        editable: path.relative(realRoot, realEditable).split(path.sep).join('/'),
        auth: token ? 'token' : 'none',
        authOk,
        maxBody: MAX_BODY
      });
      return;
    }

    if (pathname === '/__edit/save') {
      if (req.method !== 'POST') throw new ApiError(405, 'method', 'POST required');
      if (!sameOrigin(req)) throw new ApiError(403, 'origin', 'cross-origin write refused');
      if (token && req.headers['x-edit-token'] !== token) {
        throw new ApiError(403, 'auth', 'bad or missing X-Edit-Token');
      }
      const raw = await readBody(req);
      let payload;
      try { payload = JSON.parse(raw.toString('utf8')); }
      catch { throw new ApiError(400, 'json', 'invalid JSON'); }
      if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
        throw new ApiError(400, 'json', 'JSON object required');
      }
      sendJson(res, 200, await save(payload));
      return;
    }

    await serveStatic(req, res, pathname);
  }

  const server = http.createServer((req, res) => {
    handle(req, res).catch((err) => {
      const e = err instanceof ApiError ? err : new ApiError(500, 'server', err.message || 'server error');
      if (!res.headersSent) sendJson(res, e.status, { ok: false, code: e.code, error: e.message });
      else res.end();
    });
  });

  server.editable = editableArg;
  server.root = rootArg;
  return server;
}

function parseArgs(argv) {
  const out = { port: 8642, host: '127.0.0.1', root: '.', editable: 'docs', token: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const next = () => {
      const value = argv[++i];
      if (!value) throw new Error(`${arg} needs a value`);
      return value;
    };
    if (arg === '--port') out.port = Number(next());
    else if (arg === '--host') out.host = next();
    else if (arg === '--root') out.root = next();
    else if (arg === '--editable') out.editable = next();
    else if (arg === '--token') out.token = next();
    else if (arg === '--help' || arg === '-h') out.help = true;
    else throw new Error(`unknown argument: ${arg}`);
  }
  return out;
}

if (require.main === module) {
  let args;
  try { args = parseArgs(process.argv.slice(2)); }
  catch (err) { console.error(`✗ ${err.message}`); process.exit(2); }
  if (args.help) {
    console.log('node server.js [--port 8642] [--host 127.0.0.1] [--root .] [--editable docs] [--token secret]');
    process.exit(0);
  }

  const server = createServer(args);
  const editablePath = path.resolve(args.root, args.editable);
  if (!fs.existsSync(args.root) || !fs.existsSync(editablePath)) {
    console.error(`✗ ${args.root} has no ${args.editable}/`);
    process.exit(2);
  }
  server.on('error', (err) => {
    console.error(`✗ cannot start: ${err.message}`);
    process.exit(1);
  });
  server.listen(args.port, args.host, () => {
    const shown = args.host === '::' || args.host === '0.0.0.0' ? '127.0.0.1' : args.host;
    console.log(`🌱 docsify-edit → http://${shown}:${args.port}/${args.editable}/`);
    console.log(`   root      ${server.root}`);
    console.log(`   editable  ${server.editable}`);
    console.log(`   auth      ${args.token ? 'token' : 'none'}`);
    if (!['127.0.0.1', '::1', 'localhost'].includes(shown)) {
      console.log('   ⚠  not bound to localhost — anyone who can reach this port can edit');
    }
    console.log('   Ctrl-C to stop');
  });
}

module.exports = { createServer, parseArgs, MAX_BODY };
