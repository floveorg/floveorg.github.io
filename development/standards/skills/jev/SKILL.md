---
name: jev
description: >-
  Use for calibrated classification in coding tasks: label or route many items, yes/no checks on evidence, ordered scoring or ranking. Use Jev (TypeSafe's System One) instead of eyeballing lists or one call per item. MCP tools or the `jev-code` CLI fallback; needs a TypeSafe, OpenRouter or AI Gateway key.
category: utility
license: MIT
compatibility: Requires Node.js 20+ and one API key (TYPESAFE_API_KEY, OPENROUTER_API_KEY or AI_GATEWAY_API_KEY). Tools come from the jev-code MCP server, the Pi extension or the jev-code CLI.
metadata:
  author: FrancoisChastel
  source: https://github.com/FrancoisChastel/jev-code
  version: "0.5.1"
---

# jev

Jev is a decision model, not a text model. Give it evidence and typed questions;
it returns typed answers with calibrated probabilities in roughly 70–500 ms for a
fraction of a cent. It never writes prose, so there is nothing to parse and the
answer is always one of the options you supplied. Use it for narrow judgments
inside a task while you keep control of the workflow.

Start at https://docs.typesafe.ai/llms.txt (append `.md` to any page path) — the
live docs are the source of truth for tool shapes and worked examples.

## When to reach for it

- Label, route, group or triage more than a handful of items by hand.
- Write a regex or keyword heuristic for a semantic call ("is this a flaky test?").
- Assert something unverified ("tests pass", "this is backwards compatible").
- Rate severity, priority or quality consistently across many items.

Do **not** use it for prose or free-form values, an obvious single call, or exact
facts a lookup or test can settle. Jev only picks among options you give it.

## Tools

| Tool | Use when | Returns |
| --- | --- | --- |
| `jev_classify` | Many items, one label each from your classes | label, probabilities, `decision: auto\|review` |
| `jev_check` | Yes/no questions about one piece of evidence | probability, `verdict: yes\|no\|uncertain` |
| `jev_score` | Many items on one ordered scale | score, level, confidence |
| `jev_rank` | Which candidates answer a question | relevance, sorted, plus `any_relevant` |
| `jev_ask` | Mixed question types over one state | raw typed answers |

If the `jev_*` tools are absent, use the CLI: `jev-code classify --input payload.json`
and friends take the same JSON (see [cli.md](https://flove.org/development/standards/skills/jev/cli.md)).
If `jev-code` is missing too, tell the user to run
`npx -y @french-castle/jev-code@latest setup`.

## Workflow

1. **Frame the judgment.** Decide what your code will do with each answer. Pick the tool whose output maps onto that action: Choice onto branches, check onto an `if`, score onto a threshold, rank onto "open these".
2. **Gather raw evidence.** Pass the actual diff, log excerpt, issue body or file excerpt. Never pass your own summary or conclusion; a conclusion in the state biases the answer.
3. **Write complete questions and classes.** Ids are for you; the model sees only instructions, classes and levels. Say what belongs and how neighbours differ. Add a catch-all (`other`, `unclear`). Reference named state parts with backticks: `` `diff` ``.
4. **Batch.** Send every item or every question about the same evidence in one call. Limits per call: 64 items, 250 classes, 64 checks, 250 candidates, ~120K characters. Split larger sets.
5. **Act on the decision, not just the label.** `auto` and `verdict: yes|no` are safe at default thresholds; review `review`/`uncertain` yourself or ask the user. Raise thresholds when a wrong answer is costly.
6. **Report honestly.** Say what Jev decided and what you reviewed: "Jev labelled 38 failures: 31 auto-accepted, 7 I checked by hand."

## Question design

One narrow judgment per question; name the condition, not the expected conclusion.
Describe borderline cases in classes, list score levels lowest first, and treat a
probability near 0.5 as undecided. See
[question-design.md](https://flove.org/development/standards/skills/jev/question-design.md)
and [recipes.md](https://flove.org/development/standards/skills/jev/recipes.md)
(CI triage, issue labelling, file selection, PR-claim verification, injection
screening, severity ranking). Exact tool I/O shapes:
[tools.md](https://flove.org/development/standards/skills/jev/tools.md).

## In the user's application

Prototype with `jev_ask` or the CLI, then build with the official Python or
JavaScript SDK — not by shelling out to `jev-code`. Patterns and snippets:
[building-with-typesafe.md](https://flove.org/development/standards/skills/jev/building-with-typesafe.md).

## Limits and safety

Text only, English strongest; each item is truncated at 4000 characters
(`truncated: true`). Every result includes `usage` and `model`; mention cost only
if asked. Jev is calibrated, not infallible: typed output guarantees the
interface, not the truth — keep destructive actions behind your own confirmation.
The key comes from `TYPESAFE_API_KEY`, `OPENROUTER_API_KEY` or `AI_GATEWAY_API_KEY`;
`jev-code doctor` shows the host in use. Never print a key or paste one into chat.

| Symptom | Fix |
| --- | --- |
| "No API key found" | Export a key and restart the agent, or run `jev-code setup`. |
| "Request is N characters, above the budget" | Split into batches or shorten to the deciding excerpt. |
| Many `review` results | Sharpen classes, add a catch-all, pass more context. |
| `status: invalid_response` | Retry once, then report it. |
| `status: refused` | Judge the item yourself or rephrase the question. |
| `jev-code: command not found` | `npx -y @french-castle/jev-code@latest doctor` works without a global install. |
