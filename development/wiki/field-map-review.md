# Field-map review

> Generated from `development/wiki/register-path-inventory.json`.
> 2936 routed rows · 356 need review · 0 outside the 29 fields.

The default rule is: **accept the target below for the whole field**. A
row is only overridden when a task names a different owner in its title or
`Decision:` clause. Accepting a field clears all of its review rows.

| Field | Target | Rows | Review | Other targets |
|---|---|---:|---:|---|
| `docs/map` | `development/standards/plan.md` | 0 | 0 | — |
| `docs/plan` | `development/standards/plan.md` | 151 | 14 | `development/standards/README.md`×14, `tools/dev/build-work-tracker.py`×13 |
| `docs/work` | `development/standards/work.md` | 219 | 6 | `development/wiki/INDEX.md`×20, `development/standards/plan.md`×18 |
| `backend/contracts` | `development/standards/systems.md` | 145 | 36 | `development/standards/contract.md`×6, `https://flove.org/development/standards/systems.md`×3 |
| `backend/delivery` | `development/standards/scripts.md` | 154 | 25 | `tools/dev/build-work-tracker.py`×30, `development/standards/README.md`×15 |
| `backend/storage` | `development/standards/storage.md` | 71 | 24 | `development/standards/schemas.md`×4, `https://flove.org/development/standards/schemas.md`×2 |
| `backend/systems` | `development/standards/systems.md` | 247 | 48 | `tools/dev/build-work-tracker.py`×15, `https://flove.org/development/standards/systems.md`×10 |
| `backend/mynet` | `development/standards/mynet.md` | 56 | 12 | `https://flove.org/development/standards/mynet.md`×5, `development/standards/storage.md`×1 |
| `frontend/a11y` | `development/standards/accessibility.md` | 69 | 2 | `tools/dev/build-work-tracker.py`×12, `development/standards/frontend/frontend.md`×11 |
| `frontend/levels` | `development/standards/experience.md` | 163 | 0 | `tools/dev/build-work-tracker.py`×34, `https://flove.org/development/standards/frontend/frontend.md`×18 |
| `frontend/quality` | `development/standards/experience.md` | 108 | 9 | `development/standards/apps.md`×10, `development/standards/contract.md`×6 |
| `frontend/shell` | `development/standards/apps.md` | 112 | 12 | `tools/dev/build-work-tracker.py`×14, `development/standards/frontend/frontend.md`×9 |
| `frontend/tours` | `development/standards/experience.md` | 52 | 15 | `tools/dev/build-work-tracker.py`×6, `development/standards/frontend/frontend.md`×6 |
| `frontend/tree` | `development/standards/apps.md` | 117 | 17 | `tools/dev/build-work-tracker.py`×18, `development/standards/frontend/frontend.md`×12 |
| `frontend/types` | `development/standards/apps.md` | 49 | 5 | `tools/dev/build-work-tracker.py`×8, `development/wiki/work/pendings.md`×8 |
| `frontend/visual` | `development/standards/apps.md` | 60 | 0 | `development/standards/frontend/frontend.md`×23, `tools/dev/build-work-tracker.py`×6 |
| `ai/flows` | `development/standards/flows.md` | 127 | 23 | `tools/dev/build-work-tracker.py`×6, `https://flove.org/development/standards/flows.md`×4 |
| `ai/levels` | `development/standards/models.md` | 46 | 12 | `development/standards/skills/README.md`×7, `development/standards/puzzy.md`×2 |
| `ai/models` | `development/standards/models.md` | 85 | 17 | `tools/dev/build-work-tracker.py`×18, `development/standards/skills/README.md`×4 |
| `ai/skills` | `development/standards/skills.md` | 218 | 10 | `development/standards/skills/README.md`×25, `development/index.html`×8 |
| `data/index` | `development/standards/json.md` | 52 | 11 | `development/standards/frontend/routing-colours-db.md`×14, `tools/dev/build-work-tracker.py`×2 |
| `data/json` | `development/standards/json.md` | 67 | 10 | `development/standards/frontend/export.md`×9, `tools/dev/build-work-tracker.py`×8 |
| `data/mds` | `development/standards/mds.md` | 81 | 1 | `development/standards/README.md`×14, `tools/dev/build-work-tracker.py`×12 |
| `data/schemas` | `development/standards/schemas.md` | 108 | 19 | `development/standards/vocabulary.md`×8, `development/standards/frontend/routing-colours-db.md`×4 |
| `community/channels` | `development/standards/channels.md` | 90 | 8 | `development/wiki/INDEX.md`×9, `development/standards/risaliberada/plan-v2.md`×8 |
| `community/docs` | `development/standards/docs.md` | 89 | 10 | `development/standards/experience.md`×12, `development/wiki/INDEX.md`×11 |
| `community/feedback` | `development/standards/feedback.md` | 64 | 4 | `tools/dev/build-work-tracker.py`×13, `development/wiki/work/pendings.md`×6 |
| `community/language` | `development/standards/language.md` | 66 | 0 | `development/standards/contract.md`×8, `development/standards/frontend/frontend.md`×6 |
| `community/levels` | `development/standards/language.md` | 70 | 6 | `tools/dev/build-work-tracker.py`×19, `development/standards/risaliberada/risaliberada.md`×2 |

