# Astry Web · Living Wheel — Spec-Driven Plan

- **Status:** prototype implemented at `web/wheel/index.html` (Phase 1 subset; houses, export and composite remain)
- **Platform:** web (standalone page; not Chatland)
- **Implemented:** 10 bodies, 4 angles, 1–4 readings, moment/person comparison, live controls, text tables, shortest-arc animation.
- **Companion research:** `astry-cross-vocabulary.md`
- **Base:** the Western zodiac with 10 bodies, the four angles (ASC, DSC, MC, IC), and multi-reading comparison
- **Normative language:** **MUST**, **SHOULD**, **MAY** follow RFC 2119.

**One-sentence spec:** a web wheel where one to four readings are drawn simultaneously — 10 body positions and four angle anchors each — with verbs for signs, actions for lines, and a live display that can compare the same person across moments or two or more people, without turning astrology into a prediction or a compatibility score.

---

## 1. Product decisions up front

1. **“10 positions” = 10 bodies per reading:** Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto. The four angles (ASC, DSC, MC, IC) are **anchors**, not part of the 10. This is the plan’s interpretation; see §18 if the product means something else.
2. **The wheel is symbolic, not predictive.** No “today”, no “compatibility score”, no medical/financial claims.
3. **Angles are first-class.** ASC and DSC MUST be represented; MC and IC SHOULD be. If birth time or place is missing, angles are unavailable and the UI says so.
4. **Comparison is the point.** The wheel is built for one reading, but its reason to exist is overlaying two or more.
5. **Static web, local-first.** No server, no account, no birth data in URLs or analytics.
6. **SVG, not canvas-first.** The wheel must be accessible, selectable and exportable.

---

## 2. Goals and non-goals

### 2.1 Goals

- A single **living wheel** that shows 10 bodies per reading and 4 angles.
- **1–4 simultaneous readings** (same person at another moment, or 2–4 people).
- **Live custom display**: toggles and presets update immediately, with animation.
- **A shared vocabulary** for signs, planets, angles and lines: adjectives, verbs and line actions.
- **Accuracy**: real tropical longitudes, real ASC/DSC, declared orbs, no invented positions.
- **Accessibility**: a complete text alternative to the wheel.
- **Extensibility**: a future system (Vedic, Chinese, Mayan…) can be added without rewriting the wheel.

### 2.2 Non-goals

- No full chart interpretation, predictions, transits report, compatibility score.
- No Vedic/Chinese/Mayan/Celtic/Gipsy layers in this phase.
- No social network, accounts, comments or public profiles.
- No server-side storage of birth data.
- No native app work.
- No “AI reading” generation; the page is an instrument, not an oracle.

### 2.3 Success criteria

| Criterion | Target |
|---|---|
| Data accuracy | 10 bodies + 4 angles for a known chart within tolerance (§10) |
| Multi-reading | 2–4 readings, 10 markers each, no label collisions at 1280 px |
| Comparison | same-person moment overlay and 2-person overlay both work |
| Live controls | every toggle updates in < 100 ms without reload |
| Animation | time/moment change moves markers along the shortest arc |
| Text parity | the table below the wheel matches every visible marker and aspect |
| Privacy | zero network requests carrying birth data |
| Accessibility | keyboard-complete controls; wheel has a full text equivalent |
| Performance | initial page ≤ 150 KB before ephemeris; interaction at 60 fps |

---

## 3. The concept: “La Rueda Viva”

The page is a **visual instrument**. It should feel like a quiet astronomical table, not a horoscope app.

- The wheel is the main object.
- A reading is a **ring**.
- Each ring has 10 **marks** (bodies).
- Each reading has **angle axes**: ASC/DSC and optionally MC/IC.
- Lines between marks are **relations**; each relation has an action verb.
- A side panel reads the selected mark or line in plain language.
- Nothing spins continuously. The user moves the wheel; the wheel does not perform.

### 3.1 Page structure

