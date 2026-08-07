---
name: updaty-image
description: >-
  Alias of the `rebrand` skill under the name Marc uses for it. Roll a flove app's changed
  identity — its logo / mark / favicon / wordmark / name / accent palette — out to EVERY
  surface it appears on, consistently and per the flove standards. Use whenever a mark or
  logo is redrawn or replaced and must propagate, or the user types `/updaty-image` (or
  says "update the image", "update the logo everywhere", "updaty-image"): "make this the
  sensy logo everywhere", "apply the new mark across all surfaces", "the app's icon changed
  — update it everywhere", "the bio and apps index(s) too", "and in the appy ones too",
  "propagate the rebrand", "new wordmark for X", "update the palette across the app's
  pages". Trigger it even when the user only names one more surface ("…in appy too") — that
  is a propagation request. It knows the full map of places a flove app's identity lives
  (its own file, its logo study, the category launcher, the demos-index symbol, the appy
  surfaces, favicons), replaces the mark at each while matching that surface's own treatment
  (gradient / monochrome / grayscale-until-hover), applies motion per the standard, and
  verifies every surface by rendering before committing. Built flove-first; anything that
  would diverge from the shared standard is surfaced, not changed silently.
---

# updaty-image → rebrandy (alias)

`updaty-image` is Marc's name for the **rebrandy** workflow (parallel to `updaty-web`).
There is one source of truth so the two never drift.

**Do this:** read `/home/kdeneon/.agents/skills/rebrandy/SKILL.md` in full and follow it
exactly — the whole surface map, per-surface treatment rules, motion/`prefers-reduced-motion`
guidance, the render-to-verify step (with the kwallet + Google-Fonts-strip workaround), and
the scoped-commit close-out all apply verbatim. `/updaty-image` and `/rebrandy` are the same
skill; only the invocation name differs.
