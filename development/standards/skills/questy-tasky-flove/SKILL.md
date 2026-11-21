---
name: questy-tasky-flove
description: >-
  Flove dev-task pick by Q&A: questy owns when/how to ask, tasky owns the what.
  Loads the flove bundle, runs rewindow --survey and maps the answer to
  tasky.py show <id>. Use for /questy-tasky-flove or "pick my next flove task by questions".
category: planning
---

# questy-tasky-flove

Thin call, no duplicated rules. [`questy`](https://flove.org/development/standards/skills/questy/SKILL.md)
owns when/how to ask (batch, ★, answer grammar); [`tasky`](https://flove.org/development/standards/skills/tasky/SKILL.md)
owns the what (bundle, candidates, proof). The `flove` profile is the default.

## Initial questions — clicky form, in order

Host question tool by default (questy); terminal text numbers the whole form
1–N, titles included (AGENTS §12.3). Each ★ states reason and con in one line.

1. How should the pick run?
2. Pick by survey (Recommended — reason: bundle + Q001 + proven winner; con: one question round) — load bundle, ask Q001, then show and work the winner.
3. Show one id — I already know the task.
4. Just load the bundle — print `tasky.py context flove` and stop.
5. When should I ask you?
6. Judgment calls only (Recommended — reason: ask on choice, unblock and destructive steps; con: no prompt before a state move) — state moves are automatic.
7. Before every edit.
8. Never ask — non-destructive work only.

Reply with one option number per question, in order (e.g. `2 6`).

## Flow

1. `python3 tools/dev/tasky.py context flove` — the questy-all Context tree plus the Plan/Work tab managers, each marked `OK` / `missing` / `N/A`.
2. `python3 tools/dev/tasky.py rewindow --survey` — Q001 with 30 options, ★ on #1, `Ref:` hito, `Affects:` owner, `c=` PROC-10 class and question depth. Add `--choice` to rank decisions first; `easy` counts very easy tasks and proposes batches, `next --do` lists the `directo + very easy/easy` work with no question.
3. Put Q001 to the host question tool: selector options keep A/B/C + ★, terminal text uses continuous 1–N. State the ★ reason and con in the same line; never offer a bare default. Accept `3` = one, `0` = all ★, `-` = skip. Numbered mode prints every option and its full answer as text.
4. Map the chosen number to its id, then `python3 tools/dev/tasky.py weight <id>` → `options <id>`. Ask 0 questions (`directo`), one A/B/C (`ramificado`) or the three-question questy-all batch (`estructurante`): solution, hard dependencies, decision record. ★ is the owner default; a user `choice_override` + `choice_reason` tunes the class, and a hard dependency enters `depends_on` only after the answer. Explain every recommendation with its con as well as its reason (questy ★ rule); never offer ★ as a bare default.
5. Then `python3 tools/dev/tasky.py show <id>` → prove → deliver → verify in that owner doc (tasky §3–§5). Once the pointer verifies, move state automatically — no confirmation. Fold skips into `development/wiki/work/pendings.md`; never re-ask a settled question (questy-all rules).
6. Close every pick with **two** blocks below the delivery, never with the delivery alone: (a) a numbered list of `easy` READY tasks whose owner is a doc touched in the run — prove each with `tasky.py show <id>` — with one ★ whose reason **and con** are stated; (b) the next questy batch of **three new questions** under that list. Number the whole close 1–N continuously, titles included (AGENTS §12.3); number every option, state the reply format, add `Ref:`/`Affects:` and a ★ with reason and con per question. Never re-ask Q001 or a settled choice batch.

## Guardrails

- Read-only until delivery; one task at a time; a skip changes no register state.
- Do not copy questy's hats or tasky's PROC table here — follow the owners.
- No commit or push unless asked.
