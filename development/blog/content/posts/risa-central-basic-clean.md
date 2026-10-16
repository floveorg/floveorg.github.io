---
title: "The tag cloud and the playlist: how Risa's frontend grew up"
date: 2026-08-19T18:00:00
draft: false
categories: ["Tech"]
tags: ["flove", "risa", "liberada", "central", "solo"]
---

Risa is, at heart, two pieces of frontend. On the left, a **floating cloud of tags** — little chips that drift around, that you tap to filter the feed, that grow when you ask them to. On the right, the **playlist** — the player, the threads, the reactions, everything that happens when a laugh is actually listened to. Over the last month that frontend went through three lives: it was born, it was moved into a shared engine, and it was cleaned until anyone could fork it. This is the story of those two pieces across the versions — and the three names you need to keep straight: **flove0** (the distro), **risa1** (nick as tag), **risa2** (the current one, on the shared libraries).

## By the numbers

- **328 commits** on Risa's `v2-central` branch (19 Jul → 20 Aug); **94** since the v2 cut on 19 Aug.
- **177 commits** across the flove repo; **40** on liberada.net's profiles.
- **10 releases tagged** on Risa: `v1` → `v1.1.0`, then `v2.0.0`, `v2.1.0`, `v2.1.1`.
- **31 clips** in the feed; **108 pairing sessions** with the robot.
- Only numbers we counted: sessions and commits, not tokens.

## flove0 — the shelf

Before the apps, the container: **flove solo**, a downloadable, local-first package you unzip and run without the internet. A flat zip (`flove-solo.zip`), a service worker that precaches the whole catalogue, a home page that reads like a catalogue, and an Android wrapper. flove0 is the shelf the apps sit on — which is why the shelf's most public frontend growing up matters to the whole family.

## risa1 — where the tag cloud and the playlist were born

risa1's idea was *nick as tag*: a serverless Telegram bot turns your voice note into a clip, a moderator approves it, and it lands in `risa.json` for the web to read. The backend deserves a paragraph, not a chapter — upload → moderate → ffmpeg → R2 → feed → channel, with a salted key per author, a miniapp, and anti-abuse limits. And it kept getting **ongoing fix and improvement releases** (v1.0.1 → v1.0.7): accessibility to zero violations, RSS/Atom feeds, CI on every push, the critical bot fix, drafts that no longer vanish between cron runs, video-notes, the community users, the threads. Good, boring reliability work — the kind that makes a frontend safe to love.

### The subdomain: from a hash to a home

The deepest identity promise in risa1 is the **author subdomain**. Every published clip carries a salted `key` (never the Telegram id in the clear), and with a key the author's name links to `#/u/<key>`, an automatic mini author-page that aggregates all their laughs. The subdomain is that page promoted to a **home of your own**: after the first publication the bot offers `<username>.liberada.net` with a three-way prompt — "Sí, quiero / No sé / No, seguro" — and nothing auto-creates. "Sí" activates the subdomain; "No sé" asks again at the next publication; "No, seguro" silences it forever. A `/usuario <nombre>` command renames it, and the publication notice hands the author their link ("Puedes encontrar todas tus risas juntas en este enlace: …"). The miniapp (`#/entrar`) ties the 6-digit code from the bot to that key, so *you* can see your own page before the world does. It's opt-in all the way down: privacy is the default, the address is the gift.

But the frontend is where risa1 is remembered:

- **The floating tag cloud.** Not a dropdown, not a sidebar — a cloud of chips that **drift** around their space like dust in sunlight, sized by how often the tag is used, tap to filter the feed, tap again to let it go. It was built CSS-only: radio inputs, `:has()` and a `floatChips` loop that bounces chips off the walls and pushes them apart when they touch. The `+` expands the cloud a little at a time; the search box in the corner lets you type a tag, a title, a name.
- **The playlist.** Two curated worlds of laughter — *Risas de la gente* (the feed, newest first) and *Risas del mundo* (scrapped from Wikimedia Commons: contagiosa, carcajada, pícara, risita, mundo) — running through a shared player factory: transport, pagination, favourites, and a thread toggle under every clip that has replies.
- **v1.1.0 turned the playlist into a browser of content.** Clips stopped being a flat list of audios. They became a **comment section**: nested replies with depth, collapsed with a counter and a big `↳` arrow, played depth-first so a reply sounds before its sibling. **Video** got its own zone with natural proportions and no autoplay. **Deep links** (`#/c/<id>`) highlight a clip in its thread. Flat **tabs** replaced horizontal scrolling. The tags cloud stayed, but now it filtered a conversation, not just a list.

