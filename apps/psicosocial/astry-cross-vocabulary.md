# Astry · Cross-System Vocabulary — Research and Smoothing

- **Status:** research note + vocabulary proposal
- **Purpose:** give the Astry web wheel one controlled vocabulary for six traditions without flattening them.
- **Companion:** `astry-web-wheel-spec.md`
- **Normative language:** **MUST**, **SHOULD**, **MAY** follow RFC 2119.

> **Core rule:** sameness is the exception, not the default. Most cross-system pairs are **homologies** (same structural role) or **resonances** (thematic echo), not **equivalences**. The UI MUST label which one it is using.

---

## 1. Method

### 1.1 Three levels of relation

| Level | Definition | UI label | Example |
|---|---|---|---|
| **Equivalence** | Both systems explicitly define the same thing | `=` | 0° Aries = spring equinox in the tropical zodiac |
| **Homology** | Same structural role, different content | `≈` | Western *sign* ≈ Vedic *rāśi* (both 30° divisions, but tropical vs sidereal) |
| **Resonance** | Thematic echo, no shared structure | `~` | Western Aries ~ Mayan Imix (beginning/water) |
| **False friend** | Same word, different meaning | `≠` | Western *house* ≠ Vedic *bhāva* in all systems; Chinese *element* ≠ Greek *stoicheion* |

### 1.2 Cautions

- Do not translate local terms away. Show the local term and a gloss.
- Do not map 12 Western signs one-to-one onto 12 Chinese branches or 20 Mayan day signs.
- Do not use a shared color code across systems; colors are local.
- Do not treat “element” as one thing. Western four elements, Vedic tattvas and Chinese wǔxíng are different schemes.
- Do not make moral or predictive adjectives (“good”, “bad”, “lucky”, “dangerous”).
- Gipsy/Romani has no uncontested canonical astrological vocabulary in this project; it stays on hold until community review.

---

## 2. The common spine

Use these eight concepts in code, UI and documentation. They are the **shared spine**, not a claim that every system has all eight.

| # | Common concept | Question it answers | UI term (ES / EN) |
|---|---|---|---|
| 1 | **Field** | Where is it? | `campo` / `field` |
| 2 | **Agent** | What acts? | `agente` / `agent` |
| 3 | **Cycle** | When / in what rhythm? | `ciclo` / `cycle` |
| 4 | **Quality** | How is it shaped? | `cualidad` / `quality` |
| 5 | **Relation** | With what / whom? | `relación` / `relation` |
| 6 | **Angle** | From where is it seen? | `ángulo` / `angle` |
| 7 | **Action** | What does it do? | `acción` / `action` |
| 8 | **Tone** | How does it feel? | `tono` / `tone` |
| 9 | **Aim** | Toward what? | `intención` / `aim` |

The spine is deliberately **functional**, not metaphysical. It lets the UI say “here is a field, an agent, a relation” without claiming that a Vedic graha is a Western planet.

---

## 3. System vocabularies

### 3.1 Western (tropical)

| Local term | Gloss | Spine | Notes |
|---|---|---|---|
| **signo** / sign | 30° tropical sector | Field | 12 signs; not constellations |
| **planeta** / planet | celestial body or luminary | Agent | 10 bodies: Sun–Pluto |
| **casa** / house | topic sector of a chart | Cycle / Aim | House system must be declared |
| **aspecto** / aspect | angular relation | Relation | Conjunction, sextile, square, trine, opposition, minors |
| **ángulo** / angle | ASC, DSC, MC, IC | Angle | Requires time + place |
| **ascendente** / Ascendant | eastern horizon | Angle | Left of a chart |
| **descendente** / Descendant | western horizon | Angle | Opposite the ASC |
| **medio cielo** / MC | upper meridian | Angle | Public / outer |
| **fondo del cielo** / IC | lower meridian | Angle | Roots / inner |
| **regente** / ruler | planet associated with a sign | Agent | Traditional and modern |
| **decano** / decan | 10° third of a sign | Cycle | Chaldean sequence |
| **orbe** / orb | allowed deviation from exact aspect | Relation | Depends on bodies/aspect |
| **aplicativo / separativo** | applying / separating | Relation | Direction of the aspect |

**Structural notes**

