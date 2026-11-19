# Wizy · web texts

Copy deck for `apps/sys/wizy/index.html`. Visible strings only — code snippets are included where they are the panel content, but SVG labels, CSS, JSON manifests and internal JS identifiers are left out. Dynamic suggestion copy is collected in the app tables below.

**Standards reference:** [Questy FLOVE index](../../../development/standards/skills/questy-flove/index.html) · [Flove standards](../../../development/standards/index.html).

**Typography:** Manrope for body and headings, JetBrains Mono for labels — both bundled in `fonts/`.

---

## Page metadata

- **Title:** Wizy · FLOVE
- **Description:** Wizy — the contextual suggestion engine that powers flove apps.
- **Distro:** sys
- **App:** wizy

## Header

- **Brand trigger:** the Wizy logo and title open the menu.
- **Brand subline:** suggestion engine
- **Menu links:** Wizards · Influence · Affinities · More · Standards ↗
- **Theme control:** ☾ Dark mode / ☀ Light mode, inside the menu.
- **Language control:** EN · ES, inside the menu; stores `flove:lang` and sets `<html lang>`.
- **Spanish coverage:** menu, headings, depth labels, card labels, pick labels and embed surfaces; app/field data stays as its own name.

## Wizards

The page opens with the **Influence** rater, then the three wizard cards, all expanded in one row. Each card shows only **best in**, one line of field names, one line of app chips and **All** below them. The app chips filter the suggestions section underneath the cards.

- **Section title:** Wizards, introduced by the animated spark mark.
- **Card colour:** Love uses red, Joy gold, Wisdom blue — the name, field links, app chips and click states follow that colour.
- **Fields:** each field name links to its `whole/...` page.
- **App chips:** buttons, not links. The first three apps per field are shown; **All** reveals the rest. Clicking a chip selects that app and shows its filtered suggestions below; clicking it again clears the selection.
- **All / Less:** toggles the extra app chips and swaps its own label.
- **Card icon:** the wizard emoji sits on the right of each card, in the card colour, replacing the old plus/minus mark.

**Whisper carousel (5 phrases, auto):**

- **Love:** “Who would smile reading this?” → “Which detail carries the most care?” → “What would make the reader feel included?” → “Is there a person behind this worth naming?” → “What small care would make the week lighter?”
- **Joy:** “What made you laugh today?” → “Which line would a friend quote back to you?” → “Could this be the start of a series?” → “Where could the reader smile?” → “What lucky detail deserves the ending?”
- **Wisdom:** “What question does this post answer?” → “Which claim needs a source?” → “Who is the reader you are writing for?” → “What is the takeaway in one sentence?” → “Which risk is worth naming early?”

### Love

- **Name:** Love
- **Subtitle:** lovely · hotter
- **Facts:**
  - **best in** care, family, gifts, memory
  - **Fields:** Metaphysics · Science
  - **Apps shown:** Goddy · Souls · Keys
  - **All reveals:** Willy · Fivy · Cathy · Puzzy · Astry · Hacky · Poly

### Joy

- **Name:** Joy
- **Subtitle:** lucky
- **Facts:**
  - **best in** friendship, dates, chance, play
  - **Fields:** Biology · Language
  - **Apps shown:** Realy · Lovy · Linky
  - **All reveals:** Fity · DieSafe · Varyy · PracSys · Sensy · Frotis · ElectrOrchestra · Chacrikun · Raty · Comby · Wisy

### Wisdom

- **Name:** Wisdom
- **Subtitle:** formal · casual · fatal
- **Facts:**
  - **best in** decisions, health, money, legacy
  - **Field:** Psychosocial
  - **Apps shown:** Socy · Blogy · Browsy
  - **All reveals:** Profily · Trusty · MyFamily · Parenty · Crumbly · Evily · Daty · Maty · Lovy · Wizy · Nety · Confluenty

## Influence · depth

The rater sits in the entrance, directly above the three cards. Its title is centred above it.

- **Title:** Influence
- **Scale:** 0 None · 1 Little · 2 Some · 3 Blend · 4 Much · 5 Full
- **0 · None:** Suggestions stay inside the app.
- **1 · Little:** One or two flove angles in the wording.
- **2 · Some:** A few suggestions draw from flove categories.
- **3 · Blend:** Quote the app’s field page in its category colour.
- **4 · Much:** Use related-app fields as material.
- **5 · Full:** Speak with the whole flove model — related apps, fields and voices.
- **Live line:** the selected depth and its reading appear inside the rater; before a pick: “Pick a depth to set the influence.”

## Filtered suggestions

Shown below the wizard cards after an app chip is clicked. The section starts hidden.

- **Field line:** the app’s field name and wizard name, in the card’s accent colour.
- **Link:** Open {app} →
- **Title:** Suggestions for {app}
- **Reason:** Selected by {Love | Joy | Wisdom} — {the people, the care and the feeling underneath | the spark, the luck and the reason to laugh | the facts, the risk and what lasts}.
- **Chips:** the selected app’s suggestions, listed below.

### Suggestions by app

**Love**

- **Goddy:** Which matrix cell feels closest? · Where do you see yourself in the matrix? · What would you like to see fully?
- **Souls:** Which animal came first? · What colour holds the memory? · Which sense brings it back?
- **Keys:** Which triad explains this? · What would shift if you reordered it? · Which perspective is missing?

