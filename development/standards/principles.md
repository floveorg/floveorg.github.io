# flove · Development principles

Common principles guiding **all** development of the flove project —
**backend** (flovenet), **frontend** (the apps), and **communitarian**
(governance, gift-economy, contribution). One yardstick runs through all three:
*build things that would score the maximum on Worthing's eight criteria.*

→ frontend specifics: `standards/` (matrix · contract · catalogue) ·
backend: `decentral/nety/` · worldview/ethos: `worldview.md`.

> Moved here 2026-07-31 from the retired `~/Documents/context` repo.

---

## 1 · The Worthing yardstick

`solo/apps/economy/worthing.html` rates anything worth-having on **8 criteria**, 1–10 each, in
four pairs. We turn its rater into our **self-evaluation rubric**: before shipping
anything — a feature, a module, a hardware choice, a governance rule — rate it on
these eight and iterate to **maximise the score** (*"get the maximum ratings at
Worthing"*).

| Group | Criterion | Score 10 means, in development terms |
|-------|-----------|--------------------------------------|
| **Meaningful** | **Symbolical** | carries meaning & identity — the relational vocabulary, the sprout, *what it stands for* |
| | **Historical** | rooted and durable — builds on what exists, preserves continuity, made to last |
| **Powerful** | **Ideal** | aligned with the vision & principles — aspirationally *right*, not just expedient |
| | **Potential** | room to grow — composable, extensible, future-proof |
| **Useful** | **Functional** | it actually works and is usable — solves the real need |
| | **Affordable** | cheap to build, run and adopt — minimal cost & resources (*free + low-impact ecological hardware*) |
| **Friendly** | **Respectful** | ethical — privacy, consent, accessibility; respects both people and planet |
| | **(Re)generative** | gives back more than it takes — ecological regeneration, gift-economy reciprocity, FOSS that feeds the commons |

**How to use it:** sketch → rate on the 8 → pick the option that lifts the lowest
scores *without* sacrificing the others. Be **as crafty as possible**: maximise
Functional + Potential while keeping Affordable high (do the most with the least).
When a choice trades off, favour **Affordable · Respectful · (Re)generative** —
flove would rather be light, ethical and regenerative than maximal.

---

## 2 · Cross-cutting principles (backend · frontend · community)

1. **Slow it · flow it · love it.** Low-tech, calm, relational. No hype, no
   flashy-AI. The simplest thing that carries the meaning.
2. **Open source first · free-as-in-freedom.** Prefer FOSS; name the libre
   alternative before any proprietary one and mark the proprietary explicitly.
3. **Low ecological impact.** Minimal compute; **free + low-impact ecological
   hardware**; local-first over cloud; static single-file over heavy build;
   P2P / gift over centralized servers. The greenest option that still works.
4. **Crafty & resourceful.** Reuse before building; combine small pieces; squeeze
   the most function from the least code, money and energy.
5. **Local-first & portable.** Runs client-side first; one interface, swappable
   backends (the Publisher adapter) so nothing is locked to a platform.
6. **Relational / confluent.** Frame opposites as complements, not winners;
   *simplexify* — the simplest-but-still-bipolar formulation.
7. **Gift-economy & decentralized.** Reciprocal contribution over money;
   web-of-trust over authority; pseudonymous and private by default (crypto +
   biometrics stay **local**, never sent).

---

## 3 · Per-domain notes

- **Backend (flovenet).** Rust P2P, local-first, post-quantum crypto, IPFS for
  static content only, Firecracker/WASM compute, reciprocal-reputation economy
  (no money). The minimal-block / low-resource design is itself an *Affordable +
  (Re)generative* choice. → `flovenet/roadmap.md`.
- **Frontend (apps).** Single self-contained HTML, CSS-first, no build. The three
  axes (tier · distro · surface). Valid HTML/CSS + WCAG AA. →
  `flove/standards/`.
- **Community.** Gift-economy, proportional governance, web-of-trust, open
  contribution, FOSS licensing. Decisions and tools are themselves rated on the
  Worthing eight.

---

## 4 · In one line

*Make it meaningful, powerful, useful and friendly — with the least money, energy
and lock-in possible, giving more back than it takes.* That is a 10 on Worthing,
and it is what flove development aims for, everywhere.


