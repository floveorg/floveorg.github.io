---
name: exporty
description: >-
  Audit and repair a flove app's export & share surface against the §13.12 contract: verify
  everything the user selected or added shows in the summary, that it downloads correctly in all
  six formats (md·json·xml·html·jpg·csv), and that share-to-mobile (Web Share API) is wired and
  ready. Use whenever the user types /exporty or wants to check an app's download/share path:
  "does the summary export right?", "are all the formats working?", "is share to mobile ready?",
  "the JSON is missing items I selected", "tune the rating views", "verify the export for phase 1".
  Trigger even without the word "export" — any request to confirm selected/added content
  round-trips out of the app or that the share sheet works. The app is named on invocation (e.g.
  `/exporty metas/souls.html`); audit only that file. flove-first by default (summary-model, rating
  Views, CSS-only nav); override via the personal config (see CONFIG.md). Anything that changes the
  UI or diverges from the shared standard is
  surveyed inline, never changed silently. Solo-scoped: audits apps in the
  Solo distro (see development/standards/solo/README.md).
---

# exporty (solo)

Make sure a flove app's content actually **leaves the app intact** — into the summary, into the
six download formats, and out through the mobile share sheet — **without breaking how the app
works.** This is the phase-1 (pure-JS distro, no backend) acceptance check for an app's export &
share surface.

The whole skill rests on one idea from the contract (**§13.12** in `backend_plan.md` — the source
of truth; a distilled copy lives in `references/export-contract.md`): there is a single
**summary-model** object, and the live summary phrase, the rating Views, and every export format
all serialize from *that same object*. So the job is to verify they can never disagree — and to
repair the app toward that invariant when they do.

## Personal config
This skill ships with flove-first defaults. To fork/reuse it for another
project, create a personal config that overrides the defaults instead of
editing the skill (see `development/standards/skills/CONFIG.md`): a shared
`~/.config/flove/skills-config.yml`, a per-skill `settings.yml`, a hidden
`.settings`, or a `config.yml` in the skill folder. Only the keys you set
change; everything else falls back to these defaults.

## The four axes

Audit these four things. They map 1:1 to the contract.

1. **Summary parity** — every item the user selected or added appears in the live summary phrase,
   and nothing stale lingers after a deselection. When the model is entirely empty, the export
   controls are disabled (nothing to send). This includes the **Add date / Add profile** export
   extras (the two right-side opt-in checkboxes, §13.9): when checked the `date`/`profile` field
   must ride into all six formats; when off it must be absent. Full criteria in
   `references/export-contract.md` §A.1.
2. **Views ↔ `raters[]`** — the chart Views (bars · vertical · axial · spider) are four drawings
   of the *same* `raters[]` array. Each `{n,max}` maps to bar height / column / axis length /
   spider radius. A number shown in a View must equal the rater in the JSON. ("Tuning the Views"
   means exactly this: each View renders `raters[]` faithfully, no drift between chart and number.)
3. **Export correctness — the six formats** (`md·json·xml·html·jpg·csv`). For each: it is wired to
   a canonical hook, it is well-formed, it **survives a parse-back** to the same item set, it
   carries the same items as the summary (parity), it survives hostile input, prose localizes but
   machine keys don't, the filename is `<app>-summary.<ext>` (localized), MIME has `;charset=utf-8`.
4. **Share readiness** — `navigator.share` is present, the `files` variant is guarded by
   `navigator.canShare({files})` and attaches the **standalone HTML**, and the fallback ladder
   (Web Share text → clipboard → share-intent) is intact.

Concrete pass/fail criteria for every line above, plus the canonical build recipes for each format,
live in `references/export-contract.md` and `references/format-recipes.md`. **Read both before
auditing** — the recipes are what you repair *toward*, lifted from the `metas/souls.html` reference
so you never reinvent a `toXml` or a CSV quoter by hand.

## First: profile tier & distro (this decides whether export even applies)

Before checking anything, establish what the app is — because export is **advanced-tier, JS-distro
only**:

- **Tier** — grep the filename / `tier-pop` nav. `mini` and `basic` mark export **N/A
  (auto-pass)** — do not report "export missing" on them. `normal` treats it as optional.
  `advanced`/`super` are where the full contract applies.
