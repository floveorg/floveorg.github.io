# Skills — personal config override

Every skill ships with **flove-first defaults**. To reuse / fork a skill for
another project you do **not** edit the skill itself — you create a **personal
config** that overrides the defaults it reads.

## How the override works

Each skill looks for a config file in this order and uses the **first match**:

1. `~/.config/flove/skills-config.yml` — the shared, per-user config.
2. `<skill>/settings.yml` — a per-skill config living **inside** the skill folder
   (public, tracked — good for a fork or to pin team defaults).
3. `<skill>/.settings` — a hidden config file in the skill folder.
4. Nothing found → the skill uses its built-in flove-first defaults.

`<skill>/config.yml` is also accepted (it is a common name people expect).

## Recommended per-user shared config

Create `~/.config/flove/skills-config.yml` with any keys you want to override:

```yaml
# personal skills config — overrides the flove-first defaults
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

## Why

- **Portable**: a skill copied to another project changes behaviour by adding a
  config file — no source edits.
- **Clean upstream**: the repo keeps one canonical version; individual
  variations live outside it.
- **Explicit**: which parts are default vs. personal is visible in one place.