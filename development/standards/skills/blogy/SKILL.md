---
name: blogy
description: >-
  Write a project development-log article for the blog (flove.org/development/blog,
  category "Tech") when the owner (Marc by default) asks. Use whenever the owner
  types /blogy or asks to "write a blogy", "write up what's new", "do the monthly
  flove update", "blog the recent development", "milestone post", or otherwise
  wants a public write-up of what the project has been building lately. It
  gathers the real recent work (git log across the project's repos, memories,
  docs/making-of, standards changes), drafts ONE English article in the "Tech"
  category in the project's voice, and runs the drafts-first → preview → OK →
  publish flow. There is no automation: the owner triggers it (roughly monthly
  and/or at notable milestones). Flove-first by default; override via the
  personal config (see CONFIG.md). It inherits the blog setup
  ([[project_flove_blog_blogy]]) and the publish pipeline
  ([[project_flove_publish_pipeline]]).
---

# blogy — write a flove development-log post

The flove blog is a Hugo site, part of the flove repo: source in
`~/Documents/flove/development/blog` (Gitea `marc/flove`). The built HTML is
committed **into that same directory** (no `/public` segment) and ships with the
main site via `publish-web.sh` → served at `flove.org/development/blog`.
Posts live in `content/posts/*.md`. Categories are a Hugo
taxonomy; the blogy lives in the **Tech** category (URL slug `tech`).

This skill writes ONE post per run: a briefing on what flove has built since the
last blogy. The owner calls it when they want one — not on a schedule.

## Personal config

This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## Editorial voice (the owner's standing preferences — honor them)

- **English.** The blog is `defaultContentLanguage = en`.
- **Open with a philosophical, general-audience framing.** Before the technical
  themes, a short accessible opener: what this update means in human terms, and
  the one thread that ties the stretch together. Written for anyone, not just
  developers. This is the standard shape — the post
  `content/posts/whats-new-mid-2026.md` is the **reference template**; new blogys
  follow its structure.
- **Overviews, not detail-dumps.** Write a briefing / résumé — the few changes
  that moved flove furthest, grouped into a handful of themed sections. Do NOT
  list small individual tweaks (no "small things that matter" grab-bag). If it
  wouldn't matter to a reader a month from now, leave it out.
- **Philosophical first, then technical.** Open each theme in plain,
  general-public language (what it means, why it matters), *then* get specific.
- **Close warm, human, and a little funny.** End with an engaging, playful, human
  paragraph — not just the sign-off. Invite the reader in (come poke around, break
  something, tell us what you'd relate differently), keep it self-aware and light
  (e.g. "one determined human and one alarmingly patient robot"), then the
  `_slow it · flow it · love it._` sign-off.
- **Direct links** to what you mention — real, resolvable URLs (HTTP 200), not
  the short "motes" (e.g. `/blogy`) which 404 without JavaScript. Link to real
  paths: the [apps catalogue](https://flove.org/apps/), specific apps
  (`/apps/<cluster>/<app>.html`), the [standards page](https://flove.org/docs/standards.html),
  the [making-of](https://flove.org/docs/making-of/making-of.html), theory pages.
  Verify each link is 200 before using it.
- **Spotlight standards.** Changes to the standards (the design contract,
  frontend standards, backend plan, skills — all on
  `flove.org/docs/standards.html`) deserve their own section; the owner cares about
  these especially.
- **Stats on the first post / milestone posts.** A "By the numbers" block —
  commits, count of apps, timespan, pairing sessions. Only quote numbers you
  actually measured; if you can't verify a figure (e.g. total tokens), use an
  honest proxy (session count) or omit it.
- **flove voice.** Warm, low-tech, unhyped. Close with `_slow it · flow it · love it._`

## Procedure

1. **Find the window.** What has happened since the last blogy? Read the newest
   `tech` post's date, then gather the real work:
   - `git -C ~/Documents/flove log --oneline --since=<last blogy date>` (and the
     other repos if relevant: `~/flovenet`, `~/.agents/skills`).
   - Recalled memories (`MEMORY.md` + the project_* files) for what's significant.
   - `docs/making-of/` and the standards page for framing.
   For a **milestone / first** post, also gather stats: `git rev-list --count HEAD`,
   first/last commit dates, app count (catalogue), Claude session count
   (`ls ~/.agents/projects/-home-kdeneon/*.jsonl | wc -l`).

2. **Draft ONE post** at `~/Documents/flove/development/blog/content/posts/<slug>.md`:
   ```
   ---
   title: "<short, human>"
   date: <YYYY-MM-DDThh:mm:ss — a time already PAST; Hugo skips future-dated posts>
   draft: true
   categories: ["Tech"]
   tags: ["flove", ...]
   ---
   ```
   Then the body, per the voice rules above. Themed sections, briefing-length.

3. **Verify links.** `curl -s -o /dev/null -w '%{http_code}'` every URL you linked;
   fix any that aren't 200. (Motes 404 to curl — use real paths.)

4. **Preview + show the owner.** Start `hugo server -D --source ~/Documents/flove/development/blog`
   (background) and give the owner `http://localhost:1313/posts/<slug>/`. Summarize what
   the     post says. **Do not publish yet** — this is drafts-first. Wait for their OK or
   edits; iterate.

5. **On the owner's OK:** flip `draft: false`, then publish:
   `(cd ~/Documents/flove/development/blog && ./build-blog.sh publish)` — rebuilds the
   HTML in place, commits the built output, pushes to Gitea (`origin`) and runs
   `publish-web.sh` → live at flove.org/development/blog. Other source edits keep the
   scoped-git-add rule (never `git add -A` — see the scoped-git-add rule).

## Guardrails

- **Drafts-first, always.** Never publish before the owner has seen it.
- **One post per run.** Don't backfill several at once unless the owner asks.
- **Scoped commits.** Only the post file(s) you wrote; the owner edits in parallel.
- **Honest stats.** Measure or omit — never invent a number.
- Publishing is public and hard to unsay. If anything in the draft looks
  unreleased or private, flag it before pushing.
