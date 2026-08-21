---
name: questy
description: >-
  General-purpose structured Q&A skill for the accurate planning of projects.   
  Use when you want to "question
  the project", "find what's missing", or run a structured review before coding.
  
  Reads project
  docs, detects conflicts and gaps,
  agenerates typed questions in batches using
  the **Thinking Hats** (6 thinking modes) as the main type — facts · heart ·
  risk · optimism · creative · make.   Command: /questy [addon]
  [numbered|simple|explained] [in N] [hat]. At end flags
  conflicts,  routes skipped items to pendings, updates docs with answers, and generates a new set of questions based on those. 
  

   Override via the personal config (see CONFIG.md).
---

# questy — structured project Q&A

Turn the table: make the agent receive better input with less effort.

```
standards/  →  plans/  →  questions  →  pendings
   (why)        (how)      (what's missing)  (unclassified)
```

## Personal config

To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see example: `flove.org/development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.


now also carries the new categories beside questions-per-type — with the tones
and focus group added:
- **tone(s)** — how each question reads: `none` · Simple · Extended · Human
- **focus** — how deep the answer digs: `none` · Superficial · Deep · Ultradetailed

## Intro

The core of questy is building questions — turning what you know (standards,
plans, docs) into what you haven't thought about yet (gaps, conflicts, blind
spots). Every session starts by scanning your project's docs, then composing
insightful questions that probe what matters.

Its default presents batches of 5 mixed-colour questions — every question
wears one of the six Thinking Hats (⚪ facts · ❤ heart · ⬛ risk · 🟡 optimism ·
🟢 creative · 🔵 make), and each batch mixes hats, ordered abstract→concrete
within each hat group. Each question gets three options (A/B/C) with a ★
recommended pick when there's a clear best answer, or labelled "Neutral" when
there isn't. User answers compactly: `1a 2b 3c...` or `0` for all recommended.
Further customize by selecting Hats intensities and other perspectives (KISS
and Wisy) that fit your project's needs.

For a richer workflow that sets up the full file structure (standards/,
plans/, questy-docs/, pendings, conflicts, proposals) and syncs everything to git,
use the **questy1** recommended bundle —
[questy1/SKILL.md](https://flove.org/development/standards/skills/questy1/SKILL.md).


```
fallback: https://flove.org/development/standards/skills/questy/SKILL.md
```

When a session wraps, offer a **narraty recap**, follow the
[`/narraty`](https://flove.org/development/standards/skills/narraty/SKILL.md)
skill to produce a ~1-minute spoken audio that resumes and details the workflow
just created — the choices made in the form, the questions answered, and what
remains pending (point it at `answers.md` + `questy-pending.md`). The key information is the updating documents process and generating the new set of questions out of it. Narration
voices the review; the markdown stays the source of truth.

Also offer an **HTML form** for the session via
[`/questy-html`](https://flove.org/development/standards/skills/questy-html/SKILL.md):
render the questions and answers as an interactive form users open in a
browser — useful to click through the batches again with a live preview, review
the pending items, and export to markdown without re-running the session.

See a demo of an HTML questy Survey ([questy/index.html](https://flove.org/development/standards/skills/questy/))

For a comprehensive 100-step walkthrough covering all perspectives, addons, workflows, and integrations across both HTML form and console prompt tracks, see the [advanced use case](../../debates/UseCase-adv.md).

### Use case: `browsy` (default, no addon)

Questy run on a generic project without any addon selected:

**Step 1** — Check `~/.config/questy/config.md`
- If exists → load it, skip setup
- If missing → offer setup options (HTML form / console / modal / voice)

**Step 2** — Project set
- Name: browsy

**Step 3** — Ask which Thinking Hats to wear (multiselect) + See more 
- The six Hats are the session type: white facts, red heart, black risk, yellow optimism, green creative, blue make, see more
- See more opens the KISS and Wisy perspectives (explainers, formalise, tone, teleology, field, time span) — optional, weight by clicking twice

**Step 4** — Ask volume and preferences
- Questions per type (default 5), batch size (default 5, mixed-colour batches)
- tone(s) and focus knobs from the survey (none · Simple · Extended · Human , Funny / Deep, Hard, Concise)
- Ask for additional session info / free-text preferences

**Step 5** — Scan and understand context
- Read every .md in doc-roots and extra-files, map decisions, architecture, gaps
- Assess what the project has vs what's missing: coverage per hat
- Detect plan-vs-plan and plan-vs-standard conflicts, scope creep, dependency mismatches
- Prioritise areas with least coverage

**Step 6** — Select what to generate
- Filter out already-answered questions (cross-ref session history, never re-ask)
- Choose hats by what the project needs: plans light → more 🟩 creative, weak threat model → more ⬛-focused answers, unclear vision → more 🟡 optimism, no data → more ⬜ facts
- Apply each chosen hat to every area it strengthens (one hat per question, single decision per question)
- Override hat mix based on scan findings (e.g. high-risk project → force ⬛ risk on all areas)
- Weight deeper by coverage deficit: low-coverage areas get more questions and higher priority
- Order by impact: ⬛ risk > 🟩 creative > 🟦 make > 🟨 optimism > 🟥 heart > ⬜ facts
- Set batch composition: spread hats across the batch, keep one hat coherent per question

**Step 7** — Generate and present batch
- Compose questions per selection plan: 5 per hat, chosen hats, mixed-colour batch (global Q001, Q002…)
- Self-check each against existing docs before generating — skip if already answered
- Include Ref (source doc section) and Affects (impact scope)
- Each question gets A/B/C options with ★ recommended (best answer) or Neutral (no clear best)
- User answers compactly: `1a 2b 3c 4b 5c` or `0` for all recommended

**Step 8** — Process answers
- Route skipped → pendings (in-memory, if file tree addons missing)
- Detect new conflicts, track IDs

**Step 9** — Update: trigger and inventory
- User says `update` → pause current batch, save unanswered to pending queue
- Re-read all doc-root files, compare against last scan (new/deleted/changed files)
- Record current session state (answered Q IDs, skipped Q IDs) for delta computation

**Step 10** — Update: delta report
- For each changed file: extract new sections, removed sections, modified decisions
- Detect new conflicts (plan-vs-plan, plan-vs-standard) and scope creep
- Cross-ref questy-pending.md: are any previously-skipped questions now answerable?
- Show delta summary, present new questions as next batch

**Step 11** — Continue prompt
- Prompt: `(c)ontinue / (t)une {hat} / (u)pdate / (s)top`
- `c` → next batch with same settings (mixed-colour batch of 5)
- `t` / `more {hat}` → 5 more with that hat
- `u` / `update` → re-scan docs for new gaps (see questy1 minitree steps)
- `s` / `stop` → end session, offer export (markdown / JSON / HTML) and questy-html if installed

## Project and Batch

Configure what project you're working on and how the session runs.

**Project context:** name, docs route(s), create-new (start blank) or add multiple projects

**Batch mode:** use the + button in the HTML form to ask questions across multiple projects at once — each duplicate gets its own name and docs route, the prompt generates batch output with all projects listed.

**Session volume:** questions-per-type (up to 50), batch-size (how many per round, default 5), modes (simple / explained, mixed-colour batches, compact answers)



```
/questy simple in 4   → simple mode, 4 per batch
/questy in 10         → explained mode, 10 per batch
```

## Perspectives

### Other Types 

Multiselect — a question wears one or two hats at most.

The KISS catalogue d
`vision`/`arch`/`trust`/`data`/`integration` . Analogies with hats:
 (`more vision` → 🟨, `more trust` → ⬛,
`more make` → 🟦) 

In modal one-at-a-time console mode, present hats as titles only and names of
the six hats: on screen show, they count as the question's `type`.

### Rainbow Hats (the type)

Applied per-question — a question wears its hat; the hat is the type.

```
⬜ white, facts    — what do we know? data? specs? what's missing?
🟥 red, heart     — how does it feel? user fear? gut reaction? trust?
⬛ black, risk    — what could go wrong? threats? failure modes? blast radius?
🟨 yellow, optimism — benefits? value? why build this? user gain?
🟩 green, creative — alternatives? wild ideas? flipped perspective?
🟦 blue, make     — flow? connection? contract? how A talks to B?
```

Convenience area↔hat
starter (override in agents.md):
```
docs→🟨, design→🟩, threats→⬛, strategy→🟨, ux→🟥, integration→🟦, data→⬜
```

### See more — Wisy perspectives

Extended lenses that add nuance beyond the core types and hats. Each one opens a different axis of questioning.

Applied the same way as hats — say `why`, `formal`, `experimental`, `science` to activate that lens, or set them in the HTML form under Perspectives → See more. Talking nonformally works: `make it weird` → experimental teleology, `get scientific` → science field.

**Explainers** — frame the kind of answer expected:
`why`, `what`, `how`, `what-for`, `who`, `where`, `when`
- tuning: pick ONE explainer to fix the question's angle (`why` → causes,
  `what-for` → outcome); empty → answer from the hat's default voice

**Formalise** — structure the answer format:
`axiom`, `evidence`, `prediction`, `proposal`, `challenge`
- tuning: `axiom`/`evidence` for settled decisions, `prediction` for risk
  spikes, `challenge` to force a kritik against the current choice


**Teleology** — purpose orientation:
`experimental`, `random`, `fine`, `fatal`
- tuning: `experimental` opens the space (brainstorm questions), `fatal` closes it
  (what kills the project?), `fine` for the as-is default

**Field** — domain context:
`metaphysics`, `science`, `biology`, `psychology`, `sociology`
- tuning: borrow a field's analogies to reframe — `biology` → growth/lifecycles,
  `psychology` → the human behind the interface, `sociology` → teams and
  adoption

**Time span** — temporal scope:
`moment`, `day`, `week`, `month`, `year`, `decade`, `century`
- tuning: tighten to `moment` for immediate effects, stretch to `year`/`decade`
  for architecture bets and migration paths

Each lens can be weighted (click twice in the form for x2) and combined freely.

## Skills addons

Addons bundle project settings, paths, preferred choices, and constraints into a single command. They let you skip the config form and jump straight to questioning.

Addons can be applied:
- **Via the HTML form** — click preset template buttons in the Addons tab, all settings are filled at once
- **Via chat** — just say the addon name or a shortcut (e.g. "questy1", "minitree", "tree+git") and the agent fills the rest

Talking nonformally works too — say `more green` for creative-hat questions, or `make it a minitree project` to load the minitree addon. The agent recognises intent.

### Recommended: minitree → questy1

The full minitree workflow — the file structure, the files it depends on, the
config it loads — lives in the **questy1** bundle:
[questy1/SKILL.md](https://flove.org/development/standards/skills/questy1/SKILL.md).
Run `/questy minitree` here when the advanced protocol needs the same files.

### Other addons

Each addon is a small contract the agent fulfils on the user's machine — a
folder, a file, or a rule. **(1)** marks the ones the setup pre-checks (the
questy1 stack). Descriptions tell the agent exactly what to create so the
feature works in any local setup.

| Addon | (1) | What it does — how the agent implements it |
|-------|-----|----------------------------------------------|
| `tree` | **(1)** | creates `questy-docs/`, `plans/`, `standards/`, `questy-pending.md`, `conflicts.md`, `proposals.md`. Agent: create any missing folder/file under the project root; keep `standards/` frozen, `plans/` active, `questy-docs/` as reference. |
| `index` | **(1)** | generates README.md or INDEX.md mapping the folder structure and each file's purpose. Agent: scan the tree and write one line per folder/file; when the project ships docs, prefer the `wiki` output so index + docs live together (as does flove.org/development). |
| `agents` | **(1)** | creates `agents.md` with the selected options (shortcuts, constraints, pending-resolutions, territory…). Agent: fill from the agents.md section below; the file is read on every session start. |
| `git` | **(1)** | detects the local repo, adds `.gitignore` (unless `synced` is on), syncs new files. Agent: run `git status`, create `.gitignore`, stage created files. |
| `html` | | web output with questy-html live preview — <https://flove.org/development/standards/skills/questy-html/>. Agent: build the interactive questy-html form page from the survey. |
| `.github/` | | issue/PR templates + workflows. Agent: create `.github/` with issue template, PR template, and a workflow file. |
| `archive` | **(1)** | creates `archive.md`; resolved items move there, main files stay clean. Agent: move resolved questions out of `questy-pending.md`/`proposals.md` into `archive.md`, keeping their ID, status, and resolution date. |
| `pro` | | creates `questy-docs/adr/` with ADR templates. Agent: add an ADR record template (context, decision, consequences). |
| `scripts` | **(1)** | creates `scripts/` with the chosen helpers — **build, test, lint, format** are the recommended minimal skeleton. Agent: write one small `.sh` per selected helper (see Scripts included). |
| `synced` | ✓ | syncs newly created files to the existing git repo (no `.gitignore`). Agent: `git add` + `git commit` after each creation. |
| `merge rules` | | defines PR title format, description template, review checklist, merge strategy. Agent: write the PR standards below into the repo docs. |
| `commit guard` | | runs lint, format, tests before every commit. Agent: wire a pre-commit hook or CI check. |
| `finish line` | | task completion checklist. Agent: add a definition-of-done checklist to the project. |
| `blueprint` | | iteration planning structure. Agent: create a planning doc (goals, tasks, velocity). |

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
/questy simple blue        → simple, only 🟦 make questions
/questy minitree           → recommended minitree addon, numbered
/questy minitree simple    → minitree addon, simple
more red                   → 5 more 🟥 heart questions
more green                 → 5 more 🟩 creative questions
```

