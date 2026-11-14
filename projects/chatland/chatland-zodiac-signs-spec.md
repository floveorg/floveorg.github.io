# Chatland · Los Signos — Western Zodiac Implementation Plan

- **Status:** draft for implementation
- **Project:** `projects/chatland`
- **Related:** `apps/psicosocial/astry-live-signs-spec.md` (the generic multi-tradition composition engine). This plan is the Chatland-specific, Western-zodiac-only counterpart.
- **Scope:** the **twelve Western tropical zodiac signs only**, presented inside Chatland as a new place: **La Plaza de los Signos**.
- **Extension promise:** other systems (Mayan, Chinese, Vedic, Celtic, Gipsy) are **not implemented now**, but the data model, wheel engine and UI reserve a clean slot for them.
- **Normative language:** **MUST**, **SHOULD**, **MAY** follow RFC 2119.
- **One-sentence spec:** Chatland gains a calm, source-accurate zodiac wheel where the twelve signs are twelve gates around a plaza; selecting a gate opens its sign card, deselecting closes it, and the whole thing is built so another tradition can be added later without redesigning the wheel.

> This is a **symbolic, cultural and visual** feature. It is not a prediction engine, not a birth-chart calculator, and not a medical, financial or compatibility service. The page MUST say so once, plainly, near the wheel.

---

## 1. Scope

### 1.1 In scope

1. The **12 tropical zodiac signs**: Aries through Pisces.
2. Accurate sign data: glyphs, dates, elements, modalities, polarities, rulers (traditional and modern), decans, traditional body correspondences, keywords.
3. A **new Chatland place**: La Plaza de los Signos, with a 12-gate wheel and a sign card for each gate.
4. A **teaser** on the Chatland homepage and a dedicated subpage.
5. A **date → Sun sign** finder, clearly labelled as an estimate.
6. Extension points for other zodiac systems, visible in the UI as “Próximamente” only.
7. Spanish as the canonical language, with the data model ready for English.

### 1.2 Out of scope (this phase)

- Moon signs, rising signs, houses, aspects, transits, synastry or compatibility scores.
- Full natal-chart calculation or planetary ephemerides.
- Predictive, medical, legal or financial claims.
- Mayan, Chinese, Vedic, Celtic or Gipsy content.
- Mapping the twelve signs to the fifteen **lands** or the seven **residents**. Signs are gates in a plaza, not replacements for either. A `residentAffinity` field MAY be reserved but MUST stay unset in this phase.
- Native app screens (the data model SHOULD remain portable to them).
- User accounts, saved profiles, notifications or personalization.

### 1.3 Success criteria

| Criterion | Target |
|---|---|
| Accuracy | 12 signs, 4 elements, 3 modalities, 6 yin / 6 yang, 36 decans and 7 traditional planets match the tables in §4 |
| Clarity | a first-time visitor understands in 10 seconds that this is a symbolic place, not a horoscope feed |
| Interaction | selecting a gate opens its card; deselecting closes it; no other gate moves |
| Keyboard | all 12 gates reachable, arrow keys cycle, Enter opens, Esc closes |
| Deep links | `#sign-aries` opens Aries directly; back/forward works |
| Mobile | 390 px wide, wheel + cards readable, no horizontal scroll |
| Performance | page ≤ 150 KB initial HTML, ≤ 12 KB JS, ≤ 8 KB new CSS; no continuous animation |
| Extension | adding a second system requires data + one registry entry, not a wheel rewrite |

---

## 2. Why this belongs in Chatland

Chatland already has a strong spatial metaphor: **the recinto**, **lands**, **residents**, **the gate**. The zodiac should not arrive as an astrology widget bolted onto a chat app. It should arrive as **another place inside the recinto**:

- The wheel is a **plaza**.
- Each sign is a **gate** with a name and a glyph.
- The centre is the **Horizon mark**: the bubble that holds a landscape.
- The sign card is the **plaque** on the gate.
- Nothing rotates by itself. The visitor walks around; the place stays still.

The visual DNA is the existing **01 Horizon** system: a speech bubble containing a sun, a hill and a horizon. Each sign gets its own small “sky plate” inside that bubble. This makes the zodiac feel like Chatland, not like a horoscope site.

**Voice:** short sentences, present tense, warm but sober. No “mystic”, “destiny”, “energy”, “compatibility” or exclamation marks.

> **La Plaza de los Signos.** Doce puertas. Doce tramos de cielo. Ninguna adivina: cada una describe una forma de estar.

---

## 3. Canonical vocabulary

| Term (ES) | Term (EN) | Meaning | Do not use |
|---|---|---|---|
| **signo** | **sign** | one of the twelve 30° tropical sectors | “horóscopo”, “zodiac sign” as a prediction |
| **zodíaco occidental** | **Western zodiac** | the tropical system starting at the vernal equinox | “zodiac” alone when other systems are possible |
| **rueda** | **wheel** | the circular presentation of the 12 gates | “mandala”, “chart” |
| **puerta** | **gate** | one clickable sign position on the wheel | “pin”, “node” |
| **plaza** | **plaza** | the whole place around the wheel | “page”, “section” |
| **tramo** | **segment / sector** | a 30° division of the ecliptic | “month” (signs are not months) |
| **grado** | **degree** | 1/360 of the circle; 0°–29°59′ within a sign | “point” |
| **decano** | **decan** | a 10° third of a sign | “phase” |
| **elemento** | **element** | fire, earth, air, water | “type” |
| **modalidad** | **modality** | cardinal, fixed, mutable | “quality” (unless explained) |
| **polaridad** | **polarity** | yang/positive or yin/negative | “gender” |
| **regente** | **ruler** | the planet associated with a sign | “owner” |
| **domicilio** | **domicile** | a planet’s home sign | “house” (a house is different) |
| **exaltación** | **exaltation** | a planet’s honoured sign | — |
| **detrimento** | **detriment** | the sign opposite a planet’s domicile | — |
| **caída** | **fall** | the sign opposite a planet’s exaltation | — |
| **constelación** | **constellation** | an IAU star pattern; **not** a sign | “sign” |
| **carta natal** | **natal chart** | a full chart with time and place; out of scope | “reading” |
| **placa** | **plate** | the visual card for a sign | “badge” |

