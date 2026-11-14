# questy — advanced use case

All perspectives + all addons + all workflows + all scripts + all integrations.
Two parallel tracks: **HTML form** (left) and **console prompt** (right).

For each step: what questy does, what it asks, and how the user responds.

> **Type policy (2026)**: questy's type is the **Thinking Hats** — facts ·
> heart · risk · optimism · creative · make. The KISS catalogue (vision/arch/
> trust/data/integration) is deprecated and only kept here as the legacy steps
> below; anywhere the live skill runs, hats are the only type. Steps 21–31
> describing `vision/arch/…` read as the older console tracking they replaced.

---

## Phase 1 — Config check & setup (steps 1–12)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 1 | Check ~/.config/questy/config.md | Skip setup, load saved config | `/questy new-project` |
| 2 | If missing: ask setup mode | Present [1] HTML form [2] Console [3] Modal | `No config found. Setup? (1/2/3)` |
| 3 | User picks HTML form | Open flove.org/questy/ in browser | `2` → console mode |
| 4 | Prompt: Project name | [Project name...] input | `Q1: Project name? → new-project` |
| 5 | Prompt: Type | [docs] [code] [mixed] buttons | `Q2: Type? [1]code [2]docs [3]mixed → 3` |
| 6 | Prompt: State | Nowadays it's [Ok] [Messy] | `Q3: State? [1]fresh [2]ok [3]messy → 2` |
| 7 | Detect doc-roots | [Route(s)] text input | `Q4: Doc roots? → ./docs/, ./src/` |
| 8 | Validate config | No required fields, copy whatever filled | Config stored as markdown |
| 9 | Fallback check | If malformed → SKILL.md defaults | `Config parse error, using defaults` |
| 10 | Save config | Writes ~/.config/questy/config.md | Saved automatically |
| 11 | Batch mode check | + button for multi-project | `Batch mode? (y/N)` |
| 12 | Load defaults | type = the six Thinking Hats (facts/heart/risk/optimism/create/make), batch: 5, per-type: 5 | Defaults loaded |

## Phase 2 — Project context (steps 13–20)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 13 | Set active workflow | It's about [docs] [code] selector | `Workflow: code + docs` |
| 14 | Detect existing git | Scans .git in project dir | `.git found → synced workflow available` |
| 15 | Confirm extra-files path | Text input for extra session | `Extra doc roots? (optional)` |
| 16 | Map file territory | Standards/ → principles, Plans/ → proposals, Docs/ → reference | `Found: 3 standards, 2 plans, 5 docs` |
| 17 | Detect pendings.md | Check if exists from previous session | `Pending items from last session: 2` |
| 18 | Detect conflicts.md | Check if exists | `Open conflicts: 1 (plan-vs-standard)` |
| 19 | Detect proposals.md | Check if exists | `Proposals: 3 active, 1 resolved` |
| 20 | Session resume check | "What changed since last time?" | `What changed since last session? (text)` |

