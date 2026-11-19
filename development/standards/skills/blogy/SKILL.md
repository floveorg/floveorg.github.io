---
name: blogy
description: >-
  Write one flove development-log article in the blog's Tech category — gathered
  from real recent work — then draft, preview, and publish on the owner's OK. Use
  for /blogy, "write a blogy", "do the monthly flove update", "milestone post".
---

# blogy — write a flove development-log post

The blog is a Hugo site inside the repo: source in
`~/Documents/flove/development/blog`, built HTML committed into that same
directory (no `/public` segment), served at `flove.org/development/blog` by
`publish-web.sh`. Posts live in `content/posts/*.md`; categories are a Hugo
taxonomy, and a blogy goes in **Tech** (slug `tech`).

One post per run: what flove built since the last blogy. Owner-triggered, no
schedule.

## Voice — the owner's standing preferences

- **English.** `defaultContentLanguage = en`.
- **Open philosophical, then technical.** A short opener on what the update means
  in human terms and the thread tying it together; for anyone, not only
  developers. Template: `content/posts/whats-new-mid-2026.md`.
- **Overviews, not detail-dumps.** The few changes that moved flove furthest, in
  a handful of themed sections; drop anything that won't matter in a month.
- **Philosophical first, technical second** — open each theme in plain language
  (what it means, why it matters), *then* get specific.
- **Spotlight the standards.** Changes to the design contract, frontend
  standards, backend plan or skills get their own section.
- **Real links only.** Direct, resolvable URLs (HTTP 200) to the apps catalogue,
  specific apps, the standards page, the Work panel, theory pages. Never the short
  "motes" (e.g. `/blogy`) — they 404 without JavaScript.
- **Stats on a first or milestone post.** A "By the numbers" block — commits,
  app count, timespan, pairing sessions. Measure or omit; never invent a number.
- **Close warm, human, a little funny.** End with an engaging, playful paragraph
  — invite the reader in (come poke around, break something, tell us what you'd
  relate differently), keep it self-aware and light ("one determined human and
  one alarmingly patient robot") — then `_slow it · flow it · love it._`

## Procedure

1. **Find the window.** Read the newest `tech` post's date, then gather the real
   work: `git -C ~/Documents/flove log --oneline --since=<date>` (plus other
   repos when relevant: `~/flovenet`, `~/.agents/skills`), the session logs in
   `~/.agents/projects/-home-kdeneon/*.jsonl` and the standards page for framing. For a milestone or first post also gather stats:
   `git rev-list --count HEAD`, first/last commit dates, app count from the
   catalogue, session count
   (`ls ~/.agents/projects/-home-kdeneon/*.jsonl | wc -l`).
2. **Draft ONE post** at
   `~/Documents/flove/development/blog/content/posts/<slug>.md`:
   ```
   ---
   title: "<short, human>"
   date: <YYYY-MM-DDThh:mm:ss — a time already PAST; Hugo skips future-dated posts>
   draft: true
   categories: ["Tech"]
   tags: ["flove", ...]
   ---
   ```
   Body per the voice rules: themed sections, briefing length.
3. **Verify every link** with `curl -s -o /dev/null -w '%{http_code}'`; fix
   anything that isn't 200.
4. **Preview and show the owner.** Start
   `hugo server -D --source ~/Documents/flove/development/blog` in the background,
   give them `http://localhost:1313/posts/<slug>/`, summarise the post. **Do not
   publish yet** — drafts first. Wait for OK or edits; iterate.
5. **On OK:** flip `draft: false`, then
   `(cd ~/Documents/flove/development/blog && ./build-blog.sh publish)` — rebuilds
   the HTML in place, commits it, pushes to Gitea and runs `publish-web.sh` →
   live at flove.org/development/blog.

## Guardrails

- **Drafts first, always.** Never publish before the owner has read it.
- **One post per run** — no backfilling unless asked.
- **Scoped commits:** only the post file(s) you wrote, never `git add -A`
  (`https://flove.org/development/standards/skills/standing.md` rule 2).
- **Honest stats** — measure or omit.
- Publishing is public and hard to unsay: flag anything that looks unreleased or
  private before pushing.

## Personal config

See `https://flove.org/development/standards/skills/CONFIG.md` for the override routes and keys.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