- **Distro** — the six formats need real JS (Blob, canvas, Web Share). If the app is the
  **CSS-pure distro**, export is inherently N/A; its send-surface is just a print stylesheet +
  copy-to-clipboard. Audit against the distro the app actually targets; never flag a CSS-pure app
  for "missing" JS export.

If the named app is mini/basic/CSS-pure, say so plainly and stop — that's a clean pass, not a gap.

## The three buckets

Every finding sorts into one bucket. The sorting *is* the skill; the checks are routine.

1. **Safe** — the fix cannot change behavior, layout, or the item set. Apply it silently, report
   it after. Examples: a missing `;charset=utf-8`; an XML/HTML value escaped by hand → routed
   through the shared `esc`/`escAttr`; a JSON built by string concatenation → rebuilt with
   `JSON.stringify`; a CSV field with a comma left unquoted → RFC-4180 quoting; a missing
   `canShare({files})` guard added before a file share; a wrong download filename corrected to
   `<app>-summary.<ext>`; a JPG that drops lines silently → adds the visible `…`.
2. **Nav-risk** — the fix touches the summary's live-update wiring, the action-grid controls, or
   the CSS-only navigation around the export popover, so it *might* change behavior. Never apply
   blind. Survey it.
3. **Standard-divergence** — the fix is correct but would make this app differ from the §13.12
   pattern: wiring a **whole missing format** (adds UI), changing the **summary-model shape**,
   renaming the DOM hooks to the canonical `data-flove-save`/`data-flove-share`/`data-flove-copy`
   on an app that already ships other names, switching the share approach. Even when safe in
   isolation, it's a distro-level decision. Survey it.

When unsure whether something is Safe or Nav-risk, treat it as Nav-risk. One question is cheap; a
wrong silent edit is a broken app the user debugs later.

**House rule — don't fix one violation by introducing another.** Repairs respect the app's own
conventions (no inline `style=` in flove apps; tokens over ad-hoc values; the existing accent
palette). If a repair needs a helper (a shared `esc`, a `downloadBlob`), add it once and reuse it,
matching the surrounding code's idiom — don't paste a second copy.

## Orchestration mode — when /optimizy is driving

If your invocation says you're running as the **export stage of `/optimizy`** (the
orchestrator tells you so), the stage is a **functional check, not the full §13.12 audit**:
verify that the user's selections are **lively shown** in the summary (live, or via an update
button where the design allows it in the HTML) and that every **save / share / import** button
actually does its job. Apply the Safe fixes for those axes — but keep off the neighbouring
stages' ground:

- **translaty is the *last* stage and hasn't run.** Any UI, labels or share text you add
  must stay in the **base language (English)** — do **not** translate them or add `.es`
  spans; just make them translaty-ready (real text nodes / `data-*`-able attributes) so the
  later pass can wrap them. Keep the prose-localization *checks* in mind, but the app isn't
  multilingual yet, so don't fail an app for missing `.es` here.
- **`/validaty` ran just before you.** Keep your own additions valid and §13-conformant as
  you write them (no inline `style=`, shared `esc`/`downloadBlob`), so nothing needs a
  re-validate. If you add substantial new UI, *flag it* for the orchestrator rather than
  re-running a full validity pass.
- **The big scaffold is always a survey item — hand it up, don't decide it.** "App has no
  export surface → scaffold the full six-format + share surface" is a major UI change.
  Return it (with your recommendation) to the orchestrator's batched survey instead of
  asking yourself.
- **Don't open your own survey, don't write a final report, don't commit, don't touch the
  §14 table.** Return Safe-applied + risky findings as text; the orchestrator owns the one
  survey and the single report.
- **The deeper §13.12 audit (six-format parity, parse-back, hostile-input survival) is not
  in scope for this stage.** If you find a parity/parse-back violation while checking the
  functional axes, report it as a finding — don't rebuild the format surface silently.

Everything else below still applies in full — you're doing *less overlap*, not less care.

## Workflow

1. **Read & profile the target.** Read the named file. Determine tier + distro (above). If export
   doesn't apply, report that and stop. Otherwise map the app's current export surface: which of
   the six formats exist, what hooks they use, where the summary-model (or its equivalent) lives,
   how the Views read ratings, whether `navigator.share` is present. Note whether the app uses
   translaty i18n (`.en`/`.es` spans, the worldball) — if so, the prose-localization checks apply.