**Naming rules**

- Code keys are lowercase ASCII: `aries`, `taurus`, `gemini`, `cancer`, `leo`, `virgo`, `libra`, `scorpio`, `sagittarius`, `capricorn`, `aquarius`, `pisces`.
- UI labels use Spanish canonical names: **Aries, Tauro, Géminis, Cáncer, Leo, Virgo, Libra, Escorpio, Sagitario, Capricornio, Acuario, Piscis**.
- English labels are reserved in the data, not displayed in Phase 1.
- Do not translate “Aries” as “Carnero” in the sign name; the sign is **Aries**.
- “Escorpio” is the Spanish sign name; “Escorpio” is also used for the constellation, but the page MUST say they are not the same thing.

---

## 4. Accuracy contract

### 4.1 Tropical zodiac, stated once

- Chatland uses the **tropical zodiac**: 0° Aries is the **vernal equinox**; each sign is exactly **30°** of the ecliptic; the twelve signs total 360°.
- The page MUST include a short note: *“Los signos son tramos de 30° medidos desde el equinoccio. No son las constelaciones: hoy el cielo visible está desplazado respecto a la rueda.”*
- The page MUST NOT claim that the zodiac is a scientific model of personality. It is a **symbolic tradition**.
- The **13th constellation Ophiuchus** MAY be mentioned in the “Cómo leer esta rueda” note: the ecliptic crosses it, but it is not a sign in the tropical zodiac.
- A **sidereal** option is out of scope; the data model RESERVES a `zodiac: 'tropical' | 'sidereal'` field for later.

### 4.2 Dates

Dates are **approximate** and MUST be presented as ranges, not as fixed annual laws:

| Sign | Approx. dates |
|---|---|
| Aries | 21 mar – 19 abr |
| Tauro | 20 abr – 20 may |
| Géminis | 21 may – 20 jun |
| Cáncer | 21 jun – 22 jul |
| Leo | 23 jul – 22 ago |
| Virgo | 23 ago – 22 sep |
| Libra | 23 sep – 22 oct |
| Escorpio | 23 oct – 21 nov |
| Sagitario | 22 nov – 21 dic |
| Capricornio | 22 dic – 19 ene |
| Acuario | 20 ene – 18 feb |
| Piscis | 19 feb – 20 mar |

Rules:

- The exact ingress changes by year and time zone. The data table carries `startDate`/`endDate` for display only; the **finder** MUST use solar longitude, not these strings.
- The UI MUST label the ranges “fechas aproximadas”.
- The finder MUST warn near a cusp: *“Nacimiento cerca del cambio de signo: la hora y el lugar pueden cambiarlo.”*

### 4.3 Sign data table

| # | Signo | English | Glyph | Elemento | Modalidad | Polaridad | Regente tradicional | Regente moderno | Cuerpo |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Aries | Aries | ♈ | Fuego | Cardinal | Yang | Marte | Marte | Cabeza |
| 02 | Tauro | Taurus | ♉ | Tierra | Fija | Yin | Venus | Venus | Cuello, garganta |
| 03 | Géminis | Gemini | ♊ | Aire | Mutable | Yang | Mercurio | Mercurio | Brazos, pulmones |
| 04 | Cáncer | Cancer | ♋ | Agua | Cardinal | Yin | Luna | Luna | Pecho, estómago |
| 05 | Leo | Leo | ♌ | Fuego | Fija | Yang | Sol | Sol | Corazón, espalda |
| 06 | Virgo | Virgo | ♍ | Tierra | Mutable | Yin | Mercurio | Mercurio | Abdomen, intestinos |
| 07 | Libra | Libra | ♎ | Aire | Cardinal | Yang | Venus | Venus | Riñones, zona lumbar |
| 08 | Escorpio | Scorpio | ♏ | Agua | Fija | Yin | Marte | Plutón | Sistema reproductor |
| 09 | Sagitario | Sagittarius | ♐ | Fuego | Mutable | Yang | Júpiter | Júpiter | Caderas, muslos |
| 10 | Capricornio | Capricorn | ♑ | Tierra | Cardinal | Yin | Saturno | Saturno | Rodillas, huesos |
| 11 | Acuario | Aquarius | ♒ | Aire | Fija | Yang | Saturno | Urano | Tobillos, circulación |
| 12 | Piscis | Pisces | ♓ | Agua | Mutable | Yin | Júpiter | Neptuno | Pies, sistema linfático |

**Traditional rulers are primary.** Modern rulers appear in a secondary line (“Regente moderno”) and MUST NOT replace the classical ruler in the decan or dignity tables.

### 4.4 Element × modality matrix