- Western is the only system in this plan with **angles** and **houses**.
- The 10 bodies are commonly Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto. The nodes, Chiron and asteroids are not part of the 10.
- Tropical vs sidereal MUST be declared. This plan uses tropical.

### 3.2 Vedic / Jyotiṣa

| Local term | Gloss | Spine | Notes |
|---|---|---|---|
| **rāśi** | 30° zodiac sign | Field | Usually sidereal; ayanāṃśa matters |
| **graha** | “seizer”; planet/luminary | Agent | Includes Sun, Moon, Mars… Saturn, and often Rāhu/Ketu |
| **bhāva** | house / domain | Cycle / Aim | Whole-sign vs quadrant systems differ |
| **nakṣatra** | lunar mansion | Field / Cycle | 27 (or 28) divisions |
| **tithi** | lunar day | Cycle | 30 tithis |
| **yoga** | combination | Relation | Not the same as Western aspect |
| **dṛṣṭi** | aspect / sight | Relation | Different rules and orbs |
| **daśā** | planetary period | Cycle | Time-lord system |
| **guṇa** | quality: sattva, rajas, tamas | Quality | Three guṇas; not Western modalities |
| **tattva** | element/principle | Quality | Earth, water, fire, air, ether |
| **puruṣārtha** | life aim: dharma, artha, kāma, mokṣa | Aim | Four aims |
| **trikoṇa / kendra / dusthāna** | house types | Cycle | Trine / angular / difficult |
| **ayanāṃśa** | sidereal offset | Field | The tropical–sidereal difference |

**Structural notes**

- Do not equate `rāśi` with a Western sign without the ayanāṃśa caveat.
- Do not equate `guṇa` with modality. Sattva/rajas/tamas is a different axis.
- Rāhu and Ketu are nodes, not physical planets; if shown, label them as such.

### 3.3 Chinese (wǔxíng and the sexagenary cycle)

| Local term | Gloss | Spine | Notes |
|---|---|---|---|
| **wǔxíng** (五行) | five phases / moving ones | Quality | Wood, fire, earth, metal, water; not Greek elements |
| **yīn / yáng** (陰陽) | polarity | Quality | Relational, not gendered |
| **tiāngān** (天干) | heavenly stems | Agent / Cycle | 10 stems |
| **dìzhī** (地支) | earthly branches | Field / Cycle | 12 branches; animals are labels |
| **guà** (卦) | trigram | Relation / Quality | 8 trigrams of three lines |
| **bāguà** (八卦) | eight trigrams | Field | Compass arrangement |
| **jiéqì** (節氣) | solar terms | Cycle | 24 seasonal nodes |
| **liùshí jiǎzǐ** (六十甲子) | 60-year cycle | Cycle | Stems × branches |
| **shēng** (生) | generating | Relation | Nourishing cycle |
| **kè** (克) | controlling | Relation | Checking cycle |
| **wàng / xiū / qiú / sǐ** | phase states | Quality | Seasonal strength states |

**Structural notes**

- `wǔxíng` is better translated “five phases” than “five elements”.
- The 12 “Chinese zodiac” animals are branch labels, not 12 signs in the Western sense.
- Yin/yang is not the same as Western polarity, even if the UI uses `polarity` as a shared slot.

### 3.4 Mayan (Tzolkʼin)

| Local term | Gloss | Spine | Notes |
|---|---|---|---|
| **tzolkʼin** | 260-day count | Cycle | 20 day names × 13 numbers |
| **kʼin** | day / sun | Cycle | Also “day” in the count |
| **day sign** | one of 20 named days | Field | Not a Western sign |
| **tone / number** | 1–13 coefficient | Quality / Cycle | A number, not a planet |
| **trecena** | 13-day arc | Cycle | 20 trecenas |
| **Haabʼ** | 365-day solar calendar | Cycle | 18 months + Wayebʼ |
| **Long Count** | absolute day count | Cycle | Not a zodiac |
| **way / nagual** | co-essence / birth day | Agent / Aim | Regional meanings vary |
| **day lord** | deity/quality of the day | Agent | Not a planet |

**Twenty day names (Yucatec, standard sequence):**