### Modes

Two knobs shape the questions — **tone** (how each question reads) and **focus** (how deep the answer digs). Both are multiselect; pick one or several per session.

**Tone** — the voice of the question:
- **simple** — A/B/C options, mixed-colour batch, abstract→concrete, compact
- **explained** — like simple, but each option gets a one-line reason and the ★ pick includes justification
- **human** — warm, natural voice; questions read like a colleague asking, not a form — e.g. "what would you say if a friend asked you to explain this project?"
- **funny** — light, playful tone; humor lowers the barrier so the user answers more openly — use sparingly, keep it professional, never mocking

**Focus** — how hard the question presses:
- **easy** — gentle pace, plain questions; a soft warm-up that doesn't demand deep thought
- **deep** — drill into roots, nuance; each question pushes past the first answer, chasing cause, trade-offs, and second-order effects
- **hard** — unforgiving, demanding; direct pointed questions that force commitment — the opposite of easy, for gut-checks and high-stakes decisions
- **concise** — short, to the point; minimal wording, no filler, quick to read and answer

### Error handling & fallbacks

- **Missing doc-roots:** If a configured path doesn't exist, skip it silently — don't error. Warn once, continue with what exists.
- **Malformed config.md:** If config can't be parsed, fall back to SKILL.md defaults. Don't ask the user to fix it — just use defaults for that session.
- **Missing extra-files:** If an extra-file (questy-pending.md, conflicts.md) doesn't exist, don't create it automatically. Only create when the addon that generates it is selected.
- **No addon matched:** If `/questy {name}` doesn't match any addon/preset file, treat `{name}` as a project name and use defaults.
- **Empty doc-roots:** If no doc-roots are configured, scan the current working directory for .md files as a fallback.

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

