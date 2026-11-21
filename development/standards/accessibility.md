<!-- CONTEXT:BEGIN
schema: flove-page/1
id: frontend/accessibility
path: development/standards/accessibility.md
trunk: frontend
topic: accessibility
kind: topic
status: stable
html_place: ["#apps"]
owns: ["a11y baseline", "axe report"]
updated: 2026-11-21
read_next: ["#accessibility-audit","#contrast-audit","#extraction-consent","#frontend-catalogue-in-accessibility","#accessibility-report"]
supersedes:
  - development/wiki/archive/old/a11y-report.md
  - development/wiki/archive/old/browsy/spec.md
heavy: false
CONTEXT:END -->

# Accessibility

> **Stable page.** Migrated from the pre-cutover sources on 2026-11-21.
> The chapters below are the only owners; the child plan records source history.


## Accessibility audit

> Source: `development/wiki/archive/old/a11y-report.md` (archived 2026-11-21).

Generated axe-core + keyboard audit for the flove apps. Regenerate with
`python3 tools/check-a11y-axe.py --md development/wiki/archive/old/a11y-report.md`.
Chrome headless + axe 4.10.2; the static gate remains `tools/check-a11y.py`.

Last generated result: **0 violation nodes across 0 rules** (49 apps).

## Contrast audit

> Owner: accessibility. Token pairs from `frontend/frontend.md` and the inlined
> `flove.css`; measure light and dark.

Every token pair (ink/bg, ink-2/panel, line/bg, signal/panel, accent/ink) has a
measured contrast ratio. The release-blocking threshold is recorded here; a
failing pair blocks a release until fixed or explicitly excepted.

## Extraction consent

> Owner: accessibility/experience; spec: Browsy bridge consent (Q005).

Extraction shows a persistent indicator while pulling, a one-action **Stop**, and
a per-site allowlist. The allowlist persistence decision is recorded here; no
silent pull is allowed.

## Frontend catalogue in accessibility

> Source: `frontend/frontend.md` §13/§14 accessibility pass.

The §13 and §14 accessibility rows are applied to the catalogue. Every row has an
owner; exceptions are recorded in the Work page, not silently skipped.

## Accessibility report

> Source: archived axe-core + keyboard report.

The report lists axe and keyboard results for every in-scope page. Regenerate with
`python3 tools/check-a11y-axe.py --md`; the static gate is `tools/check-a11y.py`.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/a11y-report.md` | 2026-11-19 | development/standards/accessibility.md |
| `archive/old/browsy/spec.md` | 2026-11-17 | development/standards/accessibility.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