And then risa1 was frozen — a version you intend to keep trusting, packaged as the download.

## risa2 — the tag cloud and the playlist move to the shared engine

While risa1 was being polished, its future was being built in parallel: **Cloudflare D1** (a real database for follows, reactions, plays), a **service worker** for offline, and **authy** (claims, several ids, `central/users/`). risa2 is not a bump — it's another line of life, and its story is mostly told in the frontend.

### The subdomain grows a brain

The subdomain that risa1 promised as an opt-in link became, in risa2, a real architectural feature. A **Worker** serves a generic profile template for any username in `usernames.json`, so `<user>.liberada.net` works without a folder per person — the profile is *served*, not *stored*. The template resolves the user from the `Host` header (`<user>.liberada.net`) as well as the path, so the same code answers the apex and every subdomain. **Aliases** ride on top: an author can have several names — `María`, her yoga-handle, a private alias — each filtering the same feed from the same canonical profile. The DNS moved from IONOS to Cloudflare to make it real, the canonical profile lives on the subdomain, and the identity that makes it all hang together is authy: claims, several ids, and `central/users/<key>/` waiting in the wings. The tag cloud filters laughs; the subdomain filters *people* — and now the whole liberada network is addressable by name.

- **v2.0.0** — the frozen bridge: the monolithic risa1 page, versioned and downloadable.
- **v2.1.0 — Calling libs.** The tag cloud and the playlist moved out of the page and into **`central/shared/code`** as first-class `flove-*` modules: `flove-tags`, `flove-player`, `flove-feed`, `flove-app`, `flove-bottom-nav`. Now *Risas de la gente* and *Risas del mundo* run through the **same driver**; only the content changes. Ama and the next apps inherit the engine for free. Around the move, the frontend got repaired properly:
  - the **logo menu** that never opened (the CSS waited for a class the JS never added);
  - the **media toggle** that made the playlist vanish (it now filters as two independent audio/video checks, and `select()` feeds the filter so nothing disappears);
  - the **curated world playlist** restored to its scrapped Wikimedia origins via a per-section clip source;
  - the **floating tags tamed** — chips now push each other apart when they touch, and the `+` grows the space below by ten percent a click, with a `−` that shrinks it back.
- **v2.1.1 — central basic clean.** The quiet milestone: dead code swept from the libraries (a `timeAgo` nobody called, an option that stopped meaning anything, a stray padding that made a round button oval), the workshop committed, and the whole shared library landed in the repo as first-class citizens. The shared code stopped being an experiment and became the foundation.

## The human pass — the playlist learns to react

The frontend's last act in this window is the one people actually feel:

- **The `+` menu** on every clip: reply in a thread, react, favourite, download, share.
- **Reactions, the honest way** — a small emoji chip on each clip (the first emoji as the counter), a breakdown that shows who reacted with their profiles as links, the remaining emojis waiting below to be picked. Counts are **real people** — five demo users from the circle reacted to one of María's clips — not random numbers. They render when there's a session; without one, nothing is invented.
- **Threads that work** — a reply plays *its* clip, not its parent's; sub-replies nest at the right depth; a brand-new reply slots straight into the chain. Videos stay collapsed until you ask, and never autoplay on you.
- **María grew real** — her own clips in the feed, a shorter Yo list, a reactions tab named after her default emoji.

Then a long, loving polish pass, all of it on those two pieces: a centred topbar with the transport where your thumb expects it, the `+` that became a perfect circle, the play button and Publicar and the Go button all agreeing on a single red, hover and click effects that stopped disagreeing with each other, emojis that bob and grow on hover, a `Porque` that throws its benefit chips down at its own pace.

## The thread

Three names, one frontend. **flove0** is the shelf. **risa1** proved the tag cloud and the playlist — and the subdomain that gives every laugher a home — and froze them when they were trustworthy. **risa2** moved both into a shared engine, set them on D1, service workers and a Worker that serves a profile for every name, and cleaned them until anyone could fork the whole thing. Ama is next: paused for now, waiting its turn on the same two pieces and the same promise of an address you can point people to.

Come poke around — [Risa](https://risa.liberada.net) is live (tap the tags, play the world playlist), the [apps catalogue](https://flove.org/central/apps/) is getting more honest, and the [docs](https://flove.org/docs/) try hard to explain it before we've finished it. Download the distro, break a chip, tell us what you'd relate differently. It's one determined human and one alarmingly patient robot, and we're only as good as the next person who forked us.

_slow it · flow it · love it._
