# Plan: Appy dashboard redesign — Profily shell, Appy truth

> 2026-11-20. Spec. Profily moves to `addons/` as a **design reference only**;
> Appy keeps every feature and every real value. Demo of this spec:
> `apps/appy/appy-next.html`.

## 1. Goal

1.1. Give Appy Profily's card-and-grid rhythm for **Apps played** without
     copying any of Profily's demo data.

1.2. Keep Appy's own username box (`#reg-handle`), JS tab system, plays bridge
     and every existing feature (§3).

1.3. Redo the theme mechanism once, on the canonical `flove:theme` key (§6),
     instead of maintaining a third, unused toggle.

## 2. Sources and ownership

| Fact | Source |
|---|---|
| App routes and fields | `tools/routing.json` (app entry points at `apps/appy/index.html`) |
| Tree / Types view | `development/index.html` |
| Reference design | `addons/profily.html` (moved from `apps/appy/profily.html`) |
| Plays record and rollout | `development/standards/frontend/export.md` §Share → Appy rollout |
| Shared HTML renderer | `development/addons/rendery/index.html` (`accept()` → `profileHtml()`) |
| Theme contract | `development/standards/frontend/frontend.md` §13.14 |

**Profily as reference.** Its `.apps-grid` / `.app-card` rhythm
(`profily.html:859-901`) is the visual model. Its content is **not**: handle
"Marc", `@marcflove`, Soul stats, Ada/Lex/Rafa/Nora trusts, offers, Wanty data
copied from `wanty.html`, wizards copied from `blogy-normal-css.html`, and the
hardcoded `APPS` array (`profily.html:1146-1237`, `1307-1357`, `1606-1630`)
are demo fixtures and stay out of Appy. Only `flove:profily:subavatars` is
persisted there (`profily.html:1643-1655`); Appy does not read it.

## 3. Feature lock — no regressions

Anchors are in `apps/appy/index.html`; the demo changes CSS and markup only.

| Area | Anchor |
|---|---|
| Self-contained runtime + i18n | `4-54`, `2155-2160`, `6638-6665` |
| Profile card and handle box | `2331-2370`, `4297-4300`, `4566`, `4580` |
| Plays launcher, upload, cards, bridge | `2294-2327`, `5866-6107`, `6162-6497` |
| Export / share / view profile | `4203-4285`, `3077-3081` |
| Wizy Magic | `2412-2428`, `4193-4200`, `5949-5967` |
| Authy / Browsy / Risa | `3330`, `3376-3384`, `3388`, `4509`, `4539` |
| Tiers / extension cards | `2460-2571`, `5716`, `5775` |
| Nety / MyNet | `4304-4320`, `5168`, `5230`, `5325` |
| Chat / Activity / Privacy | `2916-2941`, `5274`, `2952-2996`, `3576-3603`, `4828` |
| Keyboard and ARIA conventions | `2275-2284`, `6453-6455` |

## 4. Layout

4.1. **Header.** Keep the brand button and the editable `#reg-handle` box
     unchanged. Stat chips appear only when a real key supplies a value
     (`flove:appy:plays`, Authy level, stage) — never a placeholder number.

4.2. **Apps played grid.** The existing detailed `#played-grid` is currently
     hidden with `d-none` (`index.html:2436`). In the demo it is visible and
     carries Profily's card rhythm (colour glyph, name, play metadata) while
     the card DOM built by `addPlayedApp()` (`6422-6458`) stays the same:
     `.ac-title`, `.ac-sub`, `.ac-body`, `.ac-card`, `.open`. The compact
     `#played-icons` row remains as the small-screen fallback.

4.3. **Detail.** Clicking a card keeps the `.open` toggle and the embedded
     `portraitHtml()` iframe. The canonical renderer is Rendery's `accept()`
     (`development/addons/rendery/index.html:538-553`); no second renderer is added.

4.4. **Tabs.** Same ids and order — profile · nety · mynet · chat · activity ·
     extensions · privacy (`index.html:2275-2284`). The JS `switchTab()` and
     `role=tablist` / `aria-selected` wiring are untouched.

## 5. Data contract — preserved exactly

5.1. **Record shape** written by all 54 apps: `{app, appId, category, schema,
     portrait, colour, url, via, date, id, file}`. Bridge records replace the
     same app; uploads stay as history (`index.html:5916-5923`).

5.2. **Live update.** Keep `storage`, `focus`, `visibilitychange`
     (`6095-6097`, `6201-6203`), `refreshPlays()` (`6191-6199`) and
     `window.floveAppy.onChange(hydrateFromBridge)` (`6494`). Re-render only
     the plays grid — never reload the page.

5.3. **Handoff.** Keep the `flove-appy-ready` / `flove-appy-play` postMessage
     pair (`6208-6227`), the opener/origin check, the
     `schema === 'flove-portrait/1'` + `Array.isArray(rows)` validation, and
     the iframe-height message (`6461-6468`).

5.4. **Broken records.** A play whose portrait fails validation is discarded
     with a visible message, never shown as a blank card (pending **EXP03c**).

## 6. Theme redo (§13.14)

6.1. Neither `index.html` nor `profily.html` loads `apps/appy/flove-theme.js`;
     Profily's `--auto` / `--dark` bar CSS (`flove.css:145-156`) is inert
     because its markup uses a plain `.flove-bar`.

6.2. Use one canonical mechanism: a pre-paint inline script sets
     `data-theme` from `localStorage['flove:theme']` or the OS query; the
     toggle flips it and persists `light` / `dark`; unset follows the OS.
     The ◐ control sits in the topbar dropdown next to the language ball.

6.3. Both palettes are real and readable. Appy stops using `flove-theme.js`
     (key `flove-theme`, `.dark` class) — no second path in this app. The
     shared file itself stays: `apps/metas/index.html`, `apps/blogy/index.html`,
     `apps/trusty/index.html` and `apps/puzzy/index.html` still load it.

## 7. Dashboard customisation — planned only

7.1. A future `flove:appy:dashboard` key holds widget order and visibility
     with a fixed default layout.

7.2. No customisation UI or storage write in this pass.

## 8. Verification

8.1. `python3 tools/check-a11y.py --quiet` — exit 0.
8.2. `node --check` on every inline script changed in the demo.
8.3. **EXP03c** — inject a malformed play and confirm the visible discard.
8.4. **EXP06** — confirm the portrait iframe resizes via `flove-card-height`
     and that “See profile” opens `apps/appy/index.html#profile`.
8.5. Render the demo to PNG and inspect the plays grid, dark palette and
     compact fallback before merging into the live app.

## 9. Rollout

1. Write this spec; move Profily to `addons/`; point routing at
   `apps/appy/index.html` and regenerate `tools/routing-index.json`.
2. Build `apps/appy/appy-next.html` as a copy with the §4 CSS, the §6 theme
   and no data changes. The live app keeps working.
3. After sign-off, port the demo to `apps/appy/index.html` and delete the
   demo copy. No commit or push until asked.
