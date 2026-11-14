# Astry · Live Sign Composition — Spec-Driven Development Plan

- **Status:** draft for implementation
- **App:** `apps/psicosocial/astry.html`
- **Scope:** the live visual composition of the chosen traditions (“signs”), plus the `Image` option of the Copy prompt.
- **Normative language:** **MUST**, **SHOULD**, **MAY** follow RFC 2119.
- **Already implemented:** the `Image` checkbox in the Copy prompt, its image brief, its empty-selection guard and its persistence (`imagePrompt` in `CHECK_NAMES`). The live composition below is the plan.
- **One-sentence spec:** when a tradition is checked, its authentic visual vocabulary appears in a single shared composition; when it is unchecked, that layer and all of its data disappear; the `Image` copy option asks an agent to build the same composition from original visual sources.

---

## 1. Goals, non-goals and success

### 1.1 Goals

1. Turn the tradition checkboxes into a **live composition**: selecting a sign draws its symbols; deselecting hides them immediately.
2. Make the composition **plural but legible**: different systems share one centre, one outer ring and one radial grid, while keeping their own counts, glyphs and geometry.
3. Keep every mark **traceable**: the user can tell which sign contributed which glyph, token or bridge.
4. Mirror the composition in the **Copy prompt**: the `Image` checkbox adds an explicit image brief that requires original visual sources and overlapping data.
5. Stay **honest**: do not invent astrology, do not fake precision, do not use generic “mystic” imagery.

### 1.2 Non-goals

- No WebGL, Three.js, canvas-first renderer or external graphics library.
- No real ephemeris or chart calculation in Phase 1 (see §8.2).
- No AI image generation inside Astry; the `Image` option only writes a brief for the user’s own agent.
- No new app navigation, no new storage backend, no server calls.
- No automatic cultural mixing that pretends two signs are the same symbol.

### 1.3 Success criteria

| Criterion | Target |
|---|---|
| Select 5 traditions | 5 distinct layers render in one composition, no console errors |
| Deselect 1 tradition | its layer and data are hidden within 250 ms; the other 4 do not move |
| Re-select it | identical geometry returns (deterministic) |
| Source fidelity | every glyph has a named source plate and provenance |
| Accessibility | text alternative lists every active sign and token |
| Performance | update ≤ 16 ms desktop, ≤ 50 ms mid-range mobile |
| Visual clarity | no unreadable overlap at 390 px wide |
| Image prompt | contains source constraint, overlap instruction and omission rule, in EN and ES |

---

## 2. Canonical vocabulary

Use these terms in code, comments, UI copy and the prompt. Do not introduce synonyms.

| Term (EN) | Término (ES) | Meaning | Avoid |
|---|---|---|---|
| **sign** | **signo** | a tradition selected by the user (Western, Celtic, Mayan, Vedic, Chinese, Gipsy) | “system”, “type” |
| **token** | **ficha** | a derived datum contributed by a sign (Aries, Imix, Ashwini, Dragon…) | “value”, “item” |
| **source plate** | **lámina fuente** | the documented visual reference a glyph is traced from | “inspiration”, “reference image” |
| **glyph** | **glifo** | a vector mark belonging to one sign | “icon”, “emoji” |
| **primitive** | **primitiva** | a reusable geometric unit (circle, chord, notch, bar, dot, triangle) | “shape” |
| **layer** | **capa** | one sign’s group of marks | “overlay” (except CSS) |
| **band** | **banda** | a fixed radial slot assigned to one sign | “ring” (reserve ring for the shared circle) |
| **composition** | **composición** | the single SVG containing all active layers | “collage”, “moodboard” |
| **overlap field** | **campo de superposición** | the shared centre/axes where data from different signs meets | “background” |
| **bridge** | **puente** | a visible relation between tokens of two signs | “link” (ambiguous with UI) |
| **anchor** | **ancla** | birth date/time/place used to derive tokens | “input” |
| **traceable** | **rastreable** | the user can identify the source sign of a mark | “visible” |
| **provenance** | **procedencia** | source, culture, period and rights of a plate | “origin” |
| **live composition** | **composición viva** | the renderer that reacts to the form | “preview”, “thumbnail” |