## Review examples

### `docs/plan` → `development/standards/plan.md`

- `map-06`: `development/standards/worldview.md` → `development/standards/plan.md` (`field_map`)
- `map-07`: `development/standards/worldview.md` → `development/standards/plan.md` (`field_map`)
- `map-09`: `development/standards/debates/browsy/spec.md` → `development/standards/plan.md` (`field_map`)

### `docs/work` → `development/standards/work.md`

- `work-10`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `development/standards/work.md` (`field_map`)
- `work-10`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `development/standards/work.md` (`field_map`)
- `work-10.2a`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `development/standards/work.md` (`field_map`)

### `backend/contracts` → `development/standards/systems.md`

- `contracts-02`: `development/standards/apps/README.md` → `development/standards/systems.md` (`field_map`)
- `contracts-02`: `development/standards/apps/README.md` → `development/standards/systems.md` (`field_map`)
- `contracts-03`: `development/standards/backend.md` → `development/standards/systems.md` (`field_map`)

### `backend/delivery` → `development/standards/scripts.md`

- `delivery-01`: `development/standards/apps/README.md` → `development/standards/scripts.md` (`field_map`)
- `delivery-01`: `development/standards/apps/README.md` → `development/standards/scripts.md` (`field_map`)
- `delivery-03`: `development/standards/apps/README.md` → `development/standards/scripts.md` (`field_map`)

### `backend/storage` → `development/standards/storage.md`

- `storage-01`: `development/standards/backend.md` → `development/standards/storage.md` (`field_map`)
- `storage-01`: `development/standards/backend.md` → `development/standards/storage.md` (`field_map`)
- `storage-02`: `development/standards/backend.md` → `development/standards/storage.md` (`field_map`)

### `backend/systems` → `development/standards/systems.md`

- `systems-01`: `development/standards/backend.md` → `development/standards/systems.md` (`field_map`)
- `systems-01`: `development/standards/backend.md` → `development/standards/systems.md` (`field_map`)
- `systems-02`: `development/standards/backend.md` → `development/standards/systems.md` (`field_map`)

### `backend/mynet` → `development/standards/mynet.md`

- `mynet-01`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `development/standards/mynet.md` (`default`)
- `mynet-01`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `https://flove.org/development/standards/mynet.md` (`default`)
- `mynet-02`: `development/standards/debates/plans/2026-11-17-appy-authy-mynet.md` → `development/standards/mynet.md` (`default`)

### `frontend/a11y` → `development/standards/accessibility.md`

- `a11y-06`: `development/standards/debates/browsy/spec.md` → `development/standards/accessibility.md` (`field_map`)
- `a11y-06.3`: `development/standards/debates/browsy/spec.md` → `development/standards/accessibility.md` (`field_map`)

### `frontend/quality` → `development/standards/experience.md`

- `quality-09`: `development/standards/debates/browsy/TESTING.md` → `development/standards/experience.md` (`field_map`)
- `quality-09.3`: `development/standards/debates/browsy/TESTING.md` → `development/standards/experience.md` (`field_map`)
- `quality-10`: `development/standards/debates/browsy/spec.md` → `development/standards/experience.md` (`field_map`)

### `frontend/shell` → `development/standards/apps.md`

- `shell-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/apps.md` (`field_map`)
- `shell-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/apps.md` (`field_map`)
- `shell-07`: `development/standards/debates/browsy/TESTING.md` → `development/standards/apps.md` (`field_map`)

### `frontend/tours` → `development/standards/experience.md`

- `tours-01`: `development/standards/apps/onboarding-copy.md` → `development/standards/experience.md` (`field_map`)
- `tours-01`: `development/standards/apps/onboarding-copy.md` → `development/standards/experience.md` (`field_map`)
- `tours-05`: `development/standards/apps/onboarding-copy.md` → `development/standards/experience.md` (`field_map`)

### `frontend/tree` → `development/standards/apps.md`

- `tree-01`: `development/standards/apps/README.md` → `development/standards/apps.md` (`field_map`)
- `tree-01`: `development/standards/apps/README.md` → `development/standards/apps.md` (`field_map`)
- `tree-04`: `development/standards/backend.md` → `https://flove.org/development/standards/apps.md` (`field_map`)

