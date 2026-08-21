---
name: vocaby
description: >-
  Normalize a flove app's internal nomenclature (CSS class names, input ids, JS
  identifiers, data/i18n keys, labels) so it matches the words the UI actually shows, clean out
  legacy/dead names, and keep the vocabulary's nesting intact — then mirror the cleaned
  vocabulary into the central matrix-tier table, export it, and report. This is /texty's
  superset: it edits the presentational copy (prose, titles, hints) exactly as /texty does
  and through the same editable review-form workflow, then goes deeper into the load-bearing
  names (labels, ids, keys, class names). Use this whenever the user types /vocaby (or the
  old /vocabularies) or wants to tidy naming: "the class is still called the old word",
  "the code says decks but the UI says triads", "clean up the legacy vocabulary",
  "make the internal names match the labels", "normalize the vocab", "rename the dead
  aliases", "sync the matrix-tier table", "export the cleaned vocabulary", "audit the
  wording / terms of this app". Trigger it even when the user doesn't say "vocabulary" —
  any request to reconcile what the code calls something with what the screen calls it
  counts; reach for /texty when only light presentational copy needs polishing. The
  deliverables are the review form, the cleaned file, the synced matrix, the default
  Markdown export `vocaby-<app>.md` (one item per row), the optional HTML export, and the
   report. flove-first by default (CSS-only navigation, the §13 standards, the
   development/standards/flove-vocaby.html vocab table); override via the personal config (see
   development/standards/skills/CONFIG.md). The extract → review → rename → sync → export →
   report shape works on any single-file HTML/CSS/JS app. Nothing that could break navigation
   or diverge from the shared standard is ever renamed silently — it is raised as an inline
   survey for the user to decide.
---

# vocaby

Make a flove app's **internal names agree with the words it shows on screen**, drop the
dead nomenclature, mirror the cleaned vocabulary into the matrix table, and export it —
the review form, the cleaned source, the synced matrix, the `vocaby-<app>.md` export, and
the report are the output.

**/texty's superset.** texty polishes presentational copy — the free side of the line,
nothing load-bearing. vocaby does that too, then goes deeper: it also normalizes the names
the code keys on (labels, ids, class names, i18n keys), syncs the matrix-tier table, and
exports the cleaned vocabulary. Only light copy needs polishing → /texty. Names are
involved, the deep pass is wanted, or both → here.

The defining tension: the *label* is canonical (it's what the user
reads), but the *internal name* is load-bearing — a class drives a `:checked` selector, an
input id anchors a `for=`, a data key feeds the i18n lookup. So you can't just rename code
to match a label; a careless rename trades a cosmetic mismatch for a broken app. The job is
"make the code speak the same language as the UI, **while the app keeps doing exactly what
it did**, and without flattening the vocabulary's shape."

Three things make this skill more than a find-and-replace:

- **A vocabulary is a tree, not a list.** Decks → items, parent → children, RAY → its
  labels: the nesting *is* meaning. Preserve it in the review, the renames, the export, and
  the report.
- **The human approves by number.** Every item gets a unique number in the review form
  *before* anything is touched. That numbered list is the contract — the user can say
  "apply 3, 7, 12; keep 5" and you do exactly that.
- **Renaming is atomic or it doesn't happen.** A name lives in HTML *and* CSS *and* JS at
   once. Change all sites in one move, or surface it for review — never half-rename.

## Personal config
This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## What runs on what

`/vocaby <file>` operates on **one file at a time** (e.g. `apps/puzzy/keys.html`).
There is no silent whole-repo sweep — naming is too app-specific to batch blind. The
canonical clone is `~/Documents/flove`.

## Workflow

The order matters and the user fixed it deliberately: **review the form first, sync the
matrix and export last.** Everything safe happens in between. The presentational layer runs
first through /texty's review-form workflow; the nomenclature below starts where copy ends.

1. **Read and profile the target.** Read the file. Before touching anything, map what
   decides your safety calls:
   - **CSS-only navigation?** Grep the tells: `label ... for=`, `type="radio"`/`checkbox`,
     `:checked`, `:has(`, `:target`, sibling combinators (`~`, `+`) bound to state,
     `<details>`/`<summary>`. Any name a selector keys on is a **load-bearing wall**.
   - **translaty i18n?** Grep `.en`/`.es` sibling spans, `data-ph-*`, `data-aria-*`,
     `input[name="lang"]`, `tKey(`/`__*Relabel`. If present, the *label* often lives in an
     i18n table, not inline — read it there.
   - **The app's own vocabulary contract.** Many flove apps declare it: a "VOCABULARY —
     locked terms" block (blogyadvanced), a "Deferred class renames" / "renamed from …"
     comment (keys), a TREE/DECKS data object. These are gold — they tell you the intended
     mapping and which renames the author already deferred. See `references/extraction.md`.