```
Header
  title · short explanation · privacy note
Reading strip
  [Person A · 1990-04-12 08:30 · Madrid]  [+ Añadir lectura]
Wheel stage
  left: SVG wheel (rings, zodiac, angles, aspects)
  right: live detail panel (selected mark/line) + controls
Comparison panel
  readings legend · contact list · element/modality counts · angle contacts
Text tables
  bodies table · angles table · aspects table (accessible + printable)
Notes
  method · sources · “symbolic, not predictive”
```

---

## 4. What a reading is

### 4.1 Data model

```js
Reading {
  id: 'r1',
  label: 'Marc · natal',          // user-facing
  personId: 'p1',                 // local only, not a public id
  kind: 'natal' | 'moment',
  moment: {
    localISO: '1990-04-12T08:30',
    tz: 'Europe/Madrid',
    utcISO: '1990-04-12T06:30:00Z',
    julianDay: 2447993.7708,
  },
  place: {
    label: 'Madrid, ES',
    lat: 40.4168,
    lon: -3.7038,
    elevation: 0,                 // optional
  },
  bodies: {
    sun:     { lon: 22.41, sign: 'aries',   deg: 22.41, speed: 0.99, retro: false },
    moon:    { lon: 118.03, sign: 'cancer', deg: 28.03, speed: 13.2, retro: false },
    mercury: { … }, venus: { … }, mars: { … },
    jupiter: { … }, saturn: { … }, uranus: { … },
    neptune: { … }, pluto: { … },
  },
  angles: {                       // null if time/place unavailable
    asc: 8.22, dsc: 188.22,
    mc: 18.77, ic: 198.77,
  },
  meta: {
    zodiac: 'tropical',
    houseSystem: null,            // optional later
    ephemeris: 'swiss-ephemeris-wasm@x',
  },
}
```

### 4.2 Required inputs

| Input | Needed for | Rule |
|---|---|---|
| Date | bodies | required |
| Time | angles, houses | required for ASC/DSC/MC/IC |
| Time zone | UTC conversion | required; IANA zone, not a raw offset |
| Place (lat/lon) | angles, houses | required for angles |
| Consent | another person's reading | required for any non-self reading |

- If time is missing: `angles = null`; the wheel shows bodies only and a clear note.
- If place is missing: `angles = null`; same.
- If time zone is ambiguous (historical/DST): show a warning and the resolved UTC.
- Never guess a birth time to “make the wheel look complete”.

### 4.3 Reading kinds

- **natal** — a person at birth.
- **moment** — the same person at another date/time (a symbolic snapshot, not a “transit report”).
- **person** — another person's natal reading, used for comparison.
- **group** — 2–4 readings shown together.

The UI language is **“lectura”**, not “carta” unless a full chart view is on.

---

## 5. Comparison semantics

### 5.1 Modes

| Mode | Inputs | Wheel | Language |
|---|---|---|---|
| **Single** | 1 reading | 1 ring, 10 bodies, angles | “Lectura” |
| **Momentos** | same person, 2+ moments | 2–4 rings, same zodiac frame | “Dos momentos” |
| **Encuentro** | 2 people | 2 rings, cross-aspects | “Encuentro” |
| **Grupo** | 2–4 people | 2–4 rings | “Rueda compartida” |
| **Compuesto** | 2+ readings | midpoints (optional) | “Compuesto” — later |

### 5.2 What comparison means — and does not

- It shows **contacts**: two marks in relation by aspect, sign, angle or element.
- It does **not** compute a score, rank or verdict.
- It does **not** say “compatible / incompatible”.
- A “contact” has a neutral label: **contacto**, **tensión**, **flujo**, **ajuste**, **fusión** — derived from the aspect verb.
- The panel can say: “Marte de A tensa la Luna de B, orbe 2.1°.” That is a description of the diagram, not a prediction.

### 5.3 Cross-aspect rules

