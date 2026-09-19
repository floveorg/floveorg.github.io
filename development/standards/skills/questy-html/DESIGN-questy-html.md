# questy-html — design (consolidated)

**Date:** 2026-06-18 · **Status:** evolving; making-of + feeds shipped, skill (form) implementation pending.

## What questy-html is

A skill that, in brainstorm/plan mode, does three things:
1. **Generates the live interview form** for the active session — a self-contained collapsible HTML questionnaire (opt-in; offered, not forced).
2. **Creates/updates the flove making-of archive** (`flove/making-of.html`) — each interview recorded as a replayable, answerable entry.
3. **Generates per-category RSS feeds** (`flove/feeds/*.xml`) via the reference tool `gen-feeds.js`.

Name: **questy-html** — talk (interview) → web (form, making-of, eventual conversation publishing).

## Converged decisions

- **Context model = public, wiki-git style; embeddings are POINTER-LINKS only** (revises the earlier "embed full brief text" choice). Context files live publicly and versioned; the form and copied prompt embed *links into the commit/wiki*, not inline text. Lighter prompts, single source of truth.
- **Commit association (provenance + context pointer):** each entry (optionally each question) carries `commit:{repo, sha, public, subject}`. Public repo → clickable link to the Gitea commit (built from a configurable `GIT_BASE`); private → a non-clickable `repo@sha` referral. The flove commit message already carries prompt+explanation, so the commit *is* the context the pointer resolves to.
- **Replies: personal/local now** (localStorage), with a clean seam to aggregate **shared/public** replies later via flovenet/0asis. All questions are open to replies.
- **Categories at the question level, multiple per question.** Parallel filtering: category = question-level, published date = entry-level, combinable.
- **RSS = new questions per category** (not replies); static files, one `<item>` per question, regenerated on each update.
- **`making-of.html` is always committed + pushed to flove Gitea.**

## Data shapes (making-of ENTRIES)

```
Entry: { id, title, date:"YYYY-MM-DD", cats:[...], commit?:{repo,sha,public,subject},
         summary, links:[{label,href}], qa:[Q...] }
Q (options):   { q, multi?, cats:[...], o:[{l,d}], chosen:[...], suggest:[...], commit?, note? }
Q (free-form): { q, cats:[...], answer:"...", note? }
```

## Files

- `questy-html/SKILL.md` — workflow (offer → fill → record entry → regen feeds → commit/push).
- `questy-html/template.html` — the live form (piece A).
- `questy-html/gen-feeds.js` — RSS generator (reads making-of.html, writes feeds/).
- `flove/making-of.html` — the archive (data-driven `ENTRIES`).
- `flove/feeds/*.xml` — per-category + `all` RSS.

## Status

**Shipped (committed/pushed to flove Gitea):**
- `making-of.html` — interactive replies, "★ what was decided" overlay, question-level multi-category + parallel filtering, per-category RSS subscribe links, commit-provenance chips. Entry #1 (the questy-html design conversation) reconstructed + anchored to commit `13f8162`.
- `feeds/*.xml` — 9 well-formed RSS 2.0 feeds.
- `gen-feeds.js` — reference generator.

**Pending:**
- Rename skill dir + `name:` frontmatter + memory pointer + cross-refs → `questy-html`.
- Implement the live form `template.html` (piece A), **revised to pointer-based context**: setup block (collapsed) with intent presets (Conflicts·Summarize·Draft-a-plan·Critique) + extra line + a *pointer* to the public context; per-question references render as *links* into the public wiki-git; copy-prompt assembly embeds pointer URLs, not full text.
- Rewrite `SKILL.md` to describe the full workflow incl. recording to making-of, regenerating feeds, committing/pushing, and the commit-association + `GIT_BASE`.
- Choose the public `GIT_BASE` host for deployment (currently `localhost:3000/marc`).

## Deferred (door left open)

- Shared/public reply aggregation backend (flovenet/0asis).
- Making the context repo actually public + wiki-presented.
- Conversation-publishing skill (piece C).

## Verification

Structural validators pass for making-of (parse, options/chosen/suggest/cats, parallel-filter logic, commit wiring) and feeds (xmllint well-formed). Offer behavior in SKILL.md is unchanged → no pressure-scenario re-test needed for that part; the form-template changes get the lightweight regenerate-and-validate path.
