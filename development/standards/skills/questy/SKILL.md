---
name: questy
description: >-
  General-purpose structured Q&A skill for software projects. Reads project
  docs, detects conflicts and gaps, generates typed questions in batches using
  KISS types (5 lean categories) + rainbow hats (6 thinking modes). Types and
  hats are configurable via the Settings section.   Command: /questy [addon]
  [numbered|simple|explained] [in N] [hat]. Updates docs with answers, flags
  conflicts, routes skipped items to pendings. Use when you want to "question
  the project", "find what's missing", or run a structured review before coding.
  Recommended: /questy minitree (minitree workflow).
---

# questy — structured project Q&A

Turn the table: make the agent receive better input with less effort.

```
standards/  →  plans/  →  questions  →  pendings
   (why)        (how)      (what's missing)  (unclassified)
```

## Intro

The core of questy is building questions — turning what you know (standards,
plans, docs) into what you haven't thought about yet (gaps, conflicts, blind
spots). Every session starts by scanning your project's docs, then composing
insightful questions that probe what matters.

Its mini default — the KISS types (vision, arch, trust, data, integration)
with rainbow hats — already produces sharp, structured questions out of the
box. Further customize by selecting Perspectives (types, hats, Wisy lenses)
that fit your project's needs.

For a richer workflow that sets up the full file structure (standards/,
plans/, docs/, pendings, conflicts, proposals) and syncs everything to git,
add the **minitree** addon. See the Skills addons section below — it's the
recommended way to run questy on real projects.

```
fallback: https://flove.org/development/standards/skills/questy/SKILL.md
```

For a comprehensive 100-step walkthrough covering all perspectives, addons, workflows, and integrations across both HTML form and console prompt tracks, see the [advanced use case](../../debates/UseCase-adv.md).

### Use case: `browsy` (default, no addon)

Questy run on a generic project without any addon selected:

**Step 1** — Check `~/.config/questy/config.md`
- If exists → load it, skip setup
- If missing → offer setup options (HTML form / console / modal)

**Step 2** — Project set
- Name: browsy, type: docs, state: ok

**Step 3** — Ask session purpose (multiselect)
- review docs / challenge decisions / deep dive / sanity check / set up structure / generate for others / thinking hats

**Step 4** — Ask volume
- Questions per type (default 5), batch size (default 5), types (default all: vision/arch/trust/data/integration)

**Step 5** — Scan and understand context
- Read every .md in doc-roots and extra-files, map decisions, architecture, gaps
- Assess what the project has vs what's missing: coverage per type
- Detect plan-vs-plan and plan-vs-standard conflicts, scope creep, dependency mismatches
- Prioritise areas with least coverage

**Step 6** — Select what to generate
- Filter out already-answered questions (cross-ref session history, never re-ask)
- Match types to context: if plans are light → more arch, if no threat model → more trust, if vision unclear → more vision
- Match hats to type via default mapping (vision→optimism, arch→creative, trust→risk, data→facts, integration→make)
- Override hat mapping based on scan findings (e.g. high-risk project → force ⬛ risk on all types)
- Weight deeper by coverage deficit: low-coverage areas get more questions and higher priority
- Order by impact: ⬛ risk > 🟩 creative > 🟦 make > 🟨 optimism > 🟥 heart > ⬜ facts
- Set batch composition: mix types per batch for variety, keep hats coherent per question

**Step 8** — Generate and present batch
- Compose questions per selection plan: 5 per type, chosen hats, numbered mode (global Q001, Q002…)
- Self-check each against existing docs before generating — skip if already answered
- Include Ref (source doc section) and Affects (impact scope)
- Deliver with ★ recommendation when there's a clear best answer, neutral otherwise
- User answers by global number (e.g. `1,4,7`), track answered vs skipped

**Step 9** — Process answers
- Route skipped → pendings (in-memory, no file since tree addon missing)
- Detect new conflicts, track IDs

**Step 10** — Update: trigger and inventory
- User says `update` → pause current batch, save unanswered to pending queue
- Re-read all doc-root files, compare against last scan (new/deleted/changed files)
- Record current session state (answered Q IDs, skipped Q IDs) for delta computation

**Step 11** — Update: delta report
- For each changed file: extract new sections, removed sections, modified decisions
- Detect new conflicts (plan-vs-plan, plan-vs-standard) and scope creep
- Cross-ref pendings.md: are any previously-skipped questions now answerable?
- Show delta summary, present new questions as next batch

**Step 12** — Continue prompt
- Prompt: `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`
- `c` → next batch with same settings
- `t` / `more {hat}` → 5 more with that hat
- `u` / `update` → re-scan docs for new gaps (see minitree steps 10–12)
- `s` / `stop` → end session, offer export (markdown / JSON / HTML) and questy-html if installed

### Use case: `questy minitree` (recommended)

The same flow with the minitree addon loaded — creates the full file structure
and syncs to git:

**Step 1** — Check `~/.config/questy/config.md`
- If exists → load it, skip setup
- If missing → setup flow, load minitree defaults (docs+code, tree+index+agents+git)

**Step 2** — Create project structure
- Create: standards/, plans/, docs/, pendings.md, conflicts.md, proposals.md, agents.md, .gitignore
- agents.md generated with default sections (shortcuts, constraints, pending-resolutions)

**Step 3** — Ask session purpose (multiselect)
- Same 7 options as browsy