| Elemento | Cardinal | Fija | Mutable |
|---|---|---|---|
| Fuego | Aries | Leo | Sagitario |
| Tierra | Capricornio | Tauro | Virgo |
| Aire | Libra | Acuario | Géminis |
| Agua | Cáncer | Escorpio | Piscis |

This matrix MUST be exact. It is the cleanest test that the data is right: each element appears once per modality, and each modality once per element.

### 4.5 Decans (Chaldean order)

Each sign has three decans of 10°. The rulers follow the Chaldean sequence: Mars → Sun → Venus → Mercury → Moon → Saturn → Jupiter, repeated.

| Signo | Decano I · 0°–9°59′ | Decano II · 10°–19°59′ | Decano III · 20°–29°59′ |
|---|---|---|---|
| Aries | Marte | Sol | Venus |
| Tauro | Mercurio | Luna | Saturno |
| Géminis | Júpiter | Marte | Sol |
| Cáncer | Venus | Mercurio | Luna |
| Leo | Saturno | Júpiter | Marte |
| Virgo | Sol | Venus | Mercurio |
| Libra | Luna | Saturno | Júpiter |
| Escorpio | Marte | Sol | Venus |
| Sagitario | Mercurio | Luna | Saturno |
| Capricornio | Júpiter | Marte | Sol |
| Acuario | Venus | Mercurio | Luna |
| Piscis | Saturno | Júpiter | Marte |

**Source note:** Chaldean decans as transmitted in Hellenistic and medieval astrology (e.g. *Picatrix*); other decan systems exist and MUST NOT be mixed into this table.

### 4.6 Traditional planetary dignities

| Planeta | Domicilio | Exaltación | Detrimento | Caída |
|---|---|---|---|---|
| Sol | Leo | Aries | Acuario | Libra |
| Luna | Cáncer | Tauro | Capricornio | Escorpio |
| Mercurio | Géminis, Virgo | Virgo | Sagitario, Piscis | Piscis |
| Venus | Tauro, Libra | Piscis | Aries, Escorpio | Virgo |
| Marte | Aries, Escorpio | Capricornio | Libra, Tauro | Cáncer |
| Júpiter | Sagitario, Piscis | Cáncer | Géminis, Virgo | Capricornio |
| Saturno | Capricornio, Acuario | Libra | Cáncer, Leo | Aries |

**Modern outer planets** (Uranus, Neptune, Pluto) have modern domicile associations (Aquarius, Pisces, Scorpio) but no classical exaltation/detriment/fall in this system. If shown, they MUST be labelled “moderno” and kept visually secondary.

### 4.7 Glyph policy

- Glyph source: the Unicode zodiac block U+2648–U+2653.
- Do **not** depend on a system font: draw the twelve glyphs as SVG paths, traced from public-domain or original vector sources.
- Keep a consistent stroke weight (1.75 px at 24 px), square-ish terminals, and a 24 × 24 viewBox.
- Each glyph gets a `title` in the SVG sprite: `Aries`, `Tauro`, etc.
- The visible name is always text next to the glyph; the glyph alone is never the only label.
- The glyphs are **decorative in the UI** (`aria-hidden="true"`); the button/article carries the accessible name.

### 4.8 Keywords (3 per sign, poetic not predictive)

| Signo | Palabras |
|---|---|
| Aries | impulso · comienzo · filo |
| Tauro | cuerpo · calma · constancia |
| Géminis | palabra · juego · travesía |
| Cáncer | refugio · memoria · marea |
| Leo | presencia · calor · escena |
| Virgo | oficio · detalle · cosecha |
| Libra | medida · acuerdo · balanza |
| Escorpio | hondura · verdad · corriente |
| Sagitario | horizonte · sentido · flecha |
| Capricornio | estructura · tiempo · cumbre |
| Acuario | red · aire · futuro |
| Piscis | disolución · compasión · sueño |

These are editorial, not doctrine. They MUST NOT be used to make claims about a person.

### 4.9 Body correspondences

The body column is the traditional **melothesia** (sign–body mapping). It MUST be shown with a note: *“Correspondencia simbólica tradicional. No es consejo médico.”* Do not turn it into health advice.

### 4.10 What the page must not say

- “Tu signo dice que eres…”
- “Compatible con…”
- “Predicción para hoy / esta semana / este año.”
- “Energía cósmica”, “destino”, “mala racha”.
- “Científicamente demostrado.”
- “Ophiuchus es tu verdadero signo.” (It is a constellation, not a tropical sign.)
- “Los signos son constelaciones.”

---

## 5. Information architecture

### 5.1 Homepage teaser

Add one calm teaser after **Residentes** (`#paso-3`) and before **La luz** (`#paso-4`). Do not add a ninth step to the stepbar in Phase 1; the teaser is a **link**, not a new step.

```
kicker: El cielo
h2: Doce puertas. Una plaza.
lede: La rueda del recinto: doce tramos de cielo, doce formas de estar.
cta: Entrar en la plaza →  (link to signs/index.html)
```

Visual: a cropped arc of the wheel on the right, using the Horizon bubble at the centre; no auto-rotation.

### 5.2 Dedicated page: `signs/index.html`

Structure:

1. **Header** — Chatland wordmark, back to presentation, language slot reserved.
2. **Hero** — “La Plaza de los Signos”; lede; a small note “Astrología simbólica, no ciencia.”
3. **System selector** — “Zodíaco occidental” active; “Maya · Chino · Védico” disabled with `Próximamente`.
4. **The wheel** — 12 gates, centre Horizon mark, legend.
5. **Sign cards** — 12 `<article>`s in a grid; the canonical content, readable without JS.
6. **Find your sign** — date input + result; estimate note.
7. **How to read this wheel** — signs vs constellations, tropical vs sidereal, decans, dignities, sources.
8. **Footer** — back to Chatland, source notes, “no es una predicción”.