**Naming rules**

- Code keys keep the existing tradition codes: `western`, `celtic`, `mayan`, `vedic`, `chinese`, `gipsy`.
- Display labels stay exactly as the app localizes them: `Western / Occidental`, etc.
- The `Gipsy` label is treated as a **provisional app label**; see §13. Do not rename it in this phase without a product decision.
- Band names are `band-0` … `band-5`, numbered outward-in.

---

## 3. Sign registry and source vocabulary

Every sign in `SIGN_REGISTRY` MUST provide: `code`, `label`, `band`, `sourcePlates[]`, `tokens[]`, `primitives[]`, `palette`, `render()` and `caption`.

### 3.1 Western — `western`

| Field | Spec |
|---|---|
| Tokens | zodiac sign (12), element (fire/earth/air/water), modality (cardinal/fixed/mutable), ruler, house, aspect |
| Source plates | Hellenistic and medieval zodiac wheels; standard sign glyphs (Unicode U+2648–U+2653); element triangles; aspect diagrams. Trace from public-domain plates or draw from documented conventions. |
| Primitives | 12 × 30° sector ring, glyph paths, element triangle, modality cross, aspect chord (trine 120°, square 90°, opposition 180°, sextile 60°) |
| Visual grammar | glyph pins on the band; element triangle as a quiet watermark; aspect chords across the overlap field |
| Do not | generic “space” stars, invented constellations, horoscope clip-art |

### 3.2 Celtic — `celtic`

| Field | Spec |
|---|---|
| Tokens | fid (20 Ogham letters), aicme (4 families), tree kenning, ogham letter |
| Source plates | Ogham stone inscriptions (5th–7th c.); *Book of Ballymote* and related manuscript tables. Knotwork is optional and MUST be sourced, not generic. |
| Primitives | vertical stemline, 1–5 notches on the left, right or across the stem, aicme grouping ticks, optional sourced spiral/triskele |
| Visual grammar | one radial stemline per active fid; notches on the shared tick grid; no free-floating “Celtic knot” wallpaper |
| Do not | shamrocks, leprechauns, “druid mist”, unsourced knot patterns |

### 3.3 Mayan — `mayan`

| Field | Spec |
|---|---|
| Tokens | day sign (20), tone (1–13), Haab month, Long Count position |
| Source plates | pre-Columbian codices (Dresden, Madrid, Paris) and monument inscriptions, with a specialist/community source note; day-sign cartouches and bar-and-dot numerals |
| Primitives | cartouche frame, dot = 1, bar = 5, shell = 0, day-sign contour, tone dots |
| Visual grammar | cartouche as a shared frame segment; bar-and-dot counts as repeated marks on the band; the day glyph as a mask or inset |
| Do not | pseudo-Mayan “alien” glyphs, Aztec motifs substituted for Maya, generic jungle/temple decoration |

### 3.4 Vedic — `vedic`

| Field | Spec |
|---|---|
| Tokens | rāśi (12), nakṣatra (27), graha (9), bhāva (12), pāda (4) |
| Source plates | North Indian (diamond) and South Indian (square) chart conventions; classical yantra diagrams (bindu, trikoṇa, ṣaṭkoṇa, aṣṭakoṇa, circle, lotus petals); Devanagari and traditional graha glyphs |
| Primitives | bindu, up/down triangles, hexagram, octagram, lotus petals, 27-division nakshatra ring |
| Visual grammar | bindu at the shared centre; yantra polygons overlapping in the field; nakshatra ticks on its band |
| Do not | “chakra rainbow” as a universal colour code, mandala wallpaper, New Age pseudo-Sanskrit |

### 3.5 Chinese — `chinese`

| Field | Spec |
|---|---|
| Tokens | earthly branch (12), heavenly stem (10), element (5), trigram (8), solar term (24), yin/yang polarity |
| Source plates | *Zhouyi* / bagua trigram conventions; five-element generating and controlling cycles; sexagenary cycle tables; seal-script animal forms where used |
| Primitives | solid/broken trigram line stack, octagon, five-element pentagon, 10/12/24 ticks, taiji split |
| Visual grammar | trigram stacks on the band; element pentagon as a shared field figure; generating cycle clockwise, controlling cycle as inner star |
| Do not | “feng shui” décor, red envelopes, dragons as generic ornament, fortune-cookie motifs |

