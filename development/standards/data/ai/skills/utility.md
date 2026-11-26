<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/skills/utility
path: development/standards/data/ai/skills/utility.md
trunk: ai
topic: skills
kind: topic
status: stable
html_place: ["#ai"]
owns: ["Utility skill core guidance"]
updated: 2026-11-25
read_next: ["../skills.md"]
CONTEXT:END -->

# Utility — controlled execution and release

Core guidance for `utility` skills: `tasky · updaty · updaty-apk`.

Reference this page from utility skills instead of restating shared rules.

## Utility controlled execution and release

- **Gates before mutation.** Check dirty tree, required tokens/tools, pending
  moves, and relevant validators before commit/push/publish/rebuild. A red gate
  stops; report why and the next safe action.
- **Secrets by location.** Never print tokens, keys, keystores, or credentials.
  Name the file/location that holds them.
- **Explicit scope and confirmation.** State what level/action will run, what it
  will touch, and what is left dirty. Owner confirmation before destructive or
  externally visible steps when required by AGENTS/workflow.
- **Report outcome and next.** After run/stop: what passed, what changed, what
  remains, and the next level/action.
