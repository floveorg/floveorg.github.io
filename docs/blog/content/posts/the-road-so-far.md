---
title: "The road so far"
date: 2026-07-06T09:30:00
draft: false
categories: ["Tech"]
tags: ["flove", "retrospective"]
---

Before the devlog picks up entry by entry, here's the whole arc in one place — how
flove got from an idea to the thing you can [install today](https://flove.org/).

## By the numbers

flove is young and dense. As of this first post:

- **~2 months** of building — first commit **7 May 2026**, and it hasn't stopped.
- **1,100+ commits** on the main line, from a single pair of hands.
- **~30 apps**, and **70-plus** single-file builds once you count their tiers and
  variants, grouped in about **ten clusters** — browse them all at
  [flove.org/apps](https://flove.org/apps/).
- Built as an intense **human + AI pairing** — on the order of **120 sessions** of
  working side by side with Claude.

Small team, short calendar, a lot of ground. Here's how it fits together.

## The bet

flove started from a discomfort with the extractive internet: platforms tuned to
harvest attention, measure it, and sell it back. The counter-bet is simple to say
and hard to build — an internet where **relating matters more than extracting**.
Slow instead of urgent, warm instead of optimized, human-scale instead of infinite.
That bet had to become something you could touch, so flove grew as a set of
concrete tools rather than a manifesto.

## The apps

The visible surface of flove is its [apps](https://flove.org/apps/) — small,
single-file pages, each exploring one facet of relating: writing
([blogy](https://flove.org/apps/blogy/blogy-advanced.html)), deciding and rating
([keys](https://flove.org/apps/puzzy/keys-advanced.html)), sharing what you make
([appy](https://flove.org/apps/appy/appy-basic.html)), everyday economics
([dealy](https://flove.org/apps/economy/dealy/dealy-advanced.html)), trust
([trusty](https://flove.org/apps/trusty/trusty.html)), and more. They're
deliberately humble: mostly HTML and CSS, JavaScript only where it earns its
place, no build step, and they keep working offline. You can read each one like a
page, not a black box.

## Standards: the family grammar

Why does a collection of independent little apps feel like *one* calm, coherent
thing? Because they share a set of **standards** — not bureaucracy, but *care made
repeatable*: the same gentle look, the same respect for your attention and your
data, the same promises kept in every corner. Underneath that sit a shared design
contract, a canonical vocabulary, a mandatory step-by-step onboarding, a single
summary-and-export contract, and a tier model that lets each app meet you at the
size you want. Each app still keeps its own character; the standards are the
grammar, not the script. They're all gathered now on one page —
[flove's standards](https://flove.org/docs/standards.html).

## Tiers and distributions

Two ideas gave the collection room to grow without sprawling. **Tiers**: most apps
come at several sizes — from a *mini* that does one thing up through richer
versions — so the same idea can meet you at the complexity you want. And
**distributions**: the working distro you use today, plus a portable, pure-CSS
specification meant to travel — flove's ideas expressed cleanly enough to be
rebuilt on other platforms, not just this one.

## The theory underneath

Under the apps sits the part that will get its own **Theory** shelf here later: a
coordinate system for placing things in relation to one another, and a *fuzzy*
ontology — soft axes instead of hard categories, because relating rarely fits in a
box. The apps are, in a sense, that theory made usable.

## Making it yours to keep

The most recent stretch pushed hard on one principle: flove should be **something
you keep, not a service that keeps you**. So flove became installable and fully
offline — a downloadable package you can run with no server, launchers for each
desktop, even an Android build. If flove.org vanished tomorrow, your copy would
still open. All of it is built from a single local source of truth, versioned, and
published to the open web — the same workshop this blog is now part of.

That's the road so far. The next post covers what landed most recently; from
there, the devlog just keeps walking.

_slow it · flow it · love it._
