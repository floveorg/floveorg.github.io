# Archive — retired notes

Notes kept for history that are no longer part of the active map.

## Home-directory layout

> Retired from `AGENTS.md` on 2026-11-19. It documents a past rename and the
> Claude Code runtime dirs; no agent should act on it now.

The user's working dirs were renamed from `claude` to the neutral **agents** name:

- `~/.agents` — user-owned config (skills symlink → `development/standards/skills`), the analog of old `~/.claude`
- `~/agents` — the personal notes/credential dir (old `~/Claude`), incl. `.git-credentials`
- repo convention: `.agents/` and `AGENTS.md` (old `CLAUDE.md`)

The following **Claude Code runtime dirs are kept intentionally** — they are the
tool's own state, not user content, and must NOT be renamed, duplicated, or
overwritten by future agents:

- `~/.claude.json` (Claude Code CLI state)
- `~/.local/share/claude`, `~/.local/state/claude`
- `~/.cache/claude`, `~/.cache/claude-cli-nodejs`
- `~/.local/bin/claude` (installed binary)
- `~/.vscode/extensions/anthropic.claude-code-*`

Do not create parallel `.claude`-style config or skill dirs; everything new goes
under `~/.agents` / `~/agents` / repo `.agents`.