- Intra-reading aspects: 10 bodies → 45 pairs; apply the orb table; keep all major, cap minors.
- Inter-reading aspects: 10 × 10 per pair of readings; cap to the **strongest 24** by orb and weight; the table lists the rest on demand.
- Angle contacts: body ↔ ASC/DSC/MC/IC of another reading; tighter orb (3–5°); label explicitly.
- Do not draw a dense hairball: default to major aspects only; minors are opt-in.
- Every drawn line has a matching row in the aspects table.

### 5.4 Privacy and consent

- Another person's birth data is sensitive. A non-self reading MUST show a consent checkbox: “Tengo permiso para usar estos datos.”
- Readings live in memory by default. No server, no analytics, no third-party requests.
- “Recordar solo mi lectura” may use local storage for the user's own reading; other people's readings are never persisted by default.
- Clear/reset removes readings from memory and local storage.
- URLs MUST NOT contain birth data. View preferences may use a hash; personal data must not.
- No export of another person's reading without an explicit action and a warning.

---

## 6. Wheel geometry

### 6.1 Two view modes

#### A. Zodiac mode (default for comparison)

- **Fixed zodiac frame.** 0° Aries at 9 o’clock; longitude increases counterclockwise.
- All readings share the same zodiac coordinates, so they can be compared.
- Each reading's ASC/DSC axis is drawn at its **actual longitude**; it is not forced to the left.
- MC/IC axes are drawn at their actual longitudes (optional).
- This is a “longitude wheel”, not a house-rotated natal chart.
- **Use for:** 2+ readings, same-person moments, any comparison.

#### B. Chart mode (single reading, optional)

- Rotate the zodiac frame so the reading's **ASC is at 9 o’clock**.
- MC/IC become the vertical frame (approximately; exact MC may not be 90° from ASC at all latitudes).
- Houses, if enabled, are drawn from the declared house system.
- **Use for:** one reading, familiar natal-chart view.
- **Do not use** for 2+ readings: each person would need a different rotation and the comparison would break.

### 6.2 The 10 positions

| # | Body | Glyph | Notes |
|---|---|---|---|
| 1 | Sun | ☉ | luminary |
| 2 | Moon | ☽ | luminary |
| 3 | Mercury | ☿ | |
| 4 | Venus | ♀ | |
| 5 | Mars | ♂ | |
| 6 | Jupiter | ♃ | |
| 7 | Saturn | ♄ | |
| 8 | Uranus | ♅ | modern |
| 9 | Neptune | ♆ | modern |
| 10 | Pluto | ♇ | modern |

- Markers are positioned by **ecliptic longitude**.
- Glyph + degree; retrograde `℞` optional.
- A marker is not a button in the SVG (too many focus stops); selection is via the text table and optional hover/focus on the marker group.
- Selected marker gets a halo and a detail card.

### 6.3 Angle anchors

| Anchor | Meaning | Drawing |
|---|---|---|
| **ASC** | eastern horizon | solid axis from centre to rim at `asc` |
| **DSC** | western horizon | opposite ASC; same axis, dashed half |
| **MC** | upper meridian | axis at `mc`; optional |
| **IC** | lower meridian | opposite MC; optional |

- ASC/DSC MUST be present when time+place exist.
- MC/IC SHOULD be present; allow toggling.
- Do not assume ASC–MC are 90° apart; at high latitudes they are not.
- ASC/DSC are **angles**, not automatically the 1st/7th house cusps; MC is not automatically the 10th cusp in every house system. Label them as angles.
- The angle glyphs are `AC`, `DC`, `MC`, `IC` in mono, not astrological planet glyphs.

### 6.4 Ring layout

| Readings | Radii (bodies) | Colors / patterns | Labels |
|---|---|---|---|
| 1 | 300 | primary | full |
| 2 | 300 / 240 | solid / dashed | full |
| 3 | 310 / 260 / 210 | solid / dashed / dotted | compact |
| 4 | 320 / 275 / 230 / 185 | four distinct hues + patterns | glyph + degree only |