| # | Day | Common association (working gloss) |
|---|---|---|
| 01 | Imix | water, crocodile, primordial earth |
| 02 | Ikʼ | wind, breath, life force |
| 03 | Akʼbʼal | night, darkness, dawn |
| 04 | Kʼan | maize, net, abundance |
| 05 | Chikchan | serpent |
| 06 | Kimi | death, transition |
| 07 | Manikʼ | deer, hunt |
| 08 | Lamat | Venus, star, ripe maize |
| 09 | Muluk | water, jade, offering |
| 10 | Ok | dog, guide |
| 11 | Chuwen | monkey, craft, thread |
| 12 | Ebʼ | grass, rain, road |
| 13 | Bʼen | reed, young maize |
| 14 | Ix | jaguar, night sun |
| 15 | Men | eagle, wisdom |
| 16 | Kibʼ | owl/vulture, wax, soul |
| 17 | Kabʼan | earth, thought |
| 18 | Etzʼnabʼ | flint, knife |
| 19 | Kawak | storm, rain |
| 20 | Ajaw | lord, sun, completion |

**Structural notes**

- These glosses are **associations**, not fixed personality traits.
- The “Dreamspell” calendar is a modern New Age invention, not the classical Tzolkʼin; do not mix them.
- Do not map the 20 day signs to Western signs one-to-one.

### 3.5 Celtic / Ogham

| Local term | Gloss | Spine | Notes |
|---|---|---|---|
| **fid** (pl. **feda**) | Ogham letter | Field | 20 core letters |
| **aicme** (pl. **aicmí**) | letter family | Cycle / Field | Four families of five |
| **Bríatharogam** | kenning / word-riddle | Tone | Medieval glosses |
| **stemline** | the central line of an Ogham mark | Field | A writing geometry, not a zodiac |
| **notch** | 1–5 marks against the stemline | Quality / Action | Position (left/right/across) matters |
| **tree name** | e.g. beith = birch | Tone | The tree alphabet is a medieval/learned layer |
| **ogham stone** | inscribed monument | Source | Primary material context |

**Structural notes**

- Ogham is a **writing system**, not a zodiac. It can supply a line/notch grammar for the wheel, but not a 12-sign wheel.
- The tree meanings are traditional/medieval and sometimes reconstructed; label them as such.
- Do not use generic “Celtic knotwork” as a substitute for Ogham.

### 3.6 Gipsy / Romani — **on hold**

- There is no uncontested, single “Gipsy zodiac” visual canon.
- Much commercial “gypsy astrology” imagery is stereotyped or appropriative.
- The term “Gipsy” itself is contested; the UI label needs community input.
- **No invented glyphs, no crystal balls, no scarves, no palmistry clichés.**
- Required before content: named community reviewer, provenance, permission, preferred naming.
- Until then: a typographic placeholder only, clearly marked `fuente pendiente` / `source pending`.

---

## 4. Crosswalk

| Common spine | Western | Vedic | Chinese | Mayan | Celtic | Shared UI term | Relation |
|---|---|---|---|---|---|---|---|
| Field | sign | rāśi | branch | day sign | fid | `campo` | homology only |
| Agent | planet | graha | stem | day lord | — | `agente` | partial |
| Cycle | house | bhāva | solar term | trecena | aicme | `ciclo` | partial |
| Quality | element + modality | guṇa + tattva | wǔxíng + yin/yang | tone + direction | tree/notch | `cualidad` | resonance |
| Relation | aspect | dṛṣṭi | trigram relation | — | notch pattern | `relación` | partial |
| Angle | ASC/DSC/MC/IC | — | — | — | — | `ángulo` | Western only |
| Action | verb | verb | verb | verb | mark | `acción` | designed |
| Tone | adjective | adjective | adjective | adjective | adjective | `tono` | designed |
| Aim | house topic | puruṣārtha | — | way | — | `intención` | partial |

**Display rule:** every cross-system chip shows its relation mark: `=` (rare), `≈`, `~`, or `≠`. Do not hide the caveat in a tooltip.

---

## 5. The twelve arc adjectives

These are the “signature” adjectives. They are deliberately **system-neutral**: they describe a mode of acting, not a fixed personality. They are editorial, not doctrine.