### 5.3 Navigation

- Homepage nav: add **Signos** between **Residentes** and **La luz**.
- Footer: add **La Plaza de los Signos**.
- The signs page back-link returns to `../index.html`.

---

## 6. Visual system

### 6.1 Palette

Use the existing Chatland tokens:

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#F4F3E7` | page ground |
| `--card` | `#FFFFFF` | cards |
| `--ink` | `#14211C` | text and glyph strokes |
| `--muted` | `#5B665D` | secondary text |
| `--grass` | `#2E9E6B` | earth accent |
| `--lime` | `#BFE06A` | earth highlight |
| `--sky` | `#59BBD6` | air accent |
| `--sun` | `#F0B03C` | fire highlight |
| `--clay` | `#D9663F` | fire accent |

Add one token for water: `--water:#3F7E8C` (deep sky). If the brand rejects a new hue, use `--sky` at 70% mixed with `--ink`; do not invent a bright blue.

**Rule:** text is always `--ink` or `--muted`. Element colors are tints, rules, glyph accents and plate backgrounds only. Never put small text in `--clay` or `--sun` on paper.

### 6.2 The sign plate

Each sign has a square “sky plate”:

- The Chatland bubble outline, 1.5 px `--ink`.
- Inside: a horizon with the sun and one hill.
- Element maps to the plate tint:
  - Fire: sun-high, clay sky.
  - Earth: low sun, grass/lime hills.
  - Air: pale sky, thin clouds or a high horizon line.
  - Water: deep sky, a low horizon and a reflecting line.
- The sign glyph sits at the centre of the sun, in ink, 24–32 px.
- The sign number sits in mono at the top-left; the dates at the bottom.
- Modality is carried by the sun position:
  - Cardinal: sun at the horizon (rising).
  - Fixed: sun high (noon).
  - Mutable: sun low (setting).
- No two plates are identical; hue + sun position + hill shape vary by sign.
- The plate is decorative; the card text carries the meaning.

### 6.3 The wheel

- Presentation wheel, not a natal chart.
- **Aries at 12 o’clock, clockwise.** State this in the “Cómo leer” note; a natal chart places the Ascendant on the left and measures from it, but this is a public plaza, not a chart.
- 12 equal sectors of 30°; 1.5° gap between sectors.
- Inner radius 150, outer radius 330 (on a 720 × 720 viewBox); centre Horizon bubble radius 110.
- Decan ticks at 10° and 20° inside each sector, 1 px.
- Each sector is an HTML `<button>` positioned over a decorative SVG; the SVG carries the ring, ticks and glyphs.
- Hover/focus: sector fills with the element tint at 10%; glyph moves 2 px outward. No rotation.
- Selected: fill 18%; glyph remains; a thin clay ring marks the gate.
- Disabled/planned systems: the selector shows them, the wheel does not.
- The wheel DOES NOT auto-rotate. On `prefers-reduced-motion`, no transitions.

### 6.4 Typography

- Sign names: existing display serif (`Iowan Old Style` / Palatino / Georgia), lowercase or title case as designed.
- Dates and degrees: mono, 0.68–0.75 rem, uppercase tracking.
- Body: existing sans, 16 px, 62–68 characters.
- No new font files.

### 6.5 Motion

- Wheel entrance: ring draws in once, 700 ms; gates fade in with 40 ms stagger.
- Sign selection: plate cross-fade 200 ms; no bounce.
- Dialog: 220 ms opacity + 8 px rise.
- `prefers-reduced-motion`: everything instant.
- No perpetual animation, no spinning wheel, no twinkling stars.

---

## 7. Data model

### 7.1 One source of truth

```js
const SIGN_SYSTEMS = {
  western: {
    id: 'western',
    status: 'live',
    label: { es: 'Zodíaco occidental', en: 'Western zodiac' },
    zodiac: 'tropical',
    divisions: 12,
    startAngle: -90,      // Aries at 12 o'clock
    direction: 1,         // clockwise
    source: 'Hellenistic–medieval tradition; tropical 30° sectors',
    signs: [ /* 12 entries */ ],
  },
  mayan:   { status: 'planned', divisions: 20, label: { es: 'Maya', en: 'Mayan' } },
  chinese: { status: 'planned', divisions: 12, label: { es: 'Chino', en: 'Chinese' } },
  vedic:   { status: 'planned', divisions: 27, label: { es: 'Védico', en: 'Vedic' } },
};
```

### 7.2 Sign record

```js
{
  code: 'aries',
  index: 0,
  name: { es: 'Aries', en: 'Aries' },
  glyph: 'aries',
  dates: { es: '21 mar – 19 abr', en: 'Mar 21 – Apr 19', approximate: true },
  element: 'fire',
  modality: 'cardinal',
  polarity: 'yang',
  ruler: { traditional: 'mars', modern: 'mars' },
  decans: [
    { span: [0, 10], ruler: 'mars' },
    { span: [10, 20], ruler: 'sun' },
    { span: [20, 30], ruler: 'venus' },
  ],
  body: { es: 'Cabeza', en: 'Head' },
  keywords: { es: ['impulso', 'comienzo', 'filo'], en: ['impulse', 'beginning', 'edge'] },
  source: 'Ptolemy, Tetrabiblos; Unicode U+2648; Chaldean decans',
  plate: { elementTint: 'fire', sun: 'horizon', hill: 1 },
}
```

