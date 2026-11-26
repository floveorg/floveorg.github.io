#!/usr/bin/env python3
"""skilly.py — validate the flove skill library's frontmatter & hygiene.

Catches the class of bug that silently removes a skill from the agent's
available list (invalid YAML, missing name/description, duplicate ids) plus the
safety checks (secrets, runaway descriptions) and the **size guard**: every
`SKILL.md` is loaded on every session, so it is capped, and text repeated
verbatim across skills is flagged (the copy-paste that makes a library grow
back after it has been compressed).

Usage:
    python3 tools/dev/skilly.py
Exit code 0 = all good, 1 = errors found (warnings do not fail).
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("skilly: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]  # …/tools/dev → repo root
SKILLS = ROOT / "development/standards/data/ai/skills"
INDEX = ROOT / "development/index.html"

def wiki_slug(text: str) -> str:
    """The wiki's ## → anchor rule: lowercase, drop punctuation, hyphenate."""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


SKILL_CATEGORIES = {"sys", "authoring", "planning", "utility"}
seen_checkers: dict[str, str] = {}

# Strict standard URLs (Q055/Q067/Q075/Q089): the wiki turns each MD heading
# into a slug, so an anchor is only valid when that heading really exists.
STANDARDS = ROOT / "development/standards"
STANDARD_PREFIXES = (
    "https://flove.org/development/standards/",
    "https://flove.org/development/",
)
STANDARD_FILES: set[str] = set()
STANDARD_HEADINGS: dict[str, set[str]] = {}
for _base in (STANDARDS, ROOT / "development/plans", ROOT / "development/tasks"):
    for _p in _base.rglob("*"):
        if not _p.is_file():
            continue
        _rel = _p.relative_to(ROOT).as_posix()
        STANDARD_FILES.add(_rel)
        if _p.suffix == ".md":
            _text = _p.read_text(encoding="utf-8", errors="replace")
            STANDARD_HEADINGS[_rel] = set(re.findall(r'<a id="([^"]+)"', _text))
            STANDARD_HEADINGS[_rel].update(
                wiki_slug(m.group(1)) for m in re.finditer(
                    r"^#{1,6}\s+(.*?)\s*$", _text, re.M)
            )
_index = ROOT / "development/INDEX.md"
if _index.exists():
    _rel = _index.relative_to(ROOT).as_posix()
    STANDARD_FILES.add(_rel)
    _text = _index.read_text(encoding="utf-8", errors="replace")
    STANDARD_HEADINGS[_rel] = set(re.findall(r'<a id="([^"]+)"', _text))
    STANDARD_HEADINGS[_rel].update(
        wiki_slug(m.group(1)) for m in re.finditer(
            r"^#{1,6}\s+(.*?)\s*$", _text, re.M)
    )


# One URL → repo mapping for frontmatter and body pointers alike. A skill page
# carries one full flove.org URL; the local route is derived from it, never
# written a second time. The first pair is the old published prefix, kept only
# so an existing URL is normalized before validation.
PUBLISHED_TO_REPO = (
    ("https://flove.org/development/standards/data/ai/skills/",
     "development/standards/data/ai/skills/"),
    ("https://flove.org/development/standards/skills/",
     "development/standards/data/ai/skills/"),
    ("https://flove.org/development/standards/", "development/standards/"),
    ("https://flove.org/development/", "development/"),
    ("https://flove.org/", ""),
)
CANONICAL_SKILLS_URL = "https://flove.org/development/standards/skills/"


def canonical_url(url: str) -> str:
    """Rewrite the archived published skills prefix to its live route."""
    base, sep, fragment = url.partition("#")
    for prefix in ("https://flove.org/development/standards/data/ai/skills/",):
        if base.startswith(prefix):
            base = CANONICAL_SKILLS_URL + base[len(prefix):]
    return base + (sep + fragment if sep else "")


def published_to_repo(url: str) -> str | None:
    """Derive the repo-relative path from a published URL, without its anchor."""
    target = canonical_url(url).split("#", 1)[0].rstrip(".,;)")
    for prefix, local in PUBLISHED_TO_REPO:
        if target.startswith(prefix):
            return local + target[len(prefix):]
    return None


