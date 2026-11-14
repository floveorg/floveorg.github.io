---
name: questy-html
description: Display questy surveys as self-contained HTML forms with floating reply tab — part of the questy flove theory
---

# questy-html

## Overview

questy-html renders questy-generated surveys as self-contained HTML forms. Part of the questy flove theory: guiding and involving people through questions directed through flove.org.

## Questy Flove Theory

**Browsy persistence is questy flove itself** — the guiding and involving people through questions directed through flove.org.

The theory:
1. **Questions guide** — people answer questions, making decisions visible
2. **Flove.org persists** — decisions are public, version-controlled, accessible
3. **Involvement grows** — more questions, more answers, more understanding
4. **Export enriches** — answers can be exported, enriched with prompt formatting, re-imported

This creates a feedback loop:
```
Questy (questions) → HTML form (answers) → Flove.org (public persistence) → Enrichment (more prompts) → Questy (refined questions)
```

## Workflow

### Step 1: Check for Recent Questy Survey

Before doing anything, check console history for recent questy activity:

```
Check if questy survey was recently created or is ongoing:
- Look for questy output files (*.md) in project folder
- Check console history for questy commands
- Look for incomplete surveys (questions without answers)
```

### Step 2a: Survey Found — Create/Update HTML

If a recent questy survey exists:

1. **Locate the .md survey file** — find the most recent questy output
2. **Copy template123.html** — rename to `makingof-projectname.html`
3. **Import the .md file** — use "Import questy" button in the form
4. **Open in browser** — hand over the path to the user
5. **Remind about publishing** — "When done, use updaty-web to publish to flove.org"

### Step 2b: No Survey — Create One First

If no recent questy survey exists:

1. **Suggest creating a survey first** — "No recent questy survey found. Want me to create one?"
2. **Run questy** — create the survey with appropriate questions
3. **Then create the HTML form** — proceed with Step 2a
4. **At end, remind about publishing** — "Survey ready! Use updaty-web to publish to flove.org"

## Form Location

- **Main template**: `development/standards/skills/questy-html/template123.html`
- **Output**: `html/makingof-projectname.html` in project folder
- **Live on**: `flove.org/html/makingof-projectname.html`

## Form Features

### Import Section
- **Import questy** — loads .md survey file
- **Re-import answers** — imports previously exported answers (.md or .json)

### Progress Indicator
- Shows remaining unanswered questions
- Updates in real-time as user answers
- "all answered ✓" when complete

### Question Display
- Radio buttons for single-select
- Checkboxes for multi-select
- Expandable descriptions (click row to toggle)
- Suggested picks highlighted
- Unanswered questions marked with red *

### Action Buttons
- **Save** — saves to localStorage, warns on unanswered questions
- **Copy** — copies answers to clipboard as .md
- **MD** — downloads answers as .md file
- **Share** — opens Telegram with answers pre-filled

### Floating Tab
- Position: fixed, top-right corner
- Text: "replies"
- On click: toggles reply panel visibility
- After save: shows "saved ✓"

### Reply Panel
- Shows all saved answers in real-time
- Updates as user selects options
- Fixed position, 280px wide, scrollable

## Pendings Standard

When a user skips a question (doesn't answer), it becomes a **pending**:

1. **Mark as pending** — question shows red * indicator
2. **If skipped again** — move to pendings.md file
3. **Pendings are standardized** — same format across all skills
4. **Can be revisited** — import pendings.md to see skipped questions

The pendings format:
```markdown
# Pendings

## Skipped Questions

- Q3: What is your team size? (skipped 2024-01-15)
- Q5: What integrations do you need? (skipped 2024-01-15)
```

## Questy Markdown Format

The .md file must follow this format:

```markdown
question: What is your project type?
option: Web app (Browser-based application)
option: Mobile app (Native iOS/Android)
option: CLI tool (Command-line interface)
option: Library (Reusable code package)
multi: false
suggest: Web app

question: What frameworks do you use?
option: React (Component-based UI library)
option: Vue (Progressive framework)
option: Svelte (Compile-time framework)
option: None (Vanilla JS)
multi: true
suggest: React, Svelte

question: What is your team size?
option: Solo (Just me)
option: Small (2-5 people)
option: Medium (6-15 people)
option: Large (16+ people)
multi: false
```

### Format Rules

1. **Question line**: `question: What is your question?`
2. **Option lines**: `option: Label (Description)` or `option: Label`
3. **Description line**: `description: Optional description for previous option`
4. **Multi-select**: `multi: true` or `multi: false`
5. **Suggested picks**: `suggest: Option1, Option2`

### Parsing Logic

- Lines starting with `question:` start a new question block
- Lines starting with `option:` add an option to current question
- Lines starting with `description:` add description to last option
- Lines starting with `multi:` set multi-select mode
- Lines starting with `suggest:` set recommended picks
- Empty lines separate questions

## Publishing to Web

After the survey form is ready and answers are collected, remind the user:

```
Ready to publish? Use the updaty-web skill:
1. Run updaty-web to publish to flove.org
2. Your survey will be live at flove.org/html/makingof-projectname.html
3. Decisions are now public and persistent
```

This ensures:
- Survey is publicly accessible
- Decisions are recorded and version-controlled
- Others can see and reference the choices made
- Part of the questy flove theory in action

## localStorage Keys

- `qN` — selected options for question N
- `PROJECT_NAME-replies` — saved reply set

## Template Spots

The `template123.html` has three fill spots:

1. `<title>` — minimal title (just "survey")
2. `const PROJECT_NAME` — project identifier
3. `const LS_KEY` — localStorage key (no spaces)

## Common Mistakes

- **Skipping the check** — always check for existing surveys first
- **Wrong md format** — must follow `question:`, `option:`, `multi:`, `suggest:` structure
- **Missing descriptions** — add `(Description)` after option label or use `description:` line
- **Forgetting to save** — replies only persist if saved
- **Wrong localStorage key** — each survey needs unique key to avoid collisions
- **Not reminding about publishing** — always remind about updaty-web at the end
- **No questy survey first** — if none exists, suggest creating one before HTML form
- **Not referencing flove.org** — always point to flove.org for persistence
- **Not handling pendings** — skipped questions should move to pendings.md