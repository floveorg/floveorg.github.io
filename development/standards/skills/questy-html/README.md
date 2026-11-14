# questy-html

Turn questy Q&A sessions into interactive HTML forms. Part of the questy flove theory.

## What it does

Renders questy-generated surveys as self-contained HTML forms. Users click through options, see answers compile in real time, and export the result.

## Files

- `SKILL.md` — standalone skill definition (for use outside flove)
- `questy-html-flove.md` — flove-specific workflow (questy → HTML → flove.org → publish)

## How questy uses it

When questy-html is available, questy offers to render the Q&A as an interactive HTML form at session start. The form:
- Shows questions in batches with click-to-answer
- Highlights recommended answers (★)
- Compiles a summary panel in real time
- Exports to markdown on completion

## Questy Flove Theory

**Browsy persistence is questy flove itself** — guiding and involving people through questions directed through flove.org.

The loop:
```
Questy (questions) → HTML form (answers) → Flove.org (public persistence) → Enrichment (more prompts) → Questy (refined questions)
```

## Workflow

1. Check for recent questy survey in project folder
2. If exists → copy `template123.html`, rename to `makingof-projectname.html`, import .md
3. If not → suggest creating one first, then create HTML
4. At end → remind about `updaty-web` to publish to flove.org

## Fallback (no questy-html)

If questy-html is not installed, questy can:
1. Generate a static HTML file with the Q&A content
2. Link to `https://flove.org/development/standards/skills/questy/` for the standalone form

## Form Features

- Import questy .md files
- Progress indicator (unanswered count)
- Radio buttons / checkboxes per question
- Expandable descriptions
- Save to localStorage, copy to clipboard, download .md, share to Telegram
- Floating "replies" tab with real-time answer panel

## Questy Markdown Format

```markdown
question: What is your project type?
option: Web app (Browser-based application)
option: Mobile app (Native iOS/Android)
multi: false
suggest: Web app
```

### Rules
- `question:` starts a new block
- `option:` adds an option (description in parentheses)
- `multi: true/false` sets select mode
- `suggest:` sets recommended picks
- Empty lines separate questions