def published_to_repo_candidates(url: str) -> list[str]:
    """Local files a published URL may resolve to, in local-first order.

    AGENTS.md is the split case: `development/AGENTS.md` owns the PROCs while
    `development/standards/AGENTS.md` owns the work-style rules. A `#anchor`
    decides which one the pointer means. The order is owned by
    `development/AGENTS.md#local-first-url-resolution`.
    """
    rel = published_to_repo(url)
    if rel is None:
        return []
    if rel == "development/AGENTS.md":
        return [rel, "development/standards/AGENTS.md"]
    return [rel]


def check_standard_url(url, rel, label):
    """Error on a non-wiki URL, a missing target or an invented heading."""
    if not isinstance(url, str) or not url.startswith(STANDARD_PREFIXES):
        error(f"{rel}: {label} must be a full flove.org standards URL: {url!r}")
        return False
    canonical = canonical_url(url)
    path_rel = published_to_repo(canonical)
    if path_rel not in STANDARD_FILES:
        error(f"{rel}: {label} target does not exist: {url}")
        return False
    if "#" in url:
        anchor = url.split("#", 1)[1]
        if not path_rel.endswith(".md"):
            error(f"{rel}: {label} anchor on non-MD target: {url}")
            return False
        elif anchor not in STANDARD_HEADINGS.get(path_rel, set()):
            error(f"{rel}: {label} anchor #{anchor} is not a heading in {path_rel}")
            return False
    return True

SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]+"),
    re.compile(r"glpat-[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"cfat_[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}"),
]

# The size guard. `SKILL.md` is what an agent loads to do the job; extra files are
# read on demand. Over the cap means the skill should be split, not deleted.
BODY_WORD_CAP = 1000
BODY_LINE_CAP = 150
DESC_CHAR_CAP = 320

# A repeated paragraph is the copy-paste that regrows a compressed library.
DUP_MIN_WORDS = 12
NEAR_DUP_MIN_WORDS = 20
NEAR_DUP_RATIO = 0.85
NEAR_DUP_MAX = 8
DUP_SKIP_DIRS = ("-workspace", "/packs/", "/templates/", "/presets/")
LINK_SKIP_DIRS = ("-workspace", "/evals/")
LINK_RE = re.compile(r'(?:href|src)="([^"#?]+)')
MACHINE_RE = re.compile(r"/home/[a-z0-9_-]+/|[A-Za-z]:\\\\|/Users/[a-z0-9_-]+/")
EXTERNAL_PREFIXES = ("http:", "https:", "mailto:", "data:", "#", "javascript:", "${")
DUP_SKIP_FILES = {"questy-addons-texts.md"}

# Repo paths written in backticks; placeholders (<app>, {x}) are skipped.
PATH_RE = re.compile(
    r"`((?:development|tools|apps|whole|central|docs|decentral|projects|scripts|assets)/"
    r"[^`\s]+?\.(?:md|html|js|mjs|css|sh|py|json|svg|png|jpe?g|ttf|webmanifest))`"
)
SLASH_SKILL_RE = re.compile(r"`/([a-z][a-z0-9-]+)`")
EXTERNAL_SKILLS = {"simplify", "code-review", "form", "vocabularies", "public"}

error_count = 0
warn_count = 0
JSON_MODE = False
issue_log: list[dict[str, str]] = []
skills_json: list[dict[str, object]] = []
seen_names: dict[str, Path] = {}
records: list[tuple[Path, str, str]] = []  # rel, name, description


def error(msg: str) -> None:
    global error_count
    error_count += 1
    issue_log.append({"level": "error", "message": msg})
    if not JSON_MODE:
        print(f"  ERROR  {msg}")


def warn(msg: str) -> None:
    global warn_count
    warn_count += 1
    issue_log.append({"level": "warn", "message": msg})
    if not JSON_MODE:
        print(f"  WARN   {msg}")


def check_paths(rel: Path, skill_dir: Path, text: str) -> None:
    """Warn about backticked repo paths that do not resolve.

    Placeholders (`<app>`, `{x}`, `*`, `…`) are skipped; this is a warning, not
    an error, because some paths are examples or planned artifacts. Skill-local
    `scripts/` and `assets/` paths are only checked when that folder actually
    exists (otherwise the mention is illustrative).
    """
    for match in PATH_RE.finditer(text):
        raw = match.group(1)
        if any(token in raw for token in ("<", "{", "*", "…")):
            continue
        if raw == "tools/dev/assets/devices.json":
            continue  # generated inside the downloadable package at runtime
        if raw.startswith(("scripts/", "assets/")):
            if not (skill_dir / raw.split("/", 1)[0]).is_dir():
                continue
            candidate = skill_dir / raw
        else:
            candidate = ROOT / raw
        if not candidate.exists():
            warn(f"{rel}: path does not resolve — `{raw}`")


