# flove — agent entrypoint

**Working directory:** `/home/kdeneon/Documents/flove` — never another flove folder.

This file routes and owns the advisory decision profile; standards rules stay
with their owners. Read the owner, not a copy:

| Need | Owner |
|---|---|
| How I work — duplicates, ownership, standards/skills, levels, tables, routes, language, safety | [`development/standards/AGENTS.md`](development/standards/AGENTS.md) |
| How tasks execute — PROC-01–10, queue, gates | [`development/AGENTS.md`](development/AGENTS.md) |
| Binding rules and the floor | [`development/standards/contract.md`](development/standards/contract.md) |
| Advisory decision preferences — read before choosing | [`#decision-preferences`](#decision-preferences) |
| What exists | [`development/standards/README.md`](development/standards/README.md) |
| App-local work | that app's `AGENTS.md` (e.g. [`apps/sys/nety/AGENTS.md`](apps/sys/nety/AGENTS.md)) |

Resolve `https://flove.org/...` locally first; the rule and its two local rule sources are in [`development/AGENTS.md#local-first-url-resolution`](development/AGENTS.md#local-first-url-resolution). Do not repeat a rule here. No commit or push unless asked.

<a id="decision-preferences"></a>

## Decision preferences

Advisory: changes what is recommended, not whether a question is asked. Only a domain named in `delegated` removes a question. Rules are applied per case, not uniformly (Q015).

**Source:** questy focus=preferences · Q004-Q030 · 2026-11-21
**Former home:** `development/decision-rules.json` (`flove-decision-rules/1`); this chapter is now the single home. No script parses it.

### Rules

| ID | Domain | Hat / lens | Choice | Reason | Con |
|---|---|---|---|---|---|
| Q004 | privacy_vs_convenience | red / why | Privacy holds; accept the extra steps | you keep control of what leaves your machine | more friction; some features feel slower |
| Q005 | risk | black / fatal | Silent data loss is the feared failure | silent loss corrupts trust without warning | favours slower, redundant designs |
| Q006 | priority | yellow / what-for | Durability over capability | it should still work without you maintaining it | less appetite for frequent rewrites |
| Q007 | scope | green / experimental | Small and finished over bigger and open | you get something you can use and judge | features you wanted may be cut |
| Q008 | architecture_order | blue / how | Hold the no-db order firmly; no db until the core is solid | your stated focus: consolidate no-db first, add a minimal db as overlayer | a handy db shortcut gets refused |
| Q009 | autonomy | red / who | Do it and report after, for ready tasks with no open decision | matches judgment-calls-only | you see it once it is done |
| Q010 | speed_vs_audit | white / what-for | Auditability over speed | slower, but you can check what happened | things take longer |
| Q011 | tie_break | yellow / experimental | The reversible option; keep the most options open | consistent with small-and-finished and no-db-first | can look indecisive |
| Q012 | always_ask | blue / who | Anything that changes what data is kept or where it lives | follows the privacy answer | you stop on every storage/db step |
| Q013 | offline_bias | blue / when | Partial answer now from what is on the device | matches small-and-finished and full-offline | you may decide on incomplete information |
| Q014 | data_recovery | black / fatal | Keep an automatic local recovery copy | silent loss is your feared failure and the copy stays on your machine | more data and state to manage |
| Q015 | consistency | yellow / fine | Judge each case on its own | nuance | unpredictable, more questions |
| Q016 | sharing | red / who | Private by default; share only when you say so | follows your privacy answer | fewer people benefit |
| Q017 | explanation | yellow / why | Explain the human consequence briefly, so you can judge next time | builds your own ability to decide | a few extra lines |
| Q019 | tidiness | green / how | Leave the imperfect owner; note it | stability of existing links | untidy mapping persists |
| Q020 | proactive_maintenance | blue / when | Only run backups and maintenance when asked | follows P7 and your control preference | no safety net if you forget |
| Q021 | authority | white / what | Follow your preference; flag the doc drift | personal fit | docs diverge |
| Q022 | adjacent_work | green / how | Do the safe part, list the rest | matches AGENTS 11.2 and small-and-finished | adjacent items wait |
| Q023 | ambiguity | black / fatal | Ask when the choice changes what you get; assume for reversible details | control where it matters | some questions remain |
| Q024 | safety_edges | blue / who | Credentials, sw.js and commit/push — the full AGENTS 9 list | already standing rules | more stops |
| Q025 | review_cadence | yellow / how many | One batch of about 10 tasks, then review | tighter feedback | more interruptions |
| Q026 | rank_vs_focus | white / what | Your stated focus wins; report the deviation | the rank does not know your priorities; follows Q008 | advisory order gets ignored |
| Q027 | reopen | green / when | Reopen only if it changes data, safety or architecture order; otherwise hold and flag | follows Q012, Q024 and Q008 | wrong decisions persist in small matters |
| Q028 | community | red / who | Owner-controlled; open it only when you ask | matches private-by-default and the Marc-only option | less community growth |
| Q029 | deferral | yellow / when | Defer it and record why; do not guess | matches the defer pattern and Q023 | open items accumulate |
| Q030 | dependencies | blue / what | Self-contained, even if heavier | matches privacy, offline and no-db answers | more local weight |

### Open item

- **Q018** · `error_bias` — skipped — intermediate options offered (55-58), no choice made (ref: `development/tasks/pendings.md Hot`)

### Delegated — no question

- ready tasks with no open decision — do it and report after (Q009)

### Always ask

- changes to what data is kept or where it lives (Q012)
- credentials, sw.js and commit/push (Q024)