### 3.6 Gipsy — `gipsy`

This sign requires a separate cultural-review gate. There is no uncontested, single “Gipsy zodiac” visual canon, and much commercial imagery is stereotyped or appropriative.

| Field | Spec |
|---|---|
| Tokens | **TBD by community review** (documented Romani astrological/divinatory source only) |
| Source plates | a community-approved, attributed plate; provenance and permission recorded in `sourcePlates[]` |
| Primitives (until approved) | typographic cartouche + provenance badge only; **no invented glyph** |
| Visual grammar | neutral band segment with a dotted “pending source” ring; layer remains visible as a named, honest placeholder |
| Do not | crystal balls, scarves, “mystic” hands, palmistry clichés, the Romani flag chakra used as decoration, any generic “gypsy” motif |

**Gate:** the `gipsy` renderer MUST remain in placeholder mode until a named reviewer signs off. The UI MUST NOT imply a completed visual system before that.

---

## 4. Composition geometry

### 4.1 Canvas and coordinate system

- Single inline `<svg viewBox="0 0 1000 1000">`.
- Centre `C = (500, 500)`.
- Outer ring radius `R = 440`; stroke 1.5.
- All positions are computed in **user units**, then scaled by CSS. No fixed pixel assumptions.
- `vector-effect="non-scaling-stroke"` on thin lines is allowed only if export parity is verified.
- The composition is square; mobile uses `width:100%; aspect-ratio:1`.

### 4.2 Fixed bands (one per sign)

Bands are **fixed slots**, not dynamic stacks. This is what makes deselecting feel like hiding, not reflowing.

| Slot | Radius range | Sign | Internal divisions |
|---|---|---|---|
| `band-0` | 392–432 | Western | 12 sectors |
| `band-1` | 344–384 | Chinese | 10 stems + 12 branches + 8 trigrams (nested sub-ticks) |
| `band-2` | 296–336 | Vedic | 27 nakshatras + 12 rāśis |
| `band-3` | 248–288 | Mayan | 20 day signs + 13 tones |
| `band-4` | 200–240 | Celtic | 20 fids |
| `band-5` | 152–192 | Gipsy | pending source; neutral placeholder |
| `core` | 0–140 | shared | bindu / anchor medallion |

Rules:

1. A sign MUST occupy its slot only. It MUST NOT resize or move when another sign is toggled.
2. Empty slots remain empty; the shared outer ring and core remain visible.
3. The order is stable: Western → Chinese → Vedic → Mayan → Celtic → Gipsy.
4. On narrow screens, labels collapse before geometry; the SVG itself keeps its aspect ratio.

### 4.3 The overlap field

The centre and the radial axes are the **overlap field**:

- Shared centre `C` with a small bindu / anchor mark.
- Four cardinal axes at 0°, 90°, 180°, 270°; eight if a selected sign needs diagonals.
- A 0° reference line (top) used by every band, so all systems share one orientation without pretending their counts match.
- **Bridges:** thin chords or arcs between related tokens. Bridge examples already present in the current copy:
  - Aries ↔ Imix
  - Hexagram 1 ↔ Ashwini
  - Dragon ↔ rhythm
- A bridge MUST be visually weaker than the token glyphs (stroke 0.75–1, opacity 0.35–0.5).
- A bridge MUST have a `<title>` such as `Aries → Imix`.
- Bridges appear only when both endpoint signs are active. Removing one sign removes its bridges (§5.4).

### 4.4 Layer hierarchy

| Level | Mark | Stroke / opacity | Purpose |
|---|---|---|---|
| 0 | outer ring, axes, core | 1.25 / 0.55 | shared scaffolding |
| 1 | bridge chords | 0.9 / 0.4 | cross-sign relation |
| 2 | band ticks and token marks | 1.2 / 0.8 | each sign’s data |
| 3 | glyphs and cartouches | 1.6 / 1.0 | identity |
| 4 | labels and leader lines | 1 / 0.75 | traceability |