def check_discoverable() -> list[Path]:
    """Find skill folders and fail when one is not discoverable.

    The loader only sees `<folder>/SKILL.md`. A folder without one vanishes from
    the agent's skill list without any error, so the checker must be the thing
    that notices — a glob alone would return fewer skills and still say "ok".
    """
    folders = [
        d for d in sorted(SKILLS.iterdir())
        if d.is_dir() and not d.name.startswith((".", "_")) and not d.name.endswith("-workspace")
    ]
    paths: list[Path] = []
    for folder in folders:
        path = folder / "SKILL.md"
        if path.is_file():
            paths.append(path)
        else:
            error(f"{folder.relative_to(ROOT)}: skill folder without SKILL.md — the loader will not see it")
    if not paths:
        error(f"{SKILLS.relative_to(ROOT)}: no */SKILL.md found — every skill folder needs one")
    return paths


def check_skill_index() -> None:
    """Keep the development/index.html skills table honest.

    The table carries 40+ hardcoded `…/skills/<folder>/SKILL.md` links. Renaming
    or deleting a skill folder silently 404s them, so check both directions:
    every link resolves, and every skill is linked.
    """
    if not INDEX.is_file():
        warn(f"{INDEX.relative_to(ROOT)} missing — cannot verify the skills table")
        return
    text = INDEX.read_text(encoding="utf-8")
    refs = re.findall(r"skills/([a-z0-9-]+)/([A-Za-z0-9._-]+\.(?:md|html))", text)
    linked = {folder for folder, _ in refs}
    for folder, filename in sorted(set(refs)):
        if not (SKILLS / folder / filename).is_file():
            error(f"{INDEX.relative_to(ROOT)}: links skills/{folder}/{filename} but that file does not exist")
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        if path.parent.name not in linked:
            warn(f"{INDEX.relative_to(ROOT)}: skill `{path.parent.name}` is not listed in the skills table")


def check_registration_tables() -> None:
    """Both public tables list every skill under its frontmatter `category`."""
    frontmatter: dict[str, str] = {}
    for path in SKILLS.glob("*/SKILL.md"):
        match = re.search(r"^category:\s*([a-z]+)\s*$",
                          path.read_text(encoding="utf-8"), re.M)
        if match:
            frontmatter[path.parent.name] = match.group(1)

    readme_cat: dict[str, str] = {}
    readme = SKILLS / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            row = re.fullmatch(r"`([a-z]+)`", cells[0])
            if not row or row.group(1) not in SKILL_CATEGORIES:
                continue
            # The skills cell is always last: the optional `Core` column is
            # guidance, not registry data.
            for name in re.findall(r"[a-z][a-z0-9-]*", cells[-1]):
                readme_cat[name] = row.group(1)

    work_cat: dict[str, tuple[str, str]] = {}
    if INDEX.is_file():
        rows = re.finditer(
            r'<tr data-type="skill" data-cat="([^"]+)" data-skillcat="([^"]+)">'
            r'\s*<td><a href="[^"]+"><code>([^<]+)</code></a>',
            INDEX.read_text(encoding="utf-8"))
        for row in rows:
            work_cat[row.group(3)] = (row.group(1), row.group(2))

    for name, category in sorted(frontmatter.items()):
        listed = readme_cat.get(name)
        if listed is None:
            error(f"README.md: skill `{name}` missing from the category table")
        elif listed != category:
            error(f"README.md: skill `{name}` is in `{listed}`, "
                  f"but SKILL.md says `{category}`")
        row = work_cat.get(name)
        if row is None:
            error(f"development/index.html: skill `{name}` missing from the "
                  "Apps → Types → Skills table")
        else:
            for column, value in zip(("data-cat", "data-skillcat"), row):
                if value != category:
                    error(f"development/index.html: skill `{name}` has "
                          f"{column}=`{value}`, but SKILL.md says `{category}`")


