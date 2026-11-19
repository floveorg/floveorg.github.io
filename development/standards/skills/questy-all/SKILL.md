---
name: questy-all
description: >-
  The recommended questy bundle: all of questy's perspectives and addons added —
  30 questions, batches of 3, A/B/C with ★, the Context tree and Git sync. Use
  for /questy-all or when you want the easy default.
---

# questy-all — the recommended questy bundle

Reuses [`questy/SKILL.md`](https://flove.org/development/standards/skills/questy/SKILL.md) and adds every perspective and addon: the easy
default, the Context tree and Git sync.

## What the bundle adds

- **Defaults:** 30 questions (5 per hat), batch 3, A/B/C + ★ recommended, `0`
  accepts every ★, `-` skips a question. Core hats, core ordering.
- **Context tree:** `standards/`, `plans/`, `questy-docs/`, `questy-pending.md`,
  `conflicts.md`, `proposals.md`, `questy-agents.md` (chapters: shortcuts,
  constraints, batch-overrides, export-prefs, territory, aliases).
- **Git sync:** every created file is committed; no `.gitignore`.

## Rules (bundle)

- Never delete a decision — append, or mark it resolved.
- Resolved → `archive.md` when archive mode is on; mark in place when it is off.
- Skipped → `questy-pending.md`. More than one session pending → escalate.
- Never re-ask what the docs already answer.
- `questy-agents.md` holds preferences; `questy-pending.md` the pendings;
  `conflicts.md` the danger zone; `proposals.md` the decision log. Don't duplicate
  them.

## Run

1. **Config** — load `~/.config/questy-all/config.md` if present, else defaults.
2. **Create the Context tree.**
3. **Run the main process** — scan, generate, ask and answer in batches.
4. **Fold answers back** — decisions → `proposals.md`, conflicts →
   `conflicts.md`, skips → `questy-pending.md`.
5. **Update delta** — re-scan, re-evaluate pendings, keep the global numbering.
6. **Git sync** — `questy-all: {purpose} — {N} questions answered`.
7. **Continue** — `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`; default `c`
   after three idle rounds.

See also: [`questy/SKILL.md`](https://flove.org/development/standards/skills/questy/SKILL.md) · [`questy-html/SKILL.md`](https://flove.org/development/standards/skills/questy-html/SKILL.md).

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