Q3: Current state?
  [1] fresh start  [2] exists, ok
  > 1

--- Perspectives Tab ---

Q4: Questions per type?
  [1] 1  [2] 2  [3] 3  [4] 5  [5] 10  [6] 20  [7] 50
  > 7

Q5: Default mode? (multiselect — numbered always on)
  [1] simple  [2] explained  
  
  
Q6: Questions per time (Batch size)?
  [1] 1  [2] 2  [3] 3  [4] 5  [5] 10
  > 4

Q7: Which Thinking Hats to wear? (multiselect, add twice for x2 weight)
  The six hats are the session type — what to cover == which hats to wear.
  [1] facts  [2] heart  [3] risk  [4] optimism  [5] creative  [6] make
  > 1, 3, 3, 5, 6

--- Perspectives Tab ---

Q8: Extended perspectives? (multiselect, optional, click twice for x2 weight)
  Explainers: [1] why  [2] what  [3] how  [4] what-for  [5] who  [6] where  [7] when
  Formalise: [8] axiom  [9] evidence  [10] prediction  [11] proposal  [12] challenge
  Tone: [13] normal  [14] funny  [15] formal  [16] trivial
  Teleology: [17] experimental  [18] random  [19] fine  [20] fatal
  Field: [21] metaphysics  [22] science  [23] biology  [24] psychology  [25] sociology
  Time span: [26] moment  [27] day  [28] week  [29] month  [30] year  [31] decade  [32] century
  > (empty to skip)