def check_agents_symlink() -> None:
    """`~/.agents/skills` is how every consumer reaches this folder."""
    link = Path.home() / ".agents/skills"
    if not link.is_symlink() and not link.exists():
        return
    try:
        target = link.resolve()
    except OSError:
        warn("~/.agents/skills does not resolve")
        return
    if target != SKILLS.resolve():
        warn(f"~/.agents/skills → {target} (expected {SKILLS})")


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
        if name != path.parent.name:
            warn(f"{rel}: folder `{path.parent.name}` ≠ skill name `{name}` — keep them aligned")
    if not isinstance(description, str) or not description.strip():
        error(f"{rel}: missing non-empty `description`")
    else:
        if len(description) > DESC_CHAR_CAP:
            warn(
                f"{rel}: description is {len(description)} chars "
                f"(cap {DESC_CHAR_CAP} — it is paid on every session)"
            )
        if len(description) < 40:
            warn(f"{rel}: description is very short ({len(description)} chars)")

    category = data.get("category")
    if category not in SKILL_CATEGORIES:
        error(f"{rel}: missing or invalid `category` "
              f"(one of {', '.join(sorted(SKILL_CATEGORIES))})")
    checkers = data.get("checker_of") or []
    if not isinstance(checkers, list):
        error(f"{rel}: `checker_of` must be a list of flove.org standard URLs")
        checkers = []
    for url in checkers:
        if not check_standard_url(url, rel, "checker_of"):
            continue
        if url in seen_checkers:
            error(f"{rel}: standard already claimed by {seen_checkers[url]}: {url}")
        seen_checkers[url] = str(rel)

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            error(f"{rel}: looks like a secret ({pattern.pattern})")
            break

    check_paths(rel, path.parent, text)
    body = text[m.end():]
    check_body_size(rel, body)
    if isinstance(name, str) and isinstance(description, str):
        records.append((rel, name, description))
        skills_json.append({
            "name": name,
            "words": len(body.split()),
            "lines": len([line for line in body.splitlines() if line.strip()]),
            "desc_chars": len(description),
        })
    if not JSON_MODE:
        print(f"  ok     {rel}  ({name})")


def check_body_size(rel: Path, body: str) -> None:
    """Warn when the always-loaded `SKILL.md` body outgrows the cap.

    The remedy is to move detail into a flat file beside the skill (linked by its
    route), not to delete it.
    """
    words = len(body.split())
    lines = len([line for line in body.splitlines() if line.strip()])
    if words <= BODY_WORD_CAP and lines <= BODY_LINE_CAP:
        return
    over = []
    if words > BODY_WORD_CAP:
        over.append(f"{words} words (cap {BODY_WORD_CAP})")
    if lines > BODY_LINE_CAP:
        over.append(f"{lines} non-blank lines (cap {BODY_LINE_CAP})")
    warn(f"{rel}: body is {', '.join(over)} — move detail into a flat file beside it")


def check_duplicate_paragraphs() -> None:
    """Warn on paragraphs repeated verbatim or near-verbatim across skills.

    Excludes eval scaffolding and the deep catalogues that legitimately quote
    skill text (`full/`, `packs/`, `templates/`, `presets/`).
    """
    seen: dict[str, list[str]] = {}
    paras: list[tuple[str, str]] = []
    for path in sorted(SKILLS.rglob("*.md")):
        rel = str(path.relative_to(SKILLS))
        if any(token in f"/{rel}" for token in DUP_SKIP_DIRS):
            continue
        if path.name in DUP_SKIP_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        for block in re.split(r"\n\s*\n", text):
            # CONTEXT headers are page metadata, not prose: their boilerplate
            # would otherwise near-duplicate across every page in a folder.
            if block.lstrip().startswith(("|", "```", "#", ">", "-", "*", "1.", "<!--")):
                continue
            para = " ".join(block.split())
            if len(para.split()) < DUP_MIN_WORDS:
                continue
            seen.setdefault(para, []).append(rel)
            paras.append((rel, para))
    for para, files in sorted(seen.items()):
        if len(files) > 1:
            snippet = para if len(para) <= 90 else para[:87] + "…"
            warn(f"paragraph repeated in {', '.join(files)}: \"{snippet}\"")

    # Near-duplicates: the same rule reworded is the copy-paste that survives a
    # verbatim check. Compare long paragraphs across different skills only.
    reported: set[tuple[str, str]] = set()
    long_paras = [
        (rel, p) for rel, p in paras
        if len(p.split()) >= NEAR_DUP_MIN_WORDS and not rel.endswith("README.md")
    ]
    for i, (rel_a, a) in enumerate(long_paras):
        for rel_b, b in long_paras[i + 1:]:
            if rel_a == rel_b or (rel_b, rel_a) in reported:
                continue
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            if ratio < NEAR_DUP_RATIO:
                continue
            reported.add((rel_a, rel_b))
            snippet = a if len(a) <= 90 else a[:87] + "…"
            warn(
                f"near-duplicate paragraphs in {rel_a} and {rel_b} "
                f"({ratio:.2f}): \"{snippet}\""
            )
            if len(reported) >= NEAR_DUP_MAX:
                warn(f"… more near-duplicates suppressed (cap {NEAR_DUP_MAX})")
                return