## Phase 3 — Perspective: the Thinking Hats as type (steps 21–48)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 21 | Show the Thinking Hats (the type) | [facts] [heart] [risk] [optimism] [creative] [make] | `Q8: Hats? [1]white [2]red [3]black [4]yellow [5]green [6]blue` |
| 22 | User selects vision | Click once → selected, twice → x2 weight | `1, 1 again → weighted` |
| 23 | Questy notes vision scope | What is this? Who for? Why? Others? Blind spots? | `vision active, weight: 2` |
| 24 | User selects arch | Same click pattern | `2 → arch active` |
| 25 | Questy notes arch scope | Component boundaries, data flow, scope, blind spots | `arch active` |
| 26 | User selects trust | Click | `3 → trust active` |
| 27 | Questy notes trust scope | Threat model, privacy, edge cases, recovery | `trust active` |
| 28 | User selects data | Click | `4 → data active` |
| 29 | Questy notes data scope | Structure, relationships, lifecycle, retention | `data active` |
| 30 | User selects integration | Click twice → x2 weight | `5, 5 → weighted` |
| 31 | Questy notes integration scope | A↔B contract, boundary failure, protocol, sync | `integration active, weight: 2` |
| 32 | Show rainbow hats | [white] [red] [black] [yellow] [green] [blue] | `Q9: Hats? [1]facts [2]heart [3]risk [4]optimism [5]creative [6]make` |
| 33 | User selects ⬜ white/facts | Click | `1 → facts` |
| 34 | ⬜ white explanation | What do we know? Data? Specs? What's missing? | `facts: data-proven questions` |
| 35 | User selects 🟥 red/heart | Click twice → x2 | `2, 2 → heart (weighted)` |
| 36 | 🟥 red explanation | How does it feel? User fear? Trust? | `heart: feeling + trust questions` |
| 37 | User selects ⬛ black/risk | Click | `3 → risk` |
| 38 | ⬛ black explanation | What could go wrong? Threats? Blast radius? | `risk: threat + failure questions` |
| 39 | User selects 🟨 yellow/optimism | Click | `4 → optimism` |
| 40 | 🟨 yellow explanation | Benefits? Value? Why build? User gain? | `optimism: value + benefit questions` |
| 41 | User selects 🟩 green/creative | Click | `5 → creative` |
| 42 | 🟩 green explanation | Alternatives? Wild ideas? Flipped perspective? | `creative: alternative + novel questions` |
| 43 | User selects 🟦 blue/make | Click | `6 → make` |
| 44 | 🟦 blue explanation | Flow? Connection? Contract? How A↔B? | `make: process + contract questions` |
| 45 | Show Wisy lenses | Explainers / Formalise / Tone / Teleology / Field / Time span | `Q10: Extended perspectives? (multiselect)` |
| 46 | Explainers (7) | [why] [what] [how] [what-for] [who] [where] [when] | `1-7: explainers selected` |
| 47 | Formalise (5) | [axiom] [evidence] [prediction] [proposal] [challenge] | `8-12: formalise selected` |
| 48 | Tone (4) + Teleology (4) + Field (5) + Time span (7) | Each multiselect | `13-33: all lenses configured` |

## Phase 4 — Addons: Core + Scripts + Integrations (steps 49–68)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 49 | Show core addons | [index] [agents] [tree] [git] [html] [.github/] [archive] [pro] [scripts] | `Q11: Addons? [1]index [2]agents [3]tree [4]git [5]html [6].github [7]archive [8]pro [9]scripts` |
| 50 | User selects tree | Click → creates docs/, plans/, standards/, pendings.md, conflicts.md, proposals.md | `3 → tree addon` |
| 51 | User selects index | Click → generates README.md | `1 → index addon` |
| 52 | User selects agents | Click → creates agents.md | `2 → agents addon` |
| 53 | User selects git | Click → .gitignore + repo sync | `4 → git addon` |
| 54 | User selects html | Click → web output, questy-html preview | `5 → html addon` |
| 55 | User selects .github/ | Click → issue/PR templates | `6 → github addon` |
| 56 | User selects archive | Click → archive.md for resolved items | `7 → archive addon` |
| 57 | User selects pro | Click → docs/adr/ folder | `8 → pro addon` |
| 58 | User selects scripts | Click → scripts/ folder | `9 → scripts addon` |
| 59 | Show script options | [build] [test] [deploy] [lint] [format] [typecheck] [docker] [audit] [benchmark] [docs] [release] [deps] | `Q15: Scripts? (multiselect from 12)` |
| 60 | User selects build+test+lint+format | Click each | `1,2,4,5 → build+test+lint+format` |
| 61 | User selects deploy+docs+release | Click | `3,10,11 → deploy+docs+release` |
| 62 | Show integrations | [tickets] [board] [linear] [notify] [pulse] | `Q16: Integrations? (multiselect)` |
| 63 | User selects tickets+board | Click | `1,2 → tickets+board` |
| 64 | Show agents.md sections | [shortcuts] [constraints] [pending-resolutions] [batch-overrides] [export-prefs] [territory] [aliases] [danger-zone] [decision-log] [archive] | `Q14: Agents.md options?` |
| 65 | User selects shortcuts+constraints+territory | Click | `1,2,6 → selected` |
| 66 | Show workflow options | [synced] [merge rules] [commit guard] [finish line] [blueprint] | `Q12: Workflows?` |
| 67 | User selects synced (git prerequisite) | Click (only if git selected) | `1 → synced workflow` |
| 68 | User selects merge rules | Click → opens PR standards sub-options | `2 → merge rules` |

