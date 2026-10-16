# flove libs: questy abstraction insights

Lessons from abstracting questy into `flove.css` — what works, what's missing,
and where the standards should evolve.

## What questy demonstrated

Questy was a fully self-contained 1856-line HTML file with ~350 lines of
inline CSS. After linking `../../libs/flove.css` and mapping tokens:

- **Removed**: reset (`*{margin:0;padding:0;box-sizing:border-box}`), utility
  classes (`.hidden`, `.flex-1`), body base styles — all provided by flove.css
- **Kept**: ~300 lines of questy-specific component CSS (perspective cards,
  tabs, addons, prompt preview, wisy chips)
- **Mapped**: `--text→--ink`, `--surface→--card`, `--border→--line`,
  `--green→--signal`, `--glow→--glow-a` via backward-compatible aliases

The flove.css import gives questy the shared reset, theme tokens, utility
classes, and a consistent dark palette — while questy only overrides what
it needs.

## File size leverage: where apps duplicate

Across the flove codebase, the same CSS patterns appear in every app:

| Pattern | Duplicated in | Lines each |
|---------|--------------|------------|
| Box-sizing reset | every app | 1 |
| Body font/color/bg | every app | 5-8 |
| Dark mode tokens | blogy, questy, lowai, appy | 10-15 |
| Focus ring styles | every app with forms | 3-5 |
| Button base styles | every app | 10-20 |
| Input/textarea/select | every app with forms | 15-25 |
| Utility classes (.hidden, .flex-*) | every app | 5-10 |

**Estimated waste**: ~60-80 lines per app × ~10 apps = ~600-800 lines of
duplicated CSS across the codebase.

### Recommendation: tiered imports

Not every app needs the full `flove.css`. Consider a tiered system:

```
flove-base.css    — reset, tokens, utilities (~50 lines)
flove-forms.css   — inputs, textareas, selects, focus rings (~40 lines)
flove-buttons.css — button styles, variants (~30 lines)
flove.css         — full suite (layout, nav, cards, feed, trust) (~880 lines)
```

Apps like questy that are "forms-heavy tools" could import `flove-base.css`
+ `flove-forms.css` + `flove-buttons.css` instead of the full stylesheet,
saving ~760 lines of unused CSS.

## Token standardization gaps

Questy revealed inconsistencies in how apps name their tokens:

| Concept | questy used | flove.css token | Standard? |
|---------|-------------|-----------------|-----------|
| Text color | `--text` | `--ink` | Yes (flove.css) |
| Card bg | `--surface` | `--card` | Yes (flove.css) |
| Border color | `--border` | `--line` | Yes (flove.css) |
| Success color | `--green` | `--signal` | Yes (flove.css) |
| Focus glow | `--glow` | `--glow-a` | Yes (flove.css) |
| Accent color | `--accent` | `--accent` | Yes (both) |

### Recommendation: canonical token table

The `contract.md` §2 lists 5 token families. It should expand to a
**complete token reference** that every app must use:

```css
:root {
  /* surface palette */
  --bg: ...;        /* page background */
  --ink: ...;       /* primary text */
  --muted: ...;     /* secondary text */
  --line: ...;      /* borders, dividers */
  --card: ...;      /* card/panel backgrounds */
  --panel: ...;     /* elevated surfaces */

  /* semantic palette */
  --accent: ...;    /* brand/interactive */
  --signal: ...;    /* success/positive */
  --warn: ...;      /* caution */
  --danger: ...;    /* error/destructive */

  /* effects */
  --glow-a: ...;    /* accent glow */
  --glow-s: ...;    /* signal glow */
  --glass: ...;     /* glassmorphism bg */
  --glass-border: ...;
}
```

Apps may override these in their local `:root` but must not invent new
surface/semantic tokens. Questy's aliases (`--text`, `--surface`, `--border`,
`--green`, `--glow`) should be the exception, not the norm.

## CSS-over-JS: what questy got right

Questy's form logic is ~800 lines of JS handling:
- Multi-select button toggles
- Radio-unselect patterns
- Collapse/expand with localStorage persistence
- Dynamic field generation (duplicate projects)
- JSON serialization for presets

None of this could be CSS-only — it involves data structures, localStorage,
and dynamic DOM creation. This is the legitimate JS territory that `contract.md`
§3 allows.

However, questy has CSS that could further leverage flove.css:
- **Focus rings**: questy's `input:focus { box-shadow: 0 0 0 3px var(--glow) }`
  matches flove.css's pattern — could use a shared `.field:focus` class
- **Button states**: questy's `.opt.selected` / `.opt:hover` patterns are
  nearly identical to flove.css's button variants — could share a base

### Recommendation: shared interaction classes

Add to `flove-base.css`:

```css
.flove-focus:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--glow-a);
}

.flove-selected {
  background: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
  font-weight: 600;
}
```

Apps could add these classes instead of redefining focus/selected styles.

## Standards evolution suggestions

### 1. `contract.md` should mandate the token table

Currently §2 says "always prefer tokens from flove.css" but doesn't list
all required tokens. A complete table prevents apps from inventing their
own names (as questy did with `--text`, `--surface`, etc.).

### 2. `frontend.md` should catalog CSS patterns

The 15 standards (§13.1-§13.15) cover behavioral patterns but not CSS
patterns. A new section could catalog:
- Focus ring styles
- Button state transitions
- Card/panel elevation patterns
- Form field styling conventions
- Responsive breakpoint tokens

### 3. `adoption.md` should track CSS abstraction level

For each app, track:
- [ ] Links `flove.css` (or `flove-base.css`)
- [ ] Uses canonical token names
- [ ] No invented surface/semantic tokens
- [ ] Shares interaction classes (focus, selected, hover)

### 4. Tiered CSS imports should be a standard

Apps at different tiers need different CSS:
- **nano/mini**: `flove-base.css` only (tokens + reset)
- **basic/normal**: `flove-base.css` + `flove-forms.css`
- **advanced/super**: full `flove.css`

This prevents nano apps from loading 880 lines of unused CSS and gives
advanced apps the full design system.

### 5. Token migration guide

For existing apps that use non-canonical names:
1. Add aliases in `:root` (`--text: var(--ink)`)
2. Gradually replace references in CSS
3. Remove aliases once all references are updated

Questy's approach (aliases in `:root` + gradual migration) is the pattern.

## Quantified savings

If all Central apps adopted the tiered import approach:

| App | Current CSS lines | With flove.css import | Savings |
|-----|-------------------|----------------------|---------|
| questy | ~350 | ~300 (import + overrides) | ~50 |
| blogy | ~200 | ~150 | ~50 |
| appy | ~174 | ~120 | ~54 |
| central/index | ~400 | ~300 | ~100 |

**Total**: ~450 lines saved across 4 apps, plus consistency gains.

## Next steps

1. Create `flove-base.css` (~50 lines) in `central/shared/`
2. Update `contract.md` §2 with the complete token table
3. Add CSS pattern catalog to `frontend.md`
4. Migrate questy to use `flove-base.css` + local overrides (next iteration)
5. Update `adoption.md` with CSS abstraction checklist