def check_skill_page_links() -> None:
    """Warn on dead local links and machine-specific paths inside skills."""
    for path in sorted(SKILLS.rglob("*.html")):
        rel = str(path.relative_to(SKILLS))
        if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            if not (path.parent / target).exists():
                warn(f"{rel}: dead local link `{target}`")


def check_machine_paths() -> None:
    """Warn on paths that only exist on one machine."""
    for pattern in ("*.md", "*.html", "*.js", "*.sh", "*.py"):
        for path in sorted(SKILLS.rglob(pattern)):
            rel = str(path.relative_to(SKILLS))
            if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for match in MACHINE_RE.finditer(text):
                warn(f"{rel}: machine-specific path `{match.group(0)}`")


def check_orphan_docs() -> None:
    """Warn on a skill's markdown file that nothing in the skill refers to."""
    for path in sorted(SKILLS.rglob("*.md")):
        rel = str(path.relative_to(SKILLS))
        if path.name in ("SKILL.md", "README.md") or "/" not in rel:
            continue
        if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
            continue
        mentioned = any(
            path.name in other.read_text(encoding="utf-8", errors="replace")
            for other in path.parent.iterdir()
            if other.is_file() and other != path
        )
        if not mentioned:
            warn(f"{rel}: no file in the skill links it (link it or delete it)")

ARCHIVED_NAMES = {
    r"\bupdaty-web\b": "updaty",
    r"\bvalidaty-full\b": "validaty",
    r"\bexporty-solo\b": "jsony",
    r"\bupgrady-solo\b": "updaty",
    r"\bupdaty-apk-solo\b": "updaty-apk",
    r"\bquesty1\b": "questy",
    r"\brebrandy\b": "brandy",
    r"\bvocaby-full\b": "texty",
    r"\bvocaby\b": "texty",
    r"\bbrandy-all\b": "brandy",
    r"\bbrandy-flove\b": "brandy",
    r"\bapp-registration\.md\b": "brandy/SKILL.md",
    r"\binfluence\.md\b": "flovy/SKILL.md",
    r"\bcheck-skills\.py\b": "skilly.py",
    r"\bnarrate\.sh\b": "narraty.sh",
}

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*$", re.M)
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
                  ".wav", ".mp3", ".ttf", ".woff", ".woff2"}


def _strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def _slug(text: str) -> str:
    return wiki_slug(text)


def check_markdown_links() -> None:
    """Resolve markdown link targets and `#anchors` inside the library."""
    for path in sorted(SKILLS.rglob("*.md")):
        rel = str(path.relative_to(SKILLS))
        if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
            continue
        text = _strip_code(path.read_text(encoding="utf-8", errors="replace"))
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            link, _, anchor = target.partition("#")
            dest = path if not link else (path.parent / link)
            if not dest.exists():
                warn(f"{rel}: dead markdown link `{target}`")
                continue
            if anchor and dest.suffix == ".md" and re.fullmatch(r"[a-z0-9-]+", anchor):
                target_text = dest.read_text(encoding="utf-8", errors="replace")
                targets = set(re.findall(r'<a id="([^"]+)"', target_text))
                targets.update(_slug(h) for h in HEADING_RE.findall(target_text))
                if anchor not in targets:
                    msg = f"{rel}: anchor `#{anchor}` not found in {dest.name}"
                    if dest.name == "skills.md":
                        error(msg)
                    else:
                        warn(msg)


def check_archived_names() -> None:
    """Flag names that were renamed or deleted, so prose stops resurrecting them."""
    for pattern, replacement in ARCHIVED_NAMES.items():
        rx = re.compile(pattern, re.I)
        for path in sorted(SKILLS.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".html", ".js"}:
                continue
            rel = str(path.relative_to(SKILLS))
            if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
                continue
            for match in rx.finditer(path.read_text(encoding="utf-8", errors="replace")):
                warn(f"{rel}: archived-away name `{match.group(0)}` — now {replacement}")