--- Set up Tab ---

Q9: Addons? (multiselect — 0 pre-checks the whole questy1 pack; reply "none" to skip every addon question below)
  [0] Questy1 pack (Recommended)  [1] index  [2] agents  [3] tree  [4] git  [5] github  [6] html
  [7] archive  [8] pro  [9] scripts
  > 0
  (Questy1 pack pre-checks: tree, index, agents, git, archive, scripts — with build, test, lint, format.
   Skip to Q12 below for the remaining setup.)

  Alternatives: > 2, 3, 4, 5, 7, 8   (pick any subset, e.g. agents, tree, git, github, archive, pro)
                > none               (No addons for now — skip Q10–Q13, jump to Q14 below)

Q10: Workflows? (multiselect, only if git selected)
  [1] synced (recommended)  [2] merge rules  [3] commit guard  [4] finish line  [5] blueprint
  > 1, 2

Q10b: Git detected? (if synced selected)
  If .git exists: Files will sync to your existing repo. No .gitignore needed.
  If no .git: Would you like guidelines to set up local git? (recommended)

Q11: PR standards? (only if merge rules selected)
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

Q12: Agents.md options? (multiselect)
  [1] shortcuts  [2] constraints  [3] pending-resolutions  [4] batch-overrides
  [5] export-prefs  [6] territory  [7] aliases  [8] danger-zone
  [9] decision-log  [10] archive
  > 1, 2, 3, 6, 10

