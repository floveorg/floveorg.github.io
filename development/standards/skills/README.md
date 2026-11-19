# flove-skills

Personal skill library for Claude Code and compatible agents. One real copy on
disk: `~/.agents/skills` symlinks here
(`development/standards/skills/`).

**Index:** the verified table is
`https://flove.org/development/index.html` (Web → Skills). Do not copy it into
markdown.

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
- https://flove.org/development/standards/skills/texty/SKILL.md
- https://flove.org/development/standards/skills/translaty/SKILL.md
- https://flove.org/development/standards/skills/updaty/SKILL.md
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
