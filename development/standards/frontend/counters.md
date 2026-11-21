# flove · Counters — §13.8

Part of the flove frontend standards catalogue. Index / matrix: `../README.md` · contract: `../contract.md` · back to the catalogue: `../frontend.md`.

---

## 13.8 · Counters (floating arcade chips)

Three fixed bottom-left chips that track user engagement: **Clicks ·
Selections · Stars**. Hidden until each chip has ≥1 point; they count and
paint, and nothing gates on them (the old tier gate was removed — see the
bottom of this page).

**Markup (canonical):**

```html
<div class="float-counters" aria-live="polite">
  <div class="pc pc-clicks is-empty" id="chipClicks" title="Total clicks">
    <div class="pc-badge"><span class="pc-num" id="pointsClicks">0</span></div>
    <span class="pc-label">Clicks</span>
  </div>
  <div class="pc pc-sel is-empty" id="chipSelections" title="…">
    <div class="pc-badge"><span class="pc-num" id="pointsSelections">0</span></div>
    <span class="pc-label">Selections</span>
  </div>
  <div class="pc pc-stars is-empty" id="chipStars" title="…">
    <div class="pc-badge"><span class="pc-num" id="pointsStars">0</span></div>
    <span class="pc-label">Stars</span>
  </div>
</div>
```

**Vocabulary (`pc-*` family):**

| Class | Role |
|-------|------|
| `float-counters` | Fixed-position wrapper bottom-left, vertical flex |
| `pc` | One counter chip (clicks / sel / stars) |
| `pc.is-empty` | Hides the chip until it has ≥1 point |
| `pc.pulse` | Animation on increment (`ptPop` keyframes) |
| `pc-badge` | The shape (`clip-path` per type) with neutral fill + colour grow via `--col` custom prop |
| `pc-num` | The number text |
| `pc-label` | The lowercase label ("Clicks" / "Selections" / "Stars") |
| `pc-clicks` · `pc-sel` · `pc-stars` | Per-counter modifier — drives shape & colour |

Shapes (clip-path): clicks = dodecagon, selections = triangle,
stars = 5-pointed star. Colour fills (orange / orange / gold) grow
linearly with the count, saturating at the chip's growth-max.

**Canonical default saturation (Marc 2026-05-23):**

| Counter | Growth-max |
|---------|------------|
| Clicks | **100** |
| Selections | **100** |
| Stars | **5** |

These are the defaults all flove apps inherit. Apps may override per
chip if their UX needs different thresholds, but the defaults above are
the canonical reference, carried inline in the app that shows the chips
(Fivy is the live trunk example).

**Counting rules (declared by Marc 2026-05-23):**

| Counter | Rule |
|---------|------|
| **Clicks** | +1 on every click anywhere in the page (cumulative). |
| **Selections** | Live count of the currently-checked: hearts (`#rater-show-*`) + emojis (`name^="rate-"`) + labelers (`name="topbar-labeler"` non-none) + wizards (`name^="wizard-choice-"` non-none) + non-empty textareas. |
| **Stars** | Live count of non-empty textareas (whether typed by the user OR injected by a wizard). |

**JS module — `window.flove.counters`:**

| Member | Use |
|--------|-----|
| `refresh()` | Recompute and repaint all three chips |
| `clicks` (getter) | Cumulative click count |
| `selections` (getter) | Live selection count |
| `stars` (getter) | Live star count |
| `addClick()` | Manual hook to bump the click counter (e.g. for synthetic events) |

**Distro:**

- **Every app that shows counters** inlines the block with the rest of its
  common layer — there is no shared file to load (self-containment rule,
  2026-11-15). Fivy is the live reference: markup in `.float-counters`, module
  at the tail of its inlined `flove.js`.
- Apps that do not need counters simply omit the markup; nothing else changes.

Reference impl: the counters block at the tail of Fivy's inlined `flove.js`.

