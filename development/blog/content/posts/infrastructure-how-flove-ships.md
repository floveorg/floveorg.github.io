---
title: "Infrastructure — how flove ships"
date: 2026-08-01T10:45:00
draft: false
categories: ["Infrastructure"]
tags: ["flove", "infrastructure", "gitea", "pipeline", "shelf"]
---

Nobody talks about plumbing until it leaks. That's the compliment flove pays its
infrastructure: it's the least poetic part of the project, and the one
everything else stands on. This shelf is where the plumbing gets explained — how
flove runs, how it gets published, and what keeps it from falling over when the
network drops.

## What's on it

At the center is a **self-hosted [Gitea](https://gitea.io/) server**, running in
Docker on a machine in the same house that builds flove, holding **eight
repositories**. It's the wall of the workshop: private source lives behind it,
and only what's meant to be public walks out.

Out the front door runs a deliberately boring pipeline:

folders → **Gitea** (private source) → **GitHub** (public mirror) →
[flove.org](https://flove.org/).

Around that spine, the details that make it *feel* effortless:

- **[flove.org](https://flove.org/)** — the public home, served from GitHub
  Pages, with the [solo](https://flove.org/solo/) PWA area as the real home:
  installable, offline-capable, with a service worker and an app manifest.
- **The "go local" package** — the whole solo area ships as a
  downloadable package, so flove can be taken off the shelf and run anywhere.
- **The blog build script** — drafts written privately, built locally, and only
  pushed into the public world when they're ready to be read.
- **The friendly 404** — the "receptionist" page that turns dead links into
  pointers, so even the wrong address gets a courteous answer.

## How it got here

flove started the ordinary way: folders, then a public GitHub page. The turn
came in May when the wall went up — Gitea moved into the workshop so the source
could stop depending on anyone else's goodwill. The publish scripts, the service
worker, the PWA manifest, the downloadable package — each one was bolted on as a
pain appeared, until the plumbing reached the point of boring reliability. The
blog itself is part of that same wall: its source lives privately and only the
finished pages are let out.

## What's ahead

- **nety's infrastructure** — the decentral network will need a spine of its
  own, and that work starts here.
- **More offline, more local** — the trend of the whole shelf is the same as
  the project's: fewer middlemen, more machine you control.
- **Resilience checks** — the wall should be tested the way walls get tested:
  by leaning on it.

Infrastructure is the least exciting shelf in the shop, and that's exactly the
point. When the plumbing works, the interesting stuff — the apps, the notes, the
standards — gets to be interesting in peace.

_slow it · flow it · love it._