| Sign | Arc adjective (ES) | Arc adjective (EN) | Sign verb (ES / EN) | Element | Modality | Polarity |
|---|---|---|---|---|---|---|
| Aries | incisivo/a | incisive | iniciar / initiate | fire | cardinal | yang |
| Tauro | firme | steadfast | asentar / settle | earth | fixed | yin |
| Géminis | conectivo/a | connective | enlazar / link | air | mutable | yang |
| Cáncer | cobijante | sheltering | cobijar / shelter | water | cardinal | yin |
| Leo | radiante | radiant | mostrar / show | fire | fixed | yang |
| Virgo | preciso/a | exacting | ajustar / adjust | earth | mutable | yin |
| Libra | armonizador/a | harmonizing | equilibrar / balance | air | cardinal | yang |
| Escorpio | penetrante | penetrating | ahondar / deepen | water | fixed | yin |
| Sagitario | visionario/a | far-seeing | orientar / aim | fire | mutable | yang |
| Capricornio | estructurante | structuring | estructurar / structure | earth | cardinal | yin |
| Acuario | circulante | circulating | conectar / connect | air | fixed | yang |
| Piscis | disolvente | dissolving | disolver / dissolve | water | mutable | yin |

### 5.1 Why these adjectives

- Each adjective is a **participle/adjective of action**, not a moral judgement.
- None implies “good”, “bad”, “lucky”, “dangerous”, “feminine” or “masculine”.
- Each has a verb counterpart, so the UI can move between “what it is” and “what it does”.
- They are broad enough to resonate with non-Western material without claiming identity.

---

## 6. The adjective axes

A single adjective is too blunt. The wheel uses six axes; each sign gets one value per axis. This is the **tone vector**.

| Axis | Values (ES) | Values (EN) |
|---|---|---|
| Temperature | cálido · templado · frío | warm · temperate · cool |
| Density | denso · firme · poroso | dense · firm · porous |
| Motion | veloz · pausado · oscilante | swift · slow · oscillating |
| Direction | expansivo · concentrado · envolvente | expansive · concentrated · enveloping |
| Texture | áspero · liso · fluido | rough · smooth · fluid |
| Light | luminoso · mate · reflectante | luminous · matte · reflective |

### 6.1 Proposed tone vectors

| Sign | Temp. | Density | Motion | Direction | Texture | Light |
|---|---|---|---|---|---|---|
| Aries | cálido | firme | veloz | expansivo | áspero | luminoso |
| Tauro | templado | denso | pausado | concentrado | liso | mate |
| Géminis | templado | poroso | veloz | expansivo | liso | reflectante |
| Cáncer | frío | poroso | pausado | envolvente | fluido | mate |
| Leo | cálido | firme | pausado | expansivo | liso | luminoso |
| Virgo | templado | denso | pausado | concentrado | áspero | mate |
| Libra | templado | poroso | oscilante | expansivo | liso | reflectante |
| Escorpio | frío | denso | pausado | concentrado | fluido | mate |
| Sagitario | cálido | poroso | veloz | expansivo | áspero | luminoso |
| Capricornio | frío | denso | pausado | concentrado | áspero | mate |
| Acuario | frío | poroso | oscilante | expansivo | liso | reflectante |
| Piscis | frío | poroso | pausado | envolvente | fluido | reflectante |

These vectors are a **design proposal**, to be reviewed by an editor. They are not claims about people.

### 6.2 Composing a tone string

```
Aries = incisivo · cálido · firme · veloz · expansivo · áspero · luminoso
```

The UI shows the **arc adjective** first, then the six axes on demand. This gives a short identity and a deeper texture without a wall of words.

---

## 7. Verb lexicons

### 7.1 Sign verbs

| Sign | Verb (ES) | Verb (EN) | What it names |
|---|---|---|---|
| Aries | iniciar | initiate | the first move |
| Tauro | asentar | settle | making something stay |
| Géminis | enlazar | link | connecting two things |
| Cáncer | cobijar | shelter | making a place safe |
| Leo | mostrar | show | bringing something into view |
| Virgo | ajustar | adjust | making something fit |
| Libra | equilibrar | balance | holding two sides |
| Escorpio | ahondar | deepen | going under the surface |
| Sagitario | orientar | aim | giving a direction |
| Capricornio | estructurar | structure | giving a frame |
| Acuario | conectar | connect | joining a network |
| Piscis | disolver | dissolve | letting a boundary go |

### 7.2 Planet verbs