Q13: Scripts? (multiselect)
  [1] build  [2] test  [3] deploy  [4] lint  [5] format  [6] typecheck
  [7] docker  [8] audit  [9] benchmark  [10] docs  [11] release  [12] deps
  > 1, 2, 4, 5

Q14: Integrations? (multiselect)
  [1] tickets  [2] board  [3] linear  [4] notify  [5] pulse
  > (empty to skip)

Q15: Output format? (multiselect)
  [1] story  [2] data dump  [3] spreadsheet  [4] notion sync  [5] obsidian vault
  > 1

Q16: HTML selected? (if HTML selected)
  HTML output works best with questy-html for live preview.
  If questy-html skill installed → offer to render.
  If not installed → link to https://flove.org/development/standards/skills/questy-html/ for setup steps, or open a static HTML file as fallback.

--- Done ---

Config saved to ~/.config/questy/config.md
Creating structure: questy-docs/, plans/, standards/, agents.md, .github/, archive.md, questy-docs/adr/, scripts/

--- Next steps ---

When a batch finishes, always prompt:

? What next?
  (c) continue — next batch
  (t) tune — more {hat} questions
  (u) update — re-scan docs for new gaps, conflicts and create new set of questions
  (s) stop — export and close

If none chosen after 3 rounds, default to `c` and continue with same settings.
```

**Note:** This is the default console text mode flow. When user selects option 2, follow this exact sequence. Skip conditional questions (Q10-Q11) if prerequisites not met. Allow empty answers for optional questions (Q8, Q14).

### Form Structure (questy)

Frontend lives at `https://flove.org/development/standards/skills/questy/`.

The HTML form is the intro. First section shows Project | Survey side by side (expanded by default), then two tabs:

**Project column:**
- [Create] [Project name...] [Route(s)] — when Create is active, prompt starts with "Create {project}..."; when off, starts with "{project}..." (Create is the same as the old "It's about/Messy" choice — a fresh structure vs an existing one)
- + button duplicates the name + route rows for batch/multi-project surveys

**Survey column:**
- questions per type (up to 100, default 50), batch-size, plus the **tones**
  (none · Simple · Extended · Human) and **focus** (none · Superficial · Deep ·
  Ultradetailed) knobs

**Perspectives Tab:**
- "Additional information" free-text
- Thinking Hats + See more (explainers, formalise, tone, teleology, field, time span)
- **AI suggestions** subsection (bottom of Perspectives): for (review docs, challenge decisions, deep dive, sanity check, more perspectives, set up, generate) and Thinking Hats (facts, heart, risk, optimism, creative, make) — each click once for normal, twice for x2 weight