Rules:

- More than three stroke weights in one composition is a bug.
- No `mix-blend-mode` or filters in the base composition: they do not round-trip reliably to SVG/PNG export.
- Overlap is communicated by shared geometry, not by transparency mud.
- Each sign gets a desaturated hue from the page palette; no more than two colors per sign.

### 4.5 Determinism

- Every composition derives from `(checked signs, anchor, language-independent tokens)`.
- A tiny seeded jitter (±3°) MAY be used for glyph breathing room, seeded by `hash(sign + token + date)`.
- Same inputs MUST produce identical path data on every render and reload.
- Do not use `Math.random()` in the renderer.

### 4.6 Labels and traceability

- Each sign has one label outside the outer ring at radius 470, with a 1 px leader line.
- Label lanes avoid collisions: at most one label per 30° lane; if two signs share a lane, offset radially by 18 px.
- Every layer MUST expose:
  - `data-sign="western"` on its `<g>`;
  - `data-token="aries"` on token groups;
  - `<title>` with the human-readable name;
  - `<desc>` on the root SVG listing all active signs and tokens.
- The visible caption under the SVG repeats the list in plain language.

---

## 5. Live behaviour

### 5.1 State model

```js
// One source of truth: the tradition checkboxes.
const state = {
  active: ['western', 'mayan'],   // derived from getCheckedValues('trad')
  layers: new Map(),              // code -> <g data-sign>
  bridges: new Map(),             // 'western:mayan:aries:imix' -> <path>
};
```

- Do **not** store a second copy of the selection in JS.
- The renderer is a pure function of the current form state plus the anchor.
- The existing persistence (`snapshotState`, `restoreState`, `CHECK_NAMES`) remains the only storage path.

### 5.2 Event flow

1. A tradition checkbox changes (existing listener).
2. `syncComposition()` reads `getCheckedValues('trad')`.
3. Diff against `state.active`.
4. For each added sign: create layer, set `data-state="enter"`, animate, then `active`.
5. For each removed sign: set `data-state="exit"`, animate, then `hidden`; remove its bridges.
6. Update the visible caption and the SVG `<desc>`.
7. If the active list is empty: show the empty state and hide the figure.
8. If the `Image` checkbox changes: no geometry change; only the Copy prompt changes.

### 5.3 Enter and exit

| Event | Motion | Duration |
|---|---|---|
| enter | opacity 0→1, scale 0.96→1, draw-on via `stroke-dashoffset` for line glyphs | 600 ms, stagger 80 ms |
| exit | opacity 1→0, scale 1→0.96, no layout shift | 240 ms |
| reduce motion | no transitions, instantaneous show/hide | 0 ms |

- Exit MUST finish before `hidden` is set; use `transitionend` with a timeout fallback.
- Re-selecting during an exit MUST cancel the exit and reuse the existing layer if possible.
- The composition MUST NOT animate on page load unless at least one sign is restored; restored state appears without draw-on.

### 5.4 Deselecting one of five signs — the canonical case

Given five active signs (e.g. Western, Chinese, Vedic, Mayan, Celtic):

1. The user unchecks **Celtic**.
2. `syncComposition()` marks `celtic` for exit.
3. Its `band-4` marks fade and collapse; **no other band moves**.
4. Bridges that used a Celtic token are removed.
5. The caption changes from “5 signs: … Celtic” to “4 signs: …”.
6. The SVG `<desc>` no longer mentions Celtic or its tokens.
7. The Copy prompt (if regenerated) no longer names Celtic.

Acceptance: a screenshot before/after shows only `band-4` becoming empty; all other geometry is pixel-identical.

### 5.5 Empty and partial states

- **0 signs:** the figure is hidden; caption says “Choose a sign to begin.” in EN / “Elige un signo para empezar.” in ES. No ghost ring, no “loading”.
- **1 sign:** the composition is valid; no need to force a second sign.
- **Incomplete source (Gipsy):** the placeholder band is shown with a “source pending” note; the caption says so.
- **No anchor:** tokens that need a date MAY fall back to neutral index positions; the caption MUST say “symbolic positions, not calculated”. Never display a fake degree.