- Maximum 4 simultaneous rings. A 5th reading enters **focus mode**: one primary ring at full opacity, the rest as thin ghost rings, or a separate table.
- Rings are concentric, not side-by-side. This is the “simultaneously for 2+ people” design.
- Removing a ring animates the remaining radii; the data does not jump.
- Each reading has a color + pattern + label. Color alone is never the identifier.

### 6.5 Visual grammar

- **Zodiac ring:** 12 signs, 30° each; glyphs at r=350; names at r=375 (desktop).
- **Decan ticks:** 10° and 20° inside each sign; 1 px, low contrast.
- **Body markers:** 18 px glyph, 22 px hit area, degree in mono at 24 px.
- **Aspect lines:** within ring or across rings; thin, patterned; opacity by orb.
- **Angle axes:** 1.5 px; primary solid, secondary dashed; labels at rim.
- **Background:** paper/ink, not dark neon. One accent per reading.
- **No** gradients, glows, particles or perpetual motion.

---

## 7. Animation system

### 7.1 What animates

| Event | Animation | Duration |
|---|---|---|
| First render | ring draws from 0° to 360°; markers fade in staggered | 700 ms |
| Add reading | ring expands from centre; markers scale in | 500 ms |
| Remove reading | ring collapses; markers fade; remaining rings reflow | 400 ms |
| Change moment/time | markers travel along the shortest arc; angle axes rotate | 800 ms |
| Toggle aspect | line draws on/off (dash offset) | 300 ms |
| Select mark | halo expands; detail panel cross-fades | 200 ms |
| Hover mark | 2 px lift only | 120 ms |

### 7.2 Shortest-arc interpolation

```js
const delta = ((to - from + 540) % 360) - 180; // -180..180
const next = from + delta * easedT;
```

- Never spin the long way around.
- Angle axes use the same interpolation.
- If a marker crosses 0° Aries, it travels across the boundary, not through the centre.

### 7.3 Determinism

- Same readings + same moment → same positions.
- No random jitter in the wheel.
- Animation order is fixed: Sun → Moon → Mercury → … → Pluto.
- `prefers-reduced-motion: reduce` → all durations 0; no draw-on.

### 7.4 No perpetual animation

- The wheel is still when idle.
- No twinkling, no breathing, no auto-rotation.
- The only continuous motion is a user-initiated transition.

---

## 8. Custom live display

### 8.1 Controls

A right-hand panel (“Vista”) with live controls:

| Group | Control | Values |
|---|---|---|
| **Lecturas** | Add | `Otro momento` / `Otra persona` |
| | Remove | per reading |
| | Focus | primary reading |
| **Cuerpos** | 10 toggles | Sun … Pluto |
| **Ángulos** | ASC/DSC | on/off |
| | MC/IC | on/off |
| **Aspectos** | Mode | `off` / `mayores` / `todos` |
| | Scope | `intra` / `inter` / `ambos` |
| **Etiquetas** | Mode | `glifo` / `glifo + grado` / `nombre + grado` |
| **Rueda** | Zodiac labels | `glifos` / `nombres` / `grados` |
| | Decan ticks | on/off |
| **Tono** | Show adjectives/verbs | on/off |
| **Movimiento** | Animate | on/off (respects OS) |
| **Densidad** | Compact / full | auto at < 720 px |

### 8.2 Presets

- **Rueda mínima** — signs, ASC/DSC, 10 glyphs, no aspects.
- **Carta** — 10 bodies, 4 angles, major aspects.
- **Encuentro** — 2 readings, cross-aspects, compact labels.
- **Momentos** — same person, 2 readings, angle axes, major aspects.
- **Solo relaciones** — no glyphs, aspect lines + table.

Presets only change `ViewState`; they never change the underlying readings.

### 8.3 Live state