**Settings Tab:**
- Core: Index, Agents.md, Tree, Git, HTML, .github/, questy-docs/adr/, Archive
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
- Tab state (Focus/Set up)

### Config validation

Before copying prompt, no required fields — copy whatever is filled. Empty fields are simply omitted from the prompt.

### Preset templates

Quick-start buttons for common project types:
- **React App** — code, ok structure, index+agents+tree+git+github, synced workflow
- **Node.js API** — code, ok structure, index+agents+tree+git+github+scripts, synced workflow
- **Python Package** — code, ok structure, index+agents+tree+git+github, synced workflow
- **Minitree App** — docs & code, ok structure, index+agents+tree+git+html, synced workflow
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
- name: project-name


## questions
- batch: 5
- mode: [simple|explained|extended|human] 
- types (Thinking Hats): facts, heart, risk, optimism, creative, make

## addons
- [ ] Recommended — creates questy-docs/, plans/, standards/
- [ ] git — creates .gitignore
- [ ] agents — creates agents.md
- [ ] html — generates web output
- [ ] github — creates .github/ templates
- [ ] archive — creates archive.md
- [ ] pro — creates questy-docs/adr/
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
- per-type: 10 when project is large
```

The agent reads `overrides.md` after `config.md` and applies overwrites. The HTML form suggests override options in the addons text areas when relevant (e.g. when git is selected, a note says "need custom .gitignore rules? add them in overrides.md").

### Structure creation — after Save Config

Check which folders/files exist. Create missing ones based on config under the project's working directory:

**Folders:**
- `questy-docs/` (if tree selected)
- `plans/` (if tree selected)
- `standards/` (if tree selected)
- `.github/` (if github selected)
- `questy-docs/adr/` (if pro selected)
- `scripts/` (if scripts selected)

**Files:**
- `.gitignore` (if git selected)
- `agents.md` (if agents selected)
- `questy-pending.md` (if tree selected)
- `conflicts.md` (if tree selected) — same format as questy-pending.md, focused on plan-vs-plan and plan-vs-standard conflicts that generate questions
- `proposals.md` (if tree selected) — the final resume: summary of all decisions, plans, and outcomes from the questy workflow
- `archive.md` (if archive selected)

Show result: "Created: questy-docs/, plans/, .gitignore, agents.md"

### agents.md (skill tuning file)

Per-project cheat codes the skill reads on startup:

```
# agents.md — skill tuning

## shortcuts
- skip setup questions — already configured
- default to simple mode
- prefer risk questions

## constraints
- don't touch standards/ — those are frozen
- only modify plans/ with explicit approval

## pending-resolutions
- resolve Q015 before next session
- update central-backend.md §3.2

## batch-overrides
- ask 10 questions on facts and risk, only 2 on optimism

## export-prefs
- export format: markdown only
- folder: exports/

## territory
- docs: /custom/docs/path/
- plans: /custom/plans/path/

## aliases
- treat 'ux' as 'heart' automatically
- map 'security' to 'risk'

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
- questy-docs/adr/ folder created
- archive mode enabled: resolved items move to archive.md
```

Skill reads this file first, adjusts behavior accordingly.

### Archive mode

When `archive` is selected in agents.md options:
- Resolved questions/proposals are moved to `archive.md` instead of being deleted
- The main files (proposals.md, questy-pending.md) only contain active items
- Archived items retain their ID, status, description, and resolution date
- User can toggle archive mode in the HTML survey under Addons → Agents.md → archive

### Session persistence

Questy is invoked per-message. State is maintained via files:

- **`~/.config/questy/config.md`** — project config (persists across sessions)

On session start:
1. Read `config.md` for project settings
2. If extra-files exist (questy-pending.md, conflicts.md from tree addon), scan them for context

On session end (or when user says `stop`):
- User manages their own files — no automatic session state is written

### Session start — 4 steps

**Step 1 — Thinking Hats** (multiselect — the session type, no purpose picker):
```
which thinking hats? (pick all — what to cover == which hats)
  [1] ⚪ facts — data, specs, what's missing
  [2] ❤ heart — feeling, trust, gut reaction
  [3] ⬛ risk — threats, failure modes, blast radius
  [4] 🟡 optimism — value, benefits, why build
  [5] 🟢 creative — alternatives, wild ideas
  [6] 🔵 make — flow, connection, contracts