### 7.3 Elements, modalities and planets

```js
const ELEMENTS = {
  fire:  { es: 'Fuego',  en: 'Fire',  polarity: 'yang', token: '--clay' },
  earth: { es: 'Tierra', en: 'Earth', polarity: 'yin',  token: '--grass' },
  air:   { es: 'Aire',   en: 'Air',   polarity: 'yang', token: '--sky' },
  water: { es: 'Agua',   en: 'Water', polarity: 'yin',  token: '--water' },
};

const MODALITIES = {
  cardinal: { es: 'Cardinal', en: 'Cardinal' },
  fixed:    { es: 'Fija',     en: 'Fixed' },
  mutable:  { es: 'Mutable',  en: 'Mutable' },
};

const PLANETS = {
  sun:     { es: 'Sol',      en: 'Sun',     glyph: '☉' },
  moon:    { es: 'Luna',     en: 'Moon',    glyph: '☽' },
  mercury: { es: 'Mercurio', en: 'Mercury', glyph: '☿' },
  venus:   { es: 'Venus',    en: 'Venus',   glyph: '♀' },
  mars:    { es: 'Marte',    en: 'Mars',    glyph: '♂' },
  jupiter: { es: 'Júpiter',  en: 'Jupiter', glyph: '♃' },
  saturn:  { es: 'Saturno',  en: 'Saturn',  glyph: '♄' },
  uranus:  { es: 'Urano',    en: 'Uranus',  glyph: '♅', modern: true },
  neptune: { es: 'Neptuno',  en: 'Neptune', glyph: '♆', modern: true },
  pluto:   { es: 'Plutón',   en: 'Pluto',   glyph: '♇', modern: true },
};
```

### 7.4 No duplicated content

- The 12 `<article>` cards in HTML and the JS data MUST read from the same JSON/JS object; build the cards from the data at build time or render them at load with a no-JS fallback.
- Preferred: author the data once in `assets/js/zodiac-data.js`, render the cards with JS, and place `<noscript>` summary in the page. However, SEO requires the content in the initial HTML; if the site stays framework-free, generate the HTML with a small build script or duplicate carefully with a test that compares the two.
- The cleanest static approach: keep the **12 articles in HTML** as the source of truth for copy, and keep the wheel data in JS for geometry. Use a build-time check that every code in the data has a matching article and vice versa.

---

## 8. Interaction and state

### 8.1 Selecting a gate

1. Click / `Enter` / `Space` on a gate.
2. Set `selected = 'aries'`; update the button `aria-current="true"`.
3. Open the detail panel/dialog with the sign card.
4. Update the URL hash to `#sign-aries` via `history.replaceState`.
5. On mobile, the dialog opens; on desktop, a side panel updates in place.

### 8.2 Deselecting

- Clicking the active gate again clears the selection.
- `Esc` closes the dialog and clears `aria-current`.
- Closing the dialog returns focus to the gate.
- When cleared, the centre Horizon mark returns; no other gate moves.

### 8.3 Deep links

- `#sign-aries` opens Aries on load.
- `#sign-aries` from another page (`../signs/index.html#sign-aries`) works.
- `hashchange` and `popstate` sync the UI.
- Unknown hashes fall back to the wheel with no selection and do not throw.

### 8.4 Find your sign

- Input: `date` (required), optional `time` (not required for Sun sign).
- Compute the Sun’s apparent longitude (tropical) with a low-precision solar formula; the sign index is `floor(longitude / 30)`.
- Show: sign name, approximate dates, and “Estimado por longitud solar”.
- If within **1°** of a cusp, show the cusp warning.
- Do not ask for birth place; a Sun sign does not need it.
- Do not store the date; no analytics on it.
- If JS is disabled, the date finder is hidden; the static sign cards remain.

### 8.5 Keyboard map

| Key | Action |
|---|---|
| `Tab` | move through gates and cards |
| `←` / `→` | previous / next gate (roving tabindex) |
| `↑` / `↓` | previous / next gate (optional, same as arrows) |
| `Home` / `End` | first / last gate |
| `Enter` / `Space` | open selected gate |
| `Esc` | close dialog / clear selection |

### 8.6 URL and analytics

- No analytics events required in Phase 1.
- If analytics is added later, track only `sign_open` with the sign code; never send birth dates or any personal data.

---

## 9. Extension: leaving room for other systems

### 9.1 UI

- A **system selector** at the top of the page:
  - `Zodíaco occidental` — active.
  - `Maya`, `Chino`, `Védico` — disabled chips with a small mono label **Próximamente** and `aria-disabled="true"`.
- The disabled chips are visible, not hidden. They communicate that the plaza is bigger than one tradition, without faking content.
- Do not add a dropdown that implies the others work.

### 9.2 Engine contract

The wheel engine MUST be system-agnostic:

```js
function renderWheel(system) {
  // system.divisions: 12, 20, 27, 8…
  // system.startAngle, system.direction
  // system.signs[i].glyph, .label, .tint
}
```

- For 12 signs, use the 12-gate layout in §6.3.
- For 20/27/8 divisions, the same engine SHOULD support:
  - a different number of sectors,
  - smaller glyphs,
  - a density mode (labels on hover only),
  - a different start angle.
