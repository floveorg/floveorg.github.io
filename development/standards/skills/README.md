# flove-skills

Personal skill library for Claude Code and compatible agents. One real copy on
disk: `~/.agents/skills` symlinks here
(`development/standards/skills/`).

**Index:** the verified table is
`https://flove.org/development/index.html` (Apps → Types → Skill filter). Do not
copy it into markdown.

## Categories

`category` is required in every `SKILL.md`; `checker_of` is present only when a
skill actually judges conformance to a named standard. The canonical registry
is Work · AI → Skills in `development/index.html`; this table is its mirror.

| Category | Skills |
|----------|--------|
| `sys` | backy · exporty · jsony · optimizy · skilly · texty · translaty · validaty |
| `authoring` | blogy · brandy · diagramy · narraty |
| `planning` | questy · questy-all · questy-flove · questy-html |
| `utility` | jev · tasky · updaty · updaty-apk |

## Standard → owning checker

Canonical map: [standards/README.md → Checker map](https://flove.org/development/standards/README.md#checker-map).
This file does not copy it. A skill without `checker_of` (for example `narraty`
or `blogy`) is an authoring, planning or utility skill, not a checker.

## Skills

- https://flove.org/development/standards/skills/backy/SKILL.md
- https://flove.org/development/standards/skills/blogy/SKILL.md
- https://flove.org/development/standards/skills/brandy/SKILL.md
- https://flove.org/development/standards/skills/diagramy/SKILL.md
- https://flove.org/development/standards/skills/exporty/SKILL.md
- https://flove.org/development/standards/skills/jsony/SKILL.md
- https://flove.org/development/standards/skills/narraty/SKILL.md
- https://flove.org/development/standards/skills/optimizy/SKILL.md
- https://flove.org/development/standards/skills/questy/SKILL.md
- https://flove.org/development/standards/skills/questy-all/SKILL.md
- https://flove.org/development/standards/skills/questy-flove/SKILL.md
- https://flove.org/development/standards/skills/questy-html/SKILL.md
- https://flove.org/development/standards/skills/skilly/SKILL.md
- https://flove.org/development/standards/skills/tasky/SKILL.md
- https://flove.org/development/standards/skills/texty/SKILL.md
- https://flove.org/development/standards/skills/translaty/SKILL.md
- https://flove.org/development/standards/skills/updaty/SKILL.md
- https://flove.org/development/standards/skills/jev/SKILL.md
- https://flove.org/development/standards/skills/updaty-apk/SKILL.md
- https://flove.org/development/standards/skills/validaty/SKILL.md

## Shared rules

- https://flove.org/development/standards/skills/standing.md
- https://flove.org/development/standards/skills/CONFIG.md

## Layout

One folder per skill: `<skill>/SKILL.md` plus the flat files it needs
(`scripts/`, reference docs); no `references/` subfolder. `SKILL.md` is what
every agent loads — trigger, the shape of the job, 5–8 imperative steps,
guardrails. Everything a reader needs only sometimes goes to a flat file in that
skill's folder, linked once by its flove.org URL. Target: body under ~1,000 words,
description under 320 characters.

## Repo

- Tracked directly in the flove repo (no embedded repo, no gitlink).
- Published by `publish-web.sh` under `development/standards/skills/`.
- Editing through `~/.agents/skills` or the repo path touches the same files.