---

## 6. UI and UX

### 6.1 Placement

- Add a `<section class="composition" id="composition" hidden>` directly after the traditions/focus cards, before the results area.
- Header: “Live composition” / “Composición viva”; a count `n / 6`.
- `<figure><svg id="compositionSvg"></svg><figcaption id="compositionCaption"></figcaption></figure>`.
- Footer note: “Source-based symbols. Symbolic positions, not a calculated chart.” / “Símbolos de fuente. Posiciones simbólicas, no una carta calculada.”
- Desktop: composition sits to the right of the form if the layout already supports a two-column split; otherwise full width below. Do not restructure the page in this phase.
- Mobile: full width, square, labels collapse to numbers + caption.

### 6.2 Controls

- The existing tradition chips remain the only selection controls.
- The composition is not directly editable; no drag, no zoom, no hidden gestures.
- A “Show sources” disclosure MAY list the active source plates and provenance.

### 6.3 `Image` checkbox contract (already implemented)

Markup: `#imagePromptInput`, `name="imagePrompt"`, inside `.copy-prompt-row`, before the Copy button.

When checked, `buildAgentPrompt()` appends this paragraph (localized):

> One more thing: create one image that represents this reading. Build it from the original visual source representations of the chosen signs — {signs} — using their own glyphs, symbols, colors and geometries, not generic or invented imagery. Overlap the data from the different signs in a single composition: let their forms share centers, axes, circles and lines so the readings layer into one picture instead of sitting side by side. Keep every sign's marks traceable, and leave out any tradition I did not choose.

Spanish:

> Una cosa más: crea una imagen que represente esta lectura. Constrúyela a partir de las representaciones visuales originales de los signos elegidos — {signos} — usando sus propios glifos, símbolos, colores y geometrías, no imágenes genéricas ni inventadas. Superpón los datos de los distintos signos en una sola composición: que sus formas compartan centros, ejes, círculos y líneas para que las lecturas se fundan en una imagen única en lugar de quedar lado a lado. Mantén rastreable la marca de cada signo y deja fuera cualquier tradición que no haya elegido.

Rules:

- `{signs}` is the current localized list, in the order the user checked them.
- If no tradition is selected, Copy MUST refuse and say “Choose at least one tradition for the image.” / “Elige al menos una tradición para la imagen.”
- The checkbox MUST persist with the form state (`CHECK_NAMES` includes `imagePrompt`).
- The image brief MUST match the live composition’s vocabulary and omission rule.
- The checkbox MUST NOT trigger image generation or network access.

### 6.4 Responsive rules

- 390 px: composition width 100%, labels as 2-letter codes or numbered pins; caption carries full names.
- 768 px: labels at 12 px; 1:1 composition max 560 px.
- 1280 px+: composition max 640 px; labels outside.
- No horizontal scroll at any width.

---

## 7. Accessibility

- SVG: `role="img"`, `aria-labelledby` pointing to a dynamic `<title>` and `<desc>`.
- `<desc>` example: “Composition of 4 signs: Western (Aries, fire, cardinal), Mayan (Imix, tone 1), Vedic (Ashwini), Chinese (Dragon, wood).”
- Visible caption is the text alternative; it updates with `aria-live="polite"` but only on committed changes (not during transitions).
- The checkboxes remain keyboard-operable; the SVG is not focusable.
- Colour is never the only carrier: sign code, glyph shape and label all identify a layer.
- Graphics contrast ≥ 3:1 against the composition background; text ≥ 4.5:1.
- `prefers-reduced-motion`: no draw-on, no scale, no stagger.
- Do not use `outline: none` on the checkbox.

---

## 8. Data, tokens and honesty

### 8.1 Token derivation

```js
// Phase 1: declared + anchor-derived symbolic tokens.
// Phase 4: replace `deriveTokens()` internals with verified algorithms.
function deriveTokens(signCode, anchor) {
  // anchor = { dob, time, location, lat, lon }
  // MUST return [{ id, label:{en,es}, angle?, sourceRef }]
}
```

- Each token MUST carry a `sourceRef` to the source plate or convention.
- If a token cannot be derived, return a neutral token and mark it `provisional: true`.
- The caption MUST disclose provisional tokens.