```js
ViewState {
  mode: 'zodiac' | 'chart',
  bodies: Set['sun', …],
  angles: { ascDsc: true, mcIc: false },
  aspects: { mode: 'major', scope: 'both' },
  labels: 'glyph+degree',
  zodiac: 'glyphs',
  decans: true,
  tone: true,
  motion: true,
  density: 'auto',
  primaryReadingId: 'r1',
}
```

- Every control writes to `ViewState` and calls `render()`; no “Apply”.
- `render()` diffs against the previous view and animates only what changed.
- The URL hash MAY encode `ViewState` (e.g. `#v=major`), never readings or birth data.
- Local storage MAY remember `ViewState` only.

### 8.4 Reading strip

- Each reading is a chip: label, date, color, remove.
- Add flow: `Otro momento` (same person) or `Otra persona`.
- For another person: label, date, time, place, timezone, consent.
- Drag to reorder? No. Keep order stable; the first reading is primary by default.

### 8.5 Detail panel

- **Mark selected:** body verb + sign verb + arc adjective + tone vector; e.g. “Marte · activar · Aries · iniciar · incisivo”.
- **Line selected:** aspect verb + orb + exactness; e.g. “Cuadratura · tensar · orbe 2.1°”.
- **Angle selected:** angle verb; e.g. “ASC · aparecer”.
- **Reading selected:** summary counts: elements, modalities, polarities, retrograde count.
- No interpretation, no prediction, no score.

---

## 9. Interaction and accessibility

### 9.1 Interaction map

- Add/remove readings via buttons.
- Toggle controls via checkboxes/radio groups.
- Select a mark/line via the text table (primary) or click/tap the SVG marker (enhancement).
- Hover a marker: visual highlight only; no content change.
- Keyboard: `Tab` through controls; table rows are focusable; `Enter` selects; `Esc` clears.
- Mobile: controls in a bottom sheet; wheel remains square; labels compact.

### 9.2 Accessibility

- The wheel is `role="img"` with `aria-labelledby` and a dynamic `aria-describedby` summary.
- The **text table is the accessible equivalent**, not a fallback:
  - Bodies table: reading, body, sign, degree, retrograde.
  - Angles table: reading, ASC, DSC, MC, IC.
  - Aspects table: reading A body, relation, reading B body, aspect, orb.
- Table rows highlight the corresponding SVG mark/line on focus.
- Color + pattern + label identify readings; never color alone.
- Contrast: text ≥ 4.5:1; lines ≥ 3:1.
- `prefers-reduced-motion`: no animation; instant updates.
- No drag-only or hover-only information.
- Focus visible on every control and table row.

---

## 10. Data and astronomy engine

### 10.1 Ephemeris decision (Phase 0)

| Option | Pros | Cons |
|---|---|---|
| **Swiss Ephemeris (WASM)** | gold standard; planets, angles, houses | AGPL or commercial license; large-ish |
| **Astronomy Engine (MIT)** | permissive; planets and Moon; good accuracy | angles/houses need separate formulas; Pluto support check |
| **Precomputed table** | fast, offline, deterministic | range/size; no arbitrary times |
| **Server API** | easy | violates privacy/local-first |

**Recommendation:** evaluate Swiss Ephemeris WASM first. If AGPL is acceptable for the open-source project, use it; otherwise use Astronomy Engine and implement ASC/MC with standard formulas, validated against Swiss Ephemeris test vectors.

### 10.2 Accuracy targets

- Bodies: ±0.02° versus Swiss Ephemeris for 1900–2100 (or the declared range).
- Angles: ±0.05° for a known chart at a known time/place.
- Sign boundaries: correct at 0°/30° boundaries with a 1′ guard.
- Retrograde: derived from speed; label `℞` only when confirmed.
- No rounding that hides a cusp: show 2 decimals; warn within 0.5° of a boundary.

### 10.3 Angles

