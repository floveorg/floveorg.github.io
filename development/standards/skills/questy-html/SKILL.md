---
name: questy-html
description: >-
  Turn any Q&A session into an interactive HTML form with live preview. Renders
  questy questions and answers as a web form users open in a browser, click
  through in batches, and export to markdown. Use whenever questy offers to
  render the Q&A as an interactive form at session start, or a Q&A session
  needs to become a browser form with live preview. flove-first by default;
  override via the personal config (see CONFIG.md).
---

# questy-html

Turn any Q&A session into an interactive HTML form with live preview.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## What it does

Renders questy questions and answers as a web form you can open in a browser. Users click through options, see their answers compile in real time, and export the result.

## Install

questy-html ships with the flove skills library: `development/standards/skills/questy-html/`,
symlinked from `~/.agents/skills/questy-html`. No copy needed.

## How questy uses it

When questy-html is installed, questy offers to render the Q&A as an interactive HTML form at session start. The form:
- Shows questions in batches with click-to-answer
- Highlights recommended answers (★)
- Compiles a summary panel in real time
- Exports to markdown on completion
- Exports questy-flove-dev.html with the **"Import questy"** button — the exported form loads any
  questy markdown (a `pendings.md`, an answers `.md`, a pasted survey) and re-renders it as
  clickable question blocks. Import content joins the count and travels in the copied prompt.

## Fallback (no questy-html)

If questy-html is not installed, questy can:
1. Generate a static HTML file with the Q&A content
2. Link to `https://flove.org/development/standards/skills/questy/` for the standalone form
