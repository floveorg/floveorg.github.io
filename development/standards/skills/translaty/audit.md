# translaty audit, base and strip

`translaty0` is read-only. It audits translaty-marked strings (language spans
and `data-*` attributes), not arbitrary prose, and skips `<script>`, `<style>`,
`<pre>`, `<code>` and `<kbd>`.

## Commands

```bash
# one file: structural gate + every marked group has the base language
node development/scripts/check.js app.html

# translaty0: missing base, coverage, orphan spans (read-only)
node development/scripts/check.js --audit app.html
node development/scripts/check.js --audit app.html --json

# portfolio ledger for check-distro
node development/scripts/check.js --all --json --out tools/i18n-ledger.json
node development/scripts/check.js --all --md
node development/scripts/check.js --all --strict   # exit 1 if anything lacks the base
```

`--base` defaults to `en`. A single-language page with no spans passes.

## `--base es`

The three Spanish-first projects — `liberada`, `futbolia`, `dinámicas electrónicas`
— use Spanish as the base. Set `<html data-base="es">`, keep `lang-es` checked,
and key the attributes from `es` (`data-es`, `data-ph-es`, `data-aria-es`).
Extra languages keep their 3-line toggle block; only the checked default changes.
Run `check.js --base es`.

## `--strip`

```bash
node development/scripts/strip.js app.html --lang es          # dry-run
node development/scripts/strip.js app.html --lang es --write
```

Removes `span.es`, `data-es`/`data-ph-es`/`data-aria-es`/`data-title-es`, the
worldball option `lang-es` and its CSS toggles. It refuses to strip the base
language and stops before writing if a leftover would remain. Run `check.js`
afterwards.

## Ledger

`--all` emits `flove-i18n/1`:

```json
{
  "schema": "flove-i18n/1",
  "base": "en",
  "summary": {
    "files": 12,
    "filesWithMarkers": 10,
    "groups": 340,
    "missingBase": 2,
    "coverage": {"en": 99.98, "es": 100}
  },
  "excluded": ["projects/liberada"],
  "files": [
    {"path": "apps/trusty/trusty.html", "groups": 42, "missingBase": 0,
     "coverage": {"en": 100, "es": 98}, "issues": []}
  ]
}
```

`check-distro` reads `summary.missingBase` and `summary.coverage` from
`tools/i18n-ledger.json` and reports them softly; the hard gate stays on the
single file.

## Limits

- Coverage is per marked group, not per character or per visible sentence.
- A Spanish page with no translaty spans is invisible to this audit; use a
  language pass or the `LANG01` report to find those.
- Generated exports (`development/index.html`, `docs/index.html`,
  `vocabulary.*`) are audited, but the fix belongs in their source.