| Body | Verb (ES) | Verb (EN) | Function |
|---|---|---|---|
| Sol | iluminar | illuminate | centre, show |
| Luna | nutrir | nurture | respond, hold |
| Mercurio | traducir | translate | name, exchange |
| Venus | atraer | attract | value, relate |
| Marte | activar | activate | push, cut |
| Júpiter | expandir | expand | open, grow |
| Saturno | limitar | limit | bound, structure |
| Urano | romper | break | interrupt, innovate |
| Neptuno | difuminar | blur | dissolve, imagine |
| Plutón | transformar | transform | deepen, remake |

### 7.3 Angle verbs

| Angle | Verb (ES) | Verb (EN) | Field |
|---|---|---|---|
| ASC | aparecer | appear | how one enters |
| DSC | encontrar | meet | how one meets the other |
| MC | proyectar | project | how one appears in public |
| IC | enraizar | root | where one comes from |

### 7.4 Element and modality verbs

| Quality | Verb (ES) | Verb (EN) |
|---|---|---|
| Fire | encender | kindle |
| Earth | sostener | hold |
| Air | mover | move |
| Water | fluir | flow |
| Cardinal | abrir | open |
| Fixed | mantener | maintain |
| Mutable | girar | turn |

---

## 8. Actions from lines

“Lines” can mean three different things. Keep them separate.

### 8.1 Western aspect lines

| Aspect | Angle | Verb (ES) | Verb (EN) | Adjective | Line grammar |
|---|---|---|---|---|---|
| Conjunción | 0° | fundir | fuse | fusivo | merged node / short bridge |
| Sextil | 60° | facilitar | ease | facilitador | thin dotted |
| Cuadratura | 90° | tensar | strain | tensivo | thick dashed |
| Trígono | 120° | fluir | flow | fluido | thin solid |
| Oposición | 180° | enfrentar | face | frontal | double chord through centre |
| Quincunx | 150° | ajustar | adjust | ajustante | dotted arc |
| Semisextil | 30° | rozar | graze | tangente | faint dotted |
| Semicuadratura | 45° | irritar | chafe | irritante | short thick dash |
| Sesquicuadratura | 135° | presionar | press | presionante | short thick dash + arc |
| Quintil | 72° | crear | create | creativo | fine dotted (optional) |
| Biquintil | 144° | inventar | invent | inventivo | fine dotted (optional) |

**Color rule:** do not paint trines green and squares red. Use a neutral palette plus line pattern, weight and opacity. “Support/tension” is an interpretation, not a traffic light.

### 8.2 Chinese trigram lines

| Line | Action (ES) | Action (EN) | Meaning |
|---|---|---|---|
| Solid (yang) | afirmar | affirm | active, unbroken |
| Broken (yin) | recibir | receive | receptive, open |
| Changing line | transformar | turn | the line is in transition |
| Lower trigram | habitar | inhabit | inner situation |
| Upper trigram | mostrarse | show | outer situation |

### 8.3 Ogham line

| Mark | Action (ES) | Action (EN) |
|---|---|---|
| Stemline | sostener | hold |
| 1–5 notches | marcar | mark |
| Aicme group | agrupar | group |
| Notch on the left / right / across | recibir / afirmar / cruzar | receive / affirm / cross |

### 8.4 Mayan bar and dot

| Mark | Action (ES) | Action (EN) |
|---|---|---|
| Bar (5) | agrupar | bundle |
| Dot (1) | contar | count |
| Shell (0) | vaciar | empty |
| Cartouche | contener | contain |

These line lexicons are **reserved**. The web wheel implements Western aspect lines first; the others are extension points.

---

## 9. Smoothing decisions

### 9.1 Terms that are safe to share

| Shared term | Use for | Do not use for |
|---|---|---|
| **field** | any position/division | claiming equivalence between counts |
| **agent** | any acting body/principle | claiming a graha is a planet in the astronomical sense |
| **cycle** | any time division | claiming houses = solar terms |
| **quality** | any element/modality/guna/phase | collapsing all qualities into one label |
| **relation** | any aspect/trigram/line relation | claiming dṛṣṭi = Western aspect |
| **action** | the verb layer | predicting events |
| **tone** | the adjective layer | judging character |
| **aim** | the purpose layer | moral ranking |

### 9.2 Terms that must stay local

