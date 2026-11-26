<!-- CONTEXT:BEGIN
schema: flove-page/1
id: ai/skills/maintenance
path: development/standards/data/ai/skills/maintenance.md
trunk: ai
topic: skills
kind: topic
status: stable
html_place: ["#ai"]
owns: ["Sys skill core guidance", "Read-only audit pattern"]
updated: 2026-11-26
read_next: ["../skills.md", "./skills.md"]
CONTEXT:END -->

# Sys — maintenance and checkers

Core guidance for `sys` skills: `backy · jsony · optimizy · scripty · skilly · texty · translaty · validaty`.

Reference this page from sys skills instead of restating shared rules.

## Sys maintenance and checkers

- **Gate, don’t silently fix canonicals.** Checkers report findings; structural
  or canonical fixes go to the owning skill/standard (`/jsony` contracts,
  `/texty` names/copy, etc.) unless the skill's own scope explicitly includes
  the edit.
- **Read-only audit pattern.** For audit/check/report modes, follow [Read-only audit pattern](#read-only-audit-pattern).
- **Idempotent and honest.** Re-running a check should not change meaning.
  Partial coverage is stated plainly; a partial pass is not green.
- **Severity and handoff.** Separate blocking/critical from advisory when the
  gate has consumers. Name the owner for the fix.

## Read-only audit pattern

Shared pattern for skills that inspect without mutating canonical state. Use it
when a skill has an audit/check/report mode (`translaty` coverage, `texty` L2
contract audit, `jsony` checks, `scripty`, `skilly`, similar gates).

- **Read-only by default.** Audit reports findings; it does not edit canonical
  contracts, schemas, or unrelated files. Structural fixes are handed to the
  owning skill (`/jsony` for contracts/schemas, `/texty` for names/copy, etc.).
- **Scope declared.** Name what is checked, skipped, and assumed (base language,
  schema id, file/glob, marked vs unmarked text).
- **Evidence first.** Report file/path, location, expected/actual, severity or
  confidence, and a concrete fix/owner. Prefer machine-readable output when a
  gate consumes it.
- **Coverage honesty.** State what the audit cannot see (generated/runtime-only
  strings, unmarked spans, dynamic keys). Partial pass is not green.
- **Idempotent command.** Same input gives same report; no writes, no timestamps
  in canonical files unless explicitly requested.
- **Headless run.** Never block: write the survey as text, apply the
  navigation-preserving recommendation and label those edits
  *"applied on recommendation — pending user confirmation"*.
