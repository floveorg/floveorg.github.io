# flove central · apps

Central distro apps. The canonical spec for flove apps — see
[`development/standards/`](../../development/standards/). Shared libs live in
[`central/shared/`](../shared/) (never per-app).

## Structure

```
central/
├── apps/                ← you are here — central app HTML files (flove.org deploy)
├── backend/             ← FastAPI + Turso (Railway deploy)
└── shared/              ← shared libs (read-only for both pipelines)
    ├── routing.json     — app registry (id, url, tier, tags)
    ├── css/
    │   ├── flove.css    — theme vars + toggles + wizy chips + reduced motion
    │   └── flove-base.css
    ├── js/
    │   ├── flove.js     — sound engine + summary actions + sound depth + wizard + resume
    │   ├── flove-i18n.js — language toggle (EN/ES/FR/DE/PT)
    │   ├── flove-loader.js — browsy-gift pro-enrichment loader
    │   ├── flove-settings.js
    │   └── flove-sound.js
    └── scripts/         — dev tooling (enrichment transformer + CI lint)
        ├── flove-enrich.py
        └── flove-loader-check.py
```

## Usage in apps

```html
<link rel="stylesheet" href="../shared/code/css/flove.css">
<script src="../shared/code/js/flove.js" defer></script>
<script src="../shared/code/js/flove-i18n.js" defer></script>
```

## Modules in flove.js

- **Sound engine** — click sounds via data-attributes, Web Audio synth
- **Summary actions** — collect/save/share data (txt, csv, xml, json, html, jpg, zip)
- **Sound depth** — Mini/Basic/Normal/Advanced/Super speech levels
- **Wizard** — bot text injection (magic/lovely/joy/wisdom)
- **Resume** — declarative resume buttons (copy, print, publish, insight cycle, magic toggle)
- **Autowire** — zero-config decoration for blogy.html

## Workflow

Gitea serves for agent development. Agents commit edits grouped by issue when meaningful for future recovery. If an agent holds edits >24h without committing, auto-commit as-is. Requests should not bump.
