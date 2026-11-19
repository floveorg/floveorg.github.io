---
name: questy
description: >-
  Structured Q&A planning: scan a project's docs for gaps and conflicts, then
  ask typed batches of questions turning what you know into what you haven't
  thought about yet. Use for /questy or a project review.
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
one-at-a-time console mode hats are titles only; they count as the question's
`type`.

## Knobs

- **Mode** — `simple` (numbered, short A/B/C), the default; `explained` (each
  option gets a one-line reason and the ★).
- **Focus** — `easy` (warm-up), `deep` (roots, second-order effects), `hard`
  (commitment), `concise` (no filler).

## Answers — selector and keyboard, both

Ask with the runtime's structured question tool (OpenCode: `question`) by
default. The same prompt shows the options and accepts a typed answer: click,
type A/B/C, or write freely (“A — a note”). Both are always allowed. Never ask
which UI; fall back to text silently if the tool is absent.

- **Batch** — one call with all (3 by default); **single** — one call per question.
- **★** — first option, labelled “(Recommended)”; include Neutral/Other.
- **Conditional** — a question that depends on an earlier answer goes next call.

## First questions

Ask this opening questionnaire once, in order. Its answers configure the session;
do not re-ask them per batch.

1. **Project** — Which project? Apply it as `/questy-<project>`; give the name,
   root and data references.
2. **Questions** — How many? ★ **30 total**, split across the hats in play.
3. **Batch** — How many per time? ★ **3**.
4. **Mode** — ★ **Simple options with a one-line ★ reason**, or explained
   options (every option reasoned).
5. **Focus** — ★ **None**; or easy / deep / hard / concise.
6. **Hats** — ★ **All six** — ⬜ facts, 🟥 heart, ⬛ risk, 🟡 optimism, 🟢 creative,
   🔵 make. Say one twice for ×2.
7. **More perspectives** — ★ **Hats are enough**; or *why*, *what*, *how* / *all*,
   offered after this questionnaire.
8. **Next step** — **Do you want this interview to continue in audio?**
   ★ **Neither yet**; or **audio** (a narraty recap).

Then start the first mixed batch.

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
   mixed, abstract→concrete inside each hat, as selector options with ★/Neutral.
   Global Q001+; `Ref:`/`Affects:` when there is doc context.
7. **Fold the answers.** Decisions, resolved items, skips, new conflicts and
   workflow changes → the project's decision log (Context tree) or session summary.
8. **Regenerate, never repeat.** Build the next batch from updated docs; carry
   unresolved forward; never re-ask a settled question. After each batch offer
   `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`; default `c` after
   three idle rounds. One session at a time.
9. **Close.** Summarize decisions, confirmed plans and open items; offer export
   (markdown · JSON · HTML) and a narraty recap. The HTML is a **share** artifact
   others can answer and re-share — never a substitute for the terminal selector.
   Carry the open items forward.

## End of survey

When all batches are answered: `(c)ontinue` keeps asking; `(r)esume` synthesizes
all replies into one readout; `(s)et up a decisions manager` suggests the
questy-all options, whole or per part. These are end keys; per-batch `s` = stop.

## Answer grammar

`0` = every ★ · `1a 3c` = Q001=a, Q003=c · `0 7a` = all ★ except Q007=a ·
`-` = skip (recorded as an open item).

Global numbering `Q001+`, never reset. `Ref:` (triggering doc section) and
`Affects:` (what the decision touches) are optional with doc context.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for override routes and keys.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.

## Other Questys
`questy-all` (bundle) · `questy-flove` (apps) · `questy-html` (a shareable form
others answer and re-share; not the terminal selector).
