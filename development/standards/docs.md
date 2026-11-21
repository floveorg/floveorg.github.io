<!-- CONTEXT:BEGIN
schema: flove-page/1
id: community/docs
path: development/standards/docs.md
trunk: community
topic: docs
kind: topic
status: stable
html_place: ["#md-sources"]
owns: ["Docs navigation", "privacy-first docs"]
updated: 2026-11-21
read_next: ["#access-convention","#onboarding-copy","#wiki-review","#community-framework","#community-doc-plan"]
supersedes:
  - development/wiki/archive/old/apps/onboarding-copy.md
  - development/wiki/archive/old/browsy/browsy-questions.md
  - development/wiki/archive/old/browsy/rationale.md
  - development/wiki/archive/old/standards.md
heavy: false
CONTEXT:END -->

# Docs

> **Stable page.** Migrated from the pre-cutover sources on 2026-11-21.
> The chapters below are the only owners; the child plan records source history.


<a id="access-convention"></a>
## ACCESS / COM / IDEA convention

> Owner: docs. A prefix names the destination and owner; a new proposal can be
> filed without asking, and promotion to a decision is explicit.

<a id="onboarding-copy"></a>
## Onboarding copy

> Owner: docs/experience. The 30-app onboarding copy is published once in
> `plans/frontend/experience.md#app-blocks`; this page links, never duplicates.

<a id="wiki-review"></a>
## Wiki review

> Owner: docs. Every live MD names an owner and a last-reviewed date; frozen
> pages are explicit.

<a id="community-framework"></a>
## Community and channels framework

> Owner: docs. Every community doc is marked live or historical with one
> navigation home.

<a id="community-doc-plan"></a>
## Community documentation plan

> Owner: docs. Every live debate doc has one authority line in the community
> index.

## Questy-generated documentation

> Source: `development/wiki/archive/old/standards.md` (archived 2026-11-21).

Questy can create the documentation skeleton for another project:

- `docs/`, `plans/`, `standards/` folders;
- `pendings.md`, `conflicts.md`, `proposals.md`, `archive.md`;
- `agents.md`, `.gitignore`, `.github/`, `docs/adr/` and `scripts/` when the
  matching addon is selected.

Rules: `SKILL.md` is the single source of truth and the HTML form must match it;
presets override doc-roots and extra files, never the reverse; extra files are
not read unless the addon that creates them is selected; missing doc-roots are
skipped with one warning, not an error.

## Source map

| Archived source | Date | Stable home |
|---|---|---|
| `archive/old/apps/onboarding-copy.md` | 2026-11-17 | development/standards/docs.md |
| `archive/old/browsy/browsy-questions.md` | 2026-08-01 | development/standards/docs.md |
| `archive/old/browsy/rationale.md` | 2026-11-17 | development/standards/docs.md |
| `archive/old/standards.md` | 2026-08-01 | development/standards/docs.md |

Chapters without a separate source row are `milestone-only`: they are
specified from the register (hitos and tasks) and remain owned here.