def check_skill_weight() -> None:
    """Warn when a skill folder carries what a skill should not."""
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        size = 0
        count = 0
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            rel = str(path.relative_to(SKILLS))
            if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
                continue
            size += path.stat().st_size
            count += 1
        if size > 512_000:
            warn(f"{folder.name}: {size // 1024} KB of assets — media belongs in central/shared/media, features in a flat file")
        if count > 60:
            warn(f"{folder.name}: {count} files — check for a workspace or a stray export")


def check_orphan_assets() -> None:
    """Warn on media files nothing in the skill refers to."""
    for path in sorted(SKILLS.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ASSET_SUFFIXES:
            continue
        rel = str(path.relative_to(SKILLS))
        if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
            continue
        if not any(
            path.name in other.read_text(encoding="utf-8", errors="replace")
            for other in path.parent.iterdir()
            if other.is_file() and other != path
        ):
            warn(f"{rel}: asset is not referenced by anything in its folder")


def check_script_paths() -> None:
    """Warn on `scripts/...` invocations that only work from the skill folder."""
    for path in sorted(SKILLS.rglob("*.md")):
        rel = str(path.relative_to(SKILLS))
        if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for block in re.findall(r"```[^\n]*\n(.*?)```", text, re.S):
            for line in block.splitlines():
                if re.match(r"\s*(python3?|node|bash|sh)\s+(\./)?scripts/", line):
                    warn(f"{rel}: `{line.strip()[:50]}` only works inside the skill folder — use tools/dev/…")


def check_heading_and_trigger() -> None:
    """Every skill opens with its name as H1 and states a trigger."""
    for rel, name, description in records:
        text = (ROOT / rel).read_text(encoding="utf-8")
        body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
        h1 = re.search(r"^#\s+(.+?)\s*$", body, re.M)
        if not h1:
            warn(f"{rel}: no H1 — the body should open with `# {name}`")
        elif h1.group(1).strip().split(" ")[0].strip("—-–:") != name:
            warn(f"{rel}: H1 is `{h1.group(1).strip()}` but the skill is `{name}`")
        uses = len(re.findall(r"\bUse for\b", description, flags=re.I))
        if uses == 0:
            warn(f"{rel}: description has no `Use for` trigger clause")
        elif uses > 1:
            warn(f"{rel}: description has {uses} `Use for` clauses — exactly one")


def check_readme_refs() -> None:
    """Keep the README's URL list honest without duplicating the index table.

    The README writes full flove.org URLs. Derive the local path the same way a
    reader does (local-first) instead of trusting the published prefix, so both
    the live `data/ai/skills` route and its canonical `standards/skills` alias
    name the same folder.
    """
    readme = SKILLS / "README.md"
    if not readme.is_file():
        warn("development/standards/data/ai/skills/README.md missing")
        return
    text = readme.read_text(encoding="utf-8")
    prefix = "development/standards/data/ai/skills/"
    listed: set[str] = set()
    for url in re.findall(r"https://flove\.org/[A-Za-z0-9_./-]+", text):
        url = url.rstrip(".")
        rel = published_to_repo(url)
        if rel is None or not any((ROOT / c).exists() for c in published_to_repo_candidates(url)):
            warn(f"README.md: `{url}` does not resolve locally")
            continue
        if rel.startswith(prefix) and rel.endswith("/SKILL.md"):
            name = rel[len(prefix):-len("/SKILL.md")]
            if "/" not in name:
                listed.add(name)
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if folder.name not in listed:
            warn(f"README.md: skill `{folder.name}` has no URL line")


def check_companion_files() -> None:
    """Companions stay flat and linked; shared-rule copies are already caught."""
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill = folder / "SKILL.md"
        if not skill.is_file():
            continue
        if any("references" in p.parts for p in folder.rglob("*")):
            error(f"{folder.name}/: no `references/` folder — keep companions flat")
        body = skill.read_text(encoding="utf-8", errors="replace")
        for companion in sorted(folder.rglob("*.md")):
            if companion.name == "SKILL.md":
                continue
            rel = companion.relative_to(folder).as_posix()
            if any(token in f"/{rel}" for token in LINK_SKIP_DIRS):
                continue
            if len(companion.relative_to(folder).parts) != 1:
                error(f"{folder.name}/{rel}: companion must be flat (`<skill>/topic.md`)")
            if companion.name not in body:
                warn(f"{folder.name}/SKILL.md: companion `{rel}` is not linked")


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


POINTER_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
POINTER_URL_RE = re.compile(r"https://flove\.org/[A-Za-z0-9_.~/%#-]+")
ID_RE = re.compile(r'(?:<a\s+id="([^"]+)"|\bid="([^"]+)"|\s:id=([A-Za-z0-9_-]+))')


def local_anchor_exists(rel: str, anchor: str) -> bool:
    """True when a repo file carries an explicit id or a matching heading."""
    if anchor in STANDARD_HEADINGS.get(rel, set()):
        return True
    file = ROOT / rel
    if not file.exists() or not file.is_file():
        return False
    text = file.read_text(encoding="utf-8", errors="replace")
    if any(part == anchor for match in ID_RE.finditer(text) for part in match.groups() if part):
        return True
    return file.suffix == ".md" and any(
        wiki_slug(heading) == anchor for heading in HEADING_RE.findall(text)
    )


def check_pointer_urls() -> None:
    """Validate the one full URL each body pointer carries.

    A downloaded skill cannot resolve `../../AGENTS.md`, so every repo-level
    pointer is a flove.org URL. Reading order: derive the repo path(s), jump to
    the `#anchor` locally (explicit id or heading slug); if neither file nor
    anchor exists, follow the URL. No second in-repo path is written. Files
    inside the skill's own folder ship with the download and stay relative.
    The order is owned by
    `development/AGENTS.md#local-first-url-resolution`.
    """
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        body = re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.S)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        seen: set[str] = set()
        targets = [m.group(2) for m in POINTER_LINK_RE.finditer(body)]
        targets += [m.group(0) for m in POINTER_URL_RE.finditer(body)]
        for target in targets:
            t = target.rstrip(".,;)")
            if t in seen:
                continue
            seen.add(t)
            if t.startswith("https://flove.org/"):
                rels = published_to_repo_candidates(t)
                if not rels or not any((ROOT / rel).exists() for rel in rels):
                    warn(f"{path.parent.name}: published URL has no repo counterpart: {t}")
                    continue
                anchor = t.split("#", 1)[1] if "#" in t else ""
                if anchor and not any(local_anchor_exists(rel, anchor) for rel in rels):
                    msg = f"{path.parent.name}: anchor only resolves online, not locally: {t}"
                    if any(rel.endswith("skills.md") for rel in rels):
                        error(msg)
                    else:
                        warn(msg)
                continue
            if t.startswith(("http:", "mailto:", "data:", "#", "${")):
                continue
            local = (path.parent / t.split("#", 1)[0]).resolve()
            if local.parent == path.parent:
                continue  # companion file downloaded with the skill
            if not local.exists():
                warn(f"{path.parent.name}: dead local pointer: {t}")
            else:
                warn(f"{path.parent.name}: use the full flove.org URL, not {t}")