**Joy**

- **Realy:** What is real and what is fiction here? · Which memory wants to be kept? · What would make this story truer?
- **Lovy:** What feeling is under the words? · Which voice would say this best? · What would make it warmer?
- **Linky:** Which two things are linked here? · What link is missing? · Where does the meaning drift?

**Wisdom**

- **Socy:** Which freedom is this about? · Who else is affected? · What would a fair category look like?
- **Blogy:** What question does this post answer? · Which claim needs a source? · Who is the reader you are writing for? · What would a sceptical neighbour ask? · What is the takeaway in one sentence?
- **Browsy:** Which source should you trust? · What would a peer say? · Where is the edge of the network?

**Other apps — generic fallbacks**

- **Love:** Who would this matter to? · Which detail carries the care? · What would make it feel closer?
- **Joy:** What would make this fun? · Where is the luck hiding here? · Who would laugh first?
- **Wisdom:** What would a sceptic ask? · Which claim needs a source? · What is the takeaway in one sentence?

## Prompt and embed

Two sticky buttons at the foot of the Wizards section. Both start collapsed and are disabled until an app is selected.

- **Buttons:** Prompt · Embed
- **Prompt panel:** head “system prompt”; the generated prompt, collapsed by default.
- **Embed panel:** four surface cards plus a source link to `questy-flove/index.html#simpler`.
- **Toggle label:** each button opens and closes its own panel; `aria-expanded` follows the state.

### Embed surfaces

The embed panel shows four cards in ascending weight: **Micro → Minimal → Compact → Full profile**, adapted from the four versions on the Questy FLOVE index.

- **Micro:** gauge only.
- **Minimal:** gauge and one line of guidance.
- **Compact:** gauge and the three wizard voices.
- **Full profile:** gauge, the five category chips and the three voices.
- **Each card:** a **Show embed code** button below the preview; it becomes **Hide embed code**.
- **Code:** the snippet follows the selected app and depth; each surface gets its own `surface` value and payload.
- **Source link:** questy-flove ↗

### Prompt template

```text
You are the {icon} {wizard} wizard of flove.
Voice: {wizard voice}

App: {app} · {field}
Flove influence: {depth} · {depth name} — {depth description}

Read this {app} summary and offer three gentle suggestions for what to do next.
One line each. Offer a door, never an instruction. No scores, no fluff.

Summary:
{app summary JSON}
```

The app, field and summary change with the selected chip. The influence line uses the chosen depth, or “not set”.

### Embed snippet note

Each snippet loads `wizy.js` and renders into `#wizy-box` with a surface value: `micro`, `minimal`, `compact` or `full`. Compact and full register the selected app’s first three suggestions as a `wizy.register()` pack; full also carries the app’s field and model note.

## 01 · Affinities

Collapsed by default. Three tables from the routing registry.

- **Number:** 02 · affinities
- **Title:** Affinities
- **Hint:** which family a pass should lean on
- **Lead:** Curated from routing.json app and field labels. This is the shared reference for Questy and Questy FLOVE: it seeds which family a pass should lean on. Affinity is a hint, not a schema.
- **App affinities table:** app · category · Love · Joy · Wisdom.
- **Key:** 3 = defining · 2 = strong · 1 = hint · 0 = none
- **Related apps & fields:** Love → Goddy · Astry · Hacky · Souls; Joy → Realy · Lovy · Linky; Wisdom → Socy · Blogy · Browsy · Nety.
- **Fields across apps:** the field-level weights for MyFamily, Trusty, DieSafe, Keys, Comby, Vizy, Shareful, Dealy, Sety and Crumbly.
- **Closing line:** Field labels are quoted from the routing registry; use them as starting hints when a pass asks about that area.

## 02 · Furthermore...

Collapsed by default.

- **Number:** 03 · furthermore
- **Title:** Furthermore...
- **Hint:** one state, many surfaces
- **Lead:** The state stays the same; only the surface changes. One whisper, many shapes.
- **Travels:** Full for onboarding · Compact for sidebars · Minimal for inline cards · Micro for mobile and footers.
- **Next:** embed mode + SDK, then the surface variants inside flove apps.
- **Then:** consolidate items 4–9 into the Wizy and Wisy wizards.
- **Links:** integration plan · Questy · Questy FLOVE · Wisy app
- **Closing line:** The wizard whispers; you decide.

## Footer

- **Stats:** 5 categories · 54 apps in the model · 1,957 field nodes · 3 cross-field links
- **Meta:** Wizy · Central · phase 0 · client-side PoC · standards · development
- **Standards link:** [Flove standards](../../../development/standards/index.html)

---

## Section marks

- **Wizards:** respira
- **Affinities:** orbita
- **Furthermore:** inclina
- **How it grows modal:** despliega

## Chapter motion

- **Wizards:** rise — fades up as the page settles.
- **Affinities:** slide from the right.
- **Furthermore:** drop — descends from above.
- **How it grows modal:** rise and settle from below.

## Legacy hidden modals

The old wizard half sheet, the Wisy explainer modal and the How it grows deck remain in the DOM but have no visible trigger on the page. Their copy is no longer part of the visible page flow.