- Do **not** hard-code 30° in CSS; compute `360 / divisions`.
- Do **not** reuse Western glyphs or element colors for other systems. Each system supplies its own `plate` and `palette`.

### 9.3 Data contract for future systems

A future system MUST provide:

1. `id`, `label`, `status`, `zodiac` (tropical/sidereal/other).
2. `divisions`, `startAngle`, `direction`.
3. `signs[]` with source refs and glyph paths.
4. A `source` note and a rights statement.
5. A `renderPlate()` override if its visual grammar is not the 30° sector.

The Gipsy system is explicitly **on hold** in Chatland: no invented glyphs, no decorative “gypsy” motifs; community review is required before any content.

---

## 10. Technical architecture

### 10.1 Files

| File | Purpose |
|---|---|
| `signs/index.html` | dedicated page, static 12 cards, wheel mount, dialog |
| `assets/js/zodiac-data.js` | `SIGN_SYSTEMS`, 12 signs, elements, modalities, planets, decans, dignities |
| `assets/js/zodiac.js` | wheel rendering, selection, dialog, hash sync, date finder |
| `assets/css/zodiac.css` | page layout, wheel, plates, cards, dialog (imported after `site.css`) |
| `assets/signs/zodiac-glyphs.svg` | 12 glyph symbols in a sprite |
| `assets/signs/plates/*.svg` (optional) | per-sign plates if hand-drawn beyond CSS |
| `index.html` | nav link + teaser section |
| `assets/css/site.css` | only the new `--water` token and nav spacing if needed |
| `assets/js/site.js` | no zodiac logic; no changes except possibly nav |

### 10.2 DOM sketch

```html
<section class="signs" id="signs" aria-labelledby="signs-title">
  <header class="signs-head">
    <p class="eyebrow">El cielo</p>
    <h1 id="signs-title">La Plaza de los Signos</h1>
    <p class="lede">Doce puertas. Doce tramos de cielo. Ninguna adivina: cada una describe una forma de estar.</p>
    <div class="sign-systems" role="group" aria-label="Sistemas">
      <button class="sys is-active" aria-pressed="true">Zodíaco occidental</button>
      <button class="sys" aria-disabled="true" disabled>Maya · Próximamente</button>
      <!-- … -->
    </div>
  </header>

  <div class="signs-stage">
    <div class="wheel" role="group" aria-label="Rueda de los doce signos">
      <svg class="wheel-art" viewBox="0 0 720 720" aria-hidden="true">…</svg>
      <button class="gate" data-sign="aries" aria-label="Aries, 21 de marzo a 19 de abril, fuego cardinal">…</button>
      <!-- 12 gates -->
      <div class="wheel-centre" aria-hidden="true">…Horizon mark…</div>
    </div>
    <aside class="sign-detail" id="signDetail" aria-live="polite">
      <!-- selected sign card, or the "choose a gate" empty state -->
    </aside>
  </div>

  <section class="sign-cards" aria-label="Los doce signos">
    <article id="sign-aries" data-sign="aries">…static card…</article>
    <!-- 12 articles -->
  </section>

  <section class="sign-finder">…date input…</section>
  <section class="sign-notes">…accuracy notes…</section>
</section>
```

### 10.3 CSS geometry

```css
.wheel { position: relative; aspect-ratio: 1; width: min(100%, 720px); }
.gate {
  position: absolute; left: 50%; top: 50%;
  transform:
    translate(-50%, -50%)
    rotate(calc(var(--i) * var(--step)))
    translateY(calc(var(--rim) * -1))
    rotate(calc(var(--i) * var(--step) * -1));
}
```

- Tokens: `--step: 30deg`, `--rim: 240px`, `--gate-size: 54px`.
- Gate labels stay upright via the counter-rotation.
- At 390 px: `--rim: 132px`, `--gate-size: 40px`, labels collapse to glyphs; names are in the cards and detail panel.

### 10.4 Dates and solar longitude

```js
// Low-precision apparent solar longitude (Meeus, Astronomical Algorithms, ch. 25).
// Accuracy is sufficient for a Sun-sign estimate, not for a natal chart.
function sunLongitude(date) {
  const jd = date.getTime() / 86400000 + 2440587.5;
  const n = jd - 2451545.0;
  const L = (280.460 + 0.9856474 * n) % 360;
  const g = ((357.528 + 0.9856003 * n) % 360) * Math.PI / 180;
  const lambda = L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g);
  return (lambda + 360) % 360; // tropical longitude
}
```

- Evaluate at **local noon** for a date-only input; this is a convention, not a birth chart.
- Warn when `lambda % 30` is within 1° of 0°.
- Unit-test against known equinoxes/solstices and 12 fixture dates.

### 10.5 Performance budget

| Item | Budget |
|---|---|
| HTML (signs page) | ≤ 60 KB |
| CSS (new) | ≤ 8 KB |
| JS (data + renderer) | ≤ 14 KB minified |
| SVG sprite | ≤ 12 KB |
| Images | none (all vector) |
| Total initial | ≤ 150 KB |
| LCP on 4G | < 1.5 s |
| CLS | < 0.05 |
| No continuous animation | 0 rAF loops |

---

## 11. Accessibility