**Step 4** — Ask volume
- Same: per-type (5), batch size (4), types (all: vision/arch/trust/data/integration)

**Step 5** — Scan, understand, and select
- Read every .md in doc-roots: standards/ (frozen principles, contracts, frozen decisions), plans/ (active proposals, architecture, implementation strategy), docs/ (reference, ADRs, changelogs, onboarding)
- Map all decisions found: distinguish frozen (in standards/) from active (in plans/) from reference (in docs/)
- Assess coverage per KISS type: does the project have clear vision docs? documented architecture? threat model? data schema? integration contracts? Each gap is a question opportunity.
- Cross-ref proposals.md: which topics have pending proposals? which are resolved? which were skipped?
- Filter already-answered questions using session history and proposals.md resolved items — never re-ask
- Detect conflicts: plan-vs-plan (do two proposals contradict?), plan-vs-standard (does a proposal violate a frozen principle?), scope creep (did the project outgrow its original doc-roots?)
- Match types to context: plans light → more arch, no threat model → more trust, vision unclear → more vision, well-documented area → fewer questions
- Match hats to type via default mapping (vision→optimism, arch→creative, trust→risk, data→facts, integration→make), then override based on findings (regulatory project → force risk on all, creative phase → more green)
- Weight deeper by coverage deficit: low-coverage areas get more questions and higher generation priority
- Order all gaps by impact: ⬛ risk > 🟩 creative > 🟦 make > 🟨 optimism > 🟥 heart > ⬜ facts
- Skip frozen standards/ content unless the user explicitly requests challenges to it
- Set batch composition: mix types per batch for variety, keep hats coherent per question

**Step 6** — Generate and present batch
- Compose questions per selection plan: 5 per type, chosen hats, numbered mode (global Q001+)
- Self-check each against existing docs before generating — skip if already answered
- Include Ref (source doc section) and Affects (impact scope)
- Deliver with ★ recommendation when there's a clear best answer, neutral otherwise
- User answers by global number (e.g. `1,4,7`), track answered vs skipped

**Step 7** — Process answers
- Check each answer against definition-of-done: is the decision clear? does it reference source docs? is it actionable? does it resolve the question without ambiguity? If not, re-prompt the user for clarification before recording.
- Append decisions to proposals.md with ID and cross-ref
- Route skipped → pendings.md, detect new conflicts → conflicts.md
- Archive resolved items (if archive addon)