- Compute Julian Day from UTC.
- Compute Greenwich Mean Sidereal Time; convert to Local Sidereal Time.
- Compute obliquity of the ecliptic.
- Compute MC from LST and obliquity.
- Compute ASC from LST, obliquity and geographic latitude.
- `DSC = ASC + 180°`; `IC = MC + 180°`.
- Do **not** assume `ASC + 90° = MC`.
- Validate against at least three published charts at different latitudes.
- If latitude is near the polar circle, the ASC can be undefined for some configurations; show a clear message, don’t fake it.

### 10.4 Time zones and places

- Use IANA time zones, not a fixed UTC offset.
- Resolve historical DST rules; warn for dates before reliable tz data.
- Accept lat/lon directly; optional city search from a bundled, offline dataset.
- No external geocoding API with birth data.
- If the user enters a place name only, resolve locally; never send it to a third party.

### 10.5 Orbs (defaults, declared)

| Aspect | Angle | Orb (luminaries +2°) |
|---|---|---|
| Conjunction | 0° | 8° |
| Opposition | 180° | 8° |
| Trine | 120° | 7° |
| Square | 90° | 7° |
| Sextile | 60° | 5° |
| Quincunx | 150° | 3° |
| Semisextile | 30° | 2° |
| Semisquare | 45° | 2° |
| Sesquiquadrate | 135° | 2° |

- The UI MUST show the orb used.
- The engine MUST distinguish applying/separating when speed data exists.
- Angle contacts use a 3–5° orb and are labelled separately.

### 10.6 No fake completeness

- If a body is missing from the ephemeris, show `—`, not a guessed position.
- If angles are null, hide the angle axes and say why.
- If the ephemeris range is exceeded, refuse the date with a clear message.

---

## 11. Architecture

### 11.1 Suggested files

| File | Purpose |
|---|---|
| `web/wheel/index.html` | page shell, controls, tables, live regions |
| `web/wheel/wheel.css` | layout, SVG styles, responsive |
| `web/wheel/wheel.js` | rendering, animation, interaction, state |
| `web/wheel/astro.js` | ephemeris adapter, angles, aspects, orbs |
| `web/wheel/vocab.js` | shared vocabulary, adjectives, verbs, line actions |
| `web/wheel/readings.js` | reading creation, validation, consent, storage |
| `web/wheel/data/*.json` | sign/planet data, test fixtures, source notes |
| `web/wheel/wasm/*` | ephemeris WASM, if chosen |

No framework. ES modules, SVG, Web Animations API; progressive enhancement.

### 11.2 Rendering model

- The wheel is a single `<svg>` with one `<g>` per reading.
- Each ring has:
  - a zodiac group (shared, not duplicated per reading),
  - an angle group,
  - a body group,
  - an aspect group.
- Use `transform="rotate(angle 360 360)"` for angle axes; use `translate` for markers.
- Do not recreate the whole SVG on every toggle; diff and update.
- Text tables are rendered from the same `Comparison` model.

### 11.3 Performance

- Initial page ≤ 150 KB before ephemeris.
- Readings: 4 × 10 bodies = 40 markers; aspects cap 24 inter + 45 intra × 4; still under ~200 lines.
- Animation via CSS/WAAPI on transforms/opacity; no layout reads in loops.
- No `requestAnimationFrame` loop when idle.
- Lazy-load the ephemeris only when the first reading is submitted.
- Use `will-change` sparingly; remove after animation.

---

## 12. Security, privacy and ethics

- **Local-only:** no server, no analytics on birth data, no third-party fonts or scripts.
- **Consent:** another person's data needs explicit permission; the checkbox is not pre-checked.
- **No persistence by default:** readings live in memory; own reading may be remembered locally with a clear switch.
- **No URL data:** personal data never appears in the hash, query or referrer.
- **No compatibility score:** contacts and tensions are diagram descriptions, not verdicts.
- **No medical, legal or financial claims.**
- **No “AI interpretation”** in this phase.
- **Clear/reset** removes all readings and local data.
- **Cultural humility:** this phase is Western-only; the vocabulary layer marks resonance vs equivalence for future systems.

