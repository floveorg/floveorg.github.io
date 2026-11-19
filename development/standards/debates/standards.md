# questy — project standards

Official routes and development rules for the questy skill itself.

## Paths

- `SKILL.md` — main skill definition (single source of truth)
- `presets/` — project-specific config overrides
- `tools/` — companion docs (questy-html.md, etc.)
- `proposals.md` — internal dev history (kept as-is, not cleaned)
- `~/.config/questy/config.md` — user's active config
- `~/.config/questy/overrides.md` — personal behavior overwrites

## Frontend

- URL: `https://flove.org/questy/`
- Source: `development/standards/skills/questy/index.html`
- Single-file HTML/CSS/JS, no build step
- State persisted in localStorage (`questy-state`)
- Mode format: `modeRadio` (simple|explained) + `numbered` (boolean checkbox)

## What questy creates for other projects

When tree addon selected, questy creates:
- `docs/`, `plans/`, `standards/` folders
- `pendings.md`, `conflicts.md`, `proposals.md`, `archive.md` files
- `agents.md`, `.gitignore`, `.github/`, `docs/adr/`, `scripts/` (if selected)

## Rules

- SKILL.md is the single source of truth — HTML form must match it
- Presets override doc-roots and extra-files, not the other way around
- Extra-files are NOT read by default — only when the addon that creates them is selected
- session.md does not exist — user manages their own files
- Config has no required fields — copy whatever is filled
- HTML form is the config builder, not the skill entrance
- Skill entrance is 4 steps: purpose → hats → volume → details

## Error handling & fallbacks

- **Missing doc-roots:** If a configured path doesn't exist, skip it silently — don't error. Warn once, continue with what exists.
- **Malformed config.md:** If config can't be parsed, fall back to SKILL.md defaults. Don't ask the user to fix it — just use defaults for that session.
- **Missing extra-files:** If an extra-file (pendings.md, conflicts.md) doesn't exist, don't create it automatically. Only create when the addon that generates it is selected.
- **No presets matched:** If `/questy {name}` doesn't match any preset file, treat `{name}` as a project name and use defaults.
- **Empty doc-roots:** If no doc-roots are configured, scan the current working directory for .md files as a fallback.
- **Talk2web not installed:** Generate static HTML as fallback. Don't block the session.

## Version & changelog

- Current version: 1.0.0
- Changelog lives in `proposals.md` (internal dev history)
- Version bump when: new addon, new mode, breaking config change, new preset
- Version format: semver (major.minor.patch)

## Authoring presets

To create a new preset:
1. Create `presets/{name}.md` in the questy skill directory
2. Use this template:
```markdown
# questy preset — {name}

## paths
- doc-roots: ../path1/, ../path2/
- extra-files: ../

## preferences
- prefer 🟥 heart questions
- batch size: 4
- mode: numbered+explained

## constraints
- don't touch standards/ — those are frozen
```
3. The first argument after `/questy` matches against preset filenames (case-insensitive)
4. Presets override `doc-roots` and `extra-files` from config.md

## Commands reference

- `c` or `continue` — next batch
- `more {hat}` — generate more questions with that hat (e.g. `more red`, `more green`)
- `update` — re-scan docs for new gaps
- `stop` — end session, offer export
- Numbers (e.g. `1,4,7`) — answer questions by global number
- Letters (e.g. `a,b`) — answer within a single question's options

## Proposals format

User-facing proposals (in `proposals.md`) follow this schema:
```markdown
### P{NNN} — {title}
- **status:** active | resolved | deferred
- **source:** {where it came from}
- **description:** {what and why}
- **resolution:** {how it was resolved} (if resolved)
- **date:** YYYY-MM-DD
```