## Phase 5 — Workflows & PR Standards (steps 69–80)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 69 | Show PR title format | [conventional] [ticket-number] [branch-name] | `Q13a: Title format? [1]conv [2]ticket [3]branch → 1` |
| 70 | Title → conventional | Selected | `conventional commits` |
| 71 | Show description template | [basic] [detailed] [none] | `Q13b: Description? [1]basic [2]detailed [3]none → 2` |
| 72 | Description → detailed | Selected | `detailed PR description` |
| 73 | Show review checklist | [code quality] [tests pass] [docs updated] [no breaking] [screenshot] | `Q13c: Checklist? (multiselect) → 1,2,3` |
| 74 | Checklist items → 3 selected | Click | `code+tests+docs` |
| 75 | Show merge strategy | [squash] [merge-commit] [rebase] | `Q13d: Merge? [1]squash [2]merge [3]rebase → 1` |
| 76 | Merge → squash | Selected | `squash commits` |
| 77 | Show branch naming | [feature/ticket] [feature/description] [none] | `Q13e: Branch? → 1` |
| 78 | Branch → feature/ticket | Selected | `feature/TICKET-123` |
| 79 | Show commit format | [conventional] [imperative] [none] | `Q13f: Commit? → 1` |
| 80 | Commit → conventional | Selected | `feat: conventional format` |

## Phase 6 — Output & export (steps 81–88)

| # | What questy does | HTML form | Console prompt |
|---|-----------------|-----------|----------------|
| 81 | Show output formats | [story] [data dump] [spreadsheet] [notion sync] [obsidian vault] | `Q17: Output? (multiselect)` |
| 82 | User selects story | Click → narrative format | `1 → story output` |
| 83 | User selects data dump | Click → raw JSON/MD | `2 → data dump` |
| 84 | Check questy-html | If installed → offer live preview | `questy-html found. Render as HTML?` |
| 85 | Fallback | If not installed → static HTML | `questy-html not found. Static HTML?` |
| 86 | Check skill integration | [validaty] [optimizy] [translaty] [exporty] | `Post-questy: run /validaty? /optimizy?` |
| 87 | Offer skill chain | Only installed skills shown | `Skipping — no installed skills` |
| 88 | Final config review | "Save Config" button / "Copy Prompt" | `Config complete. Save? (y/N)` |

## Phase 7 — Scan & understand (steps 89–95)

| # | What questy does | What it finds | Console output |
|---|-----------------|--------------|----------------|
| 89 | Scan standards/ | Read all .md files, map frozen decisions | `Reading standards/… found 3 files` |
| 90 | Scan plans/ | Read active proposals, architecture docs | `Reading plans/… found 2 files` |
| 91 | Scan docs/ | Read reference, ADRs, changelogs | `Reading docs/… found 5 files` |
| 92 | Detect conflicts | Compare plan-vs-plan, plan-vs-standard | `Conflict: P002 vs standards §3.1` |
| 93 | Assess coverage | Map types to existing content | `Arch: covered ∎∎∎∎∘ 80% | Trust: covered ∎∘∘∘∘ 20%` |
| 94 | Prioritise gaps | Order by risk + coverage deficit | `Priority: trust (gap) > integration (gap) > data (partial) > vision > arch` |
| 95 | Filter answered | Cross-ref proposals.md resolved items | `Skipping: Q004, Q007, Q015 (already resolved)` |

## Phase 8 — Generate, process, close (steps 96–100)

| # | What questy does | Presentation | User action |
|---|-----------------|-------------|-------------|
| 96 | Generate trust questions (gap priority) | Batch 1: 5 trust questions with ⬛ risk hat, global Q016-Q020 | `1,3,5 → answered 3, skipped 2` |
| 97 | Generate integration questions | Batch 2: 5 integration questions, type→hat mapping applied | `2,4 → answered 2` |
| 98 | Generate remaining | Arch, data, vision in impact order | `c → next batch` |
| 99 | Process answers | Update proposals.md (new decisions), pendings.md (skipped), conflicts.md (new clashes), archive.md (if resolved) | `stop → end session` |
| 100 | Export & commit | Git add+commit all changed files; offer markdown/JSON/HTML export; if questy-html → live preview | `Exported to exports/questy-2026-07-29.md` |