2. **Detect across all four axes.** Walk `references/export-contract.md` line by line against the
   app. For each format, actually **build the output and parse it back**: JSON through
   `JSON.parse`, XML through a `DOMParser` (or `node`-side check), HTML loaded in a sandbox to
   confirm the phrase is present, CSV split and compared. Feed one hostile probe (an item
   containing `<`, `&`, `"`, a comma, a newline, an emoji) and confirm it survives whole and inert
   in every format. Compare each format's item set to the live summary — that's the parity check.
   Tools, with graceful fallback:
   - JS: `node --check` on each inline export script (extract to a temp file if needed).
   - JSON/XML/HTML/CSV: write a small throwaway `node` script that builds each format from a
     sample model and asserts parse-back + parity. Reuse it across apps — it's faster and more
     reliable than eyeballing, and it's the same check every time.
   - Defer deep HTML/a11y validity of the *exported* HTML doc to `/validaty`; here, just confirm
     it's well-formed and standalone.

3. **Classify every finding** into Safe / Nav-risk / Standard-divergence.

4. **Apply the Safe fixes — all of them, every axis.** A prompt that names one axis ("is the JSON
   right?", "tune the views") tells you where to spend *extra* depth — it is **not** a licence to
   skip the cheap Safe fixes elsewhere. If you spotted an unescaped XML value while checking the
   views, fix it too. Enumerate every finding first, then sweep the whole Safe bucket. Keep a
   running list of what changed and why.

5. **Survey the rest.** Batch all Nav-risk and Standard-divergence findings into **one inline
   survey** (below). Apply each per the user's choice.

6. **Re-verify.** Re-run the parse-back/parity script and `node --check`. Claim success from a
   clean re-run, never from intent. Reason through every interactive path you touched to confirm
   the summary still updates live and the export popover still opens. Never open a browser yourself
   — that's the user's job (a standing preference).

7. **Report honestly.** What auto-fixed, what was surveyed and how the user decided, which formats
   now pass parse-back + parity, what remains and why. If you only covered part of a large file,
   say so. Offer to update the **§14 adoption table** row for this app (Export column) if its
   status changed — but don't edit `backend_plan.md` without the user's go-ahead.

## The survey — how and when to ask

Trigger a survey when there is **at least one** Nav-risk or Standard-divergence finding. Ask with
the environment's inline mechanism (in Claude Code, `AskUserQuestion`). **Never render an HTML form**
unless the user explicitly invokes `/questy-html` — answer and ask inline by default (standing user
preference).

Each question carries enough for a real decision: the issue, the *concrete* fix, **why** it's risky
or divergent, and clear options. Typical option sets: *Apply the fix* / *Apply a safer alternative
(described)* / *Leave as-is* / (for divergence) *Apply here and flag it to propagate as the §13.12
standard*. Recommend the option you'd pick and say why. Batch related decisions into one short set,
not a drip of pop-ups. Zero risky findings → ask nothing; just fix, verify, report.

**The big one: an app with no export yet.** Some apps have a "Save" button with no handler, or no
export surface at all. Scaffolding the whole six-format + share surface from the souls recipes is a
large, UI-changing change — always a survey item, never silent. Offer it as a clear choice: *scaffold
the full surface now* / *scaffold a subset (say which formats)* / *report only, I'll wire it later*.

### Headless / non-interactive mode

If no human can answer (subagent, batch, CI), **never block.** Write the survey out as text — for
each risky finding: issue, concrete fix, why it's risky/divergent, options, your recommendation —
then apply the recommended option and label those edits *"applied on recommendation — pending user
confirmation"* so they can review and revert. Default to the choice that preserves navigation and
the item set; never fall back to a UI-breaking change just because no one answered.

## Scope honesty & non-goals

- This skill **does not commit or deploy.** It audits and repairs the working tree; any commit/push
  follows the user's own Gitea workflow. (Offer it; don't do it unprompted.)
- It **defers to sibling skills**: deep HTML/a11y/mobile validity → `/validaty`; naming/vocabulary
  cleanup → `/vocaby`; adding languages → `/translaty`. Don't duplicate them; lean on them.
- It does not redesign the app or invent a new export aesthetic — the recipes are the canonical
  shape. If correctness needs a redesign, report it as a finding.
- Coverage honesty over false completeness: a partial, truthful pass ("4 of 6 formats verified,
  csv and jpg pending") beats a confident "all good" that isn't.
