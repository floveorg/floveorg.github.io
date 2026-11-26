---
status: stable
section: data/mds
created: 2026-11-21
also: [development/standards/frontend/frontend.md#1320-data-depth-levels, development/pages.json]
---

# frontend/data-depth plan

> **Child plan.** The stable page owns the facts; this file records the dated
> source history and open plan decisions. Updated 2026-11-21.
> Its `data/mds` section follows the stable page
> `standards/frontend/frontend.md#1320-data-depth-levels`, not the folder name —
> the same convention puts the `plans/data/*` plans under `ai/*` sections.

## Source index

### bridges/oasis.md — 2026-08-01

- Archive: `development/archive/old/bridges/oasis.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/browsy-questions.md — 2026-08-01

- Archive: `development/archive/old/browsy/browsy-questions.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/pre-build/README.md — 2026-11-17

- Archive: `development/archive/old/browsy/pre-build/README.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### browsy/rationale.md — 2026-11-17

- Archive: `development/archive/old/browsy/rationale.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### others/flove-libs-insights.md — 2026-08-01

- Archive: `development/archive/old/others/flove-libs-insights.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### plans/central-backend.md — 2026-08-01

- Archive: `development/archive/old/plans/central-backend.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### questy-proposals.md — 2026-11-15

- Archive: `development/archive/old/questy-proposals.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### root/adoption.md — 2026-08-01

- Archive: `development/archive/old/root/adoption.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### root/backend.md — 2026-08-01

- Archive: `development/archive/old/root/backend.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

### standards.md — 2026-08-01

- Archive: `development/archive/old/standards.md`
- Stable home: `development/standards/frontend/frontend.md#1320-data-depth-levels`
- Status: summarised in the stable page; no open decision is recorded here.

## Export & share §13.12 redesign — 2026-11-25

> Executed 2026-11-25. Destination: inlined into
> `development/standards/frontend/frontend.md` §13.12 (replacing its two-line
> stub); `frontend/export.md` and `skills/exporty/` were deleted after the live
> pointers were repointed. Scope is **JSON and HTML only**: the summary panel and
> the Magic row stay owned by `frontend/summary.md` and were not copied here.
> The runtime-only checks moved to `jsony/export-surface.md`.

1. **Model** — summary section vs portrait file; one model; `flove-portrait/1` envelope; parity; hostile input; filename.
2. **Share** — Magic → Share, Save inside Share, native sheet, `canShare({files})`, DOM hooks.
3. **Renderer** — Rendery (`development/addons/rendery/index.html`) as the live view, HTML/XML, source URL sanitizing; card from the same rows.
4. **Exceptions** — `EXPORT_EXCEPTIONS` set, keys/souls/fivy/worthing variants, archived serializers.
5. **Runtime conformance** — the check table plus the "green ≠ filled-data parity" warning.
6. **Pages outside the contract** — the exempt-page table and the distro/offline rule.
7. **Conflict resolved** — the six-format DOM rows in `frontend/summary.md` were relabelled as legacy debt and their canonical hooks changed to `data-flove-save="json"` (+ `"html"` where shipped); `data/schemas/puzzy.md` now says the HTML card, not six formats. The summary panel and Magic row were not copied — both remain owned by `frontend/summary.md`. Older apps still carrying `save-fmt-*` markup are pending app conversion, not a second standard.