### 8.2 Honesty rules

- Phase 1 does **not** compute real planetary positions, nakshatras or Tzolk’in dates. It uses **declared traditions + documented symbolic tokens** (index, element, modality, cycle position) and says so.
- Never display degrees, minutes, planetary longitudes or “today’s energy” unless a verified algorithm produced them.
- Do not blend two traditions into a single “result” token; show bridges, not mergers.
- Do not claim a symbol is “original” if it is a modern reconstruction. Say “after [source]” in the provenance disclosure.

### 8.3 Persistence

- No new keys. The composition derives from `CHECK_NAMES` (`trad`) and the existing fields.
- `imagePrompt` is now part of `CHECK_NAMES` and restores with the form.
- Reset clears the composition by clearing the checkboxes; no separate cleanup needed.

---

## 9. Export and sharing

- **Prompt:** the `Image` checkbox adds the brief described in §6.3. This is the only shipped export change in this phase.
- **SVG (future):** `toSvgComposition()` serializes the live `<svg>` with inline styles, `<title>`, `<desc>` and `<metadata>` listing sources.
- **PNG (future):** rasterize the SVG at 2048×2048 on a canvas; dark background; no external fonts (use paths or system fonts).
- **Fidelity:** exported SVG/PNG MUST match the live preview; no blend modes, no CSS variables that cannot be resolved.
- **Attribution:** embedded metadata and visible caption list the source plates.
- **Do not** add a seventh “Save” format until the export passes the fidelity test.

---

## 10. Implementation phases

### Phase 0 — Sources and vocabulary freeze (2 days)

- [ ] Build `SIGN_REGISTRY` with `sourcePlates[]` and provenance links.
- [ ] Trace or commission the Phase 1 glyph set: Western 12, Celtic 20 fids, Mayan 20 day signs + numerals, Vedic 12/27 + yantra primitives, Chinese 8 trigrams + 12 branches, Gipsy placeholder.
- [ ] Record rights (public domain / permission / original).
- [ ] Freeze the vocabulary table in §2.
- [ ] Gate: a reviewer can name the source of every glyph.

### Phase 1 — Static renderer (3 days)

- [ ] Add `SIGN_REGISTRY`, `renderSign()`, `renderComposition()`.
- [ ] Draw the shared scaffolding and all six bands.
- [ ] Render a hard-coded 5-sign fixture behind a dev flag.
- [ ] Gate: snapshot test of path data; no visual overflow at 390/768/1280.

### Phase 2 — Live binding (2 days)

- [ ] Hook `input[name="trad"]` change to `syncComposition()`.
- [ ] Implement enter/exit state machine and `prefers-reduced-motion`.
- [ ] Empty state and caption.
- [ ] Gate: select 5, deselect 1, re-select 1; others do not move.

### Phase 3 — Overlap and traceability (2 days)

- [ ] Add bridge rules and rendering.
- [ ] Add labels, leader lines, collision lanes.
- [ ] Add `<title>` / `<desc>` and the visible caption.
- [ ] Gate: 5-sign composition readable; every layer identifiable.

### Phase 4 — Export, accessibility, QA (2 days)

- [ ] SVG/PNG export behind the existing Save ladder (optional).
- [ ] Keyboard and screen-reader pass.
- [ ] EN/ES copy pass; the `Image` prompt already exists.
- [ ] Performance budget and visual regression.
- [ ] Gate: acceptance criteria in §11 all pass.

### Phase 5 — Gipsy source review (parallel, external)

- [ ] Community reviewer and provenance documented.
- [ ] Replace placeholder only after sign-off.
- [ ] Gate: no invented “Gipsy” glyph ships.

---

## 11. Acceptance criteria (Given / When / Then)

1. **Five signs, one picture**
   Given Western, Chinese, Vedic, Mayan and Celtic are checked,
   when the composition renders,
   then one SVG shows five bands, one shared centre and no label collisions.

2. **Deselect one sign**
   Given those five signs are visible,
   when Celtic is unchecked,
   then `band-4` and Celtic’s bridges disappear within 250 ms,
   and the geometry of the other four bands is unchanged.

