<!-- CONTEXT:BEGIN
schema: flove-page/1
id: community
path: development/standards/community/community.md
trunk: community
topic: community
kind: topic
status: stable
html_place: ["#plan-maps"]
owns: ["Community scope and umbrella contract"]
updated: 2026-11-26
read_next: ["#community-01", "#community-05"]
CONTEXT:END -->

# Community

> **Umbrella owner.** This page owns the cross-child Community contract and
> the 5-stage hito map. Child standards keep their own detail (`guide/`,
> `feedback/`, `language/`, `channels/`); the dated source history lives in
> [`development/plans/community/community.md`](../../plans/community/community.md).

## Why

Community currently appears as a Tracker domain with child sections
(`guide`, `feedback`, `language`, `channels`) but has no own milestones in the
Plans matrix. The result is 0 community hitos and no community-level progress
signal. This plan proposes a hybrid roadmap: 5 umbrella community hitos, one
per stage, each linking to existing child work and adding a small explicit
task roadmap.

## Confirmed policy

1. **Owner standard now.** `development/standards/community/community.md` is the
   umbrella owner standard; child standards keep their specific detail.
2. **Plans tree mirrors sections.** New hitos point to
   `development/plans/<section>/...#<hito-id>` as the default plan-pointer home,
   matching the existing plans tree (for Community:
   `development/plans/community/community.md#community-01`). Do not add an
   unnecessary `<axis>` folder when the section path already exists.
3. **Hitos get plan/standard links; tasks can be lighter.** A hito should have
   at least one stable plan/standard pointer. Tasks may inherit the hito plan,
   point to a specific plan anchor, or point to a standard/evidence path.
4. **New hitos only; old links grandfathered.** Existing non-standard links are
   not churned. Checkers should ignore legacy non-standard link shape; enforce
   plan/standard pointer policy only for newly created hitos.
5. **Hybrid reuse.** Community hitos are umbrella hitos. They aggregate/recycle
   intent and link to child hitos as related evidence; child hitos remain owned
   by their child section unless explicitly retagged.
6. **Normalize on milestone creation.** When converting this plan into
   milestones, expand each hito to the 7/8 tasks required by
   `build-work-tracker.py --check`, with `evidence.by=optimizy`, gaps/criterion,
   pointer, owner, and `Deliverable/Done when/Decision` in hito notes.

## Proposed hito map

| Stage | ID | Hito | Recycles / relates to | Candidate plan pointer |
|---|---|---|---|---|
| seed | `community-01` | Community contract & scope | `docs-01`, `channels-01`, `levels-20` | `#community-01` |
| infant | `community-02` | Proposal & moderation loop | `docs-03`, `channels-02`, `feedback-01` | `#community-02` |
| mature | `community-03` | Feedback-to-plan pipeline | `feedback-02`, `feedback-03`, `docs-04` | `#community-03` |
| grown | `community-04` | Language & channel governance | `language-03/04`, `channels-03`, `feedback-04` | `#community-04` |
| full | `community-05` | Community health & portable participation | `levels-23`, `docs-05`, Mynet community surfaces | `#community-05` |

## Build/check constraints to resolve before creating milestones

`tools/dev/tasks/build-work-tracker.py --check` currently enforces:

- fixed expected counts (`EXPECTED_MILESTONES/TASKS/ARCHIVED`, etc.);
- open hitos need **7 tasks** (`seed/infant/mature`) or **8 tasks**
  (`grown/full`);
- task evidence `by` must be `optimizy`, with gap/criterion/pointer shape;
- hito notes must contain `Deliverable:`, `Done when`, `Decision:` once;
- standard links must resolve.

**Proposal:** when converting this plan into milestones, create 7/8 tasks per
hito using the 2 core tasks below plus standard skeleton tasks (define/register,
apply in one live case, verify, link owner, review, etc.), all with
`evidence.by=optimizy`. Use existing resolvable standards as `standards` until a
dedicated `community.md` standard is created, or create
`development/standards/community/community.md` first.

---

<a id="community-01"></a>
## community-01 · Community contract & scope

- **Stage:** seed
- **Intent:** define Community as the shared space over guide, feedback,
  language and channels, with owner, boundaries, and entry points.
- **Recycles / relates to:** `docs-01` (docs as fallback), `channels-01`
  (contribution channels), `levels-20` (seed profile), Community child plans.
- **Owner candidate:** `development/standards/community/guide/guide.md` or a
  new `development/standards/community/community.md`.
- **Plan pointer:** `development/plans/community/community.md#community-01`

### Core tasks (user-facing)

1. Define Community scope, owner, and boundaries in a standard.
2. Register entry points for guide/feedback/language/channels and link them in
   Plans.

### Candidate roadmap (to normalize to 7 tasks for seed)

