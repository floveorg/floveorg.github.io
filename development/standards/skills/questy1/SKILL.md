---
name: questy1
description: >-
  The recommended questy bundle — a common, easy default built on
  questions-perspectives mining. Wears the six Thinking Hats (facts white · heart red·
  risk black · optimism yellow · creative green · make blue) and its paralel colours as the only type, mines project docs for
  gaps and conflicts, and batches numbered questions (Q001…) that update the
  docs and route skips to pendings. Optional **minitree** addon sets up the full
  file structure standards/, plans/, questy-docs/, pendings, conflicts, proposals and
  syncs to git. Command: /questy1 [colour] [in N]. For the basic questy workflow, see the
  questy skill (flove.org/development/standards/skills/questy/skill.md). You can also override this settings via the personal
  config (see CONFIG.md).
---


## Personal config

To fork/reuse, edit the personal config that
overrides the defaults instead of editing the skill (see example:
`development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change.

## The easy default — questions with recommended answers

Every question wears one of the six Thinking Hats (⚪ facts · ❤ heart · ⬛ risk
· 🟡 optimism · 🟢 creative · 🔵 make) — the hat is the type.

### Question format

Each question is 1–2 sentences max, followed by **A/B/C recommended answers**
with a **★ Recommended** pick (one sentence rationale):

```
Q001 ⬛ Is the shared library's architecture sound?
  A) Yes — modular, zero deps, progressive decomposition.
  B) Right direction, but needs a dependency manifest.
  C) Rethink — move to ES modules or Web Components.
  ★ B — Implicit load-order coupling is a quiet bomb.
```

### Ordering

- **Abstract → concrete** — most strategic/philosophical first, most tactical last
- **Mix hat colours** — do NOT group by colour. Q001 might be ⬛, Q002 🟢, Q003 🟡
- Within the gradient, weight by impact: ⬛ > 🟢 > 🔵 > 🟡 > ❤ > ⚪

### Batch flow

1. Show **5 questions** with A/B/C + ★ recommendation
2. User answers like: `1a 2b 3c 4a 5b` (or `0` for all recommended, `-` to skip any)
3. Record answers → next batch of 5
4. Repeat until all questions done

### Volume

- 5 questions per hat by default (30 total)
- Batch size: 5
- Global numbering: Q001+ always

```
docs → scan for gaps & conflicts → mix hats → abstract→concrete → batch 5 → answer → update docs
```


## Questy1 as an Addons Recommended bundle for questy

A richer workflow that sets up the full file structure (standards/,
plans/, questy-docs/, pendings, conflicts, proposals) and syncs everything to git.


## Use case: `questy1 minitree` (recommended)

The same mining run with the minitree addon loaded — creates the full file
structure and syncs to git:

**Step 1** — Config
- If `~/.config/questy1/config.md` exists → load it, skip setup
- If missing → setup flow, load recommended defaults (minitree + index + git)

**Step 2** — Create project structure
- Create: standards/, plans/, questy-docs/, questy-pending.md, conflicts.md, proposals.md,
  agents.md, .gitignore

**Step 3** — Ask which hats to wear (multiselect) + See more
- The six hats; optional See more (Wisy lenses: explainers, formalise,
  teleology, field, time span) — weight by clicking twice
- Ask about tones (simple,extended,human,funny) and focuses(easy,deep,concise)  


**Step 4** — Volume and batch
- total questions (default 30), per type (default 5), batch size (default 5)
- additional session info free-text

**Step 5** — Scan and select
- Read every .md: standards/ (frozen), plans/ (active), proposals.md
  (decided), questy-docs/ (reference)
- Map decisions, coverage per hat, detect plan-vs-plan / plan-vs-standard
  conflicts and scope creep
- Never re-ask answered; skip frozen standards/ unless challenged explicitly
- Order by impact: ⬛ > 🟢 > 🔵 > 🟡 > ❤ > ⚪

**Step 6** — Generate and answer
- Batch 5 at a time, abstract→concrete, colours mixed
- Each question: A/B/C recommended answers + ★ Recommended pick
- User answers like `1a 2b 3c 4a 5b` (or `0` for all recommended)
- Skipped → questy-pending.md; conflicts → conflicts.md; clear decisions → proposals.md

**Step 7** — Git sync
- Stage and commit: `questy1: {purpose} — {N} questions answered`

**Step 8** — Update (delta)
- Re-scan doc-roots, diff against last snapshot, re-evaluate pendings
- Superseded → archive; skips now answerable → back to the pool
- Present next batch, continuing global numbering

**Step 9** — Continue
- `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`; after 3 idle rounds default
  to `c`

## See more

This bundle keeps the shown texts short. The full, advanced protocol — every
perspective, addon, tune, script and integration, plus the HTML form ⇄ console
tracks — lives in the questy skill:

- **https://flove.org/development/standards/skills/questy/SKILL.md**

Use questy when the run outgrows questy1: advanced batch mode, merge rules,
workflows, archive, scripts. Offer it inline when the owner asks for
improvements instead of keeping everything in this prompt.

Interactive HTML form demo: **https://flove.org/development/standards/skills/questy/questy-flove-dev.html** 
