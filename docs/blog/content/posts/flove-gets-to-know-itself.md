---
title: "flove gets to know itself"
date: 2026-07-20T12:00:00
draft: true
categories: ["Tech"]
tags: ["flove", "docs", "standards", "search"]
---

Every so often we stop, look up from the workbench, and tell you what flove has
been up to. This is one of those — flove thinking out loud in public again.

If the last update was about making flove something you can **have and keep**
(installable, offline, yours), this stretch was about flove learning to **know
itself**: writing down how it actually works, so it can explain itself — to you,
and to the odd pairing of a human and a robot who keep building it. Less a pile
of apps, more a thing that can hand you its own reasoning when you ask. Here's
what that looked like.

## flove wrote down its own thinking — and made it searchable

The biggest shift: flove now has a real **home for its docs**. Everything that
used to live scattered — the design philosophy, the backend spec, the coordinate
system it's built on, the worldview underneath it — is now one browsable place,
the [dev docs](https://flove.org/apps/dev/). It reads like a small book you can
wander: a sidebar, a search box, and pages that link to each other.

Underneath it there's something we're quietly proud of: a **theory pack** with
its own little [reader](https://flove.org/docs/theory/), and an *agent search*
sitting on top of the whole corpus. Ask it a question in plain words — "what's
the tier model?", "how does the coordinate system work?" — and it finds the
passage, across the docs and the theory both. It runs on plain keyword search out
of the box, so there's no heavyweight AI model to download; it just works. The
point isn't cleverness — it's that flove can now *answer for itself* instead of
making you dig.

## The standards got a backbone

flove is a family of apps that are meant to feel like one thing — same shapes,
same words, same restraint. What keeps them coherent is a set of shared
**standards**, and this stretch they grew a proper spine. They now live as a tidy
little sub-book — a stable index, the mandatory contract, the pattern catalogue,
and a per-app adoption checklist — all reachable from the
[standards page](https://flove.org/apps/dev/standards/). We also wrote down the
*procedures* that had only lived in our heads: how the docs are edited, how they
publish, how to check your own work. It's the connective tissue of flove, and a
lot of the recent care went straight into it.

## Apps that quietly remember you

Most of the internet remembers you on *its* servers. flove is trying the
opposite: your creations gather in one place **you** own. This stretch the
app-to-profile bridge grew up — the things you make in an app now land in your
personal profile on their own, on your device, no account and no server in sight.
(There's a companion post on exactly that — it graduated from a button you press
to something that just happens.) Seven apps are wired in so far, from
[souls](https://flove.org/apps/metas/souls.html) to
[goddy](https://flove.org/apps/metas/goddy.html) to
[pracsys](https://flove.org/apps/bio/pracsys.html); the
[profile](https://flove.org/apps/appy/appy-basic.html) is where they collect.

## Staying light enough to keep

A copy of flove is supposed to feel like something you own, not a service you
depend on — which means the downloadable copy has to stay *small*. As a couple of
media-heavy corners crept in (some Bach for one app, a bank of laughs for
another), the download quietly ballooned. So we moved that media out to where big
files belong and pointed the apps at it, and the "go local" package slimmed right
back down. On the live site nothing changed; the download just stopped getting
heavy. Housekeeping, but the kind that keeps the promise.

## Until the next one

So that's late July: flove getting to know itself — able to explain its own
thinking, quietly remembering what you make, and still small enough to keep in
your pocket. Built, as ever, by one determined human and one alarmingly patient
robot, going slow on purpose.

If you've read this far, you're exactly the kind of person flove is for. Come
[poke around the apps](https://flove.org/apps/), open the
[docs](https://flove.org/apps/dev/) and ask them something, break something, and
tell us what *you'd* relate differently. We'll be right here.

_slow it · flow it · love it._
