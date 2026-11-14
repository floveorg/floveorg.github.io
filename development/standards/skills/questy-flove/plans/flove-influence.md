# Flove influence — the 1–5 scale (spec)

**Status:** shared spec — referenced by `questy/index.html` (the gauge) and
`questy-flove/` (the flove edition).

The **Flove influence** gauge sits at the top of every survey. It is a single
self-assessed intensity pick (1–5): *how deep should this pass go into the flove
way of working?* It is **guided, not gated** — nothing hides behind the answer;
it only tilts how the questions are written and how the session lands.

## The levels

| # | name  | one-liner | effect on the interview |
|---|-------|-----------|-------------------------|
| 1 | **None**  | purely about your project, no flove | questions stay generic; no flove vocabulary, no flove conventions |
| 2 | **Touch** | just a touch — minimal flavour | a light flove accent (a shared convenience here and there), no ceremony |
| 3 | **Blend** | well blended — flove where it helps | flove conventions applied where they genuinely fit; the app flows like a flove app when it costs nothing |
| 4 | **Soak**  | deeply soaked — flove standards throughout | the app follows the flove standards end to end; surfaces, motion, i18n, export align with the family |
| 5 | **All-in** | the full flove workflow | every hat, every addon, the whole pipeline (design → validate → vocab → translate → export → publish) |

## Reading the scale

- **1–2 · flavour:** the project stays itself; flove is seasoning.
- **3 · blend:** the default sweet spot — conventions when they help, never by
  force.
- **4–5 · alignment:** the project becomes a flove citizen — standards, shared
  CSS/JS, vocabulary, and the circuit's identity.

## Rule of thumb

> Pick the lowest number that still gives the project what it needs. 3 is the
> recommended default; reach for 4–5 when the app will live in the flove
> circuit (shared player, tags, flove.json, publish pipeline), and 1–2 when the
> target is a standalone thing that merely borrows a look.

## In Questy FLOVE

In questy-flove the gauge is the same scale but the *target is flove itself*:
1 = ask about the app plainly, 5 = assume the app is a full flove citizen and
question it against every standard. The export JSON carries the chosen level as
`influence`.
