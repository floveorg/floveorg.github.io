# flove · The contract

The binding values every flove app honours, and the floor beneath them. The
detail lives in the standards linked here — one home per face.

## Values and the floor

### Ambition

- **Wholism** — the whole is the unit of design; parts earn their place by what
  they make possible together.
- **Simplexity** — the simplest form that still holds the whole.
- **All is near** — everything within reach; a person uses what is theirs
  through local pieces.
- **Super relationism** — relations of relations; the graph goes one level
  deeper than the link.
- **Radical fuzzy logic: confluentism** — opposites meet as complements; truth is
  a confluence.

### Minimalism

- **Slow it · flow it · love it.** Low-tech, calm, relational: the simplest thing
  that carries the meaning.
- **Crafty & resourceful.** Reuse, combine small pieces, and get the most
  function from the least code, money and energy.
- **Low ecological impact.** Minimal compute, free + low-impact hardware.

### Open context, clear ontology

Radical open source starts with context. Every app declares where it lives and
what it holds — category, colour and hat, fields, vocabulary — in one explicit
ontology that anyone can read, fork and extend.

- **Open source first.** FOSS by default.

**Test:** the app's category and fields resolve from `tools/routing.json`; its
labels match the vocabulary matrix; a stranger understands the app from its
declared context.

→ https://flove.org/tools/routing.json
→ https://flove.org/development/standards/vocabulary.md
→ https://flove.org/development/standards/frontend/frontend.md (§13.7 · §13.19)

### The person owns it

Her work and her data live on her device, and she leaves with everything at any
time. One self-contained file, offline, with everything it needs inside it. She
can undo what she did, and the memory stays local until she clears it.

- **Local-first & portable.** Client-side first; one interface with swappable
  backends, so the work moves with her.

**Test:** it runs from `file://`; the export produces a complete file; the page
makes no network request; destructive actions confirm or restore; reset exists;
a reload restores the state and clearing removes it everywhere.

→ https://flove.org/development/standards/frontend/frontend.md (§13.20)
→ https://flove.org/development/standards/frontend/export.md
→ https://flove.org/development/standards/adoption.md

### Honest exchange

The app says what it does, asks before anything leaves, and speaks one
vocabulary in every language it ships.

**Test:** every share and export is an explicit action; a fresh profile is
private; every figure traces to a source; labels match the matrix; the language
switch flips every string.

→ https://flove.org/development/standards/frontend/export.md
→ https://flove.org/development/standards/adoption.md
→ https://flove.org/development/standards/frontend/frontend.md (§13.17 · §13.2)
→ https://flove.org/development/standards/vocabulary.md
→ https://flove.org/development/standards/worldview.md

### Scalability

- **Grow from the smallest piece.** One field, then one app, then one category,
  then the network. Each layer works alone and composes upward.
- **The version is the adoption date.** `YY-M` marks the month a standard was
  adopted; `.N` separates releases within that month.
- **A version promises continuity.** `26-11` means every standard adopted through
  November 2026; the changelog lists what entered and what retired.
- **History stays visible.** Every page carries a changelog link, and the archive
  keeps old versions readable.

→ https://flove.org/development/standards/apps/README.md

### UX principles

| Principle | What it asks | How it shows |
|---|---|---|
| **State is data** | Navigation, view and memory live in CSS, the URL or local storage. | A reload returns to the same place; a shared link opens the same view. |
| **The interface explains itself** | Help sits where the interface lives: labels, empty states, hints and examples teach the app in place. | A person learns by using it, with the explanation at hand. |
| **Calm motion** | Movement respects attention: short, purposeful and quiet, and it carries meaning. | Motion shows cause and effect; reduced motion stops it. |
| **Progressive disclosure** | The first screen gives the few things that matter; the rest appears one layer at a time, with a way back. | A summary first, then detail; an *advanced* door for the rest. |
| **Show the state** | Every action gives a visible answer: what changed, what is saved, what is pending. | Toasts, badges, filled counters, a saved tick. |
| **Keep the thread** | One vocabulary, one layout language, one place for the same control. | The same topbar, the same summary actions, the same names. |
| **Depth on demand** | Simple first, advanced when asked; the simple path stays complete. | Defaults that work; options revealed on request. |

### Expansive, Communitarian

- **Gift-economic & decentralized.** Reciprocal contribution over money;
  web-of-trust over authority.

### The floor

- **Accessibility** — contrast 4.5:1, visible focus, 40×40 touch targets,
  reduced motion.
  → https://flove.org/development/standards/skills/validaty/fix-catalog.md
- **Tokens** — defined in §13.19; `flove.css` implements them.
- **One file** — the skeleton is §13.20.
- **Export** — `flove-portrait/1`; share guarded by `canShare`.
  → https://flove.org/development/standards/frontend/export.md
- **Language** — §13.2.