| Candidate task | Purpose | Depends on |
|---|---|---|
| Name the Community owner standard/path | Remove ambiguity about where Community is defined | - |
| Define scope/boundaries (guide, feedback, language, channels) | Make Community a real umbrella, not a label | owner |
| Map child sections to Community entry points | Connect existing child work | scope |
| Record “Community vs child section” decision | Prevent duplication/drift | scope |
| Add Plans/Work pointer for Community domain | Make it discoverable | map |
| Verify one live navigation path reaches each child | Basic smoke path | pointer |
| Review with owner and capture open gaps | Close seed with explicit next gaps | verify |

### Questions to nail down

- Is Community a **domain umbrella** only, or does it also own cross-child
  policy decisions?
- Should the canonical standard be `community/community.md` (new) or remain in
  `community/guide/guide.md`?
- Which child hitos are “supporting evidence” vs “owned by child section”?
- Should Community get its own Plans infobox stats independent from child
  subsection filters?
- What is the minimum “community entry point” for a user arriving at Plans?

### Done when

- A Community standard/path is named.
- The four child sections have explicit entry points and boundaries.
- Plans/Work can link to the community plan anchor.

---

<a id="community-02"></a>
## community-02 · Proposal & moderation loop

- **Stage:** infant
- **Intent:** define how people propose, discuss, moderate and decide; keep safe
  defaults and escalation clear.
- **Recycles / relates to:** `docs-03` (ACCESS/COM/IDEA convention),
  `channels-02` (debate/contribution channels), `feedback-01` (feedback
  surface).
- **Owner candidate:** `development/standards/community/channels/channels.md`
  with `guide.md` as onboarding surface.
- **Plan pointer:** `development/plans/community/community.md#community-02`

### Core tasks (user-facing)

1. Specify proposal, moderation, and decision flow and roles.
2. Add a minimal proposal template with owner and status.

### Candidate roadmap (7 tasks for infant)

| Candidate task | Purpose | Depends on |
|---|---|---|
| Define proposal lifecycle states | Make proposal status explicit | community-01 |
| Define roles: proposer, reviewer, moderator, owner, decider | Avoid invisible authority | lifecycle |
| Map ACCESS/COM/IDEA to lifecycle | Reuse existing convention | lifecycle |
| Add minimal proposal template/checklist | Make filing easy | lifecycle |
| Define moderation/escalation safe defaults | Handle conflict/spam/abuse | roles |
| Record decision log destination | Keep decisions traceable | template |
| Test one proposal through the flow | Verify the loop works | all above |

### Questions to nail down

- Who can promote IDEA to decision, and where is that recorded?
- What is the minimum moderation model before Nety/public social features?
- Are moderation actions local-only, maintainer-only, or community-visible?
- Which proposals require owner confirmation before publication?
- What is the escalation path for harmful/unsafe content?

### Done when

- A proposal can be filed without asking where it goes.
- Roles and escalation path are named.
- One sample proposal can move through the lifecycle.

---

<a id="community-03"></a>
## community-03 · Feedback-to-plan pipeline

- **Stage:** mature
- **Intent:** turn community feedback into tracked, triaged, actionable
  plan/tasks with privacy and consent.
- **Recycles / relates to:** `feedback-02` (voice-note policy),
  `feedback-03` (feedback pipeline), `docs-04` (doc dependency map).
- **Owner candidate:** `development/standards/community/feedback/feedback.md`.
- **Plan pointer:** `development/plans/community/community.md#community-03`

### Core tasks (user-facing)

1. Define intake/triage states and privacy/consent rules.
2. Wire one live feedback item to a plan/task with evidence.

### Candidate roadmap (7 tasks for mature)

| Candidate task | Purpose | Depends on |
|---|---|---|
| Define feedback intake channels and owners | Know where feedback lands | community-02 |
| Define triage states and SLA/priority light rule | Make feedback actionable | intake |
| Define privacy/consent/retention rules | Avoid unsafe feedback handling | intake |
| Define feedback→plan/task promotion criteria | Prevent backlog noise | triage |
| Add evidence format for promoted feedback | Keep traceability | promotion |
| Wire one live feedback item through pipeline | Prove the path | all above |
| Review false positives/noise and adjust criteria | Keep pipeline usable | live case |

### Questions to nail down

- Which feedback channels are canonical (Telegram, Git, form, voice note)?
- What data must never be copied into public plans/tasks?
- Who can triage, and who can close/reject feedback?
- What counts as enough evidence to create a hito/task?
- How are duplicates and conflicting feedback merged?

### Done when

- Feedback has named intake, triage, privacy, and promotion rules.
- One real feedback item is traceable to a plan/task.

---

<a id="community-04"></a>
## community-04 · Language & channel governance

