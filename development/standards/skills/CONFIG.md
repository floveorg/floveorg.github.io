# Skills — personal config override

Every skill ships with **built-in defaults**. To reuse / fork a skill for
another project you do **not** edit the skill itself — you create a **personal
config** that overrides the defaults it reads.

## How the override works

Each skill looks for a config file in this order and uses the **first match**:

1. `~/.config/flove/skills-config.yml` — the shared, per-user config.
2. `<skill>/settings.yml` — a per-skill config living **inside** the skill folder
   (public, tracked — good for a fork or to pin team defaults).
3. `<skill>/.settings` — a hidden config file in the skill folder.
4. Nothing found → the skill uses its built-in defaults.

`<skill>/config.yml` is also accepted (it is a common name people expect).

## Example of recommended config setup for a project

The template below is an **example**, not a live file — nothing reads
`~/.config/flove/skills-config.yml` on this machine today. The only real
personal configs in use are questy's (next section); copy the template as a
starting point when adopting a skill family into a new project.

### Recommended per-user shared config per Routes and keys

Two independent decisions go into every personal config — **the route**
(where the file lives) and **the keys** (what it overrides):

- **Routes** — the lookup order in "How the override works" doubles as your
  menu. Pick the first route that fits the job:
  1. *Shared* `~/.config/flove/skills-config.yml` — one file steering every
     skill at once; right for identity-level keys (`project_name`, `owner`,
     `repo`, `domain`). Caution: it is the **first match**, so once it exists
     it shadows any per-skill file — keep project-specific values out of it.
  2. *Per-skill* `<skill>/settings.yml` — tracked inside the skill folder;
     right for a fork or team-pinned defaults that travel with the skill.
  3. *Hidden* `<skill>/.settings` — local-only tweaks you never commit.
  4. `<skill>/config.yml` — accepted alias for either per-skill naming.
- **Keys** — override only what differs from the built-in defaults written
  into each SKILL.md; every unset key falls through. A key sitting in a file
  the skill never reads (because an earlier route matched) has no effect —
  first match wins.

Day-to-day workflow: copy the template → delete every key that already equals
its default → place the file on the chosen route → run the skill once and
confirm it picks up the override before relying on it.

Create `~/.config/flove/skills-config.yml` with any keys you want to override:

```yaml
# personal skills config — overrides the built-in defaults
master:
  project_name: flove            # default "flove"
  owner: Marc                    # default "Marc"
  repo: ~/Documents/flove        # default path
  domain: flove.org              # default public site
  gitea: origin                  # local first remote
  github: floveorg/floveorg.github.io
  solo: flove-solo               # downloadable package name
solo:
  project_name: flove-solo
  domain: flove.org
```

Only keys you provide are overridden; the rest fall back to the defaults that
are written into each skill file.

### Real questy configs (live examples)

The two personal configs actually in use today are questy's. Note they are
plain markdown rather than YAML — the loader cares about the sections and
keys, not the extension:

`~/.config/questy/config.md`:

```markdown
# questy config — flove

## project
- type: docs
- name: flove

## workflow
- active: docs
- state: ok

## questions
- batch: 5
- mode: numbered
- types: vision, arch, trust, data, integration
- per-type: 5

## paths
- doc-roots: …/development/standards/, …/development/standards/debates/plans/
- extra-files: …/debates/pendings.md, …/debates/proposals.md,
  …/debates/agents.md, …/debates/plans/conflicts.md,
  …/skills/questy/proposals.md
- frontend: https://flove.org/development/standards/skills/questy/

## addons
- [ ] tree · git · agents · html · github · archive · pro · scripts
```

`~/.config/questy1/config.md`:

```markdown
# Questy1 personal config

## Presentation style

### Question format
- Each question wears a Thinking Hat colour (⚪ facts · ❤ heart · ⬛ risk ·
  🟡 optimism · 🟢 creative · 🔵 make)
- Each question has A/B/C recommended answers with a ★ Recommended pick

### Answer format
- User answers like: `1a 2b 3c 4a 5b`
- `0` = accept all recommended answers
- `-` = skip any question (goes to pendings)
- Free-form answers are also accepted instead of A/B/C

### Ordering
- Abstract to concrete — strategic first, tactical last
- Mix hat colours — do NOT group by colour
- Within the gradient, order by impact: ⬛ > 🟢 > 🔵 > 🟡 > ❤ > ⚪

### Batch size
- 5 questions per batch, 30 total (5 per hat)

### Tone
- Friendly, concise; each question 1-2 sentences max; one-sentence rationale

## File structure
- questy-docs/context.md · questy-pending.md · conflicts.md · proposals.md
- agents.md · standards/ · plans/
```

## Why

- **Portable**: a skill copied to another project changes behaviour by adding a
  config file — no source edits.
- **Clean upstream**: the repo keeps one canonical version; individual
  variations live outside it.
- **Explicit**: which parts are default vs. personal is visible in one place.