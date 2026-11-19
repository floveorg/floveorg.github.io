# docsify-edit

WYSIWYG editing for [docsify](https://docsify.js.org), saved back to the
Markdown files. You edit the rendered page — not a Markdown textarea — and the
plugin writes the `.md` file through a tiny local save API.

It is deliberately a **plugin**, not a hard fork: docsify is upgraded normally,
and the editor can be bundled into a fork when you want it on by default.

```
rendered page ──contenteditable──▶ turndown ──▶ POST /save ──▶ .md on disk
      ▲                                                         │
      └──────────────── docsify re-render ◀─────────────────────┘
```

## Why it is safe to edit

The plugin does not re-serialize the whole page. It snapshots every top-level
block, tracks which blocks you actually touched, and writes back:

- **untouched blocks**: kept byte-for-byte from the original `.md` (line
  wrapping, table padding, HTML comments, code fences, YAML front-matter);
- **touched blocks**: converted from the rendered DOM back to Markdown;
- **unchanged page**: the original file is returned untouched.

A `base` SHA-256 of the file is sent with every save, so a stale tab cannot
overwrite a newer version: the server answers `409 conflict`.

## Quick start

The repository ships a **standalone demo** at
[`addons/docsify-edit/`](../../addons/docsify-edit/README.md) (docsify + this
plugin + three sample pages). `./build-demo.sh` syncs the plugin and vendor into
it.

### 1. Load the plugin

```html
<script src="vendor/docsify-edit.js"></script>
<script>
  window.$docsify = {
    edit: {
      endpoint: '/__edit',
      // default: page-relative vendor/ — point these at wherever Turndown lives
      paths: {
        turndown: 'vendor/turndown.min.js',
        gfm: 'vendor/turndown-plugin-gfm.min.js'
      }
    },
    plugins: [window.DocsifyEdit && DocsifyEdit.plugin].filter(Boolean)
  };
</script>
<script src="vendor/docsify.min.js"></script>
```

The package ships Turndown under `tools/docsify-edit/vendor/`; if you copy the
plugin into `vendor/`, copy those two files beside it or adjust `edit.paths`.

The plugin only shows its **Edit page** button when the save API answers. On a
static host it stays invisible. By default it pings only on localhost; set
`edit.allowRemote: true` if the save server lives elsewhere (put it behind
authentication).

### 2. Run a save server

```bash
# Node (self-contained, zero dependencies)
node tools/docsify-edit/server/node/server.js \
  --port 8642 --root . --editable docs

# Python (the flove repository's reference server)
python3 tools/serve-edit.py --port 8642
```

Open the site, click **✎ Edit page**, edit, then **Save** / `Ctrl+S`.
**Cancel** / `Esc` discards.

## Server API

| Method | Path | Body | Response |
|---|---|---|---|
| `GET` | `/__edit/ping` | — | `{ok, api, version, editable, auth, maxBody}` |
| `POST` | `/__edit/save` | `{path, markdown, base?, dryRun?}` | `{ok, path, bytes, base, backup, mtime}` |

`path` is relative to the editable directory. `base` is the SHA-256 of the raw
file when editing started. Errors are JSON `{ok:false, code, error}` with
`400/403/404/409/413/500`.

The server must be same-origin; `Origin` is checked on every POST. It binds to
localhost by default and refuses symlinks/paths outside the editable directory.
Writes are atomic and serialized per path. Backups go to
`~/.cache/docsify-edit/` (200 most recent).

## Configuration

| Key | Default | Meaning |
|---|---|---|
| `endpoint` | `'/__edit'` | API base; ping is `endpoint + '/ping'`, save is `endpoint + '/save'` |
| `scope` | `null` | expected `editable` path from the server; hides the button on the wrong server |
| `paths.turndown` | `'vendor/turndown.min.js'` | Turndown script, loaded on first edit |
| `paths.gfm` | `'vendor/turndown-plugin-gfm.min.js'` | GFM tables/strikethrough/task lists |
| `labels.*` | English | Button/status labels (`edit`, `save`, `cancel`, `editing`, `saving`, `saved`, `unsaved`, `nothing`, `hint`) |
| `width` | `80` | Wrap width for paragraphs you edit |
| `toolbar` | `true` | Show bold/italic/headings/lists/links/undo |
| `reloadOnSave` | `true` | Reload after a successful save |
| `allowRemote` | `false` | Ping from a non-localhost hostname |
| `unregisterServiceWorker` | `true` | Remove a dev service worker so assets stay fresh |
| `token` | `null` | Sent as `X-Edit-Token`; the server can require it |
| `onSaved` | `null` | `function ({path, markdown, response})` after a successful save |

## What you can edit

- paragraphs, headings, bold/italic, links, images, lists, quotes, code;
- tables (GFM), task-list checkboxes, inline code;
- YAML front-matter is preserved and hidden from the editor;
- HTML comments (e.g. tracking markers) are preserved;
- `Enter`/`Tab` insert a new line/two spaces inside code blocks;
- `Ctrl+S` saves, `Esc` cancels, the toolbar keeps the selection.

Known limits:

- Markdown/HTML constructs that docsify does not render (e.g. raw reference
  definitions) are not visible to edit; untouched blocks are still preserved.
- A paragraph and an adjacent list can be reflowed when you edit that block;
  untouched blocks are not affected.
- The plugin needs a save server. A purely static docsify site cannot write
  files.

## Using it in a docsify fork

A fork is only necessary if you want editing **enabled by default** or want the
save server in the same repo. Otherwise, ship this as a plugin.

To bundle it in a fork:

1. Copy `src/docsify-edit.js` into the fork (or import it as a plugin module).
2. Register it in the docsify bootstrap:
   ```js
   Docsify.plugins = [].concat(Docsify.plugins || [], DocsifyEdit.plugin);
   ```
3. Ship the save server (Node) next to the docs, or document the API.
4. Keep the server same-origin and authenticated if exposed beyond localhost.

The plugin uses only the public docsify plugin API (`hook.mounted`,
`hook.doneEach`, `vm.route.path`, `vm.config`), so it survives normal docsify
upgrades.

## Tests

```bash
# Python server: security, conflicts, CRLF/BOM, dry-run, tokens
python3 tools/test_serve_edit.py

# JavaScript: Markdown round-trip helpers (node:test)
cd tools/docsify-edit && npm test
```

The browser end-to-end suite lives in `test/e2e.js` and needs a running site +
save server. It covers typing, bold, task toggles, code-block Enter, tables,
deletes, no-op saves and conflict handling.

## License

MIT. Turndown and turndown-plugin-gfm are MIT (see `LICENSE`).