**Collapse + timer toggles (Marc 2026-05-28):**

Two ~26 px round chips wrap the counter stack — both sit inside
`.float-counters` and share the badge palette (`#dcd5d5` neutral, accent
ink). They MUST be ~40 % smaller than the Clicks badge so they read as
satellites, not peers.

```html
<div class="float-counters" aria-live="polite">
  <div class="pc-advance-text" id="advanceText" hidden>…</div>
  <button class="pc-toggle pc-collapse" id="countersCollapse">−</button>
  <div class="pc pc-clicks …">…</div>
  <div class="pc pc-sel …">…</div>
  <div class="pc pc-stars …">…</div>
  <button class="pc-toggle pc-timer-toggle" id="timerToggle" aria-pressed="false">+</button>
  <div class="pc-timer" id="pcTimer" aria-live="polite">
    <div class="pc-timer__row"><span>Total</span><b id="timerTotal">0s</b></div>
    <div class="pc-timer__row"><span>Clicks</span><b id="timerClicks">0</b></div>
    <div class="pc-timer__row"><span>Avg gap</span><b id="timerAvg">—</b></div>
    <div class="pc-timer__row"><span>Last</span><b id="timerLast">—</b></div>
  </div>
  <button class="pc-toggle pc-expand" id="countersExpand">+</button>
</div>
```

| Class | Role |
|-------|------|
| `pc-toggle` | Base round 26 px chip (shared by collapse / timer / expand) |
| `pc-collapse` | "−" above the stack — adds `is-collapsed` to `.float-counters` |
| `pc-timer-toggle` | "+" below the stack — adds `is-on` to `#pcTimer`, flips its glyph to "−" |
| `pc-expand` | "+" shown only when `.float-counters.is-collapsed` — restores default state |
| `pc-timer` / `pc-timer__row` | Timer panel + its label/value rows |

Behaviour rules:

- **Collapse** (`pc-collapse` → `.is-collapsed`): hides the chips, the
  unlock text, the timer panel, and both `pc-collapse` / `pc-timer-toggle`
  themselves; leaves only `pc-expand`. Collapsing also force-hides the
  timer panel (do not preserve `is-on` across collapse).
- **Timer** (`pc-timer-toggle` → `pc-timer.is-on`): souls-style event
  log (each document click pushes `Date.now()` into a soft-capped 500-
  entry array). Rows: **Total** (`now − first`), **Clicks** (count),
  **Avg gap** (mean Δ between consecutive events, `—` until ≥ 2 events),
  **Last** (`now − last`). Tick `renderTimer` once per second while the
  panel is open; clear the interval when closed/collapsed. Duration
  format = the souls `fmtDuration` (sub-10 s shows `1.4s`, then `s` /
  `m s` / `h m`).
- **Click counting**: the toggle clicks DO count toward the page's
  cumulative `Clicks` counter (no `stopPropagation` on the buttons —
  consistent with "any click anywhere on the page").

Reference impl: the counters block at the tail of Fivy's inlined `flove.js`.
There is no shared timer module — each app keeps its own inline copy, which is
the self-containment rule.

### Threshold unlocks — removed from the trunk (2026-11-15)

Counters used to drive WIP `tier-pop` unlocks (`clicks ≥ 20`,
`selections ≥ 10`, `stars ≥ 2`), a `.dl-btn` level message and an iframe
preview of the locked tier. **All of it is gone from this trunk**: the
`UNLOCK` map, `checkUnlocks()`, `showDlMessage()`, `openTierIframe()` /
`closeTierIframe()` and the `#unlockToast` / `#tierIframeOverlay` markup were
removed from `addons/code/js/flove.js` and from every inlined copy.

The counters themselves stay: they count and paint, nothing more. The gated
variant survives only in the demo sketch `apps/blogy/`, which is not part of
the trunk. See `development/wiki/archive/old/plans/2026-11-14-app-tier-planned.md`.
