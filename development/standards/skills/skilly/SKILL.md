---
name: skilly
description: >-
  Sanity-check the flove skill library — frontmatter, secrets, dead repo paths,
  SKILL.md size caps, dead links and paragraphs copied across skills. Use for
  /skilly, after editing a skill, or when a polish pass touched the library;
  never for an app page.
---

# skilly

The skill library's own health check. Skills load on every session, so a broken
frontmatter silently hides one and a bloated `SKILL.md` taxes every conversation.

## When it runs

- after you edit any file under `development/standards/skills/`;
- at the end of a polish pass **only if that pass edited a skill**;
- when asked "are the skills healthy?".

It does **not** run for an app or page polish — a page has no skill library to
check. A polish pass calls `/skilly` as an inner gate, the way it leaves the
JSON backbone to `/jsony`; neither is a page stage.

## Run it

```bash
python3 development/standards/scripts/check-skills.py
```

Exit 0 = no errors. Warnings do not fail the script but must be resolved or
explained in the report.

## Read the output

| Finding | Remedy |
|---|---|
| ERROR frontmatter / duplicate `name` | fix the `---` YAML: non-empty `name` + `description` |
| ERROR secret-looking string | remove it; name the file that holds the secret instead |
| WARN backticked path does not resolve | fix the repo path, or drop the backticks if illustrative |
| WARN body over 1,000 words / 150 lines | move detail into a flat file in that skill, link it once |
| WARN description over 320 chars | cut to trigger + scope; it is paid every session |
| WARN paragraph repeated across skills | keep one canonical copy; link to it |
| WARN dead local link / machine path in a skill page | fix the route; a skill page must resolve inside the library |
| WARN dead markdown link or `#anchor` | fix the path; the heading it points at must exist |
| WARN markdown nothing in the skill links to | link it from `SKILL.md` or delete it |
| WARN retired skill or file name | use the current name (the warning says which) |
| WARN skill folder over 512 KB or 60 files | media goes to `central/shared/media`, a dump goes to a flat file |
| WARN unreferenced asset | link it or delete it |
| WARN bare `scripts/…` in a command | use `development/scripts/…`; skill assets stay under `assets/` |
| WARN missing H1, H1 ≠ `name`, no `Use for` | open with `# <name>`; state the trigger in the description |

Never "fix" a warning by deleting content the skill still needs.

## Boundaries

- It validates and reports; it does not rewrite skills. Fix what the finding names.
- Zero errors is the gate. Warnings may be explained (for example a deliberate
  duplicate inside an eval fixture) but not ignored.
- The same script is the distro gate: `development/scripts/check-distro.sh` runs it too.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