2. **Extract the vocabulary, with its nesting.** Don't re-grep by hand — run the bundled
   scanner, which is deterministic and lists *every* site of each name (so a later rename
   can be atomic) and pre-classifies the buckets:

   ```bash
   python scripts/extract_vocab.py <file> --labeled   # the high-signal seed for the table
   python scripts/extract_vocab.py <file> --out inv.json   # the full inventory
   python scripts/extract_vocab.py <file> --deep-json deep.json  # translatable display layer only
   ```

   The scanner runs on **two layers**: (1) the machine layer — every class/id/input-name/
   data-attr/i18n-key, each `sites` line, a `load_bearing` flag (state selector / `for=` /
   `:has(#id)` / `aria-*` keys on it → Nav-risk), the resolved `label`, `maybe_legacy`, the
   `data_blocks` nesting, and legacy markers; and (2) the **display layer** — every visible,
   translatable string (`kind:"display"` en/es dual spans, control/heading/option/summary
   text, or `kind:"attr"` for `data-aria-*` / `data-ph-*` / `aria-label` / `placeholder` /
   `title`), plus a rebuilt `i18n_dict` (`key → {en, es}`) from any `I18N.strings` / `tKey`
   dictionary so each `i18n-key` is tied to its translation. Display strings are
   presentational and Safe to translate/rename; the machine names carry the Nav-risk.
   `--deep-json` emits just that display+i18n layer — the exact shape the Deep-labels view
   in `flove-vocaby.html` consumes.

   It emits, per term: a stable `id`, the `name`, its `kind` (class / id / input-name /
   data-attr / i18n-key), every `sites` line, whether a state selector keys on it
   (`load_bearing` → Nav-risk), the resolved UI `label` (from `<label for=>` / `aria-label`),
   a `maybe_legacy` flag (near a "renamed from…" legacy marker), plus `data_objects`
   (deck→items nesting) and `legacy_markers`. `--labeled` keeps only terms with a visible
   label or a legacy flag — start the review there, fall back to the full inventory for
   coverage. The script *discovers*; your job is to tie names to the canonical label, judge
   the dubious buckets, and spot mismatches it can't (semantic keys, `tKey` namespaces,
   nesting deeper than deck→items). `references/extraction.md` explains the layers, the
   contract patterns, and how nesting shows up per app.

