<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/skills/planning
path: development/standards/data/ai/skills/planning.md
trunk: ai
topic: skills
kind: topic
status: stable
html_place: ["#ai"]
owns: ["Planning skill core guidance"]
updated: 2026-11-25
read_next: ["../skills.md"]
CONTEXT:END -->

# Planning — decide before writing

Core guidance for `planning` skills: `flovy · questy · questy-all · questy-html · questy-tasky-flove`.

Reference this page from planning skills instead of restating shared rules.

## Planning decide before writing

- **Batch before write.** Collect the whole question batch/decision set before
  writing files, moving state, or rebuilding projections. Read-only until answers
  are in, unless the skill explicitly defines a safe incremental checkpoint.
- **Ask, don’t infer.** When task choice, destructive step, ambiguity, or
  procedure edit matters, ask the user. Verified automatic state moves may
  proceed per AGENTS rules.
- **Options with consequences.** Recommendations include a clear pick and its
  downside/consequence; no downside, no star/recommendation.
- **Traceable decisions.** Record chosen option, reason, and dependencies when
  the decision affects tasks/state/projections.
