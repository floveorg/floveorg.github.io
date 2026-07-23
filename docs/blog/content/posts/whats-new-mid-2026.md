---
title: "What's new — mid-2026"
date: 2026-07-06T10:00:00
draft: false
categories: ["Tech"]
tags: ["flove", "release", "pwa"]
---

Every so often we'll stop, look up from the workbench, and tell you what flove has
been up to. This is the first of those — a devlog, though really it's just flove
thinking out loud in public.

If there's one thread running through everything below, it's this: most of the
internet is built to *hold onto you* — your attention, your data, your habit of
coming back. flove is quietly trying the opposite. The big moves this stretch were
all about making flove something you can simply **have and keep** — on your own
device, working whether or not the network (or we) are around. Less a service that
keeps you; more a thing you own. Here's what that looked like in practice.

## flove goes local and offline

The biggest shift: flove is now **installable and works with no connection**. A
service worker precaches the whole runnable site, so once you've visited, every
[app](https://flove.org/apps/) opens offline. Pages load network-first — online
you always get the latest, offline flove keeps running from cache instead of
breaking. "Go local" also became a real package you can run with no server:
per-OS launchers that serve flove on localhost and open it, a mobile page that
opens the offline copy, and an Android build. A copy of flove should feel like an
app you own, not a service you depend on.

## Standards got a backbone

The shared standards that keep the apps feeling like one family — the design
contract, the canonical vocabulary, the onboarding, the summary-and-export
contract — took a real step forward this stretch. They now live, homogenized and
public, on a single page: [flove's standards](https://flove.org/docs/standards.html).
It's the connective tissue of flove, and where a lot of the recent care went.

## A big tidy-up

Under the surface, a lot got cleaner: the project root was reorganised, the pieces
regrouped, and every behind-the-scenes document moved into a single
[making-of](https://flove.org/docs/making-of/making-of.html) area — kept out of the
offline download so the package stays lean. And — you're reading part of it — this
blog went up, with its shelves for Main, Tech, and Theory.

## Until the next one

So that's mid-2026: a slower internet, stubbornly refusing to be in a hurry, built
by one very determined human and one alarmingly patient robot. If you've somehow
read this far, congratulations — you're exactly the kind of person flove is for.
Come poke around, install it, break something, and tell us what *you'd* relate
differently. We'll be right here, going slow on purpose.

See you in the next one. 👋

_slow it · flow it · love it._