```

**Step 1b — See more** (optional, multiselect): Wisy perspectives — explainers
(`why`/`what`/`how`/`what-for`/`who`/`where`/`when`), formalise, tone, teleology,
field, time span. Weight by clicking twice.

**Step 2 — Volume**:
```
how many questions?
  per hat: [1] 2  [2] 5  [3] 10  [4] 20
  batch size: [1] 3  [2] 5 (default)  [3] 10
  hats: [1] all  [2] facts only  [3] heart only  [4] risk only  [5] optimism only  [6] creative only  [7] make only  [8] pick...
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
- Tree → creates questy-docs/, plans/, standards/ folders
- Git → detects local git repo, syncs files (no .gitignore if synced workflow selected — override in overrides.md)
- HTML → generates web-viewable output, mentions questy-html skill for live preview (if installed)
- .github/ → adds issue/PR templates and workflows
- Archive → creates archive.md for resolved items (shows info when checked)
- Pro → adds questy-docs/adr/ folder for ADR templates (shows info when checked)
- Scripts → adds scripts/ folder with helper scripts (shows info when checked)

### Scripts included

When Scripts addon is selected, creates one small `.sh` helper per chosen
option. Each is a thin wrapper the agent writes locally so the user's workflow
stays reproducible — same command, same result, on any machine. **(1)** marks the
recommended minimal skeleton (build, test, lint, format).