### `frontend/types` → `development/standards/apps.md`

- `types-04`: `development/standards/apps/README.md` → `development/standards/apps.md` (`field_map`)
- `types-04`: `development/standards/apps/README.md` → `https://flove.org/development/standards/apps.md#pipeline` (`field_map`)
- `types-04`: `development/standards/apps/README.md` → `https://flove.org/development/standards/apps.md` (`field_map`)

### `ai/flows` → `development/standards/flows.md`

- `flows-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/flows.md` (`field_map`)
- `flows-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/flows.md` (`field_map`)
- `flows-04.2a`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/flows.md` (`field_map`)

### `ai/levels` → `development/standards/models.md`

- `levels-16`: `development/standards/backend.md` → `development/standards/models.md` (`field_map`)
- `levels-16`: `development/standards/backend.md` → `development/standards/models.md` (`field_map`)
- `levels-17`: `development/standards/debates/browsy/spec.md` → `development/standards/models.md` (`field_map`)

### `ai/models` → `development/standards/models.md`

- `models-06`: `development/standards/adoption.md` → `development/standards/models.md` (`field_map`)
- `models-06`: `development/standards/adoption.md` → `development/standards/models.md` (`field_map`)
- `models-08`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/models.md` (`field_map`)

### `ai/skills` → `development/standards/skills.md`

- `skills-13`: `development/standards/debates/standards.md` → `development/standards/skills.md` (`field_map`)
- `skills-13`: `development/standards/debates/standards.md` → `development/standards/skills.md` (`field_map`)
- `skills-24`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/skills.md` (`field_map`)

### `data/index` → `development/standards/json.md`

- `index-01`: `development/standards/backend.md` → `development/standards/json.md` (`field_map`)
- `index-01`: `development/standards/backend.md` → `development/standards/json.md` (`field_map`)
- `index-05`: `development/standards/backend.md` → `development/standards/json.md` (`field_map`)

### `data/json` → `development/standards/json.md`

- `json-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/json.md` (`field_map`)
- `json-04`: `development/standards/debates/proposals/frontend-wizy.md` → `development/standards/json.md` (`field_map`)
- `json-08`: `development/standards/debates/bridges/oasis.md` → `development/standards/json.md` (`field_map`)

### `data/mds` → `development/standards/mds.md`

- `mds-08`: `development/standards/adoption.md` → `development/standards/mds.md` (`field_map`)

### `data/schemas` → `development/standards/schemas.md`

- `schemas-01`: `development/standards/apps/README.md` → `development/standards/schemas.md` (`field_map`)
- `schemas-01`: `development/standards/apps/README.md` → `development/standards/schemas.md` (`field_map`)
- `schemas-04`: `development/standards/debates/browsy/spec.md` → `development/standards/schemas.md` (`field_map`)

### `community/channels` → `development/standards/channels.md`

- `channels-07`: `development/standards/debates/standards.md` → `development/standards/channels.md` (`field_map`)
- `channels-07`: `development/standards/debates/standards.md` → `https://flove.org/development/standards/channels.md#questy-project-standards` (`field_map`)
- `channels-07`: `development/standards/debates/standards.md` → `https://flove.org/development/standards/channels.md` (`field_map`)

### `community/docs` → `development/standards/docs.md`

- `docs-03`: `development/standards/debates/standards.md` → `development/standards/docs.md` (`field_map`)
- `docs-03.3`: `development/standards/debates/standards.md` → `development/standards/docs.md` (`field_map`)
- `docs-04`: `development/standards/apps/onboarding-copy.md` → `development/standards/docs.md` (`field_map`)

### `community/feedback` → `development/standards/feedback.md`

- `feedback-06`: `development/standards/apps/onboarding-copy.md` → `development/standards/feedback.md` (`field_map`)
- `feedback-06`: `development/standards/apps/onboarding-copy.md` → `https://flove.org/development/standards/feedback.md#10-step-onboarding-apps-without-an-intro` (`field_map`)
- `feedback-06`: `development/standards/apps/onboarding-copy.md` → `https://flove.org/development/standards/feedback.md` (`field_map`)

### `community/levels` → `development/standards/language.md`

- `levels-23`: `development/standards/debates/browsy/spec.md` → `development/standards/language.md` (`field_map`)
- `levels-23.3`: `development/standards/debates/browsy/spec.md` → `development/standards/language.md` (`field_map`)
- `levels-27`: `development/standards/debates/browsy/rationale.md` → `development/standards/language.md` (`field_map`)

## Sign-off

Reply with the field keys to accept, or the keys to override with a new
target. Until then these rows stay `needs_review`.
