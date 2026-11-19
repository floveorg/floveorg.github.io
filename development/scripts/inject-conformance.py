#!/usr/bin/env python3
"""Insert the runtime conformance() block into every app that exposes a portrait.

The block is inert until called: development/tools/conformance.html loads each
app in an iframe and calls window.flovePortrait.conformance(). It never writes
user data — merge() is exercised with an empty envelope only.

Usage:
  python3 development/scripts/inject-conformance.py --check   # report missing / drifted
  python3 development/scripts/inject-conformance.py --apply   # write the block
"""

from __future__ import annotations

import argparse
import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = "<!-- flove-conformance:start -->"
END = "<!-- flove-conformance:end -->"

BLOCK = """\
<!-- flove-conformance:start -->
<script data-flove-conformance>
/* Runtime conformance — dev harness: development/tools/conformance.html
   Supersedes selfTest(); never writes user data (merge gets an empty envelope).
   Parity vs floveFields() is advisory: rows are semantic layers, not a field
   dump, so an app's field ids may not appear verbatim. */
(function(){
  var api = window.flovePortrait;
  if (!api || typeof api.get !== 'function' || typeof api.conformance === 'function') return;

  function flatFields(list, out){
    out = out || [];
    (list || []).forEach(function(f){
      if (!f || !f.id) return;
      out.push(f.id);              // leaf ids are already dotted (bonds.friendship)
      if (f.fields) flatFields(f.fields, out);
    });
    return out;
  }
  function norm(s){
    return String(s == null ? '' : s).toLowerCase()
      .replace(/[\\s_:.\\/-]+/g, '.').replace(/^\\.+|\\.+$/g, '');
  }
  function slug(s){
    return String(s == null ? '' : s).toLowerCase()
      .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }

  api.conformance = function(opts){
    opts = opts || {};
    var checks = [];
    function check(name, ok, level, detail){
      checks.push({ name: name, ok: !!ok, level: level || 'critical',
                    detail: detail == null ? '' : String(detail) });
    }

    var p = null, getError = '';
    try { p = api.get(); } catch (e) { getError = e && e.message || String(e); }
    check('get() returns an envelope', p && typeof p === 'object', 'critical', getError);
    if (!p || typeof p !== 'object'){
      return { ok: false, app: null, checks: checks, errors: ['get()'], coverage: null };
    }

    var app = slug(p.app);
    check('schema is flove-portrait/1', p.schema === 'flove-portrait/1', 'critical', p.schema);
    check('app slug is present', !!app, 'critical', p.app);

    var filename = app + '-portrait.json';
    check('filename is <app>-portrait.json',
          /^[a-z0-9][a-z0-9-]*-portrait\\.json$/.test(filename), 'advisory', filename);
    var json = '';
    try { json = JSON.stringify(p); } catch (e) { json = ''; }
    var mime = '';
    try { mime = new Blob([json], { type: 'application/json;charset=utf-8' }).type; } catch (e) {}
    check('blob MIME is application/json;charset=utf-8',
          mime === 'application/json;charset=utf-8', 'advisory', mime);
    check('envelope survives JSON.stringify', json.length > 2, 'critical', json.length + ' chars');

    var v = null;
    try { v = api.validate ? api.validate(p) : null; }
    catch (e) { v = { ok: false, errors: [e.message] }; }
    check('validate() accepts the envelope', v && v.ok, 'critical',
          v && (v.errors || []).join('; '));

    var rows = Array.isArray(p.rows) ? p.rows : null;
    check('rows[] is an array', !!rows, 'critical', rows ? rows.length + ' rows' : typeof p.rows);
    if (!rows){
      return { ok: false, app: app, checks: checks, errors: ['rows[]'], coverage: null };
    }

    var keys = [], items = [], blank = false, untitled = false;
    rows.forEach(function(r){
      r = r || {};
      var k = norm(r.key);
      if (k) keys.push(k);
      var list = Array.isArray(r.items) ? r.items : [];
      if (list.length && !String(r.title || '').trim()) untitled = true;
      list.forEach(function(it){
        if (it === null || it === undefined) { blank = true; return; }
        if (typeof it === 'string' && !it.trim()) { blank = true; return; }
        items.push(typeof it === 'object' ? JSON.stringify(it) : String(it));
      });
    });
    check('row keys are unique', new Set(keys).size === keys.length, 'critical',
          keys.length + ' keys');
    check('items are never blank', !blank, 'critical');
    check('filled rows have a title', !untitled, 'critical');

    var fieldsSource = window.floveFields, fields = [];
    var fieldsKind = typeof fieldsSource;
    try {
      if (fieldsKind === 'function') fields = flatFields(fieldsSource() || []);
      else if (Array.isArray(fieldsSource)) fields = flatFields(fieldsSource);
    } catch (e) {}
    check('floveFields() is callable', fieldsKind === 'function' || fieldsKind === 'undefined',
          'advisory', fieldsKind === 'function' || fieldsKind === 'undefined' ? '' : fieldsKind);
    var haystack = norm(keys.join(' ') + ' ' + items.join(' ') + ' ' +
                        (p.phrase || '') + ' ' + json);
    var mapped = fields.filter(function(id){ return haystack.indexOf(norm(id)) !== -1; });
    check('field ids discoverable in the portrait (parity is advisory)', true, 'advisory',
          mapped.length + '/' + fields.length + ' fields · ' +
          Math.round(fields.length ? mapped.length / fields.length * 100 : 100) + '%');

    var c = null;
    try { c = api.consult ? api.consult(opts.consult || {}) : null; } catch (e) { c = null; }
    var consulted = c && Array.isArray(c.rows)
      ? c.rows.map(function(r){ return norm(r && r.key); }) : [];
    check('consult() returns flove-consult/1',
          c && c.schema === 'flove-consult/1' && Array.isArray(c.rows), 'critical',
          c && c.schema);
    check('consult() rows are a subset of get() rows',
          consulted.every(function(k){ return keys.indexOf(k) !== -1; }), 'critical',
          consulted.length + ' consulted');

    var merged = null, mergeError = '';
    try {
      merged = api.merge
        ? api.merge({
            schema: 'flove-portrait/1', app: p.app, version: 1,
            generatedAt: p.generatedAt, lang: p.lang,
            rows: [{ key: '__conformance__', kind: 'probe', title: '', items: [] }],
            consent: p.consent, source: p.source
          })
        : null;
    } catch (e) { mergeError = e && e.message || String(e); }
    check('merge() accepts a probe row without applying it',
          merged && merged.ok === true && (merged.applied || 0) === 0, 'advisory',
          mergeError || (merged ? 'applied ' + (merged.applied || 0) : 'no merge()'));

    var errors = checks.filter(function(x){ return !x.ok && x.level === 'critical'; })
                       .map(function(x){ return x.name; });
    var advisories = checks.filter(function(x){ return !x.ok && x.level === 'advisory'; })
                           .map(function(x){ return x.name; });
    return { ok: errors.length === 0, app: app, checks: checks,
             errors: errors, advisories: advisories,
             coverage: fields.length ? { mapped: mapped.length, total: fields.length } : null };
  };
})();
</script>
<!-- flove-conformance:end -->
"""