---

## 13. Implementation phases

### Phase 0 — Vocabulary + astronomy decisions (3 days)

- [ ] Freeze the shared vocabulary from `astry-cross-vocabulary.md`.
- [ ] Choose ephemeris and license; document it.
- [ ] Build 12 validation charts (different latitudes, dates, times).
- [ ] Define the exact orb table and angle policy.
- [ ] Gate: every term and formula has a source.

### Phase 1 — Astro engine (5 days)

- [ ] `astro.js`: Julian Day, bodies, angles, aspects.
- [ ] Test against Swiss Ephemeris for 12 charts.
- [ ] Cusp and polar-latitude handling.
- [ ] No UI; a JSON fixture runner.
- [ ] Gate: accuracy tolerances pass.

### Phase 2 — Single wheel (4 days)

- [ ] Zodiac mode + chart mode.
- [ ] 10 bodies + 4 angles.
- [ ] Glyphs, degree labels, sign ring, decan ticks.
- [ ] Text tables + accessible summary.
- [ ] Gate: a known chart renders correctly at 390/768/1280.

### Phase 3 — Multi-reading (4 days)

- [ ] Add moment/person; 2–4 rings.
- [ ] Ring radii, colors, patterns, legend.
- [ ] Cross-aspects, angle contacts.
- [ ] Remove/reorder; no ghosts.
- [ ] Gate: 2 people, 10 markers each, readable at 1280.

### Phase 4 — Live custom display + animation (3 days)

- [ ] `ViewState`, controls, presets.
- [ ] Shortest-arc marker/axis animation.
- [ ] Add/remove ring animations.
- [ ] Reduced motion.
- [ ] Gate: every control updates within 100 ms; no reload.

### Phase 5 — QA, privacy, handoff (3 days)

- [ ] `html-validate`, JS syntax, link check.
- [ ] Keyboard/screen-reader pass; contrast.
- [ ] Privacy audit: no birth data in network/URL/storage.
- [ ] Performance/Lighthouse.
- [ ] Documentation: how to add a body, a reading, a system.

### Phase 6 — Optional (not scheduled)

- [ ] Houses (Placidus/Whole Sign) with a declared system.
- [ ] Composite/midpoint charts.
- [ ] Vedic/Chinese/Mayan layers via the shared spine.
- [ ] Export SVG/PNG/JSON (with privacy warnings).

---

## 14. Acceptance criteria

1. **Ten + four**
   Given a reading with date, time, place and timezone,
   then 10 body markers and ASC/DSC (and optionally MC/IC) render.

2. **Angles require time/place**
   Given no birth time,
   then angles are omitted with a clear message; bodies still render.

3. **Same person, another moment**
   Given two moments of the same person,
   then two rings render, each with 10 markers; changing the second moment animates its markers.

4. **Two people**
   Given two people with consent,
   then two rings render with distinct color/pattern; cross-aspects are listed and drawn (major only by default).

5. **Remove one reading**
   Given 3 readings,
   when one is removed,
   then its ring, markers, axes and aspects disappear; the remaining rings reflow smoothly; no ghost data.

6. **Live controls**
   Given the wheel is visible,
   when bodies/angles/aspects/labels are toggled,
   then the wheel updates immediately without reload and the text table stays in sync.

7. **Shortest arc**
   Given a marker at 350° and a new position at 10°,
   then it moves forward 20°, not backward 340°.

8. **Text parity**
   Then every visible marker and aspect has a matching row in the tables.

9. **Privacy**
   Then no network request contains birth date/time/place; no URL contains it.

10. **No prediction**
    Then no copy says what will happen, who is compatible, or what a person is like.

---

## 15. Test plan

### 15.1 Astronomical fixtures

