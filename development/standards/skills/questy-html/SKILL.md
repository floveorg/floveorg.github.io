---
name: questy-html
description: >-
  Render a Q&A session as an interactive HTML form with live preview: batches of
  click-to-answer questions, ★ highlights, a compiled summary and markdown export.
  Use for /questy-html or when a session should become a browser form.
category: planning
---

# questy-html

Turns any Q&A session into an interactive HTML form with live preview. Reuses
[`questy/SKILL.md`](https://flove.org/development/standards/skills/questy/SKILL.md) and adds the form.

## What the form does

- Questions in batches, click to answer; ★ recommendations highlighted.
- A summary panel compiling answers in real time.
- Markdown export on completion.
- An **"Import questy"** button in the exported form: it loads any questy
  markdown (a `pendings.md`, an answers `.md`, a pasted survey) and re-renders it
  as clickable question blocks. Imported content joins the count and travels in the
  copied prompt.

## How questy uses it

When questy-html is present, questy offers to render the session as a form at
session start. Without it, questy can generate a static HTML file with the Q&A, or
link to the standalone form at
`development/standards/skills/questy/index.html`.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for the override routes and keys.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