3. **Re-select**
   Given Celtic is hidden,
   when it is checked again,
   then its geometry is identical to the first render.

4. **Empty state**
   Given no sign is checked,
   then the figure is hidden and the caption says “Choose a sign to begin.” / “Elige un signo para empezar.”

5. **Image prompt**
   Given at least one sign and `Image` are checked,
   when Copy is pressed,
   then the prompt names the selected signs, requires their original visual sources,
   requires overlapping data in one composition,
   and excludes unchecked traditions.

6. **No sign + Image**
   Given `Image` is checked and no sign is selected,
   when Copy is pressed,
   then no text is copied and the hint asks for at least one tradition.

7. **Language**
   Given the page is in Spanish,
   when the composition and prompt render,
   then labels, caption and image brief are Spanish.

8. **Reduced motion**
   Given `prefers-reduced-motion: reduce`,
   then every layer change is instantaneous.

---

## 12. Test plan

- **Unit:** registry completeness; every sign has a band, source, palette and renderer; tokens have `sourceRef`.
- **Determinism:** render twice with the same fixture; compare serialized path data.
- **DOM:** active count equals `input[name="trad"]:checked`; no orphan `<g data-sign>` after 400 ms.
- **Visual:** screenshots at 1280, 768, 390 with 0, 1, 5 and 6 signs.
- **A11y:** accessible name/description; keyboard selection; contrast check.
- **i18n:** EN/ES labels, caption, empty state, prompt; no untranslated leaves.
- **Performance:** measure `syncComposition()`; keep < 16 ms desktop, < 50 ms mobile; node count < 1200.
- **Export:** serialize and rasterize a 5-sign fixture; compare to preview.

---

## 13. Risks and ethics

| Risk | Mitigation |
|---|---|
| Cultural appropriation | Source plates, provenance, community review; no invented “ethnic” glyphs |
| Gipsy/Romani stereotyping | Placeholder mode until a named reviewer approves; no crystal-ball/palmistry imagery |
| Fake precision | Say “symbolic positions, not a calculated chart”; no unverified degrees |
| Visual clutter | Fixed bands, three stroke weights, label lanes, low bridge opacity |
| Copyright | Public-domain sources or permission; attribute; do not trace a single modern copyrighted illustration |
| Performance | SVG primitives, no filters/blend modes, measure before adding detail |
| Terminology drift | The vocabulary table in §2 is normative; update it before adding synonyms |
| Over-promising in the prompt | The prompt asks for authentic sources and traceability; it must not guarantee occult accuracy |

---

## 14. Open questions

1. Which specific source plates are approved for Western, Celtic, Mayan, Vedic and Chinese? (Phase 0.)
2. Who reviews the Gipsy/Romani material, and what display term do they prefer?
3. Does the composition live beside the form or inside the results area?
4. Should export include the composition by default, or only when explicitly requested?
5. Should bridges be user-toggleable (“show relations”) or always on for active signs?
6. Do we add real chart algorithms in Phase 4, or keep symbolic longer?

---

## 15. Appendix — code skeleton

```js
const SIGN_REGISTRY = {
  western: {
    code: 'western',
    label: { en: 'Western', es: 'Occidental' },
    band: 0,
    sourcePlates: [
      { id: 'zodiac-wheel', ref: 'Hellenistic/medieval zodiac wheel', rights: 'public-domain', url: '' },
    ],
    palette: { ink: '#dfe7ff', accent: '#8ea2ff' },
    render(g, ctx) {
      // draw 12 glyph pins, element triangle, aspect chords
    },
  },
  // celtic, mayan, vedic, chinese, gipsy…
};

function syncComposition() {
  const active = getCheckedValues('trad');
  // diff, enter/exit, bridges, caption, <desc>
}

function renderComposition() {
  const svg = document.getElementById('compositionSvg');
  // shared ring + axes + core
  // one <g data-sign="..."> per band
}
```

**Definition of done:** the 8 acceptance criteria pass, the 5-sign screenshot is readable at 390 px, the source disclosure names every glyph, and the Gipsy layer is either honestly pending or approved.