3. **Detect what's off.** Flag, per term: internal ≠ external (code says the old word),
   dead aliases / commented "renamed from …" leftovers, legacy sets the standards mark as
   dead code (e.g. the péntadas `p1–p5` / "fivys" in keys — see the user's memory), and any
   name that drifts from the §13 shared vocabulary. Propose the aligned name for each.

4. **Build the editable review form — then stop.** Mirror /texty: write a single-file
   `<app>-vocaby-review.html` next to the app. One row per item — every presentational
   string from the copy layer AND every nomenclature term from the scanner. Each row shows
   the current value and why it's off, the proposed value as an editable `<textarea>`, an
   **Apply**/**Keep** toggle, and its number and bucket (Safe / Nav-risk /
   Standard-divergence). Below the table, a **Copy** button that serialises every row into a
   recognisable payload — first line `vocaby-review\t<app>\t<timestamp>`, then one line per
   row `id\tapply|keep\t<proposed>` (tabs, newlines escaped). **Never edit the app before
   the payload comes back** — the review form is the contract, same as /texty. The form is
   the user's to own: they edit the textareas by hand in the HTML file, then Copy and paste
   the payload back. Numbers stay stable across the form, the file, and the export — one
   item, one number, all its sites.

5. **Apply the approved changes — atomically.** Parse the returned payload plus any survey
   answers: apply every row marked `apply`, skip `keep`/`drop`. For each approved name,
   change *every* site in one pass — the HTML attribute, the CSS selector(s), the JS
   string/identifier, the data key, the i18n entry. A name that appears in a
   `:checked`/`for=`/`:has()` selector must move in the same edit as its markup. If a rename
   can't be made atomic with confidence, it belongs in the survey, not in a half-done edit.

6. **Sync the matrix file — `development/standards/flove-vocaby.html`** (renamed 2026-08-03
   from the old `flove-tiers-matrix.html`; the user's canonical vocab matrix). It keeps a
   *copy* of each app's vocabulary in its `vocab[app][slot][labeler]` object — it's the
   shown mirror of the file you just cleaned, and it goes stale the moment the file changes.
   Update that app's entry to match the cleaned vocabulary (rename/remove/add slots and
   values, preserve nesting and the labeler columns). **Read the file first**: its
   `SLOTS`/`LABELERS`/`appSlots`/`vocab` arrays at the top are the source of truth for the
   exact shape, and its **"Prompt for Claude" export** (`vocabLines()`, one
   `app.V#: [slot · labeler] value` row per item) is the reference prompt the update task
   should match. `references/matrix-tier-sync.md` has the details, how to resolve which
   `vocab[...]` key a file maps to (1:1 per app; ask inline if ambiguous), and how to edit
   it surgically without disturbing the other apps.

7. **Export the cleaned vocabulary.** Write `vocaby-<app>.md` next to the app — the default
   export. Render the vocabulary as a Markdown table, **one item per row**: number, internal
   name, shown as / label, kind, nesting, bucket, status (kept / renamed / removed /
   legacy). Cover every term you acted on and the fine nesting the matrix can't hold. If the
   user wants the same fine vocabulary as a page too, optionally write `vocaby-<app>.html`
   (the same table, standalone). These are the deliverables on disk; the scanner's
   `inv.json` from step 2 is internal tooling, not an app export.

8. **Re-verify and report honestly.** Reason through every interactive path whose name you
   moved — does the `:checked`/`for=`/`:has()` chain still resolve? If translaty or a
   linter is present, re-run its gate (see `/validaty`). Never open a browser yourself — the
   user does that. Then report: what was renamed, what was surveyed and how they decided,
   what the matrix sync changed, what the export holds, the fine vocabulary itself, and
   anything left untouched and why.

## Safety: the three buckets

Borrowed from `/validaty`, because the risk is identical — a rename that satisfies the
naming goal but breaks a selector is worse than the mismatch it fixed.

1. **Safe** — the name is internal-only (no selector, no `for=`, no external consumer keys
   on it) and you can change every site at once. Apply on approval, report it.
2. **Nav-risk** — the name feeds a CSS-only nav selector (`:checked`, `for=`, `:has(#id)`,
   sibling combinator) or a JS handler that looks it up by string. Renaming *might* change
   behavior. Never apply blind — survey it.
3. **Standard-divergence** — the rename is locally correct but would make this app's term
   differ from the shared flove vocabulary (§13). Even if safe in isolation, it's a
   distro-level call. Survey it.

When unsure between Safe and Nav-risk, treat it as Nav-risk. One question is cheaper than a
silently broken navigation the user debugs days later.

## The survey — how and when to ask

Trigger an inline survey when there is **at least one** Nav-risk or Standard-divergence
term. In Claude Code use `AskUserQuestion`. Ask inline by default (standing user
preference) — the `<app>-vocaby-review.html` file is the one deliberate exception, because
it is the shared review-form mechanism this workflow is built on (same as /texty); don't
render one-off HTML dialogs beyond it. Each question carries: the term and its number, the
concrete rename, *why* it's risky or divergent, and options — typically *Rename everywhere*
/ *Rename here but keep the old selector hook as an alias* / *Leave as-is* / (divergence)
*Rename and flag as a new §13 standard to propagate*. Recommend the option you'd pick and
say why. Batch them into one coherent set, not a drip of pop-ups. Zero risky terms → ask
nothing; just apply the Safe set, sync the matrix, export, report.

If you can't reach a human (subagent / batch / CI), don't block: write the survey as text,
apply the navigation-preserving recommendation for each, label those edits "applied on
recommendation — pending confirmation," and leave the paper trail.

## Orchestration mode — when /optimizy is driving

If your invocation says you're running as the **vocaby stage of `/optimizy`** (the
orchestrator tells you so), run the Safe rename set and the §13.7 alignment — but keep off
the neighbouring stages' ground:

- **translaty is the *last* stage and hasn't run.** Rename the load-bearing names (classes,
  ids, i18n keys, labels) on the clean single-language file, *before* translaty inflates it.
  Do **not** wrap strings in language spans or touch any `.es` content — that's translaty's
  job; your renames must leave the file single-language and translaty-ready.
- **`/code-review` ran just before you.** It has already moved selectors; you're the one
  finalizing nomenclature. Re-verify any selector your rename touches, the same way you
  would on a standalone run — navigation still resolves after your pass.
- **The survey is the orchestrator's batched one.** Return Nav-risk / Standard-divergence
  findings as text, with your recommendation, instead of opening your own `AskUserQuestion`
  set; the orchestrator folds them into its single batched survey. The `<app>-vocaby-review.html`
  file stays a deliverable, not a survey mechanism, unless the user invokes `/questy-html`.
- **Don't write a final report, don't commit, don't touch the §14/board table.** Return
  Safe-applied + risky findings as text; the orchestrator owns the one report and the commit.

Everything else below still applies in full — you're doing *less overlap*, not less care.

## Scope honesty & non-goals

- **Does not commit or deploy.** It edits the working tree; commit/push follows the user's
  own Gitea workflow.
- **Does not redesign.** Presentational copy is editable — that is the /texty layer; the
  *label* is the source of truth — this skill bends the *code* toward the label, never the
  label toward the code. If a label itself is wrong, report it; don't rename it to fix the code.
- **Does not flatten.** If preserving nesting and reporting cleanly truly conflict, keep the
  nesting and say so.
- **The export is Markdown, not JSON.** The app deliverable is `vocaby-<app>.md` (one item
  per row) plus the optional `vocaby-<app>.html`; no `vocab-*.json` is written — the
  scanner's `inv.json` from step 2 is internal tooling, not a deliverable.
- Coverage honesty over false completeness: a partial, truthful pass on a 11k-line file like
  keys.html beats a confident "all renamed" that quietly skipped the nav-critical half.
