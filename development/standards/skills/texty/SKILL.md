---
name: texty
description: >-
  Polish a flove app's presentational texts — prose, titles, hints, empty
  states, help and intro copy — without touching the load-bearing names (labels,
  ids, class names, i18n keys) that code couples to. Use for /texty or "tidy the
  texts", "fix the copy", "smooth the prose", "rewrite the intro", "the empty
  state is harsh". If the edit touches names, selectors or keys, use /vocaby
  (texty's superset). Delivers the review form, edited file and report on any
  HTML/CSS/JS page.
---

# texty

Polish the **presentational layer** of an app's texts — everything the reader sees as
*copy* — while never touching the names the machine depends on. The defining line: a
label is load-bearing, a paragraph is not. Rewording "Press here to continue" is free.
Renaming the `id` that a `for=` or `:checked` selector anchors to is not a copy edit — it
is a /vocaby job. This skill stays strictly on the free side of that line.

If the edit touches a name, selector, label or key, hand off to **/vocaby**
(its superset).

## Personal config

See `development/standards/skills/CONFIG.md` for the override routes and keys.

## What counts as presentational (in scope)

- Titles, headings, and subheads that are display-only.
- Prose: intros, help paragraphs, explainers, section copy.
- Hints, tooltips, empty states, "no results" / "nothing yet" messages.
- Button/link *labels* **only when nothing in the code looks them up by string** (no
  `:checked`, no `for=`, no `tKey(`, no JS string match, no i18n table entry). When in
  doubt, it's a label → hand off to /vocaby.
- Quotes, slogans, footer blurbs.

## What is NOT yours (out of scope)

- Anything another selector or handler keys on by name.
- Class names, `id`s, `name=` attributes, `data-*` keys, i18n keys/`data-ph-*`/`tKey(`
  identifiers.
- Structure: whether a heading is an `<h1>`/`<h2>`, an `aria-label`, or the lang
  split — that is /validaty or /translaty territory.
- The vocabulary contract an app declares (a "VOCABULARY — locked terms" block): if the
  app locks a term, don't rewrite around it — surface the conflict instead.

## Workflow

1. **Profile the file first.** Grep the coupling tells: `label … for=`, `type="radio"`/
   `checkbox`, `:checked`, `:has(`, `:target`, `tKey(`, `data-ph-*`, `data-aria-*`, JS
   `querySelector`/`getElementById` by string, `input[name="lang"]`. Anything on that map
   is a **wall** — reword around it, never through it.
2. **Extract the presentational strings.** Read the visible copy: `<title>`, headings,
   paragraphs, hints, empty states, button labels that pass the in-scope test, quotes.
   For each, note the current wording and what reads off (stiff, inconsistent, wrong
   voice, unclear, untranslated leftovers, legacy terms).
3. **Build the review form — the editable HTML table, then stop.** Write a single-file
   `<app>-texty-review.html` next to the app: one row per extracted string, each showing
   the current text and why, with the proposed wording as an editable `<textarea>` and an
   **Apply**/**Keep** toggle. Below the table, a **Copy** button that serialises every row
   into a recognisable payload — first line `texty-review\t<app>\t<timestamp>`, then one
   line per row `id\tapply|keep\t<proposed>` (tabs, newlines escaped). **Never edit the app
   before the payload comes back** — the review form is the contract, same as /vocaby. The
   form is the user's to own: they edit the textareas by hand in the HTML file, then Copy
   and paste the payload back.
4. **Apply the returned rewrites.** Parse the pasted payload: apply every row marked
   `apply`, skip `keep`/`drop`. Change only those strings, in place. Preserve surrounding
   markup, `lang=` attributes, spans, and any `data-*` you didn't touch. Never widen the
   edit to a coupled name to "make the sentence flow" — that crosses into vocaby.
5. **Re-verify and report honestly.** Reason through any string you changed: does anything
   in JS/CSS reference it by value? If a rewrite accidentally sits on a wall, undo it and
   flag the term for /vocaby. Then report what was reworded, what was surveyed and how the
   user decided, and anything left untouched and why.

## Safety: the three buckets

1. **Safe** — display-only copy, no coupling, can be reworded freely. Apply on approval.
2. **Coupled** — looks like copy but something keys on it by value (an i18n table, a JS
   string match, a `for=`/`:checked` chain). **Never edit.** Surface it and point to
   /vocaby.
3. **Voice call** — the wording is fine but the user wants a different tone/register.
   Apply freely once approved; it is still copy, not names.

When unsure between Safe and Coupled, treat it as Coupled — rewording a string the code
matches on silently breaks the app.

## Scope honesty & non-goals

- **Does not rename names.** Labels, ids, class names, keys → /vocaby. If the work you're
  asked for keeps hitting those, say so and hand off; don't drift into doing vocaby's job
  "on the side."
- **Does not translate.** Adding languages / worldball → /translaty. Texty edits the
  single-language copy and preserves the existing lang split untouched.
- **Does not fix validity/a11y.** → /validaty.
- **Does not commit or deploy.** It edits the working tree; commit/push follows the user's
  own Gitea workflow.
- **No app export.** The only file written before approval is the review form; the
  edited file and the report complete the output.
