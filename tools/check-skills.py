#!/usr/bin/env python3
"""check-skills.py — validate the flove skill library's frontmatter & hygiene.

Catches the class of bug that silently removes a skill from the agent's
available list (invalid YAML, missing name/description, duplicate ids) plus a
few safety checks (secrets, runaway descriptions).

Usage:
    python3 tools/check-skills.py
Exit code 0 = all good, 1 = errors found (warnings do not fail).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("check-skills: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "development/standards/skills"

SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]+"),
    re.compile(r"glpat-[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

# Repo paths written in backticks; placeholders (<app>, {x}) are skipped.
PATH_RE = re.compile(
    r"`((?:development|tools|apps|whole|central|docs|decentral|projects|references|scripts|assets)/"
    r"[^`\s]+?\.(?:md|html|js|mjs|css|sh|py|json|svg|png|jpe?g|ttf|webmanifest))`"
)
SLASH_SKILL_RE = re.compile(r"`/([a-z][a-z0-9-]+)`")
EXTERNAL_SKILLS = {"simplify", "code-review", "form", "vocabularies", "public"}

error_count = 0
warn_count = 0
seen_names: dict[str, Path] = {}
records: list[tuple[Path, str, str]] = []  # rel, name, description


def error(msg: str) -> None:
    global error_count
    error_count += 1
    print(f"  ERROR  {msg}")


def warn(msg: str) -> None:
    global warn_count
    warn_count += 1
    print(f"  WARN   {msg}")


def check_paths(rel: Path, skill_dir: Path, text: str) -> None:
    """Warn about backticked repo paths that do not resolve.

    Placeholders (`<app>`, `{x}`, `*`, `…`) are skipped; this is a warning, not
    an error, because some paths are examples or planned artifacts. Skill-local
    `references/`, `scripts/` and `assets/` paths are only checked when that
    folder actually exists (otherwise the mention is illustrative).
    """
    for match in PATH_RE.finditer(text):
        raw = match.group(1)
        if any(token in raw for token in ("<", "{", "*", "…")):
            continue
        if raw == "tools/devices.json":
            continue  # generated inside the downloadable package at runtime
        if raw.startswith(("references/", "scripts/", "assets/")):
            if not (skill_dir / raw.split("/", 1)[0]).is_dir():
                continue
            candidate = skill_dir / raw
        else:
            candidate = ROOT / raw
        if not candidate.exists():
            warn(f"{rel}: path does not resolve — `{raw}`")


def check_skill(path: Path) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        error(f"{rel}: missing YAML frontmatter (--- … ---)")
        return
    frontmatter = m.group(1)
    try:
        data = yaml.safe_load(frontmatter)
    except Exception as exc:  # noqa: BLE001 - report parser message
        error(f"{rel}: invalid YAML frontmatter — {exc}")
        return
    if not isinstance(data, dict):
        error(f"{rel}: frontmatter is not a mapping")
        return

    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not name.strip():
        error(f"{rel}: missing non-empty `name`")
    elif name in seen_names:
        error(f"{rel}: duplicate skill name `{name}` (also {seen_names[name]})")
    else:
        seen_names[name] = rel
    if not isinstance(description, str) or not description.strip():
        error(f"{rel}: missing non-empty `description`")
    else:
        if len(description) > 1000:
            warn(f"{rel}: description is {len(description)} chars (consider trimming)")
        if len(description) < 40:
            warn(f"{rel}: description is very short ({len(description)} chars)")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            error(f"{rel}: looks like a secret ({pattern.pattern})")
            break

    check_paths(rel, path.parent, text)
    if isinstance(name, str) and isinstance(description, str):
        records.append((rel, name, description))

    print(f"  ok     {rel}  ({name})")


def check_skill_references() -> None:
    """Warn on backticked `/skill` references that are not in the library."""
    names = set(seen_names)
    for rel, _, _ in records:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for match in SLASH_SKILL_RE.finditer(text):
            token = match.group(1)
            if token in names or token in EXTERNAL_SKILLS:
                continue
            warn(f"{rel}: references `/{token}` but no skill has that id")


def check_duplicate_triggers() -> None:
    """Warn when the same quoted trigger phrase appears in several skills."""
    phrase_map: dict[str, list[str]] = {}
    for rel, _, description in records:
        for phrase in re.findall(r'"([^"]{18,80})"', description):
            key = " ".join(phrase.lower().split())
            if len(key.split()) < 3:
                continue
            phrase_map.setdefault(key, []).append(str(rel))
    for phrase, rels in sorted(phrase_map.items()):
        if len(rels) > 1:
            warn(f"trigger phrase repeated in {', '.join(rels)}: \"{phrase}\"")


def main() -> int:
    if not SKILLS.is_dir():
        print(f"check-skills: skills folder not found: {SKILLS}", file=sys.stderr)
        return 2

    paths = sorted(SKILLS.glob("*/SKILL.md"))
    print(f"check-skills: {len(paths)} skills in {SKILLS.relative_to(ROOT)}\n")
    for path in paths:
        check_skill(path)

    check_skill_references()
    check_duplicate_triggers()

    print(f"\n{error_count} error(s), {warn_count} warning(s)")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