- **(1)** `scripts/build.sh` — compile/bundle project for production. Agent: wrap the project's own build command (esbuild, webpack, tsc…) and output to `dist/`.
- **(1)** `scripts/test.sh` — run test suite with coverage. Agent: run the project's test runner; fail the script if coverage drops below threshold; print a short report.
- `scripts/deploy.sh` — publish to target environment. Agent: detect the platform (Vercel, GitHub Pages, SSH, Docker) and call its publish command — see flove's own [publish-web.sh](https://flove.org/development/standards/skills/updaty-web/SKILL.md) reference.
- **(1)** `scripts/lint.sh` — check code style and formatting. Agent: run the project's linter, auto-fix what it can, report the rest with non-zero exit on errors.
- **(1)** `scripts/format.sh` — auto-fix style issues. Agent: run the formatter (prettier, black, gofmt…) and verify the tree is clean.
- `scripts/typecheck.sh` — run TypeScript/type checker. Agent: run `tsc --noEmit` or the language's type gate; fail on type errors.
- `scripts/docker.sh` — build and run Docker containers. Agent: wrap `docker build` + `docker run`, handle multi-stage builds and tagging.
- `scripts/audit.sh` — scan dependencies for vulnerabilities. Agent: call the package manager's audit command and block on critical findings.
- `scripts/benchmark.sh` — run performance benchmarks. Agent: run the project's bench harness and compare against a stored baseline.
- `scripts/docs.sh` — generate documentation from source. Agent: run the doc generator (docsify, jsdoc, sphinx…) — the wiki addon's docsify site (https://flove.org/development/standards/index) is the flove reference.
- `scripts/release.sh` — automate versioning and changelogs. Agent: bump semver, generate the changelog, create the git tag — see [upgrady](https://flove.org/development/standards/skills/upgrady-solo/SKILL.md).
- `scripts/deps.sh` — safe dependency updates. Agent: update deps, check for breaking changes, run tests; revert on failure.

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
3. **Generate** — by hat (the type), default 5 per hat. Order: ⬛ > 🟩 > 🟦 > 🟨 > 🟥 > ⬜. Self-check each question against existing docs before presenting — skip if already answered. Each question wears its hat (one hat = one question).
4. **Present** — mixed-colour batches of 5, ordered abstract→concrete within each hat group. Each question gets A/B/C options with ★ recommended (best answer) or Neutral (no clear best). User answers compactly: `1a 2b 3c 4b 5c` or `0` for all recommended. Pre-answer with the recommended picks when user sends `0`.
5. **Process answers** — conflict check, dedup, route skipped → pendings, track IDs.
6. **Continue** — after each batch, prompt explicitly: `(c)ontinue / (t)une {hat} / (h)tml / (u)pdate / (s)top`. Lock to one session — no concurrent sessions. If none chosen after 3 rounds, default to `c`. On `update`, use the full delta cycle from the questy1 minitree steps.
7. **Suggest questy-html** — at survey start, if questy-html skill is installed, offer to render Q&A as interactive HTML form. If not installed, link to https://flove.org/development/standards/skills/questy-html/ or generate static HTML as fallback.
8. **Export** — at session end, offer export: markdown, JSON, or HTML.
9. **Proposals** — generate or update `proposals.md` with the final resume: all decisions made, plans confirmed, open items, and next steps. This is the simplified product of the questy session.

#### Numbered mode

```
[Q001] [🟦 make] What is the boundary between component A and B?

  A) A handles everything, B is passive
  B) A is trust-only, B is everything else
  ★ C) A = on-demand, B = published + sync hub
  D) They're equal partners with no clear boundary

  Ref: plans/architecture.md §3.2
  Affects: sync design, API contract, deployment split
```

★ = recommended

`Ref:` = which doc section triggered this question (traceability).
`Affects:` = what other areas this decision impacts (scope awareness).
Both are optional — include when agent has enough doc context.

#### Simple mode

Batches of 5, mixed hats, ordered abstract→concrete within each hat group.
User answers with letter picks per question or `0` for all recommended.

Batch 1:
```
⬜ facts · ⬛ risk · 🟨 optimism · 🟦 make · 🟩 creative  (5/15)
────────────────
Q001 what data do we actually have?
  a) docs only  b) docs + user feedback  c) docs + feedback + analytics ★

Q002 what could go wrong on day one?
  a) nothing major  b) onboarding gap ★  c) performance cliff

Q003 what's the main user benefit?
  a) saves time  b) fewer errors ★  c) both equally

Q004 how should the first screen work?
  a) show everything  b) guided tour first ★  c) minimal + progressive

Q005 what if we flipped the default approach?
  a) keep as-is  b) try the opposite  c) build a quick prototype ★

> 1c 2b 3b 4b 5c
```

Batch 2:
```
⬛ risk · 🟦 make · 🟩 creative · ⬜ facts · 🟨 optimism  (5/15)
────────────────
Q006 what's the biggest unknown?
  a) user demand  b) technical feasibility ★  c) maintenance cost

Q007 how do components A and B talk to each other?
  a) shared state  b) events  c) direct API calls ★

Q008 what's a weird alternative worth exploring?
  a) CLI-only  b) voice-first  c) agent-in-the-loop ★

Q009 what's the most critical data flow?
  a) input→process→output  b) user→server→user ★  c) unclear

Q010 if this succeeds, what changes a year from now?
  a) replaces manual work  b) becomes a platform ★  c) both

> 2c 3c 4c 5a 6b
```

After batches, user can reply with any combination:
`0` = all recommended | `1a 3c` = Q001=a, Q003=c | `0 7a` = all recommended except Q007=a

#### Explained mode

Like simple, but each option gets a one-line reason and the recommended pick
includes a short justification:

```
⬜ facts · ⬛ risk · 🟨 optimism · 🟦 make · 🟩 creative  (5/15)
────────────────
Q001 what data do we actually have?
  A) docs only — limited visibility
  B) docs + user feedback — better signal
  ★ C) docs + feedback + analytics — strongest base

Q002 what could go wrong on day one?
  A) nothing major — low risk start
  ★ B) onboarding gap — users don't know where to start
  C) performance cliff — works small, breaks at scale

Q003 what's the main user benefit?
  A) saves time — fewer steps
  ★ B) fewer errors — more reliable outcomes
  C) both equally — balanced value

> 1c 2b 3b
```

When user sends `0`, pre-answer all questions with the recommended picks and
show the batch summary.

### Rules

- Never delete decisions — only add or mark resolved
- When archive mode is enabled: move resolved items (update to archive.md
- When archive mode is disabled: mark resolved in-place (never delete unless user explicitly says so)
- New decisions: append to plan with ID, cross-ref question
- Skipped → pendings. >1 session pending → escalate
- Never re-ask a question with an answer in existing docs
- Global numbering: Q001+ across entire session, never reset