- **Stage:** grown
- **Intent:** make bilingual/community language style, channel policies, and
  voice-note/access rules explicit and auditable.
- **Recycles / relates to:** `language-03/04`, `channels-03`, `feedback-04`.
- **Owner candidates:** `development/standards/community/language/language.md`,
  `development/standards/community/channels/channels.md`,
  `development/standards/community/feedback/feedback.md`.
- **Plan pointer:** `development/plans/community/community.md#community-04`

### Core tasks (user-facing)

1. Publish language/channel policy bundle.
2. Audit existing channels/messages against the policy and record gaps.

### Candidate roadmap (8 tasks for grown)

| Candidate task | Purpose | Depends on |
|---|---|---|
| Define language style/tone/length rules | Consistent es/en communication | community-03 |
| Define channel purpose and audience per channel | Avoid channel drift | community-02 |
| Define access/privacy/retention rules per channel | Safety and consent | feedback policy |
| Define voice-note/transcription/consent policy | Cover rich media feedback | feedback-04 |
| Define BotFather/privacy or platform-specific settings where relevant | Concrete channel config | channel rules |
| Audit current channels against policy | Find real gaps | policy bundle |
| Record remediation owners and dates | Make audit actionable | audit |
| Add review cadence for policy drift | Keep grown state alive | remediation |

### Questions to nail down

- Which rules are mandatory vs advisory?
- What is the canonical owner when language, feedback and channels overlap?
- Which channel settings are required before public use?
- How are translations reviewed for tone, not just literal accuracy?
- What is the retention/removal path for voice notes and derived transcripts?

### Done when

- A policy bundle exists for language/channels/feedback-sensitive rules.
- Existing channels have been audited and gaps have owners.

---

<a id="community-05"></a>
## community-05 · Community health & portable participation

- **Stage:** full
- **Intent:** define community health signals, review cadence, and portable
  participation boundaries across local/shared/community surfaces.
- **Recycles / relates to:** `levels-23` (masks/pseudonyms, local/Nety
  boundary), `docs-05` (review checklist/ownership), Mynet community-facing
  surfaces.
- **Owner candidates:** `development/standards/community/guide/guide.md` +
  `development/standards/backend/mynet/mynet.md` for identity boundary.
- **Plan pointer:** `development/plans/community/community.md#community-05`

### Core tasks (user-facing)

1. Define community health signals and review cadence.
2. Specify portable participation boundary with explicit consent.

### Candidate roadmap (8 tasks for full)

| Candidate task | Purpose | Depends on |
|---|---|---|
| Define local-only vs shareable health signals | Prevent surveillance drift | community-04 |
| Define review cadence and owners | Keep community healthy | signals |
| Define onboarding/re-entry path | Support new and returning participants | guide |
| Define portable participation/profile boundary | Connect Mynet identity carefully | mynet/levels-23 |
| Define consent/revocation for shared participation data | User control | boundary |
| Add aggregate/public reporting rules | Share health without exposing people | signals |
| Run one review cycle using the signals | Prove the loop | cadence |
| Record gaps and next-cycle owners | Keep full state maintainable | review cycle |

### Questions to nail down

- Which health signals are useful without becoming surveillance?
- What participation data can move from local to shared, and with what consent?
- How does a pseudonym/mask map to community participation?
- What is the minimum viable public community health report?
- How often is the community reviewed, and who can trigger an out-of-cycle review?

### Done when

- Health signals and review cadence are defined and privacy-bounded.
- Portable participation has an explicit consent boundary.

---

## Suggested implementation order (after confirmation)

1. Confirm hito ids/names/stages and the 2 core tasks per hito.
2. Decide owner standard: create `development/standards/community/community.md`
   or use `guide.md` as temporary owner.
3. Convert each hito into 7/8 tasks with `optimizy` evidence shape; add
   `Deliverable/Done when/Decision` notes.
4. Add milestones to `development/tasks/milestones.json` under tracker stage
   subsections with `section: community`, `path: ["tracker","community"]`,
   `source: development/plans/community/community.md#community-0X`.
5. Update `build-work-tracker.py` expected counts/check assumptions deliberately
   in the same change.
6. Rebuild/check Work tracker; confirm Plans infoboxes show the new community
   hitos and icon links resolve to plan anchors.

## Decisions confirmed

- **A. Owner standard:** created `development/standards/community/community.md` now.
- **B. Task count:** keep 2 core tasks visible in plan; normalize to 7/8 tasks on milestone creation.
- **C. Recycle mode:** hybrid/recommended — keep child hitos untouched, link as related evidence.
- **D. Checker policy:** grandfather old non-standard links; enforce only for newly created hitos.
- **E. Plans tree rule:** use `development/plans/<section>/...#<hito-id>` (existing section tree; no extra `<axis>` folder when section path already exists).