def candidates() -> list[Path]:
    """Every routing app that exposes a portrait — manifest or not (keys has none)."""
    routing = json.loads((ROOT / "tools/routing.json").read_text(encoding="utf-8"))
    out = []
    for app in routing.get("apps", []):
        url = str(app.get("url") or "")
        if not url.endswith(".html"):
            continue
        path = ROOT / url
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        # The shared header defines a fallback (flovePort) on every page. Require
        # a real bridge: an object or an assigned get().
        if not re.search(r"window\.flovePortrait\s*=\s*\{", text) and \
           not re.search(r"window\.flovePortrait\.(get|conformance)\s*=", text):
            continue
        out.append(path)
    return out


def injected(text: str) -> str:
    if START in text and END in text:
        head, rest = text.split(START, 1)
        _, tail = rest.split(END, 1)
        return head + BLOCK.rstrip("\n") + tail
    idx = text.rfind("</body>")
    if idx == -1:
        return text.rstrip("\n") + "\n" + BLOCK
    return text[:idx] + BLOCK + text[idx:]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only (default)")
    ap.add_argument("--apply", action="store_true", help="write the block")
    args = ap.parse_args()

    missing, drifted, changed = [], [], 0
    for path in candidates():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if START not in text:
            missing.append(path)
            continue
        new = injected(text)
        if new != text:
            drifted.append(path)
            if args.apply:
                path.write_text(new, encoding="utf-8")
                changed += 1
        elif args.apply:
            pass
    if missing:
        if not args.apply:
            for path in missing:
                print(f"missing  {path.relative_to(ROOT)}")
        if args.apply:
            for path in missing:
                text = path.read_text(encoding="utf-8", errors="ignore")
                path.write_text(injected(text), encoding="utf-8")
                changed += 1
    if drifted and not args.apply:
        for path in drifted:
            print(f"drifted  {path.relative_to(ROOT)}")
    total = len(missing) + len(drifted)
    if args.apply:
        print(f"conformance: {changed} file(s) written")
        return 0
    print(f"conformance: {total} file(s) need the block "
          f"({len(missing)} missing, {len(drifted)} drifted)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
