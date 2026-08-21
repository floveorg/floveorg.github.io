---
title: "Git, agents, and the long way here"
date: 2026-08-01T10:00:00
draft: false
categories: ["Blogy"]
tags: ["flove", "blogy", "gitea", "agents", "retrospective"]
---

Every workshop needs a wall to hang things on. For a long time flove built its
walls out of trust in other people's platforms — code in someone's cloud, notes
in someone's app, publishing through someone else's pipeline. The internet taught
us that works until it doesn't. This post is the story of flove growing its own
walls: a little server that keeps the work, and a pair of hands — one human, one
machine — that have been learning to build together on the other side of them.

It's also the story of how this blog got its new shelves. Pull up a chair.

## A place that's ours

On **7 May 2026** the first line of flove landed in a repository. From that day
the working rule has been stubbornly simple: everything lives *here*, in git,
versioned and owned, before it ever goes anywhere. For a few weeks "here" meant
a folder on a laptop. Then, on **24 May**, flove got a place of its own — a
self-hosted [Gitea](https://gitea.io/) server, running in Docker on a machine in
the same house that builds flove. No third party in the middle of the work; the
wall is ours.

That wall holds one thing above all: **flove** — the site itself, more than
**1,400 commits** since that first day, and the drawer every other shelf grows
out of.

Public work flows out to [flove.org](https://flove.org/) through GitHub Pages;
private work stays behind the wall. That split — **source private, outcome
public** — is the quiet backbone of everything flove has shipped.

## Three tiers, one flove

The site that grew on that wall isn't one thing. It's three tiers stacked on top
of each other, each with its own job and its own front door, and knowing which
is which tells you more about flove than any single app could.

- **solo** — the PWA home, and the heart of the collection. This is where the
  *single-file* apps live, each one readable, saveable, and workable offline
  through a service worker. The whole shelf is gathered on the
  [apps catalogue](https://flove.org/solo/apps/), with drawers like
  [appy](https://flove.org/solo/apps/appy/appy-basic.html),
  [trusty](https://flove.org/solo/apps/trusty/trusty.html),
  [blogy](https://flove.org/solo/apps/blogy/),
  [economy](https://flove.org/solo/apps/economy/),
  [metas](https://flove.org/solo/apps/metas/),
  [puzzy](https://flove.org/solo/apps/puzzy/),
  [lowai](https://flove.org/solo/apps/lowai/), and
  [psicosocial](https://flove.org/solo/apps/psicosocial/). Start here:
  [flove.org/solo](https://flove.org/solo/).

- **central** — the shared workshop the apps build on. This tier holds flove's
  *libraries* — [flove.css](https://flove.org/central/shared/css/flove.css), the
  flove.js sound and wizard engine, the i18n layer, the loader and settings —
  the low-code core that every app can draw on instead of reinventing. It also
  grows a *different branch of apps* than solo, the hub-facing builds:
  [appy](https://flove.org/central/apps/appy/),
  [blogy](https://flove.org/central/apps/blogy/),
  [gody](https://flove.org/central/apps/gody/),
  [sety](https://flove.org/central/apps/sety/), and
  [questy](https://flove.org/development/standards/skills/questy/), the planning ritual. The hub
  door: [flove.org/central](https://flove.org/central/).

- **decentral** — the network running *parallel to solo*, flove's bet on
  talking to each other without asking permission. Two legs here:
  [browsy](https://flove.org/decentral/browsy/), the in-browser extension, and
  **nety**, the self-hosted network — the most *advanced and quite ready to
  use* of the three tiers, with its own identity, trust graph, and P2P layers
  ([nety on GitHub](https://github.com/floveorg/nety)). Much of it already
  works; much still needs building. The door:
  [flove.org/decentral](https://flove.org/decentral/).

## Two pairs of hands

Almost none of those 1,400 commits were written by one person alone. flove is
built as an intense **human + agent pairing** — on the order of **330 sessions**
so far, working side by side with a robot that has been learning flove's grammar
as fast as Marc writes it.

The trick that made this scale wasn't the agent. It was the **skills**: small,
reproducible instruction files that tell the agent how flove wants things done —
the [standards](https://flove.org/development/blog/categories/standards/), the frontend
contract, the blogy voice, the publish pipeline. Skills turned "an assistant who
guesses" into "a colleague who has read the manual". They live, versioned, in
their own repo behind the wall, and they are as much a product of flove as any
app.

## A pipeline with a front door

What ships is what the wall lets out. The flow is boring on purpose:

folders → **Gitea** (private source) → **GitHub** (public mirror) →
[flove.org](https://flove.org/).

Drafts and private decisions never leave the wall until they're meant to. The
blog's build script, the service worker that makes the site work offline, the
"go local" package — all of it hangs off that one boring flow. You can read the
whole plumbing in the
[Infrastructure](https://flove.org/development/blog/categories/infrastructure/) category.

## By the numbers

As of this post: **1,433 commits** on the main line, from **7 May to today**;
**three tiers** — [solo](https://flove.org/solo/),
[central](https://flove.org/central/), and
[decentral](https://flove.org/decentral/) — holding **roughly 80 single-file
apps** on the [apps shelf](https://flove.org/solo/apps/); **330+ agent
sessions**; and **one rule that never bent** — relate, don't extract.

## The blog grows five shelves

And now, the part you're standing in. When this blog started it had three
shelves — *Main, Tech, Theory*. flove has outgrown that tidy trio, so the blog
has been re-shelved into five, each with its own door in the top bar:

- **[Apps](https://flove.org/development/blog/categories/apps/)** — the collection one by
  one: the builds, the launches, the small decisions.
- **[Blogy](https://flove.org/development/blog/categories/blogy/)** — the build log: what
  got made, what broke, what's next. This post lives here.
- **[Infrastructure](https://flove.org/development/blog/categories/infrastructure/)** — how
  flove runs and gets published: the pipeline, hosting, the tooling.
- **[Notes](https://flove.org/development/blog/categories/notes/)** — short things from the
  workbench that don't need a whole post.
- **[Standards](https://flove.org/development/blog/categories/standards/)** — the grammar
  underneath the apps, and the skills that keep it honest.

Each shelf has an opening post of its own, telling you what's on it, how it got
there, and where it's heading. This one is the front door.

So that's the long way here: a wall that's ours, a pair of hands learning to
build together, and a blog finally big enough to say where things live. If
you've read this far, you're exactly the kind of person flove is for — come poke
around, break something, and tell us what you'd relate differently. We'll be
right here, going slow on purpose.

_slow it · flow it · love it._