- The wheel is **not** an SVG-only control: each gate is a real `<button>` with a text accessible name.
- Accessible name example: `Aries, 21 de marzo a 19 de abril, fuego, cardinal`.
- Roving tabindex: one gate at a time; arrows move focus; `Home`/`End` jump.
- Visible focus ring: 2 px `--ink` + 2 px offset on paper; never remove outline.
- The decorative SVG has `aria-hidden="true"`; the centre mark is decorative.
- The detail panel uses `aria-live="polite"` only when a selection is committed; do not announce hover.
- The dialog uses native `<dialog>` with a focus trap fallback for older browsers; `Esc` closes; focus returns to the gate.
- Color is never the only signal: element/modality are written in text; glyphs have names.
- Contrast: body text ≥ 4.5:1; large text ≥ 3:1; glyph strokes ≥ 3:1.
- Chart/table alternatives: the 12 cards are the text equivalent; no information lives only in the wheel.
- `prefers-reduced-motion`: no draw-in, no cross-fade, no hover lift.
- The date finder has a label, a submit button, an `aria-live` result, and a clear “estimated” note.

---

## 12. SEO, sharing and i18n

- **Title:** `La Plaza de los Signos · Chatland`
- **Description:** `Los doce signos del zodíaco occidental en Chatland: fechas, elementos, modalidades, regentes y decanos. Una plaza simbólica, no una predicción.`
- **Canonical:** `/signs/`; update if the production path differs.
- **Structured data:** `ItemList` with 12 `ListItem`s linking to `#sign-aries` etc. Do not use `FAQPage` for astrology claims.
- **Static content:** the 12 cards are in the initial HTML, so the page is readable and indexable without JS.
- **Internal links:** homepage teaser → `/signs/`; signs page → `/#paso-3`; footer link both ways.
- **i18n:** Phase 1 is Spanish (`lang="es"`). Keep all strings in the data model with `{ es, en }`; add `lang` attributes when English ships. Do not machine-translate sign names.
- **OG image:** a single 1200 × 630 crop of the wheel with the title; no personal data.

---

## 13. Content and voice

- Use the Chatland voice from the main site: short, warm, place-based.
- Prefer “tramo”, “puerta”, “plaza”, “cielo” over “predicción” and “energía”.
- Every sign card answers four questions, in this order:
  1. **Qué es:** “Aries abre la rueda…”
  2. **Cuándo:** approximate dates.
  3. **Cómo se compone:** element, modality, ruler.
  4. **Qué mira:** 3 keywords + body correspondence (with the symbolic note).
- One honest note, not a legal wall:
  > *“Esto es astrología simbólica, no ciencia. La rueda no calcula una carta natal ni dice qué te va a pasar.”*
- Do not use testimonials, compatibility scores or “signo ascendente” clickbait.

### 13.1 Sign card copy skeleton

```
01 · Aries  ♈
21 mar – 19 abr
Fuego · Cardinal · Yang
Regente: Marte (tradicional y moderno)
Decanos: Marte · Sol · Venus
Cabeza
impulso · comienzo · filo

Aries abre la rueda: el primer tramo después del equinoccio.
Su elemento es el fuego y su modalidad, cardinal: la chispa que inicia.
```
(Each sign gets a 2–3 sentence original text; do not paste generic horoscope copy.)

---

## 14. Implementation phases

### Phase 0 — Accuracy and content (2 days)

- [ ] Freeze the data tables in §4.
- [ ] Verify 12 dates, 4 × 3 matrix, 6/6 polarity, 36 decans, 7 dignity rows.
- [ ] Write the 12 sign cards in Spanish (2–3 sentences each).
- [ ] Source note for glyphs, decans and melothesia.
- [ ] Gate: a reviewer can check every cell against a cited source.

### Phase 1 — Static page and plates (3 days)

- [ ] Create `signs/index.html` with header, hero, system selector, 12 static cards, notes, footer.
- [ ] Create the 12 glyphs as an SVG sprite.
- [ ] Build the 12 plates (CSS or inline SVG) using the Horizon motif.
- [ ] Add homepage teaser + nav/footer links.
- [ ] Gate: no JS, all 12 signs readable; Lighthouse structure clean.

### Phase 2 — Wheel and selection (3 days)

- [ ] Render the 12 gates over the decorative wheel.
- [ ] Roving tabindex, arrow keys, focus ring.
- [ ] Select/deselect, detail panel, dialog.
- [ ] Hash deep links and back/forward.
- [ ] Gate: 12 gates, keyboard complete, no other gate moves.

### Phase 3 — Date finder and polish (2 days)

- [ ] `sunLongitude()` + sign finder + cusp warning.
- [ ] EN/ES data shell (only ES visible).
- [ ] `prefers-reduced-motion`, mobile 390, print styles.
- [ ] Gate: fixture dates pass; no layout shift.

### Phase 4 — QA, SEO and handoff (2 days)

- [ ] `html-validate`, JS syntax, link check.
- [ ] Lighthouse, contrast, screen-reader pass.
- [ ] OG image, meta, ItemList.
- [ ] Documentation: how to add a sign, how to add a future system.
- [ ] Gate: all acceptance criteria pass.

### Phase 5 — Future systems (not scheduled)

- [ ] Maya: 20 day signs + 13 tones; needs source review.
- [ ] Chinese: 12 branches + 10 stems + 5 elements; needs a different visual grammar.
- [ ] Vedic: 12 rāśis + 27 nakṣatras; needs a sidereal toggle and source review.
- [ ] Celtic/Gipsy: source/community review before any code.
- No dates until Phase 0–4 ship.

---

## 15. Acceptance criteria

1. **Twelve signs**
   Given the page loads,
   then exactly 12 gates and 12 sign articles exist, with the codes in §4.3.