- `rāśi`, `graha`, `bhāva`, `nakṣatra`, `guṇa`, `tattva`, `puruṣārtha`
- `wǔxíng`, `tiāngān`, `dìzhī`, `guà`, `jiéqì`
- `tzolkʼin`, `trecena`, `Haabʼ`, `way`
- `fid`, `aicme`, `Bríatharogam`
- `Ascendente`, `Descendente`, `MC`, `IC` (Western only)
- `Gipsy` / `Romani` — pending review

### 9.3 Adjectives that are safe across systems

Use the 12 arc adjectives and the six axes. They are **modes**, not identities. When applied to a non-Western sign, label them `resonancia` / `resonance`, never `equivalencia`.

### 9.4 Adjectives to ban

- lucky, unlucky, good, bad, positive, negative (for polarity), dark, dangerous
- masculine, feminine (for polarity or signs)
- compatible, incompatible (for people)
- destined, fated, cursed
- toxic, narcissistic, avoidant (clinical language)
- “energy” as a catch-all

---

## 10. Worked examples

### 10.1 Western Aries

```
Field: Aries (30° tropical sector)
Agent: Mars (traditional and modern)
Quality: fire · cardinal · yang
Action: initiate
Tone: incisive · warm · firm · swift · expansive · rough · luminous
Angle: depends on birth time and place
```

### 10.2 Vedic Mesha (Aries rāśi)

```
Field: Meṣa (sidereal; ayanāṃśa required)
Agent: Mars (Maṅgala)
Quality: fire tattva; rajasic tendency (do not collapse into Western modality)
Action: initiate
Tone: incisive (resonance, not equivalence)
```

### 10.3 Chinese Dragon branch

```
Field: 辰 chén (earthly branch; not a Western sign)
Agent: associated stem depends on the year
Quality: earth branch, yang, dragon label
Action: initiate? — do not force; use “rise / emerge” as resonance
Tone: expansive, luminous (resonance)
```

### 10.4 Mayan Imix

```
Field: Imix (day sign, 1 of 20)
Agent: day lord / way (regional)
Quality: water, primordial earth
Action: contain / germinate
Tone: fluid, dense, enveloping (resonance)
```

The examples show the method: **shared spine, local content, marked relation**.

---

## 11. Sources and reading

- Western: Ptolemy, *Tetrabiblos*; Vettius Valens, *Anthology*; standard definitions of the four angles and major aspects.
- Vedic: classical Jyotiṣa introductions; terms for rāśi, graha, bhāva, nakṣatra, guṇa, tattva, puruṣārtha.
- Chinese: *Wuxing* (五行) as five phases; heavenly stems and earthly branches; bagua; 24 solar terms.
- Mayan: Tzolkʼin day names and associations; note the difference between classical count and modern Dreamspell.
- Celtic: Ogham as a writing system; feda and aicmí; Bríatharogam kennings; tree associations as a medieval/learned layer.
- Gipsy/Romani: no source is used until community review.

### 11.1 Starting references (verify against primary sources in Phase 0)

These are orientation references, not the final scholarly bibliography.

- Western aspects: <https://en.wikipedia.org/wiki/Astrological_aspect>
- Western angles: <https://www.chani.com/astro-education/new-mc-ic-and-dc-are-now-in-the-chani-app>
- Western bodies: <https://en.wikipedia.org/wiki/Planets_in_astrology>
- Tzolkʼin day names: <https://en.wikipedia.org/wiki/Tzolk%CA%BCin>
- Chinese wǔxíng: <https://en.wikipedia.org/wiki/Wuxing_(Chinese_philosophy)>
- Ogham: <https://en.wikipedia.org/wiki/Ogham>
- Ogham introduction: <https://www.ogham.academy/blog/short-intro>
- Vedic glossary (developer-facing): <https://vedika.io/glossary>
- Unicode glyph block: <https://www.unicode.org/charts/PDF/U2600.pdf>
- Astronomy Engine: <https://github.com/cosinekitty/astronomy>
- Swiss Ephemeris: <https://www.astro.com/swisseph/>

**Caveat:** several popular astrology sites mix traditions, repeat modern inventions, or present interpretation as fact. Phase 0 MUST prefer primary texts, museum/ manuscript sources, and astronomical references over content farms.

**Definition of done for this vocabulary:** every cross-system chip can name its relation (`=`, `≈`, `~`, `≠`), every shared adjective is non-predictive, and no local term is replaced by a Western one without a gloss.