def main() -> int:
    global JSON_MODE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true",
                        help="emit one machine-readable report instead of prose")
    args = parser.parse_args()
    JSON_MODE = args.json

    if not SKILLS.is_dir():
        print(f"skilly: skills folder not found: {SKILLS}", file=sys.stderr)
        return 2

    paths = check_discoverable()
    if not JSON_MODE:
        print(f"skilly: {len(paths)} skills in {SKILLS.relative_to(ROOT)}\n")
    for path in paths:
        check_skill(path)

    check_skill_index()
    check_registration_tables()
    check_agents_symlink()
    check_skill_references()
    check_duplicate_triggers()
    check_duplicate_paragraphs()
    check_skill_page_links()
    check_machine_paths()
    check_orphan_docs()
    check_markdown_links()
    check_pointer_urls()
    check_archived_names()
    check_skill_weight()
    check_orphan_assets()
    check_script_paths()
    check_heading_and_trigger()
    check_readme_refs()
    check_companion_files()

    if JSON_MODE:
        print(json.dumps({
            "skills": sorted(skills_json, key=lambda row: str(row["name"])),
            "errors": error_count,
            "warnings": warn_count,
            "issues": issue_log,
        }, indent=2))
    else:
        print(f"\n{error_count} error(s), {warn_count} warning(s)")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