Definition-of-done means every accepted answer must produce a decision that is specific (not vague), sourced (links back to the question's Ref), and actionable (the team can implement or decide from it). Answers that don't meet these criteria are bounced back with a explanation of what's missing.

**Step 8** — Git sync
- Stage and commit new/changed files
- Commit message: `questy: {purpose} — {N} questions answered`

**Step 9** — Update: inventory and snapshot
- Pause current batch, save unanswered to pending queue
- Record full session state (answered IDs, skipped IDs, decided topics)
- Snapshot the current proposals.md and conflicts.md as pre-update baseline
- Re-read every file in doc-roots and extra-files
- Compare file list and timestamps against last scan: new, deleted, renamed, changed

**Step 10** — Update: edit related files and move out old questions

The core editing phase touches every tracked file type. Which files are involved:

- **`standards/*.md`** — Frozen principles, contracts, and settled decisions. If the user added content that contradicts a standard, the conflict is flagged in conflicts.md rather than edited directly (standards are frozen by convention). If the user explicitly requests a standard change, a new version is appended with a changelog entry.
- **`plans/*.md`** — Active proposals, architecture docs, implementation strategies. New user content is applied here: a new section for each new proposal, amendments appended to existing proposals with a revision history line. If a resolved proposal is contradicted by the new content, it is reopened with a `reopened` status and a cross-reference to the conflicting file. If a standing proposal is fully superseded, it is moved to archive.md.
- **`docs/*.md`** — Reference material, ADRs, onboarding, changelogs. ADRs get new entries appended if the update implies a new decision. Changelogs get a new line. General docs are edited inline where the user's changes map to existing content.
- **`proposals.md`** — The master decision log. Each answered question during the session wrote a line here. During the update, superseded proposals get status `superseded` with a cross-ref to archive.md. Reopened proposals get status `reopened` with a note on what changed. Proposals that remain valid are left untouched.
- **`conflicts.md`** — Detected plan-vs-plan, plan-vs-standard, and scope-creep conflicts. During update: conflicts resolved by the new content get status `resolved` and a closing note. New conflicts detected from the changes get a new entry. False-positive conflicts (the update clarified the ambiguity) are removed entirely.
- **`pendings.md`** — Skipped questions that were not answerable at the time. During update: each pending question is re-evaluated against the updated files. Those that are now answerable are moved back to the active pool (removed from pendings.md, added to the next batch). Those still not answerable stay.
- **`archive.md`** — Superseded proposals, stale questions, and closed conflicts. Questions whose answers are now stale or invalid get a new entry here with status `superseded` and a cross-ref to the updated file that made them stale. The original proposal.md entry is updated to reference the archive location. Conflicts that were resolved also get archived with resolution notes.
- **`.questy/session-state.json`** — Internal session tracking: answered IDs, skipped IDs, decided topics, last-scan timestamps. Updated to reflect which items were archived and which were reopened, so the next batch generation can deduplicate correctly.
- **`.gitignore`, `agents.md`** — Project scaffold files. Only edited if the update expands the project's scope into new types that require new agent defaults or new ignore patterns.

For each changed file (detected in step 10 by fingerprint comparison), the specific action:
1. Determine the file's category (standards/plans/docs from its path)
2. Diff the old vs new user content to isolate what actually changed
3. Apply the change to the right section of the right document, preserving existing structure
4. If the change contradicts a prior proposal or standard, create or update the corresponding entry in conflicts.md or proposals.md
5. After all files are processed, re-scan all previously-asked questions against the updated files:
   - Questions whose answers are now stale or invalid → move to archive.md with status `superseded`
   - Questions still valid → keep in place
   - Skipped questions now answerable → move from pendings.md back to active pool
- Detect new plan-vs-plan and plan-vs-standard conflicts from the changes
- Check scope creep: did the update expand beyond original doc-roots?

**Step 11** — Update: compose replacement questions and show delta
- Re-run coverage per type against the updated files: gaps shrink or grow?
- Adjust hat priorities based on new content (e.g. new threat model → less risk, more creative)
- Compose new questions targeting only the new gaps, new conflicts, and replacement needs
- Deduplicate against full session history and archived questions — never re-ask
- Show delta report: files edited, questions superseded→archived, questions unarchived
- Present the new/replacement questions as next batch, continuing global Q numbering

**Step 12** — Continue prompt or export
- Prompt: `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`
- `c` → next batch
- `t` / `more {hat}` → more with that hat
- `u` / `update` → re-run delta cycle (inventory, diff, re-evaluate + generate)
- `s` / `stop` → export markdown/JSON/HTML, git commit final state; if questy-html installed, offer live preview

## Project and Batch

Configure what project you're working on and how the session runs.

**Project context:** name, type (docs/code/mixed), state (ok/messy)

**Session volume:** questions-per-type (up to 50), batch-size (how many per round), modes (simple, explained, numbered)

**Batch mode:** use the + button in the HTML form to ask questions across multiple projects at once — each duplicate gets its own name and docs route, the prompt generates batch output with all projects listed.

```
/questy simple in 4   → simple mode, 4 per batch
/questy in 10         → numbered, 10 per batch
```

## Perspectives

### Types (KISS default — edit freely)

Multiselect — a question can carry multiple types.
Say any alias: `more vision`, `more trust`, `more arch`.

```
vision, context, why, who          — What is this? Who for? Why? What are others doing? What are we not thinking about?
arch, architecture, components     — Component boundaries, data flow, in/out of scope, blind spots
trust, security, failure           — Threat model, privacy, edge cases, race conditions, recovery, what breaks?
data, structure, lifecycle         — Structure, relationships, lifecycle, migration, retention
integration, contracts, sync       — A↔B contract, boundary failure, protocol, sync semantics
```

In modal one-at-a-time console mode, present types as titles only: `vision`, `arch`, `trust`, `data`, `integration` — no description text after the dash.

### Rainbow Hats (thinking modes)

Applied per-question to shift perspective. A question can carry a hat alongside its type.

```
⬜ white, facts    — what do we know? data? specs? what's missing?
🟥 red, heart     — how does it feel? user fear? gut reaction? trust?
⬛ black, risk    — what could go wrong? threats? failure modes? blast radius?
🟨 yellow, optimism — benefits? value? why build this? user gain?
🟩 green, creative — alternatives? wild ideas? flipped perspective?
🟦 blue, make     — flow? connection? contract? how A talks to B?
```

Default type→hat mapping (override in agents.md):
```
vision→🟨optimism, arch→🟩creative, trust→⬛risk, data→⬜facts, integration→🟦make
```

### See more — Wisy perspectives

Extended lenses that add nuance beyond the core types and hats. Each one opens a different axis of questioning.

Applied the same way as hats — say `why`, `formal`, `experimental`, `science` to activate that lens, or set them in the HTML form under Perspectives → See more. Talking nonformally works: `make it weird` → experimental teleology, `get scientific` → science field.

**Explainers** — frame the kind of answer expected:
`why`, `what`, `how`, `what-for`, `who`, `where`, `when`

**Formalise** — structure the answer format:
`axiom`, `evidence`, `prediction`, `proposal`, `challenge`

**Tone** — voice of the question:
`normal`, `funny`, `formal`, `trivial`

**Teleology** — purpose orientation:
`experimental`, `random`, `fine`, `fatal`

**Field** — domain context:
`metaphysics`, `science`, `biology`, `psychology`, `sociology`

**Time span** — temporal scope:
`moment`, `day`, `week`, `month`, `year`, `decade`, `century`

Each lens can be weighted (click twice in the form for x2) and combined freely.

## Skills addons

Addons bundle project settings, paths, preferred choices, and constraints into a single command. They let you skip the config form and jump straight to questioning.

Addons can be applied:
- **Via the HTML form** — click preset template buttons in the Addons tab, all settings are filled at once
- **Via chat** — just say the addon name or a shortcut (e.g. "minitree", "tree+git") and the agent fills the rest

Talking nonformally works too — say `more green` for creative-hat questions, or `make it a minitree project` to load the minitree addon. The agent recognises intent.

### Recommended: minitree

The minitree addon sets up questy's full workflow — a project that keeps its docs
(standards/, plans/), tracks gaps (pendings.md), conflicts (conflicts.md), and
decisions (proposals.md), and syncs everything to git.

```
/questy minitree              → recommended: docs+code, tree+index+agents+git
/questy minitree simple       → same, simple mode
/questy minitree simple in 4  → same, 4 per batch
```

These files exist because the workflow depends on them:

- **standards/** — principles, contracts, frozen decisions (the *why*)
- **plans/** — active proposals, architecture, implementation (the *how*)
- **docs/** — reference, ADRs, onboarding, changelogs
- **pendings.md** — questions skipped this session, to resolve next time
- **conflicts.md** — plan-vs-plan and plan-vs-standard clashes discovered during questioning
- **proposals.md** — final resume: decisions made, plans confirmed, open items
- **agents.md** — per-project tuning (shortcuts, constraints, aliases)
- **.gitignore** — keeps generated artifacts out of version control

Config that minitree loads:

```markdown
# questy defaults — minitree
## project
- type: docs+code
- name: (your project)
## workflow
- active: docs+code
- state: ok
## questions
- batch: 5
- mode: numbered
- types: vision, arch, trust, data, integration
- per-type: 5
## paths
- doc-roots: ./standards/, ./plans/
- extra-files: ./
- fallback: https://flove.org/development/standards/skills/questy/SKILL.md
```

### Other addons

| Addon | Implies |
|-------|---------|
| `tree` | creates docs/, plans/, standards/, pendings.md, conflicts.md, proposals.md |
| `index` | generates README.md or INDEX.md |
| `agents` | creates agents.md with selected options |
| `git` | detects local repo, syncs files, creates .gitignore |
| `html` | web output, questy-html live preview |
| `.github/` | issue/PR templates + workflows |
| `archive` | creates archive.md, resolved items move there |
| `pro` | creates docs/adr/ with ADR templates |
| `scripts` | creates scripts/ with build/test/lint helpers |
| `synced` | sync newly created files to existing git repo |
| `merge rules` | defines PR title, description, review checklist, merge strategy |
| `commit guard` | runs lint, format, tests before commit |
| `finish line` | task completion checklist |
| `blueprint` | iteration planning structure |

To add a custom addon: create `presets/{name}.md` with doc-roots, extra-files, preferences, constraints. The agent matches the first argument after `/questy` against filenames in `presets/`.

```
# presets/minitree.md (example)
doc-roots: ../standards/, ../plans/
extra-files: ../
preferences: prefer 🟥 heart questions, batch size: 4, mode: numbered+explained
constraints: don't touch standards/ — those are frozen
```

## See more

### Usage

```
/questy                    → numbered, all types
/questy simple             → simple, batches of 10
/questy simple in 4        → simple, 4 per batch
/questy green              → only 🟩 creative questions
/questy simple blue        → simple, only 🟦 integration
/questy minitree           → recommended minitree addon, numbered
/questy minitree simple    → minitree addon, simple
more red                   → 5 more 🟥 heart questions
more green                 → 5 more 🟩 creative questions
```

### Modes

- **simple** or **explained** — radio, pick one
- **numbered** — checkbox, adds numbered layout on top of the chosen radio
- Combos: `simple`, `explained`, `numbered+simple`, `numbered+explained`
- **simple** — lettered options, compact, fast
- **explained** — like simple, but each question includes reasoning, context, and a recommendation with justification
- **numbered** — multiple choice with ★ recommended, formal layout

### Error handling & fallbacks

- **Missing doc-roots:** If a configured path doesn't exist, skip it silently — don't error. Warn once, continue with what exists.
- **Malformed config.md:** If config can't be parsed, fall back to SKILL.md defaults. Don't ask the user to fix it — just use defaults for that session.
- **Missing extra-files:** If an extra-file (pendings.md, conflicts.md) doesn't exist, don't create it automatically. Only create when the addon that generates it is selected.
- **No addon matched:** If `/questy {name}` doesn't match any addon/preset file, treat `{name}` as a project name and use defaults.
- **Empty doc-roots:** If no doc-roots are configured, scan the current working directory for .md files as a fallback.
- **Talk2web not installed:** Generate static HTML as fallback. Don't block the session.

### Setup

On first run, check if `~/.config/questy/config.md` exists:
- If exists → load config, skip intro
- If missing → ask user how they want to configure:

```
No questy config found. How do you want to set up?

  [1] HTML form — open flove.org/development/standards/skills/questy/ in browser
  [2] Console — numbered options, answer in chat
  [3] Modal — one question at a time, step by step
```

**Option 1: HTML form**
- Opens `https://flove.org/development/standards/skills/questy/`
- User fills form, clicks "Copy Prompt"
- Paste prompt back here, I'll create the structure

**Option 2: Console — numbered options**
- Quick Q&A in chat, batched questions
- You reply with numbers (e.g. `1, 3, 5`)
- Fastest for experienced users

**Option 3: Modal — one at a time**
- Step-by-step, one question per message
- Guided flow, good for first-timers
- More conversational

After setup, config saved to `~/.config/questy/config.md`.

### Console text mode — full flow

```
--- Questy Setup ---

Q1: Project name?
  > questy-survey

Q2: What's this about? (multiselect)
  [1] code  [2] docs  [3] mixed
  > 2

Q3: Current state?
  [1] fresh start  [2] exists, ok  [3] messy
  > 1

--- Questions Tab ---

Q4: Questions per type?
  [1] 1  [2] 2  [3] 3  [4] 5  [5] 10  [6] 20  [7] 50
  > 7

Q5: Default mode? (multiselect)
  [1] simple  [2] explained  [3] numbered
  > 1, 3

Q6: Batch size?
  [1] 1  [2] 2  [3] 3  [4] 5  [5] 10
  > 4

Q7: Session purpose? (multiselect, click twice for x2 weight)
  [1] review docs for gaps  [2] challenge decisions  [3] deep dive topic
  [4] quick sanity check  [5] set up structure  [6] generate for others
  > 1, 2, 3(x2)

--- Perspectives Tab ---

Q8: KISS types? (multiselect, click twice for x2 weight)
  [1] vision  [2] arch  [3] trust  [4] data  [5] integration
  > 1, 2, 3, 4(x2), 5

Q9: Thinking hats? (multiselect, click twice for x2 weight)
  [1] facts  [2] heart  [3] risk  [4] optimism  [5] creative  [6] make
  > 1, 3(x2), 5, 6

Q10: Extended perspectives? (multiselect, optional, click twice for x2 weight)
  Explainers: [1] why  [2] what  [3] how  [4] what-for  [5] who  [6] where  [7] when
  Formalise: [8] axiom  [9] evidence  [10] prediction  [11] proposal  [12] challenge
  Tone: [13] normal  [14] funny  [15] formal  [16] trivial
  Teleology: [17] experimental  [18] random  [19] fine  [20] fatal
  Field: [21] metaphysics  [22] science  [23] biology  [24] psychology  [25] sociology
  Time span: [26] moment  [27] day  [28] week  [29] month  [30] year  [31] decade  [32] century
  > (empty to skip)

--- Addons Tab ---

Q11: Addons? (multiselect)
  [1] index  [2] agents  [3] tree  [4] git  [5] github  [6] html
  [7] archive  [8] pro  [9] scripts
  > 2, 3, 4, 5, 7, 8

Q12: Workflows? (multiselect, only if git selected)
  [1] synced (recommended)  [2] merge rules  [3] commit guard  [4] finish line  [5] blueprint
  > 1, 2

Q12b: Git detected? (if synced selected)
  If .git exists: Files will sync to your existing repo. No .gitignore needed.
  If no .git: Would you like guidelines to set up local git? (recommended)

Q13: PR standards? (only if merge rules selected)
  Title format: [1] conventional  [2] ticket-number  [3] branch-name
  > 1
  Description: [1] basic  [2] detailed  [3] none
  > 2
  Review checklist: (multiselect)
  [1] code quality  [2] tests pass  [3] docs updated  [4] no breaking  [5] screenshot
  > 1, 2, 3
  Merge rules: [1] squash  [2] merge-commit  [3] rebase
  > 1
  Branch naming: [1] feature/ticket  [2] feature/description  [3] none
  > 1
  Commit format: [1] conventional  [2] imperative  [3] none
  > 1

Q14: Agents.md options? (multiselect)
  [1] shortcuts  [2] constraints  [3] pending-resolutions  [4] batch-overrides
  [5] export-prefs  [6] territory  [7] aliases  [8] danger-zone
  [9] decision-log  [10] archive
  > 1, 2, 3, 6, 10

Q15: Scripts? (multiselect)
  [1] build  [2] test  [3] deploy  [4] lint  [5] format  [6] typecheck
  [7] docker  [8] audit  [9] benchmark  [10] docs  [11] release  [12] deps
  > 1, 2, 4, 5

Q16: Integrations? (multiselect)
  [1] tickets  [2] board  [3] linear  [4] notify  [5] pulse
  > (empty to skip)

Q17: Output format? (multiselect)
  [1] story  [2] data dump  [3] spreadsheet  [4] notion sync  [5] obsidian vault
  > 1

Q18: HTML selected? (if HTML selected)
  HTML output works best with questy-html for live preview.
  If questy-html skill installed → offer to render.
  If not installed → link to https://flove.org/development/standards/skills/questy-html/ for setup instructions, or generate a static HTML file as fallback.

--- Done ---

Config saved to ~/.config/questy/config.md
Creating structure: docs/, plans/, standards/, agents.md, .github/, archive.md, docs/adr/, scripts/

--- Next steps ---

When a batch finishes, always prompt:

? What next?
  (c) continue — next batch
  (t) tune — more {hat} questions
  (h) html — live preview (if questy-html installed)
  (u) update — re-scan docs for new gaps, conflicts
  (s) stop — export and close

If none chosen after 3 rounds, default to `c` and continue with same settings.
```

**Note:** This is the default console text mode flow. When user selects option 2, follow this exact sequence. Skip conditional questions (Q12-Q13) if prerequisites not met. Allow empty answers for optional questions (Q10, Q16).

### Form Structure (questy)

Frontend lives at `https://flove.org/development/standards/skills/questy/`.

The HTML form is the intro. Two-tab layout:

**Addons Bar (fixed above tabs):**
- [Create] [Project name...] [Route(s)] — when Create is active, prompt starts with "Create {project}..."; when off, starts with "{project}..."
- It's about [docs] [code]
- Nowadays it's [Ok] [Messy] (hidden when Create is active)

**Questions Tab:**
- "I want X simple/explained/numbered in groups of Y" — explained adds reasoning, context, and recommendations to each question
- For: review docs, challenge decisions, deep dive, sanity check, set up, generate
- Perspectives: KISS types + Thinking Hats + See more (explainers, formalise, tone, teleology, field, time span)

**Addons Tab:**
- Core: Index, Agents.md, Tree, Git, HTML, .github/, docs/adr/, Archive
- Scripts: build, test, deploy, lint, format, typecheck, docker, audit, benchmark, docs, release, deps
- Integrations: tickets, board, linear, notify, pulse
- Workflows: synced (recommended), merge rules, commit guard, finish line, blueprint
- PR Standards (when merge rules selected)
- Output: story, data dump, spreadsheet, notion sync, obsidian vault

**Buttons:**
- "Save Config" — writes to `~/.config/questy/config.md`, creates structure, stays open
- "Copy Prompt" — autoupdates form selections, copies prompt to clipboard

### Auto-save

All inputs auto-save to localStorage (500ms debounce). On page load, restores previous state:
- Project name, doc roots, extra session/types/integrations text
- All option buttons (selected, weighted, humanized states — humanized shows plain-English descriptions alongside technical labels)
- Tab state (Questions/Addons)

### Config validation

Before copying prompt, no required fields — copy whatever is filled. Empty fields are simply omitted from the prompt.

### Preset templates

Quick-start buttons for common project types:
- **React App** — code, ok structure, index+agents+tree+git+github, synced workflow
- **Node.js API** — code, ok structure, index+agents+tree+git+github+scripts, synced workflow
- **Python Package** — code, ok structure, index+agents+tree+git+github, synced workflow
- **Minitree App** — docs+code, ok structure, index+agents+tree+git+html, synced workflow
- **CLI Tool** — code, ok structure, index+agents+tree+git+github+scripts, synced workflow
- **Documentation** — docs, ok structure, index+agents+tree+git, synced workflow

Click once to apply preset. Shows toast confirmation.

### Batch mode

The plus (+) button next to the project name field in the HTML form (`questy/index.html`) duplicates the project name and docs route fields for multiple projects:
- Each duplicate has its own project name and docs route
- Remove button (×) on each duplicate
- In copy prompt, generates "batch mode" output with all projects listed

### Config history (optional)

Config snapshots can be saved to localStorage (max 10):
- Not saved by default — enable via the ↻ history button in the bottom bar
- Each manual copy prompt or save creates a snapshot you can roll back to

### Skill integration (if available)

Copy prompt includes "skill integration" section — only include skills that are installed:
1. `/validaty` — check structure, a11y, mobile, i18n
2. `/optimizy` — polish code, vocabulary, translations
3. `/translaty` — add languages if needed
4. `/updaty-web` — publish to web

Check skill availability before including. If none are installed, skip this section.

### Config storage — `~/.config/questy/config.md`

Human-readable markdown format:

```markdown
# questy config — auto-generated

## project
- type: node | rust | python | go | docs | mixed
- name: project-name

## workflow
- active: code | docs | mixed
- state: ok | messy

## questions
- batch: 5
- mode: [simple|explained] + [numbered]
- types: vision, arch, trust, data, integration

## addons
- [ ] tree — creates docs/, plans/, standards/
- [ ] git — creates .gitignore
- [ ] agents — creates agents.md
- [ ] html — generates web output
- [ ] github — creates .github/ templates
- [ ] archive — creates archive.md
- [ ] pro — creates docs/adr/
- [ ] scripts — creates scripts/

## scripts
- [ ] build.sh — compile/bundle for production
- [ ] test.sh — run test suite with coverage
- [ ] deploy.sh — publish to target environment
- [ ] lint.sh — check code style
- [ ] format.sh — auto-fix style issues
- [ ] typecheck.sh — TypeScript type checker
- [ ] docker.sh — build/run Docker containers
- [ ] audit.sh — scan dependencies for vulnerabilities
- [ ] benchmark.sh — run performance benchmarks
- [ ] docs.sh — generate documentation
- [ ] release.sh — automate versioning and changelogs
- [ ] deps.sh — safe dependency updates

## agents.md
- shortcuts
- constraints
- pending-resolutions
- batch-overrides
- export-prefs
- territory
- aliases
- danger zone
- decision-log
- archive
```

### Local overrides — `~/.config/questy/overrides.md`

Personal overwrites of the standard skill behavior. Layers on top of `config.md`:

```markdown
# questy overrides — personal

## .gitignore
- always create .gitignore (even with synced workflow)
- add custom entries: .env, dist/, .DS_Store

## extra-doc-roots
- /custom/local/docs/

## constraints
- never modify scripts/ after initial creation
- skip integrations section entirely

## batch-defaults
- per-type: 10 when project is "messy"
```

The agent reads `overrides.md` after `config.md` and applies overwrites. The HTML form suggests override options in the addons text areas when relevant (e.g. when git is selected, a note says "need custom .gitignore rules? add them in overrides.md").

### Structure creation — after Save Config

Check which folders/files exist. Create missing ones based on config under the project's working directory:

**Folders:**
- `docs/` (if tree selected)
- `plans/` (if tree selected)
- `standards/` (if tree selected)
- `.github/` (if github selected)
- `docs/adr/` (if pro selected)
- `scripts/` (if scripts selected)

**Files:**
- `.gitignore` (if git selected)
- `agents.md` (if agents selected)
- `pendings.md` (if tree selected)
- `conflicts.md` (if tree selected) — same format as pendings.md, focused on plan-vs-plan and plan-vs-standard conflicts that generate questions
- `proposals.md` (if tree selected) — the final resume: summary of all decisions, plans, and outcomes from the questy workflow
- `archive.md` (if archive selected)

Show result: "Created: docs/, plans/, .gitignore, agents.md"

### agents.md (skill tuning file)

Per-project cheat codes the skill reads on startup:

```
# agents.md — skill tuning

## shortcuts
- skip setup questions — already configured
- default to simple mode
- prefer trust questions

## constraints
- don't touch standards/ — those are frozen
- only modify plans/ with explicit approval

## pending-resolutions
- resolve Q015 before next session
- update central-backend.md §3.2

## batch-overrides
- ask 10 vision questions but only 2 data questions

## export-prefs
- export format: markdown only
- folder: exports/

## territory
- docs: /custom/docs/path/
- plans: /custom/plans/path/

## aliases
- treat 'ux' as 'vision' automatically
- map 'security' to 'trust'

## danger zone
- identified risks: [list]
- impact: high/medium/low
- mitigation: [strategies]

## decision-log
- ADR-001: [decision]
- context: [why]
- consequences: [what happened]

## archive
- .github/ templates included
- docs/adr/ folder created
- archive mode enabled: resolved items move to archive.md
```

Skill reads this file first, adjusts behavior accordingly.

### Archive mode

When `archive` is selected in agents.md options:
- Resolved questions/proposals are moved to `archive.md` instead of being deleted
- The main files (proposals.md, pendings.md) only contain active items
- Archived items retain their ID, status, description, and resolution date
- User can toggle archive mode in the HTML survey under Addons → Agents.md → archive

### Session persistence

Questy is invoked per-message. State is maintained via files:

- **`~/.config/questy/config.md`** — project config (persists across sessions)

On session start:
1. Read `config.md` for project settings
2. If extra-files exist (pendings.md, conflicts.md from tree addon), scan them for context

On session end (or when user says `stop`):
- User manages their own files — no automatic session state is written

### Session start — 4 steps

**Step 1 — Purpose** (multiselect):
```
what do you want this session to cover? (pick all)
  [1] review docs for gaps
  [2] challenge current decisions
  [3] deep dive a specific topic
  [4] quick sanity check
  [5] set up project structure
  [6] generate questions for someone else
  [7] thinking hats — apply perspective shifts
```

Based on selections, adjust:
- [1] full scan, all types
- [2] focus on conflicts + trust + arch
- [3] filter to chosen type, increase batch
- [4] 2 per type, fast mode
- [5] run setup flow only
- [6] numbered mode, export-friendly output
- [7] show hat selection (step 1b)

**Step 1b — Thinking hats** (only if [7] selected, multiselect):
```
which thinking hats? (pick all)
  [1] ⬜ white — facts, data, specs
  [2] 🟥 red — heart, feeling, trust
  [3] ⬛ black — risk, threats, failure
  [4] 🟨 yellow — optimism, value, benefit
  [5] 🟩 green — creative, alternatives
  [6] 🟦 blue — process, connection, flow
```

**Step 2 — Volume**:
```
how many questions?
  per type: [1] 2  [2] 5  [3] 10  [4] 20
  batch size: [1] 3  [2] 5  [3] 10
  types: [1] all  [2] vision only  [3] arch only  [4] trust only  [5] data only  [6] integration only  [7] pick...
```

**Step 3 — Additional details** (optional, text):
```
anything specific to focus on? (optional — e.g. "focus on auth module", "skip frontend", "prioritize security")
```

After first session, skip these steps on resume — go straight to "what changed since last time?"

### Resume flow

On resume, ask one question:
```
what changed since last time?
```
Then read only the `doc-roots` and `extra-files` that matter. Map decided topics, conflicts, gaps, pendings. Skip already-answered questions.

### Addons flow

When addons are selected:
- Index → generates README.md or INDEX.md
- Agents.md → creates agents.md with selected options
- Tree → creates docs/, plans/, standards/ folders
- Git → detects local git repo, syncs files (no .gitignore if synced workflow selected — override in overrides.md)
- HTML → generates web-viewable output, mentions questy-html skill for live preview (if installed)
- .github/ → adds issue/PR templates and workflows
- Archive → creates archive.md for resolved items (shows info when checked)
- Pro → adds docs/adr/ folder for ADR templates (shows info when checked)
- Scripts → adds scripts/ folder with helper scripts (shows info when checked)

### Scripts included

When Scripts addon is selected, creates:
- `scripts/build.sh` — compile/bundle project for production
- `scripts/test.sh` — run test suite with coverage
- `scripts/deploy.sh` — publish to target environment
- `scripts/lint.sh` — check code style and formatting
- `scripts/format.sh` — auto-fix style issues
- `scripts/typecheck.sh` — run TypeScript/type checker
- `scripts/docker.sh` — build and run Docker containers
- `scripts/audit.sh` — scan dependencies for vulnerabilities
- `scripts/benchmark.sh` — run performance benchmarks
- `scripts/docs.sh` — generate documentation from source
- `scripts/release.sh` — automate versioning and changelogs
- `scripts/deps.sh` — safe dependency updates

### Workflows

When workflows are selected:
- synced → sync newly created files to existing git repo — recommended
- merge rules → defines PR title format, description template, review checklist, merge strategy
- commit guard → runs linting, formatting, tests before commit
- finish line → checklist for task completion
- blueprint → iteration planning structure

### PR Standards

When merge rules workflow is selected, configure:
- title format: conventional / ticket number / branch name
- description template: basic / detailed / none
- review checklist: code quality, tests pass, docs updated, no breaking, screenshot
- merge rules: squash / merge commit / rebase
- branch naming: feature/ticket / feature/description / none
- commit format: conventional / imperative / none

### Flow

1. **Scan** — if resuming, ask "what changed since last time?" then read only `doc-roots` and `extra-files` that matter. First run: full scan. Map decided topics, conflicts, gaps, pendings.
2. **Conflicts first** — present any plan-vs-plan, plan-vs-standard, scope creep, dependency mismatches.
3. **Generate** — by type, default 5 per type. Order: ⬛ > 🟩 > 🟦 > 🟨 > 🟥 > ⬜. Self-check each question against existing docs before presenting — skip if already answered. Optionally attach a hat to each question for perspective shift.
4. **Present** — numbered or simple mode. Batches of 3. Global numbering: Q001, Q002, Q003 per batch, continuing across batches. User replies with global numbers (e.g. `1,4,7` = Q001+Q004+Q007 from different batches). ★ marks recommended when there's a clear best answer; otherwise present options neutrally.
5. **Process answers** — conflict check, dedup, route skipped → pendings, track IDs.
6. **Continue** — after each batch, prompt explicitly: `(c)ontinue / (t)une {hat} / (h)tml / (u)pdate / (s)top`. Lock to one session — no concurrent sessions. If none chosen after 3 rounds, default to `c`. On `update`, see the minitree use case steps 10–12 for the full 3-step delta cycle (inventory, diff, re-evaluate + generate).
7. **Suggest questy-html** — at survey start, if questy-html skill is installed, offer to render Q&A as interactive HTML form. If not installed, link to https://flove.org/development/standards/skills/questy-html/ or generate static HTML as fallback.
8. **Export** — at session end, offer export: markdown, JSON, or HTML.
9. **Proposals** — generate or update `proposals.md` with the final resume: all decisions made, plans confirmed, open items, and next steps. This is the simplified product of the questy session.

#### Numbered mode

```
[Q001] [arch] [🟦 make] What is the boundary between component A and B?

  ○ A handles everything, B is passive
  ○ A is trust-only, B is everything else
  ★ A = on-demand, B = published + sync hub
  ○ They're equal partners with no clear boundary

  Ref: plans/architecture.md §3.2
  Affects: sync design, API contract, deployment split
```

★ = recommended

`Ref:` = which doc section triggered this question (traceability).
`Affects:` = what other areas this decision impacts (scope awareness).
Both are optional — include when agent has enough doc context.

#### Simple mode

Batches of 3, global numbering continues across batches.
User replies with any numbers from all batches seen so far.

Batch 1:
```
vision (3/15)
────────────────
Q001 who is the primary user?
  a) me only  b) any developer  c) both, optimized for me ★

Q002 success metric — fewer questions or better?
  a) fewer  b) better  c) both equally ★

Q003 should the skill learn from past sessions?
  a) learn  b) stateless  c) hybrid ★

> c, c, c
```

Batch 2:
```
arch (3/15)
───────────────
Q004 large project scan — always full, or ask first?
  a) always full scan  b) ask first ★  c) incremental

Q005 session logs — markdown, JSON, or both?
  a) markdown  b) JSON  c) both ★

Q006 always recommend ★, or sometimes neutral?
  a) always  b) sometimes neutral ★  c) user configures

> b, a, b
```

Batch 3:
```
trust (3/15)
───────────────
Q007 wrong doc-roots paths — what happens?
  a) suggest fix ★  b) create them  c) suggest + create

Q008 overlapping sessions — duplicate questions?
  a) track IDs  b) lock to one session ★  c) warn

Q009 bad questions generated — who catches?
  a) user skips  b) self-check docs ★  c) both

> a, b, b
```

After 3 batches (9 questions), user can reply with any combination:
`1,4,7` = Q001+Q004+Q007 | `2,5,8,9` = Q002+Q005+Q008+Q009 | etc.

#### Explained mode

Like simple, but each option gets a longer phrase and a recommendation with reasoning:

```
vision (3/15)
────────────────
Q001 who is the primary user?
  a) me only — solo workflow, no sharing needed
  b) any developer — public tool, broad audience
  c) both, optimized for me ★ — personal first, others welcome

  Recommendation: c — you're the primary user, but designing for
  others forces cleaner interfaces. Keeps it flexible.

Q002 success metric — fewer questions or better?
  a) fewer — speed matters most
  b) better — depth matters most
  c) both equally ★ — balanced approach

  Recommendation: c — fewer questions without quality loses value.
  Better questions without pace loses engagement. Balance wins.

> c, c, c
```

### Rules

- Never delete decisions — only add or mark resolved
- When archive mode is enabled: move resolved items to archive.md
- When archive mode is disabled: mark resolved in-place (never delete unless user explicitly says so)
- New decisions: append to plan with ID, cross-ref question
- Skipped → pendings. >1 session pending → escalate
- Never re-ask a question with an answer in existing docs
- Global numbering: Q001+ across entire session, never reset
