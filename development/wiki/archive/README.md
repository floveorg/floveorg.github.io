# Archive — opaque pre-cutover snapshot

This directory is the **restore and evidence copy** of the files replaced by the
docs → wiki migration (2026-11-21).

- `old/` is byte-identical to the pre-cutover sources; `SHA256SUMS` and
  `manifest.json` verify it.
- Every manifest entry is `status: archived`, `live: false`, `owner: null`.
- Nothing here is an owner. No task, hito, page or gate may use an archived path
  as its live destination.
- The archive is excluded from `wiki.json`, the docs manifest and every content
  gate. Links to it are historical citations only.
- Do not edit files under `old/`. To change a fact, edit its live owner under
  `development/standards/` or `development/wiki/`; the archive stays frozen.

The live owners are the 19 topic pages, the standing books, `wiki/INDEX.md` and
the register under `wiki/work/`.
