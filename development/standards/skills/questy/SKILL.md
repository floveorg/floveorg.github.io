---
name: questy
description: >-
  Structured Q&A planning: scan a project's docs for gaps and conflicts, then
  ask typed batches of questions turning what you know into what you haven't
  thought about yet. Use for /questy or a project review.
category: planning
---

# questy

what you know  →  what is missing  →  questions  →  answers
   (docs)          (gaps/conflicts)     (the batch)     (decisions)

## The six hats (the question's type)

```
⬜ white, facts     — what do we know? data? specs? what's missing?
🟥 red, heart       — how does it feel? user fear? gut reaction? trust?
⬛ black, risk      — what could go wrong? threats? failure modes? blast radius?
🟡 yellow, optimism — benefits? value? why build this? user gain?
🟢 green, creative  — alternatives? wild ideas? flipped perspective?
🔵 blue, make       — flow? connection? contract? how A talks to B?
```

Hats are multiselect and weighted (name one twice for ×2). A question wears one
or two at most.

## More perspectives — the extended lenses

Name one to activate it; each is weighted ×2 and combinable.

- **Explainers** — `why`, `what`, `how`, `what-for`, `who`, `where`, `when`: pick
  ONE (`why` → causes, `what-for` → outcome).
- **Formalise** — `axiom`, `evidence`, `prediction`, `proposal`, `challenge`
  (`prediction` for risk spikes).
- **Teleology** — `experimental`, `random`, `fine`, `fatal` (`fatal` → what kills
  the project?).
- **Field** — `metaphysics`, `science`, `biology`, `psychology`, `sociology`:
  borrow analogies to reframe.
- **Time span** — `moment` … `decade`, `century`: tighten or stretch.

`vision`/`arch`/`trust`/`data`/`integration` are shorthand areas leaning on a hat:
`more vision` → 🟨, `more trust` → ⬛, `more make` → 🟦; `ux`→🟥, `docs`→🟨,
`design`→🟩, `threats`→⬛, `strategy`→🟨, `integration`→🟦, `data`→⬜. In
console-mode hats are titles only; they count as the question's `type`.

## Knobs

- **Mode** — `simple` (short options), the default; `explained` (one-line reason
  + con + ★ per option). Numbering follows the Answers rule, not the mode.
- **Focus** — `easy` (warm-up), `deep` (roots, second-order effects), `hard`
  (commitment), `concise` (no filler).

## Answers — selector and keyboard, both

Ask with the runtime's structured question tool (OpenCode: `question`) by
default. The same prompt shows the options and accepts a typed answer: click,
type A/B/C, or write freely (“A — a note”). Both are always allowed. Never ask
which UI; use text silently if the tool is absent.

- **Batch** — one call with all (3 by default); **single** — one per question.
- **★** — first option, labelled “(Recommended)”; state its con beside its reason.
  No downside, no recommendation. Include Neutral/Other.
- **Conditional** — a question that depends on an earlier answer goes next call.

**Terminal text is always numeric.** Number every option 1–N across the whole
survey — never A/B/C, never reset per batch; ★ is each triplet's first. `Q001+`
are question IDs, not answers. A shown selector keeps A/B/C; never mix them.
Print `Ref:`/`Affects:` per question, numbers once at end.

## First questions

Ask once, never re-ask.

1. **Project + start** — name, root, refs; resume (what changed?) or fresh.
   Show ★ tuning: 30 total · batch 3 (or config) · numbered text · no focus ·
   all six hats · no extra lens · audio off; or **tune it** → ask 2 and 3.
2. **Shape** — total, batch, mode, focus, hats, lens; default as above.
3. **Audio** — neither by default, or narraty recap; last option: **set up a
   decisions manager** (questy-all).

## The loop

1. **Load the ground.** Resuming: ask what changed, read only what matters;
   first run: full scan. With a Context tree read its files; otherwise keep
   decisions in the session. Map decided / open / unknown.
2. **Settle conflicts first.** Plan-vs-plan, plan-vs-standard, scope creep and
   dependency mismatches are written down; they change the questions. Never ask
   around a conflict you can name.
3. **Pick the lens.** Choose the hats and any perspective (why / formal /
   experimental / field / time). A name said twice is ×2.
4. **Draft inside the lens.** One ask, one hat (max two), `Ref:` the triggering
   section, `Affects:` what the decision touches. Prefer what docs cannot answer;
   drop what they already answer. Keep the batch size.
5. **Self-check.** (a) Already answered? drop. (b) Two questions? split. (c) Earns
   its hat? re-home or drop. (d) ★ defensible, or is Neutral honest? (e) One line?
   tighten. (f) Changes a decision? if not, it is trivia.
6. **Present one mixed batch.** Hat order ⬛ > 🟩 > 🟦 > 🟨 > 🟥 > ⬜; present
   mixed, abstract→concrete inside each hat, with ★/Neutral. Selector options
   use A/B/C; terminal text uses continuous 1–N (see Answers). Global Q001+;
   `Ref:`/`Affects:` when there is doc context.
7. **Fold the answers.** Decisions, resolved items, skips, new conflicts and
   workflow changes → the project's decision log (Context tree) or session summary.
8. **Regenerate, never repeat.** Build the next batch from docs; carry unresolved
   forward; never re-ask settled. After each batch offer `(c)ontinue`, `(u)pdate`,
   `(f)inish` (default `c` after three idle rounds). `(u)` writes the replied
   questions into all related docs, proposes easy follow-up tasks tied to those
   decisions and updates, then offers `(c)` / `(f)`. `(f)` = quit/stop/end.
   One session at a time.
9. **Close.** Print the end-of-survey readout once; carry its open items forward.

## End of survey

One readout when the last batch is folded:

1. **Decisions** — Q IDs + chosen option; conflicts settled this run.
2. **Open items** — skips and unresolved with `Ref:`/owner; carry forward, never
   re-ask.
3. **Export** — into the owning doc, never a new file: markdown · JSON · HTML.
   HTML is a share artifact, not the terminal selector.
4. **Recap** — offer narraty here, once.

Keys: `(c)ontinue` · `(u)pdate` (see loop 8) · `(f)inish` ends the session ·
`(r)esume` gives one readout · `(s)et up a decisions manager` suggests questy-all.

## Answer grammar

Terminal text: `0` = all ★ · `1 4 7` = one per question · `-` = skip (open) ·
`Q007=20` = override · `0 Q007=20` = all ★ but that. Selector: `A`/`B`/`C`,
`0` = all ★, `-` = skip; notes kept.

`Q001+` global; answers are a separate 1–N survey run. `Ref:`/`Affects:` optional.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for override routes and keys.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.

## Other Questys
`questy-all` (bundle) · `questy-flove` (apps) · `questy-html` (a shareable form
others answer and re-share; not the terminal selector).