- 12 charts across 1900–2020, latitudes 0°, 40°, 60°, and negative latitudes.
- Known ASC/DSC/MC/IC values from a trusted ephemeris.
- Cusp cases within 1′ of 0°/30°.
- Retrograde cases (Mercury, Mars, Jupiter, Saturn).
- Time-zone edge cases (DST transitions, historical zones).
- Missing time/place → null angles.

### 15.2 Vocabulary tests

- Every sign has an arc adjective + verb.
- Every body has a verb.
- Every angle has a verb.
- Every aspect has a verb + adjective + line grammar.
- No banned adjectives (§9.4 of the vocabulary doc).
- Cross-system chips carry `=`, `≈`, `~`, `≠`.

### 15.3 UI tests

- 1/2/3/4 readings at 390/768/1280.
- Add/remove reading; no layout shift.
- Toggle every control; text table parity.
- Keyboard; focus ring; screen-reader summary.
- Reduced motion.
- Hover/click marker; detail panel.

### 15.4 Privacy tests

- Network panel: zero birth data requests.
- URL/hash: no birth data.
- Local storage: only own reading, only if enabled.
- Reset clears memory and storage.

---

## 16. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Ephemeris license | Decide in Phase 0; fallback plan |
| Angle accuracy | Validate against known charts; no fake |
| Time zone ambiguity | IANA zones; warning; show UTC |
| Visual clutter with 4 rings | Fixed radii; label modes; cap aspects; patterns |
| “10 positions” ambiguity | Define as 10 bodies; angles separate |
| Compatibility framing | Contact vocabulary; no score |
| Privacy of another person | Consent; no storage; no network |
| Cultural flattening | Shared spine, local terms, relation marks |
| Animation overload | No idle motion; reduced motion |
| Overbuilding | Phase gates; no houses/minors until core passes |

---

## 17. Open questions

1. Is this **Astry-branded** or a separate web instrument?
2. Does “10 positions” mean the 10 bodies, or 10 fixed slots (e.g., 10 selected points)? This plan uses the 10 bodies.
3. Max simultaneous readings: 4, or more with focus mode?
4. Swiss Ephemeris AGPL acceptable, or must it be MIT-only?
5. Do we need houses in Phase 1, or are angles enough?
6. Do we show minor aspects by default, or only on demand?
7. Is local storage allowed for the user's own reading?
8. Spanish only, or ES/EN from the start?
9. Do we allow export of another person's comparison, and with what warning?
10. Should “chart mode” rotate to ASC, or keep the zodiac fixed everywhere?

---

## 18. Appendix — relation to “10 positions”

The implementation interprets the request as:

- **10 body positions** per reading: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.
- **4 angle anchors** per reading: ASC, DSC, MC, IC.

Why: this is the standard Western set of 10 bodies, and the angles are the frame that the request explicitly asks to represent. If the product instead wants “10 positions” as 10 selected points (e.g., 5 bodies + 5 angles), the renderer already supports a `positions[]` array; the data model SHOULD keep `bodies` and `angles` separate and let the view choose 10.

---

## 19. References

- Vocabulary and smoothing: `astry-cross-vocabulary.md`.
- Western aspects: <https://en.wikipedia.org/wiki/Astrological_aspect>
- Western angles: <https://www.chani.com/astro-education/new-mc-ic-and-dc-are-now-in-the-chani-app>
- Western bodies: <https://en.wikipedia.org/wiki/Planets_in_astrology>
- Unicode zodiac glyphs: <https://www.unicode.org/charts/PDF/U2600.pdf>
- Astronomy Engine (MIT candidate): <https://github.com/cosinekitty/astronomy>
- Swiss Ephemeris (license review): <https://www.astro.com/swisseph/>

**Definition of done:** one to four rings, 10 bodies and 4 angles each, accurate ASC/DSC, live controls, shortest-arc animation, text parity, zero birth data on the network — and a wheel that feels like an instrument, not a horoscope.