2. **Accuracy**
   Given the data,
   then each element × modality cell matches §4.4, polarity is 6/6, and all 36 decans match §4.5.

3. **Select / deselect**
   Given Aries is closed,
   when the Aries gate is clicked,
   then its card opens and the gate is marked current;
   when clicked again, the card closes and no other gate moves.

4. **Keyboard**
   Given focus is on a gate,
   then arrows cycle gates, `Home`/`End` jump, `Enter` opens, `Esc` closes and returns focus.

5. **Deep link**
   Given `#sign-pisces`,
   then Piscis opens on load; back/forward sync the state.

6. **Finder**
   Given 1 April 2026,
   then the finder returns Aries; given 1 May 2026, Tauro;
   near a cusp it shows the cusp warning.

7. **Accuracy note**
   Then the page states that signs are 30° tropical sectors, not constellations, and that this is symbolic, not predictive.

8. **Extension**
   Then the system selector shows Western active and the others disabled as “Próximamente”; no broken controls.

9. **Mobile and a11y**
   Then 390 px has no horizontal scroll; every gate has an accessible name; reduced motion is honoured.

10. **No false claims**
    Then no copy promises predictions, compatibility, medical or financial outcomes.

---

## 16. Test plan

### 16.1 Data tests

- `signs.length === 12`.
- Every sign has all fields; `ruler.traditional` exists.
- Element counts: 3 each; modality counts: 4 each; polarity: 6/6.
- Decan sequence follows the Chaldean order; 36 entries; spans 0–10/10–20/20–30.
- Dignity table has 7 planets and no modern outer planet in the classical columns.
- No duplicate codes; `index` is 0–11 and matches the wheel order.

### 16.2 Date tests

| Date | Expected |
|---|---|
| 2026-03-21 | Aries |
| 2026-04-19 | Aries (cusp check) |
| 2026-04-20 | Tauro |
| 2026-06-21 | Cáncer (cusp) |
| 2026-09-23 | Libra (cusp) |
| 2026-12-22 | Capricornio (cusp) |
| 2027-02-19 | Piscis |

Use a fixed locale/timezone in tests; assert the cusp warning appears within 1°.

### 16.3 UI tests

- 12 gates, 12 articles, one active at a time.
- Select/deselect; URL hash changes; no layout shift.
- Arrow/Home/End/Enter/Esc.
- Mobile 390/768/1280 screenshots.
- No console errors; no failed requests.

### 16.4 Accessibility / quality

- `html-validate` passes.
- Axe or manual: names, roles, focus order, contrast.
- Reduced motion: no transitions.
- Lighthouse: performance ≥ 95, accessibility 100, best practices ≥ 95, SEO 100 (targets; test on the real deploy).

---

## 17. Risks and decisions

| Risk | Mitigation |
|---|---|
| Turning Chatland into a horoscope app | The plaza is a place, not a feed; no predictions, no compatibility, no daily content |
| Inaccurate dates | Ranges are approximate; the finder uses solar longitude; cusp warning |
| Signs vs constellations confusion | Explicit note; no constellation art passed off as signs |
| Cultural overreach | Western zodiac only; other systems gated; sources documented |
| Visual clutter | 12 gates, one centre, no perpetual motion; labels collapse on mobile |
| Accessibility of a wheel | HTML buttons over a decorative SVG; full text alternative |
| SEO duplication | 12 static articles; one canonical; no thin tag pages |
| Scope creep into charts | Houses/aspects/transits explicitly out of scope; no chart UI |
| Font glyph coverage | SVG paths, not Unicode font glyphs |

---

## 18. Open questions

1. Does the plaza live as a **subpage** (recommended) or as a ninth homepage step?
2. Should the homepage teaser show the full wheel or a cropped arc?
3. Do we show decans and dignities to everyone, or fold them into an “Avanzado” disclosure?
4. Does Chatland want a **sidereal** toggle later, or stay tropical-only?
5. Should signs have future **resident affinities** (a sign-linked resident) or stay independent?
6. Is the water token `#3F7E8C` accepted into the palette, or should water use a sky/ink mix?
7. English in Phase 2 or after launch?

---

## 19. Appendix — sources and accuracy notes

- **Tropical zodiac definition:** 30° sectors measured from the vernal equinox; signs are not constellations.
- **Dates:** approximate Sun-ingress ranges; exact ingress varies by year/time zone.
- **Decans:** Chaldean order as transmitted in Hellenistic and medieval sources; other decan systems exist and are not mixed here.
- **Dignities:** classical rulership, exaltation, detriment and fall; modern outer-planet rulerships are marked separately.
- **Glyphs:** Unicode zodiac block U+2648–U+2653; SVG paths traced from public-domain or original vector sources.
- **Melothesia:** traditional symbolic body correspondences; not medical advice.
- **Constellations:** IAU boundaries; the ecliptic crosses 13 constellations, including Ophiuchus; this does not add a 13th tropical sign.
- **Precession:** the tropical wheel is anchored to the equinox, so it no longer coincides with the visible constellations; the page says so.
- **Recommended references:** Ptolemy, *Tetrabiblos*; Vettius Valens, *Anthology*; *Picatrix* (decans); standard astronomical ephemeris for ingress checks; Unicode charts for glyph reference.

**Definition of done:** the 12 signs are accurate, the wheel is calm and accessible, the page reads as a Chatland place rather than an astrology feed, and a second tradition can be added by data and one registry entry without redesigning the wheel.
