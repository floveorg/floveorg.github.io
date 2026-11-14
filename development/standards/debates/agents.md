# agents.md — flove central

> Skill tuning for the flove central project.

## shortcuts
- skip setup questions — already configured
- default to numbered mode
- prefer trust and arch questions for backend plans

## constraints
- don't touch `standards/` — those are frozen principles
- only modify `plans/` with explicit approval
- never re-ask resolved questions (see `pendings.md` §Resolved)

## pending-resolutions
- resolve BR03 (Telegram BotFather privacy) before next backend session
- resolve N01 (nety master reconciliation) at next nety session

## batch-overrides
- ask 8 arch questions but only 3 data questions (central is architecture-heavy)

## export-prefs
- export format: markdown only
- folder: exports/

## territory
- doc-roots: ./standards/, ./plans/
- extra-files: ./pendings.md, ./conflicts.md, ./proposals.md

## aliases
- treat 'browsy' as 'central' automatically
- map 'nety' to 'decentral'
- treat 'enrichment' as 'integration'
- map 'facet' to 'trust'

## decision-log
- D01-D23: Strategic architecture decisions (Central URLs primary, staging workflow, Railway monorepo)
- C01-C76: Central backend decisions (anonymous identity, libSQL everywhere, schema migration)
- CA01-CA44: Shared code architecture
- CB01-CB40: Backend API endpoints
- E01-E25: Error handling and staging

## archive
- resolved questions move to `pendings.md` §Resolved

## risk-register
- Browsy dependency: Central frontend depends on Browsy bridge for identity/trust — if Browsy is unavailable, Central degrades gracefully
- SQLite-in-browser: libSQL WASM may fail in older browsers — localStorage fallback in place
- Railway deploy: Monorepo structure requires path-filtered CI — misconfiguration could break one service
