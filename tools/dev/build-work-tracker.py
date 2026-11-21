#!/usr/bin/env python3
"""Canonical Work tracker block for development/index.html.

  --build  regenerate the JSON block from the real Gitea snapshot (pendings.md)
  --check  validate the block embedded in development/index.html

Gate: run --check before AND after any edit to milestones.json,
development/AGENTS.md or the canonical block. It checks counts, axis order,
URLs/anchors, checker ownership, dependency cycles, the PROC mirror and Skills
chip/row parity.

The HTML block is canonical for the page: it renders a custom mirror of the
register. `common.json` is a generated projection of the same rows for views
that want the hito/task join; it is never a second authority. There is no live
fetch in the default page. MD/wiki stays external via ↗ links. `fields[]` is
never inferred — it is manual only.
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import quote

import register_projection as projection
import procedures_source

ROOT = Path(__file__).resolve().parents[2] / "development"
HTML = ROOT / "index.html"
PEND = ROOT / "wiki/work/pendings.md"
MILESTONES_FILE = ROOT / "wiki/work/milestones.json"
BEGIN = "<!-- WORK-DATA:BEGIN -->"
END = "<!-- WORK-DATA:END -->"
SCRIPT_OPEN = '<script type="application/json" id="work-data">'
SCRIPT_CLOSE = "</script>"


STAGE_NAMES = ["seed", "infant", "mature", "grown", "full"]
STAGE_LABELS = STAGE_NAMES
# Six top-level areas. Docs leads; UX is no longer top-level — its work folds
# into Frontend as the User Experience tab.
TABS = ["docs", "backend", "frontend", "ai", "data", "community"]
EXPECTED_MILESTONES = 326
EXPECTED_TICKETS = 37
EXPECTED_ROWS = 75
EXPECTED_TASKS = 1559
EXPECTED_ARCHIVED = 805
EFFORTS = ("very easy", "easy", "medium", "hard", "very hard")

def L(es, en):
    return {"es": es, "en": en}

def F(es, en, state="on"):
    return {"es": es, "en": en, "state": state}

def LV(theme, note, features):
    return {"theme": theme, "note": note, "features": features}

# The stage matrix recovered from the pre-tracker presentation (work-cards.js
# + the static Plan card). One section per original group, five degrees each.
# `on` = shipped · `part` = partial · `todo` = not built. The page derives the
# percentage per degree, the achieved level and the higher-level gaps from here.
DEGREES = [
    {"section": "backend", "levels": [
        LV("Browsy & Nety plan",
           L("Especificación de Browsy, plan de Nety y modelo descentralizado: la forma ya está acordada antes de construir.",
             "Browsy specification, Nety plan and the decentral model: the shape is agreed before building."),
           [F("Plan de Browsy y Nety", "Browsy & Nety plan")]),
        LV("Browsy",
           L("Extensión anfitriona con clases P/L/S y puente de identidad y confianza; queda por construir.",
             "Host extension with P/L/S classes and the identity/trust bridge; still to build."),
           [F("Browsy", "Browsy", "todo")]),
        LV("Nety",
           L("Capa P2P con gateway GraphQL y red libp2p; el plan existe, la red no.",
             "P2P layer with the GraphQL gateway and the libp2p network; the plan exists, the network does not."),
           [F("Nety", "Nety", "todo")]),
        LV("Integraciones",
           L("Adaptadores de integración: 0asis primero, luego ActivityPub, Matrix y Solid.",
             "Integration adapters: 0asis first, then ActivityPub, Matrix and Solid."),
           [F("Integraciones", "Integrations", "todo")]),
        LV("Puzzy · Epsilon",
           L("Motor completo: ejes y raters múltiples, primitivas relacionales.",
             "Full engine: multi-axis, multi-rater and relational primitives."),
           [F("Puzzy · Epsilon", "Puzzy · Epsilon", "todo")]),
    ]},
    {"section": "frontend", "levels": [
        LV("routing.json",
           L("routing.json con esquema flove-routing/3: apps, árbol de campos y categoría; jsony bloquea la deriva.",
             "routing.json with the flove-routing/3 schema: apps, field tree and category; jsony blocks drift."),
           [F("routing.json", "routing.json"), F("flove-routing/3", "flove-routing/3"),
            F("jsony · --check", "jsony · --check")]),
        LV("perfil fácil",
           L("Perfil fácil y retrato portable compartido con Appy.",
             "Easy profile and a portable portrait shared with Appy."),
           [F("perfil fácil", "easy profile"), F("retrato JSON", "portrait JSON")]),
        LV("base de datos",
           L("Central (FastAPI + Turso), en curso: CRUD completo y proxy de la API.",
             "Central (FastAPI + Turso), active: full CRUD and the API proxy."),
           [F("base de datos · FastAPI + Turso", "database · FastAPI + Turso", "todo")]),
        LV("browsy",
           L("La extensión Browsy como anfitrión y puente de identidad y confianza; especificación lista.",
             "The Browsy extension as host and identity/trust bridge; specification ready."),
           [F("browsy", "browsy", "todo")]),
        LV("demás",
           L("Adaptador Publisher: demostración de integración con 0asis y otras plataformas.",
             "Publisher adapter: integration demo with 0asis and other platforms."),
           [F("demás · adaptador Publisher", "else · Publisher adapter", "todo")]),
    ]},
    {"section": "ai", "levels": [
        LV("Questy · planes",
           L("Questy genera planes y prompts canónicos de agente en la capa local.",
             "Questy generates plans and canonical agent prompts in the local tier."),
           [F("Questy · planes", "Questy · plans")]),
        LV("Prompts de agente",
           L("Prompts de agente canónicos, reutilizados por los skills.",
             "Canonical agent prompts, reused by the skills."),
           [F("Prompts de agente", "Agent prompts")]),
        LV("Wizy básico",
           L("Afinador local sobre el perfil; aún por construir.",
             "Local finetuner over the profile; still to build."),
           [F("Wizy básico", "Wizy basic", "todo")]),
        LV("Sugerencias offline",
           L("Sugerencias en el dispositivo, sin red.",
             "Suggestions on the device, without a network."),
           [F("Sugerencias offline", "Offline suggestions", "todo")]),
        LV("Wizy-Browsy",
           L("El wizy corporativo entra por Browsy y devuelve sugerencias.",
             "The corporate wizy comes through Browsy and returns suggestions."),
           [F("Wizy-Browsy", "Wizy-Browsy", "todo")]),
    ]},
    {"section": "data", "levels": [
        LV("Plan de código compartido",
           L("La capa común se inlina en cada app; addons/code/ es solo la copia de referencia.",
             "The common layer is inlined in each app; addons/code/ is only the reference copy."),
           [F("Plan de código compartido", "Shared code plan")]),
        LV("Recuperación de id y feeds de apps",
           L("Recuperar la identidad y los feeds de las apps desde el propio dato.",
             "Recover identity and app feeds from the data itself."),
           [F("Recuperación de id y feeds de apps", "Id recovery & apps feeds", "todo")]),
        LV("Feeds de favs y mates",
           L("Feeds de favoritos y contactos construidos sobre el retrato portable.",
             "Favourites and mates feeds built on the portable portrait."),
           [F("Feeds de favs y mates", "Favs & mates feeds", "todo")]),
        LV("Authy",
           L("Authy abre MyNet: Telegram verificado en L3, phone L4, bio L5.",
             "Authy opens MyNet: Telegram verified at L3, phone L4, bio L5."),
           [F("Authy", "Authy", "todo")]),
        LV("Sety",
           L("Sety se activa en el nivel avanzado: idioma, escalas y valores por defecto.",
             "Sety activates at the advanced tier: language, scales and defaults."),
           [F("Sety", "Sety", "todo")]),
    ]},
    {"section": "ux", "levels": [
        LV("Limpieza",
           L("Simplifica, valida y revisa antes de tocar nada: menos datos, sin fuga a terceros y consentimiento claro. Las banderas UX se anotan.",
             "Simplify, validate and review before any change: least data, no third-party leak, clear consent. UX flags are noted."),
           [F("simplify", "simplify"), F("validaty · HTML, CSS, JS, JSON", "validaty · HTML, CSS, JS, JSON"),
            F("code-review", "code-review"), F("a11y · móvil · i18n listos", "a11y · mobile · i18n readiness"),
            F("banderas UX anotadas", "UX flags noted", "todo")]),
        LV("Datos y palabras",
           L("Exporta y cierra la letra: el retrato hace ida y vuelta, guardar/compartir/importar funcionan, y copia, nombres e idiomas quedan fijos.",
             "Export and finalise the words: the portrait round-trips, save/share/import work, then copy, names and languages are final."),
           [F("ida y vuelta del retrato", "portrait round-trip"),
            F("texty · copia y nombres", "texty · copy and names"),
            F("translaty · idiomas", "translaty · languages")]),
        LV("Usabilidad",
           L("Cumple cada mínimo aplicable de §13.18; si falta uno, el nivel falla. El resto de secciones se audita con la misma matriz.",
             "Meet every applicable minimum in §13.18; a missing minimum fails the level. Every other section is audited with the same matrix."),
           [F("mínimos de §13.18", "§13.18 minimums"),
            F("menú · tour · metadatos · stats", "menu · tour · metadata · stats"),
            F("auditar el resto de secciones", "audit every other section", "todo")]),
        LV("Función",
           L("Los trabajos concretos de nivel 4, sección por sección: 6 de 18 filas entregadas, el resto previsto o parcial.",
             "The concrete level-4 jobs, section by section: 6 of 18 rows shipped, the rest planned or partial."),
           [F("nivel 4 · 6/18 entregados", "level 4 · 6/18 shipped"),
            F("nivel 4 · 12/18 pendientes", "level 4 · 12/18 pending", "todo")]),
        LV("Acabado",
           L("El acabado de nivel 5 más una lista priorizada de recomendaciones (impacto × esfuerzo): 1 de 18 filas entregada.",
             "Level-5 craft plus a prioritized recommendation list (impact × effort): 1 of 18 rows shipped."),
           [F("nivel 5 · 1/18 entregado", "level 5 · 1/18 shipped"),
            F("nivel 5 · 17/18 pendientes", "level 5 · 17/18 pending", "todo")]),
    ]},
    {"section": "community", "levels": [
        LV("Bot · notas de voz · moderación · R2 MP3 · web",
           L("Bot de Telegram, moderación humana y audios en R2 con su web.",
             "Telegram bot, human moderation and R2 audio with its web view."),
           [F("Bot", "Bot"), F("notas de voz", "voice notes"), F("moderación", "moderation"),
            F("R2 MP3", "R2 MP3"), F("web", "web")]),
        LV("URL de perfil & Feed & LocalFavs",
           L("Enriquecimiento de la web con perfil, feed y favoritos locales.",
             "Web enrichment with profile, feed and local favourites."),
           [F("URL de perfil", "Profile URL"), F("Feed", "Feed"), F("LocalFavs", "LocalFavs")]),
        LV("Hilo (y más)",
           L("Respuestas en hilo y algo más allá.",
             "Threaded replies and over."),
           [F("Hilo (y más)", "Thread (and over)")]),
        LV("Apps entrelazadas",
           L("Apps que se enlazan entre sí en lugar de vivir aisladas.",
             "Apps that link to each other instead of living alone."),
           [F("Apps entrelazadas", "Entangled apps", "todo")]),
        LV("Botnet de flove",
           L("La red de bots de flove como capa de conversación distribuida.",
             "The flove botnet as a distributed conversation layer."),
           [F("Botnet de flove", "Flove botnet", "todo")]),
    ]},
    {"section": "docs", "levels": [
        LV("Backend plan",
           L("El diagrama de arquitectura del backend y las fases Seed, Alpha, Beta, Gamma, Delta y Epsilon: la forma constructiva ya está cerrada.",
             "The backend architecture diagram and the Seed, Alpha, Beta, Gamma, Delta and Epsilon phases: the build shape is settled."),
           [F("Backend plan", "Backend plan")]),
        LV("Vocabulary matrix",
           L("La matriz de vocabulario fija los nombres canónicos antes de que el dato se propague.",
             "The vocabulary matrix fixes canonical names before data spreads."),
           [F("Vocabulary matrix", "Vocabulary matrix")]),
        LV("Shared code plan",
           L("La capa común inlinada en cada app con addons/code/ como copia de referencia.",
             "The common layer inlined in every app with addons/code/ as the reference copy."),
           [F("Shared code plan", "Shared code plan", "todo")]),
        LV("Tiers & distros",
           L("Tiers y distros: qué se entrega en cada paquete y con qué complejidad.",
             "Tiers and distros: what ships in each package and at what complexity."),
           [F("Tiers & distros", "Tiers & distros", "todo")]),
        LV("Auth & tokens",
           L("Autenticación y tokens como condición final para publicar y sincronizar.",
             "Authentication and tokens as the final condition for publishing and syncing."),
           [F("Auth & tokens", "Auth & tokens", "todo")]),
    ]},
]

# One-word benefit per degree: what you gain when that feature set is done.
# It replaces the standard ladder/theme as the visible card label; the ladder
# and the original theme stay in the tooltip and in the expanded detail.
BENEFITS = {
    "backend": [L("Plano", "Blueprint"), L("Puente", "Bridge"), L("Red", "Network"),
                L("Integración", "Integration"), L("Fusión", "Fusion")],
    "frontend": [L("Rutas", "Routing"), L("Perfil", "Profile"), L("Almacén", "Storage"),
                 L("Enlace", "Link"), L("Presencia", "Presence")],
    "ai": [L("Intención", "Intent"), L("Prompt", "Prompt"), L("Asistente", "Assistant"),
           L("Intuición", "Insight"), L("Simbiosis", "Symbiosis")],
    "data": [L("Contrato", "Contract"), L("Recuperación", "Recovery"), L("Fuentes", "Feeds"),
             L("Identidad", "Identity"), L("Ajustes", "Settings")],
    "infra": [L("Paquete", "Package"), L("Ejecución", "Runtime"),
              L("Continuidad", "Continuity"), L("Malla", "Mesh"),
              L("Simplicidad", "Simplicity")],
    "ux": [L("Claridad", "Clarity"), L("Confianza", "Trust"), L("Facilidad", "Ease"),
           L("Potencia", "Power"), L("Oficio", "Craft")],
    "community": [L("Bienvenida", "Welcome"), L("Hogar", "Home"), L("Hilo", "Thread"),
                  L("Trama", "Weave"), L("Enjambre", "Swarm")],
    "docs": [L("Forma", "Shape"), L("Nombre", "Naming"), L("Compartido", "Shared"),
                L("Distro", "Distro"), L("Seguridad", "Security")],
}

# Assign the canonical 1–5 ladder and the one-word benefit by position.
for _deg in DEGREES:
    for _i, _lv in enumerate(_deg["levels"]):
        _lv["stage"] = STAGE_NAMES[_i]
        _lv["benefit"] = BENEFITS[_deg["section"]][_i]

# UX is no longer a top-level section. Its five stage subsections fold into Frontend:
# every milestone survives, keeping its original section as a titled part.
_by_axis = {d["section"]: d for d in DEGREES}
_front = _by_axis["frontend"]
_ux = _by_axis["ux"]
for _i in range(5):
    _front_lv, _ux_lv = _front["levels"][_i], _ux["levels"][_i]
    _front_lv["features"] = _front_lv["features"] + _ux_lv["features"]
    _front_lv["note"] = L(
        _front_lv["note"]["es"] + " Incluye accesibilidad, visual, quality, shell, tours y niveles UX.",
        _front_lv["note"]["en"] + " Includes a11y, visual, quality, shell, tours and UX levels.")
DEGREES = [_by_axis[s] for s in TABS]


# The original 62 DEGREES features are the seed. `milestones.json` recycles them
# and completes every one of the 30 subsections (6 sections x 5 stages) with part-
# tagged milestones taken from the live standards/plans. The builder stays the
# single source of truth for the JSON block embedded in development/index.html.
def load_milestones():
    if not MILESTONES_FILE.exists():
        return None
    return json.loads(MILESTONES_FILE.read_text(encoding="utf-8"))


SKILL_CATEGORIES = ["sys", "authoring", "planning", "utility"]
PROCEDURE_FIELDS = ("id", "title", "standard", "checker", "definition_of_done", "advice",
                    "inputs", "outputs", "gates")


def wiki_slug(text):
    """The wiki's ## → anchor rule: lowercase, drop punctuation, hyphenate."""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def load_heading_slugs():
    """Map each standards file to the set of wiki anchors it really contains."""
    files, headings = set(), {}
    for base in (ROOT / "standards", ROOT / "wiki"):
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            files.add(rel)
            if path.suffix == ".md":
                slugs = set()
                text = path.read_text(encoding="utf-8")
                slugs.update(re.findall(r'<a id="([^"]+)"', text))
                for line in text.splitlines():
                    m = re.match(r"^#{1,6}\s+(.*?)\s*$", line)
                    if m:
                        slugs.add(wiki_slug(m.group(1)))
                headings[rel] = slugs
    return files, headings


def check_standard_url(url, files, headings, label, errors):
    text = str(url)
    if not re.match(r"^https://flove\.org/development/(?:standards|wiki)/", text):
        errors.append("%s: standard must be a full flove.org standards URL: %r"
                      % (label, url))
        return
    rel = text[len("https://flove.org/development/"):].split("#", 1)[0]
    if rel not in files:
        errors.append("%s: standard target does not exist: %s" % (label, url))
        return
    if "#" not in text:
        return
    anchor = text.split("#", 1)[1]
    if not rel.endswith(".md"):
        errors.append("%s: anchor on non-MD standard: %s" % (label, url))
    elif anchor not in headings.get(rel, set()):
        errors.append("%s: anchor %r is not a heading in %s" % (label, anchor, rel))


def check_markdown_anchors(files, headings, errors):
    """Verify ## anchors in prose MD links across the whole standards book."""
    for path in sorted((ROOT / "standards").rglob("*.md")):
        text = re.sub(r"```.*?```", "", path.read_text(
            encoding="utf-8", errors="replace"), flags=re.S)
        for match in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
            target = match.group(1)
            link, sep, anchor = target.partition("#")
            if not sep or not re.fullmatch(r"[a-z0-9-]+", anchor):
                continue
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            dest = (path.parent / link).resolve() if link else path.resolve()
            try:
                rel = dest.relative_to(ROOT).as_posix()
            except ValueError:
                continue
            if not dest.exists() or rel not in files or not rel.endswith(".md"):
                continue
            if anchor not in headings.get(rel, set()):
                errors.append("%s: anchor #%s is not a heading in %s"
                              % (path.relative_to(ROOT), anchor, rel))


def _fm_list(fm, key):
    """Read a simple YAML block list from frontmatter without a YAML dependency."""
    m = re.search(r"^%s:\s*\n((?:\s+-\s+.*\n?)+)" % re.escape(key), fm, re.M)
    if not m:
        return []
    return [re.sub(r"^\s+-\s+", "", line).strip().strip("'\"")
            for line in m.group(1).splitlines()]


def build_skill_registry():
    """Publish the skill frontmatter taxonomy in Work (Q047 canonical map)."""
    out = []
    for path in sorted((ROOT / "standards/skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        cat = re.search(r"^category:\s*(\S+)\s*$", fm, re.M)
        out.append({
            "name": path.parent.name,
            "category": cat.group(1) if cat else None,
            "checker_of": _fm_list(fm, "checker_of"),
        })
    return out


def _doc_path(source):
    """A doc path that resolves from development/index.html."""
    if not source:
        return None
    return re.sub(r"^development/", "", source.split("#")[0]) or None


def apply_milestones(degrees, data):
    by_axis = {a["section"]: a for a in data.get("sections", [])}
    for deg in degrees:
        box = by_axis.get(deg["section"])
        if not box:
            continue
        for i, lv in enumerate(deg["levels"]):
            subs = box.get("subsections", [])
            if i >= len(subs):
                continue
            out = []
            for m in subs[i].get("milestones", []):
                out.append({
                    "es": m["es"],
                    "en": m["en"],
                    "state": m.get("state", "todo"),
                    "section": m.get("section", "levels"),
                    "doc": _doc_path(m.get("source")),
                    "depends_on": list(m.get("depends_on") or []),
                    "notes": m.get("notes", ""),
                    "standards": list(m.get("standards") or []),
                    "keep": bool(m.get("keep")),
                    "hito_id": m.get("id"),
                    "hito_stage": m.get("stage"),
                    "tasks": list(m.get("tasks") or []),
                    "needs_split": bool(m.get("needs_split")),
                })
            if out:
                lv["features"] = out


MILESTONES = load_milestones()
if MILESTONES:
    apply_milestones(DEGREES, MILESTONES)

# Five phase sets only: Seed · Infant · Mature · Grown · Full. The old F5 and
# Next buckets fold into Full, so every row is one of exactly five phases.
PHASES = ["F1", "F2", "F3", "F4", "F5"]
PHASE_FOLD = {"F0": "F1", "Next": "F5"}  # legacy codes only
STAGE_TO_PHASE = dict(zip(STAGE_NAMES, PHASES))
LEVELS = {
    "S1": "Planned & specified",
    "S2": "In build",
    "S3": "In quality",
    "S4": "Documented",
    "S5": "Delivered & operating",
}
GLYPH = {"S1": "\u00b7", "S2": "+", "S3": "-", "S4": "+", "S5": "\u2713",
         "done": "\u2713", "na": "\u2014"}

# The six top-level navigation categories and the domain sub-tabs planned for
# each one. `port` points at the one real DOM node holding that domain's original
# content; the page moves that node into the sub-tab section (it never copies it)
# and shows the filtered tracker table beside it. One source only — this block.
# Sub-tab ids are the canonical `subtab` values on the rows, so filtering keeps
# working. Every label is ONE WORD; the full original name lives in `desc`
# (es/en spans), which the page shows above the ported content. `port.nodes`
# moves several real panels into one tab as sections — never copies them.
# Cap: 5 tabs per section.
AXES = [
    {"slug": "docs", "label": "Docs", "label_es": "Docs", "domains": [
        {"id": "plan", "label": "Plan",
         "port": {"nodes": ["plan-maps"],
                  "sections": ["Mindmap · Decentral model"]},
         "feature": {"es": 'La matriz de grados 1–5 con los hitos de cada eje y el botón Mapa en lugar del título de la sección.', "en": 'The degrees 1–5 matrix with the milestones of each axis and a Map button in place of the section title.'},
         "desc": '<span class="es"><b>Plan</b> conserva un botón <b>Mapa</b> en el lugar del título: abre el minidiagrama de 480×270 en un modal centrado. El otro mapa (<b>decentral-model</b>, con flecha a Browsy host) vive en <b>Backend</b>. El antiguo <b>backend-plan.svg</b> se retira. Ya no hay pestaña Mapa.</span><span class="en"><b>Plan</b> keeps one <b>Map</b> button in the section title\'s place, opening the 480×270 mini-diagram in a centred modal. The other map (<b>decentral-model</b>, with a Browsy-host arrow) lives in <b>Backend</b>. The old <b>backend-plan.svg</b> is gone. There is no Map sub-tab any more.</span>'},
        {"id": "work", "label": "Work",
         "feature": {"es": '326 hitos por campo de su sección, 37 debates y 75 filas de pendings en una tabla con sección, fase y dependencias.', "en": '326 milestones by their section\'s own fields, 37 debates and 75 pendings rows in one table with section, phase and dependencies.'},
         "desc": ''},
     ]},
    {"slug": "backend", "label": "Backend", "label_es": "Backend", "domains": [
        {"id": "scripts", "label": "Scripts & API",
         "parts": [{"id": "contracts", "label": "Contracts"},
                   {"id": "delivery", "label": "Delivery"}],
         "feature": {"es": 'Contratos y entrega en un solo bloque: flove-fields, routing.json y los scripts que los validan y publican.', "en": 'Contracts and delivery in one block: flove-fields, routing.json and the scripts that check and publish them.'},
         "desc": '<span class="es">Contratos y <b>Delivery</b> fusionados: <code>routing.json</code>, <code>flove-fields</code>, <code>jsony</code>, distro, <code>sw.js</code> y el despliegue. Las dos secciones originales — <b>Contracts</b> y <b>Delivery</b> — siguen visibles como títulos dentro de la pestaña.</span><span class="en"><b>Contracts</b> and <b>Delivery</b> merged: <code>routing.json</code>, <code>flove-fields</code>, <code>jsony</code>, distro, <code>sw.js</code> and deployment. Both original titles remain as sections inside the tab.</span>'},
        {"id": "systems", "label": "System apps",
         "parts": [{"id": "systems", "label": "Systems"}],
         "feature": {"es": 'La plataforma completa en un solo sitio: el árbol de apps/sys/, tools/ y development/ tipado como backend…', "en": 'The whole platform in one place: the apps/sys/, tools/ and development/ tree typed as backend…'},
         "desc": '<span class="es">La plataforma completa en un solo sitio: el árbol de <code>apps/sys/</code>, <code>tools/</code> y <code>development/</code>, Authy · LocalHost · P2P · Browsy · Wizy · Nety. Los hitos del antiguo tab <b>Levels</b> se reparten entre esta sección, <b>Scripts &amp; API</b> y <b>Storage</b>.</span><span class="en">The whole platform in one place: the <code>apps/sys/</code>, <code>tools/</code> and <code>development/</code> tree, Authy · LocalHost · P2P · Browsy · Wizy · Nety. Milestones from the old <b>Levels</b> tab are spread across this section, <b>Scripts &amp; API</b> and <b>Storage</b>.</span>'},
        {"id": "mynet", "label": "MyNet",
          "port": {"nodes": ["mynet-plan"], "sections": ["MyNet · MyNet"]},
          "feature": {"es": 'MyNet como subsistema de backend: vista previa, claims, puertas de publicación, círculos y perfil portátil.', "en": 'MyNet as a backend subsystem: preview, claims, publish gates, circles and a portable profile.'},
          "desc": '<span class="es">MyNet es el conjunto de funciones de Appy que se abre sobre <code>claims</code> y la fila <code>profiles</code>. Sus hitos y tareas cubren las cinco stages, de la vista previa sin nodo al perfil portátil verificado por firma y SHA.</span><span class="en">MyNet is the Appy feature set that opens over <code>claims</code> and the <code>profiles</code> row. Its hitos and tasks cover all five stages, from the node-free preview to a portable profile verified by signature and SHA.</span>'},
         {"id": "storage", "label": "Storage",
         "feature": {"es": 'Base de datos y almacenamiento: el retrato persistente, localStorage, la bóveda Browsy y las claves puzzy.', "en": 'Database & storage: the persistent portrait, localStorage, the Browsy vault and puzzy keys.'},
         "desc": '<span class="es">Base de datos y almacenamiento: el retrato persistente, <code>localStorage</code>, la bóveda y los guardianes de Browsy, y las claves puzzy.</span><span class="en">Database &amp; storage: the persistent portrait, <code>localStorage</code>, the Browsy vault and keepers, and the puzzy keys.</span>'},
     ]},
    {"slug": "frontend", "label": "Frontend", "label_es": "Frontend", "domains": [
        {"id": "apps", "label": "Apps",
         "parts": [{"id": "tree", "label": "Tree"}, {"id": "types", "label": "Types"}],
         "port": {"nodes": ["apps-tree", "apps-types"], "sections": ["Tree", "Types"]},
         "feature": {"es": 'Árbol y tipos: las apps con su ruta real, su manifest y su type; UX se fusiona aquí.', "en": 'Tree and types: apps with their real path, manifest and type; UX folds in here.'},
         "desc": '<span class="es">Árbol (Tree) y Tipos (Types) en una pestaña: qué apps existen, dónde viven y qué <code>type</code> manda.</span><span class="en">Tree and Types in one tab: which apps exist, where they live and which <code>type</code> rules.</span>'},
        {"id": "accessibility", "label": "Accessibility",
         "parts": [{"id": "a11y", "label": "A11y"}, {"id": "visual", "label": "Visual"},
                   {"id": "quality", "label": "Quality"}, {"id": "shell", "label": "Shell"}],
         "feature": {"es": 'Accesibilidad, visual, calidad web y shell: foco, contraste, color, i18n, móvil y navegación.', "en": 'A11y, visual, web quality and shell: focus, contrast, colour, i18n, mobile and navigation.'},
         "desc": '<span class="es">A11y, Visual, Quality y Shell se fusionan: foco, contraste, <code>aria</code>, color, tipografía, i18n, móvil, cabecera y paneles. Los cuatro títulos originales quedan como secciones.</span><span class="en">A11y, Visual, Quality and Shell merge: focus, contrast, <code>aria</code>, colour, typography, i18n, mobile, header and panels. All four original titles remain as sections.</span>'},
        {"id": "experience", "label": "User Experience",
         "parts": [{"id": "tours", "label": "Tours"}, {"id": "levels", "label": "Levels"}],
         "port": {"nodes": ["data-ux"], "sections": ["Levels"]},
         "feature": {"es": 'Recorridos, textos y niveles UX: la visita guiada y la escalera de cuatro y cinco estrellas.', "en": 'Tours, copy and UX levels: the guided walk and the four-and-five star ladder.'},
         "desc": '<span class="es">Recorridos y textos (Tours) junto a los niveles UX (Levels). La escalera de funcionalidad seed · infant · mature · grown · full se lee en la matriz de grados del propio eje.</span><span class="en">Tours &amp; copy together with the UX Levels. The seed · infant · mature · grown · full ladder is read in the section stage matrix.</span>'},
     ]},
    {"slug": "ai", "label": "AI", "label_es": "IA", "domains": [
        {"id": "models", "label": "Models", "port": {"node": "ai-body"},
         "feature": {"es": 'Modelos y prompts (Models & prompts): los modelos que producen el JSON de cada app; Appy lo valida y lo…', "en": 'Models & prompts: the models that produce each app summary JSON; Appy validates it and keeps it in…'},
         "desc": '<span class="es">Modelos y prompts: los modelos que producen el <code>JSON</code> de cada app; Appy lo valida y lo guarda en <code>flove:appy:plays</code>.</span><span class="en">Models &amp; prompts: the models that produce each app summary <code>JSON</code>; Appy validates it and keeps it in <code>flove:appy:plays</code>.</span>'},
        {"id": "skills", "label": "Skills",
         "feature": {"es": 'Habilidades (Skills): las manos que ejecutan el trabajo — questy, jsony, texty, updaty, validaty…', "en": 'Skills: the hands that do the work — questy, jsony, texty, updaty, validaty…'},
         "desc": '<span class="es">Habilidades: <code>questy</code>, <code>jsony</code>, <code>texty</code>, <code>updaty</code>, <code>validaty</code>… Cada skill tiene su propio ciclo y se abre desde <a href="standards/skills/questy/index.html">skills/ ↗</a>.</span><span class="en">Skills: <code>questy</code>, <code>jsony</code>, <code>texty</code>, <code>updaty</code>, <code>validaty</code>… Each skill has its own cycle and opens from <a href="standards/skills/questy/index.html">skills/ ↗</a>.</span>'},
        {"id": "flows", "label": "Flows", "port": {"node": "ai-body"},
         "feature": {"es": 'Flujos y evaluación (AI apps & flows · Eval): Wizy conecta lo privado con lo público y el flujo privado…', "en": 'Flows & eval (AI apps & flows · Eval): Wizy bridges the private and public worlds and the private ↔…'},
         "desc": '<span class="es">Flujos y evaluación: Wizy conecta lo privado con lo público y el flujo se mide antes de publicarse. Eval se funde aquí.</span><span class="en">Flows &amp; eval: Wizy bridges the private and public worlds and the flow is measured before publishing. Eval folds in here.</span>'},
        {"id": "levels", "label": "Levels",
         "feature": {"es": 'Grados de funcionalidad 1–5 (seed · infant · mature · grown · full) en IA.', "en": 'Feature degrees 1–5 (seed · infant · mature · grown · full) for AI.'},
         "desc": '<span class="es">Grados de funcionalidad 1–5 en IA: qué conjuntos de funciones ya están conseguidos y qué queda en los grados superiores.</span><span class="en">Feature degrees 1–5 for AI: which feature sets are already achieved and what remains in the higher degrees.</span>'},
     ]},
    {"slug": "data", "label": "Data", "label_es": "Datos", "domains": [
        {"id": "mds", "label": "MDs", "port": {"node": "md-sources"},
         "feature": {"es": 'Los Markdown son la herramienta de fallback de lo canónico: esta página.', "en": 'The Markdown files are the fallback tool for the canonical source: this page.'},
         "desc": '<span class="es">Los Markdown son la herramienta de fallback de lo canónico: esta página. Standards y documentos de trabajo, con el detalle en el wiki.</span><span class="en">The Markdown files are the fallback tool for the canonical source: this page. Standards and working documents, with the detail in the wiki.</span>'},
        {"id": "index", "label": "Index", "port": {"node": "data-levels"},
         "feature": {"es": 'Índice y niveles de dato (Index · Data levels): los cinco niveles de profundidad y los índices que…', "en": 'Index · Data levels: the five depth levels and the indexes that validate data.'},
         "desc": '<span class="es">Índice y niveles de dato: los cinco niveles de profundidad y los índices que validan el dato.</span><span class="en">Index · Data levels: the five depth levels and the indexes that validate data.</span>'},
        {"id": "json", "label": "JSON", "port": {"node": "data-json"},
         "feature": {"es": 'JSON y manifests: los sobres canónicos flove-portrait/1 y flove-work/1, routing.json y los manifests…', "en": 'JSON & manifests: the canonical envelopes flove-portrait/1 and flove-work/1, routing.json and embedded…'},
         "desc": '<span class="es">JSON y manifests: los sobres canónicos <code>flove-portrait/1</code> y <code>flove-work/1</code>, <code>routing.json</code>. La columna vertebral: una fila, una definición.</span><span class="en">JSON &amp; manifests: the canonical envelopes <code>flove-portrait/1</code> and <code>flove-work/1</code>, <code>routing.json</code>. The backbone: one row, one definition.</span>'},
        {"id": "schemas", "label": "Schemas",
         "feature": {"es": 'Esquemas y Puzzy (Schemas & Puzzy): el vocabulario que da forma al dato y la capa difusa de búsqueda.', "en": 'Schemas & Puzzy: the vocabulary that shapes data and the fuzzy search layer.'},
         "desc": '<span class="es">Esquemas y Puzzy: el vocabulario que da forma al dato y la capa difusa de búsqueda.</span><span class="en">Schemas &amp; Puzzy: the vocabulary that shapes data and the fuzzy search layer.</span>'},
     ]},
    {"slug": "community", "label": "Community", "label_es": "Comunidad", "domains": [
        {"id": "docs", "label": "Docs",
         "feature": {"es": 'Documentación y wiki (Docs & wiki): el detalle que no cabe en el tracker.', "en": 'Docs & wiki: the detail that does not fit in the tracker.'},
         "desc": '<span class="es">Documentación y wiki: el detalle que no cabe en el tracker. Los enlaces <code>↗</code> salen a los MD.</span><span class="en">Docs &amp; wiki: the detail that does not fit in the tracker. The <code>↗</code> links go out to the MD files.</span>'},
        {"id": "feedback", "label": "Feedback",
         "port": {"nodes": ["msg-telegram", "msg-chatland"],
                  "sections": ["Telegram · Feedback", "Chatland · Channels"]},
         "feature": {"es": 'Feedback y soporte: Telegram recoge notas de voz y un grupo humano modera; Chatland abre los canales de…', "en": 'Feedback & support: Telegram collects voice notes moderated by a human group; Chatland opens the…'},
         "desc": '<span class="es">Feedback y soporte: Telegram y Chatland en dos paneles reales, una sola conversación.</span><span class="en">Feedback &amp; support: Telegram and Chatland as two real panels, one conversation.</span>'},
        {"id": "language", "label": "Language",
         "feature": {"es": 'Idioma y audiencia (Language & audience): español e inglés, y a quién va dirigido cada mensaje.', "en": 'Language & audience: Spanish and English, and who each message is for.'},
         "desc": '<span class="es">Idioma y audiencia: español e inglés, y a quién va dirigido cada mensaje.</span><span class="en">Language &amp; audience: Spanish and English, and who each message is for.</span>'},
        {"id": "channels", "label": "Channels",
         "feature": {"es": 'Canales de contribución (Contribution & channels): dónde se propone, se debate y se decide dentro de…', "en": 'Contribution & channels: where things are proposed, debated and decided inside flove.'},
         "desc": '<span class="es">Canales de contribución: dónde se propone, se debate y se decide dentro de flove.</span><span class="en">Contribution &amp; channels: where things are proposed, debated and decided inside flove.</span>'},
        {"id": "levels", "label": "Levels",
         "feature": {"es": 'Grados de funcionalidad 1–5 (seed · infant · mature · grown · full) en Comunidad.', "en": 'Feature degrees 1–5 (seed · infant · mature · grown · full) for Community.'},
         "desc": '<span class="es">Grados de funcionalidad 1–5 en Comunidad.</span><span class="en">Feature degrees 1–5 for Community.</span>'},
     ]},
]
# Row-level `domain` -> merged `subtab` and the original title kept as `section`.
DOMAIN_SUBTAB = {
    "backend": {"workflow": "scripts", "gates": "scripts",
                "solo": "systems", "trust": "systems", "backend": "systems",
                "levels": "systems", "release": "scripts", "build": "scripts",
                "delivery": "scripts", "pwa": "scripts", "mynet": "mynet",
                "backup": "storage", "storage": "storage"},
    "frontend": {"desk": "accessibility", "nety": "apps",
                 "apps": "accessibility", "build": "accessibility",
                 "interface": "accessibility", "voice": "accessibility",
                 "a11y": "accessibility", "docs": "experience",
                 "standards": "experience", "i18n": "experience",
                 "experience": "experience", "interview": "experience",
                 "review": "experience", "levels": "experience"},
    "ai": {"backend": "models", "models": "models"},
    "data": {"backend": "json", "backup": "json", "data-model": "schemas",
             "export": "json", "fields": "json", "taxonomy": "schemas",
             "vocabulary": "schemas"},
    "community": {"curators": "channels", "nety": "feedback",
                  "risa": "feedback", "social": "channels",
                  "community": "channels"},
    "docs": {"decisions": "work", "general": "work", "multiuser": "work",
             "nety": "work", "pending": "work", "puzzy": "work",
             "standards": "work", "trusty": "work", "vizy": "work",
             "workflow": "work"},
}
DOMAIN_SECTION = {
    "backend": {"workflow": "contracts", "gates": "contracts",
                "solo": "systems", "trust": "systems", "backend": "systems",
                "levels": "systems", "release": "delivery", "build": "delivery",
                "delivery": "delivery", "pwa": "delivery", "mynet": "mynet",
                "backup": "storage", "storage": "storage"},
    "frontend": {"desk": "shell", "nety": "tree",
                 "apps": "visual", "build": "visual",
                 "interface": "visual", "voice": "visual", "a11y": "a11y",
                 "docs": "tours", "standards": "tours", "i18n": "tours",
                 "experience": "levels", "interview": "levels",
                 "review": "levels", "levels": "levels"},
}
AXES_BY_SLUG = {a["slug"]: a for a in AXES}

# Spanish labels for every domain and part. The page renders es/en spans; the
# English label stays the canonical key used by routes and milestone sections.
LABEL_ES = {
    "plan": "Plan", "work": "Trabajo",
    "scripts": "Scripts y API", "contracts": "Contratos", "delivery": "Entrega",
    "systems": "Sistemas", "storage": "Almacenamiento", "mynet": "MyNet",
    "apps": "Apps", "tree": "Árbol", "types": "Tipos",
    "accessibility": "Accesibilidad", "a11y": "Accesibilidad",
    "visual": "Visual", "quality": "Calidad", "shell": "Interfaz",
    "experience": "Experiencia de usuario", "tours": "Recorridos",
    "levels": "Niveles",
    "models": "Modelos", "skills": "Habilidades", "flows": "Flujos",
    "mds": "MDs", "index": "Índice", "json": "JSON", "schemas": "Esquemas",
    "docs": "Docs", "feedback": "Comentarios", "language": "Idioma",
    "channels": "Canales",
}
for _a in AXES:
    for _d in _a["domains"]:
        _d["label_es"] = LABEL_ES.get(_d["id"], _d["label"])
        for _part in _d.get("parts", []):
            _part["label_es"] = LABEL_ES.get(_part["id"], _part["label"])


def subtab_for(category, domain):
    """Return the merged sub-tab id for a canonical row."""
    return DOMAIN_SUBTAB.get(category, {}).get(
        domain, AXES_BY_SLUG[category]["domains"][0]["id"])


def section_for(category, domain):
    """Return the original title id kept as the row section."""
    return DOMAIN_SECTION.get(category, {}).get(domain, subtab_for(category, domain))


def subtab_for_section(axis, section):
    """Find the domain that owns a section id (a subsection id or a part id)."""
    for d in AXES_BY_SLUG.get(axis, {}).get("domains", []):
        if d["id"] == section or any(p["id"] == section for p in d.get("parts", [])):
            return d["id"]
    domains = AXES_BY_SLUG.get(axis, {}).get("domains", [])
    return domains[0]["id"] if domains else section


def valid_sections(axis):
    """Every section id a milestone/row may carry inside an axis."""
    out = set()
    for d in AXES_BY_SLUG.get(axis, {}).get("domains", []):
        out.add(d["id"])
        out.update(p["id"] for p in d.get("parts", []))
    return out


def required_sections(axis):
    """The titled sections every degree box must cover (parts replace merged tabs)."""
    out = set()
    for d in AXES_BY_SLUG.get(axis, {}).get("domains", []):
        if d.get("parts"):
            out.update(p["id"] for p in d["parts"])
        else:
            out.add(d["id"])
    return out

# Explicit classification: ID prefix -> (category, domain, type, phase, field).
PREFIX = {
    "VARIOUS_Q": ("docs", "decisions", "question", "Next", "decisions"),
    "QUESTYDEMO": ("frontend", "interview", "demo", "Next", "questy"),
    "BR": ("community", "risa", "community", "F5", "risa"),
    "GH": ("backend", "levels", "infra", "F1", "git"),
    "N": ("frontend", "nety", "app", "F3", "nety"),
    "NF": ("frontend", "nety", "app", "F3", "nety"),
    "ARCH": ("backend", "levels", "infra", "F4", "architecture"),
    "V": ("frontend", "voice", "design", "Next", "voice"),
    "A11Y": ("frontend", "a11y", "standard", "F2", "a11y"),
    "UX": ("frontend", "experience", "design", "F2", "ux"),
    "VOCAB": ("data", "vocabulary", "standard", "F2", "vocabulary"),
    "W": ("backend", "workflow", "backend", "F1", "workflow"),
    "T": ("data", "taxonomy", "data", "F2", "taxonomy"),
    "PZ": ("docs", "puzzy", "plan", "F5", "puzzy"),
    "DS": ("frontend", "desk", "design", "F5", "desk"),
    "BUI": ("frontend", "build", "demo", "F2", "build"),
    "NUI": ("frontend", "interface", "demo", "F3", "nety"),
    "RC": ("community", "curators", "community", "F5", "nety"),
    "RISADNS": ("community", "risa", "community", "F5", "risa"),
    "BACKY": ("backend", "storage", "infra", "F1", "storage"),
    "LANG": ("frontend", "i18n", "standard", "F2", "i18n"),
    "PEN": ("docs", "pending", "question", "Next", "tracker"),
    "REV": ("frontend", "review", "review", "F2", "review"),
    "CB_S": ("backend", "solo", "backend", "F4", "solo"),
    "EXP": ("data", "export", "standard", "F2", "export"),
    "FIELDS": ("data", "fields", "standard", "F2", "fields"),
}

# Keyword overrides applied to the title (first match wins).
KEYWORDS = [
    (("ai", "model", "llm", "lora", "fine-tun"), ("ai", "models", "ai", "Next", "ai")),
    (("infra", "pwa", "install", "deploy", "r2", "build", "release", "git", "ci"),
     ("backend", "delivery", "infra", "F1", "infra")),
    (("json", "field", "schema", "export", "portrait", "vocab", "taxonom"),
     ("data", "data-model", "standard", "F2", "data")),
    (("a11y", "accessible", "focus", "contrast", "screen reader"),
     ("frontend", "a11y", "standard", "F2", "a11y")),
    (("i18n", "translat", "language", "locale"),
     ("frontend", "i18n", "standard", "F2", "i18n")),
    (("theme", "onboard", "footer", "design", "visual", "colour", "color"),
     ("frontend", "interface", "design", "F2", "visual")),
    (("community", "curator", "moderat", "risa", "linguist", "social"),
     ("community", "community", "community", "F5", "community")),
    (("browsy", "crypto", "permission", "keys", "login", "encrypt", "cubes", "visibility", "cross-link"),
     ("backend", "trust", "backend", "F4", "backend")),
]

def classify(rid, title):
    """Return (category, domain, type, phase, field, state, subcategory, labels)."""
    low = title.lower()
    cats = ""
    if " \u00b7 " in title:
        head, tail = title.split(" \u00b7 ", 1)
        cats = tail.split(" \u2014 \u25c7")[0]
        title = head
    labels = [c.strip() for c in cats.split(",") if c.strip()]

    base = None
    for key in sorted(PREFIX, key=len, reverse=True):
        if rid.startswith(key):
            base = PREFIX[key]
            break
    # A specific ID prefix wins; generic ones (VARIOUS_Q, PEN) use keyword rules.
    generic = base is None or rid.startswith(("VARIOUS_Q", "PEN"))

    def has(needle):
        # Short tokens need word boundaries ("ai" must not match "maintained").
        if len(needle) <= 4:
            return re.search(r"\b" + re.escape(needle) + r"\b", low) is not None
        return needle in low

    if generic:
        for needles, mapped in KEYWORDS:
            if any(has(n) for n in needles):
                base = mapped
                break
    if base is None:
        base = ("docs", "general", "question", "Next", "tracker")

    category, domain, typ, phase, field = base
    # VARIOUS_Q rows carry a real domain in their cats; keep it.
    if rid.startswith("VARIOUS_Q") and labels:
        domain = labels[0]
        field = labels[0]
    # A11y is its own UX lens now; a question about it must not fall into Tours.
    if category == "ux" and any(n in low for n in (
            "a11y", "accessib", "contrast", "screen reader", "keyboard")):
        domain = "a11y"

    state = "S1"
    if "live demo" in low or "hecho" in low or "\u2705" in low:
        state = "S5"
    elif "partly live" in low or "in build" in low:
        state = "S2"
    elif "revisi" in low or "review" in low:
        state = "S3"

    return category, domain, typ, phase, field, state, state, labels


def origin_of(heading):
    """Map a pendings.md ### heading to a filterable kind + short origin slug."""
    h = heading.lower()
    if "making-of" in h:
        kind = "decision"
    elif "review" in h or "validaci" in h:
        kind = "review"
    elif "tiers" in h or "designs" in h:
        kind = "design"
    else:
        kind = "pending"
    slug = re.sub(r"[^a-z0-9]+", "-",
                  re.sub(r"\s*\(\d{4}-\d\d-\d\d\)$", "", h)).strip("-")
    return kind, slug or "other"


def build_rows():
    text = PEND.read_text(encoding="utf-8")
    rows = []
    seen = set()
    heading = ""
    for line in text.splitlines():
        mh = re.match(r"^###\s+(.+)$", line.strip())
        if mh:
            heading = mh.group(1).strip()
            continue
        m = re.match(r"^- \*\*([A-Z0-9_]+(?: [A-Za-z][A-Za-z0-9 ]*)?)\*\* (.+)$", line)
        if not m:
            continue
        bold, rest = m.group(1), m.group(2).strip()
        # "REV01 Tours" → id REV01, title "Tours — …"
        if " " in bold:
            rid, tail = bold.split(" ", 1)
            title = tail + " \u2014 " + rest.lstrip("\u2014 ").strip()
        else:
            rid, title = bold, rest
        if rid in seen:
            continue
        # Retired / resolved items are out of scope for the tracker.
        if title.startswith("~~") or "\u2705" in title or re.search(
                r"\b(hecho|retirado|done)\b", title, re.I):
            continue
        seen.add(rid)
        category, domain, typ, phase, field, state, subcat, labels = classify(rid, title)
        phase = PHASE_FOLD.get(phase, phase)  # five phases only: legacy F0 / Next → F1 / F5
        kind, origin = origin_of(heading)
        rows.append({
            "id": rid,
            "title": title,
            "state": state,
            "labels": labels or [domain],
            "milestone": phase,
            "field": field,
            "source": "standards",
            "updated": "2026-11-19",
            "phase": phase,
            "category": category,
            "domain": domain,
            "subtab": subtab_for(category, domain),
            "section": section_for(category, domain),
            "type": typ,
            "subcategory": subcat,
            "fields": [],
            "choice": "directo",
            # Final referrer: the canonical Work filter for this entry's
            # category, as an absolute flove.org route.
            "refs": [{"label": "Work · " + AXES_BY_SLUG[category]["label"],
                      "url": "https://flove.org/development/index.html#work?tab=docs"+
                             "&view=r2&subtab=work&category=" + category}],
            "kind": kind,
            "origin": origin,
        })
    rows.sort(key=lambda r: r["id"])
    return rows


# A stage-matrix milestone is filed under the `levels` tab of its axis; the
# three sections without one use their closest canonical section instead.
DEGREE_SECTION = {"backend": "systems", "data": "index", "docs": "plan"}
DEGREE_STATE = {"on": "S5", "part": "S3", "todo": "S1"}


def work_refs(category, section, label, deps=()):
    """Dependency links first; the absolute Work filter is always the last one."""
    base = ("https://flove.org/development/index.html#work?tab=docs"
            "&view=r2&subtab=work&category=" + category)
    refs = [{"label": "Depends on " + str(d),
             "url": base + "&q=" + quote(str(d))} for d in deps]
    if section:
        base += "&section=" + section
    refs.append({"label": label, "url": base})
    return refs


def build_features(rows):
    """The complete Work register: every degree milestone (recycled seed plus
    the subsection-tagged ones from milestones.json), the 37 new debate tickets,
    and the 75 pendings rows. Each item carries category, subsection, state and
    phase; dependencies become links before the final absolute Work filter.
    PROC-10 adds `choice` so Work can filter by question depth."""
    register = MILESTONES or {}
    by_hito = {m.get("id"): m for m in projection.hitos(register)}
    ci = projection.ChoiceIndex(register)
    out = []
    for deg in DEGREES:
        axis = deg["section"]
        fallback = DEGREE_SECTION.get(axis, "levels")
        for i, lv in enumerate(deg["levels"]):
            phase = PHASES[min(i, len(PHASES) - 1)]
            for j, ft in enumerate(lv.get("features", [])):
                st = ft.get("state", "todo")
                state = DEGREE_STATE.get(st, "S1")
                section = ft.get("section") or fallback
                deps = list(ft.get("depends_on") or [])
                kept = bool(ft.get("keep"))
                tasks = list(ft.get("tasks") or [])
                # Q152: the Work Effort filter exposes archived + the
                # five efforts a hito's tasks carry, in canonical order.
                cats = []
                if any(t.get("state") == "hecha" for t in tasks):
                    cats.append("archived")
                cats += [e for e in EFFORTS
                         if any(t.get("effort") == e for t in tasks)]
                out.append({
                    "id": "DF-%s-%d-%02d" % (axis[:4].upper(), i + 1, j + 1),
                    "title": ft["en"],
                    "title_es": ft["es"],
                    "state": state,
                    "labels": [STAGE_NAMES[min(i, len(STAGE_NAMES) - 1)], section],
                    "milestone": phase,
                    "field": axis,
                    "source": "standards",
                    "doc": ft.get("doc"),
                    "ticket": ft.get("ticket"),
                    "depends_on": deps,
                    "standards": list(ft.get("standards") or []),
                    "updated": "2026-11-20",
                    "hito_id": ft.get("hito_id"),
                    "hito_stage": ft.get("hito_stage"),
                    "tasks": tasks,
                    "taskcat": cats,
                    "choice": ci.hito_class(by_hito[ft["hito_id"]])
                    if ft.get("hito_id") in by_hito else "directo",
                    "needs_split": bool(ft.get("needs_split")),
                    "phase": phase,
                    "category": axis,
                    "domain": section,
                    "subtab": subtab_for_section(axis, section),
                    "section": section,
                    "type": "feature" if kept else "question",
                    "subcategory": state,
                    "fields": [],
                    "refs": work_refs(axis, section,
                                      "Work · " + AXES_BY_SLUG[axis]["label"], deps),
                    "kind": "feature" if kept else "review",
                    "origin": "stage-matrix" if kept else "debate",
                })
    for t in (MILESTONES or {}).get("new_tickets", []):
        cat, section = t["category"], t["section"]
        phase = STAGE_TO_PHASE.get(t.get("stage"), t.get("stage") or "F1")
        state = t.get("state", "S1")
        deps = list(t.get("deps") or [])
        out.append({
            "id": t["id"],
            "title": t["title_en"],
            "title_es": t["title_es"],
            "state": state,
            "labels": [section, "debate"],
            "milestone": phase,
            "field": cat,
            "source": "standards",
            "doc": _doc_path(t.get("source")),
            "ticket": t["id"],
            "choice": "directo",
            "depends_on": deps,
            "updated": "2026-11-20",
            "phase": phase,
            "category": cat,
            "domain": section,
            "subtab": subtab_for_section(cat, section),
            "section": section,
            "type": "question",
            "subcategory": state,
            "fields": [],
            "refs": work_refs(cat, section,
                              "Work · " + AXES_BY_SLUG[cat]["label"], deps),
            "kind": "review",
            "origin": "debate",
        })
    out.extend(rows)
    out.sort(key=lambda r: (r["category"], r["id"]))
    return out


def build_archive():
    """Compact page-facing projection of tasks_archive for the Work archive.

    The embedded block is the offline fallback; common.json carries the same
    ids for the page join. Both come from register_projection, never hand-edited.
    """
    return projection.archive_projection(MILESTONES or {}, detailed=True)


def canonical():
    rows = build_rows()
    return {
        "schema": "flove-work/1",
        "generated": "2026-11-20",
        "snapshot": "Gitea flove · development/wiki/work/pendings.md",
        "tabs": TABS,
        "sections": AXES,
        "phases": PHASES,
        "levels": LEVELS,
        "glyphs": GLYPH,
        "stageNames": STAGE_NAMES,
        "degrees": DEGREES,
        "groups": ["phase", "field", "source", "category", "subtab",
                   "domain", "type", "subcategory", "kind", "origin",
                   "section", "taskcat", "choice"],
        "rows": rows,
        "procedures": procedures_source.load(),
        "queuePolicy": projection.queue_policy(MILESTONES or {}),
        "archive": build_archive(),
        "skillCategories": SKILL_CATEGORIES,
        "skills": build_skill_registry(),
        # Work shows the whole register: degree milestones + pendings rows.
        "features": build_features(rows),
    }


def extract_block(html):
    i = html.find(BEGIN)
    j = html.find(END, i + len(BEGIN))
    if i < 0 or j < 0:
        return None, None
    inner = html[i + len(BEGIN):j].strip()
    if not inner.startswith(SCRIPT_OPEN) or not inner.endswith(SCRIPT_CLOSE):
        return None, None
    raw = inner[len(SCRIPT_OPEN):-len(SCRIPT_CLOSE)]
    return (i, j + len(END)), raw


MOVES_INBOX = ROOT / "wiki/work/work-moves.json"
COUNT_MIRRORS = [
    "standards/README.md",
    "wiki/INDEX.md",
    "wiki/work/measures.md",
]


def sync_archived_count(old: int, new: int) -> None:
    """Update the mirrored archive count in this gate and the three MDs."""
    if old == new:
        return
    targets = [Path(__file__).resolve()] + [ROOT / p for p in COUNT_MIRRORS]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        if str(old) not in text:
            continue
        path.write_text(text.replace(str(old), str(new)), encoding="utf-8")


def apply_moves(path: Path, commit: bool = False) -> None:
    """Fold a reviewed Work export into the register, 1 move + 1 replacement.

    The 7/8-tasks-per-open-hito shape is a gate, so a done task cannot simply be
    removed: PROC-09 requires a fully specified replacement in the same hito.
    The patch is reviewed by committing it to the inbox; this command validates
    it, prints the plan, and only mutates the register with --commit.
    """
    register = projection.load_register()
    try:
        patch = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit("FAIL: cannot read %s: %s" % (path, exc))
    errors = []
    if patch.get("schema") != "flove-work-moves/1":
        errors.append("schema must be flove-work-moves/1")
    moves = patch.get("moves") or []
    replacements = patch.get("replacements") or []
    ids = [m.get("id") for m in moves]
    if not ids or len(ids) != len(set(ids)):
        errors.append("moves must be a non-empty list of unique ids")
    live = projection.live_tasks(register)
    archived = {t.get("id") for t in register.get("tasks_archive") or []}
    by_hito = {m.get("id"): m for m in projection.hitos(register)}
    counts_by_hito = {}
    for move in moves:
        tid = move.get("id")
        if tid not in live:
            errors.append("%s is not a live task" % tid)
            continue
        hito = by_hito.get(move.get("hito_id") or live[tid].get("hito_id"))
        if not hito:
            errors.append("%s has no owning hito" % tid)
            continue
        real_owner = next((h for h in projection.hitos(register)
                           if tid in {t.get("id") for t in (h.get("tasks") or [])}), None)
        if real_owner and real_owner.get("id") != hito.get("id"):
            errors.append("%s: hito_id must be %s" % (tid, real_owner.get("id")))
        counts_by_hito[hito["id"]] = counts_by_hito.get(hito["id"], 0) + 1
    rids = [r.get("id") for r in replacements]
    if len(rids) != len(set(rids)):
        errors.append("replacement ids must be unique")
    if len(replacements) != len(moves):
        errors.append("PROC-09: one fully specified replacement per move (%d/%d)"
                      % (len(replacements), len(moves)))
    repl_by_hito = {}
    for repl in replacements:
        rid, hid = repl.get("id"), repl.get("hito_id")
        if rid in live or rid in archived:
            errors.append("replacement %s already exists" % rid)
        if hid not in counts_by_hito:
            errors.append("replacement %s targets a hito with no move" % rid)
        if repl.get("stage") not in STAGE_NAMES or repl.get("effort") not in EFFORTS:
            errors.append("replacement %s needs a canonical stage and effort" % rid)
        if not str(repl.get("en") or "").strip() or not str(repl.get("es") or "").strip():
            errors.append("replacement %s needs en/es titles" % rid)
        if not str(((repl.get("evidence") or {}).get("gaps") or [""])[0]).strip():
            errors.append("replacement %s needs a done criterion" % rid)
        if (repl.get("evidence") or {}).get("by") != "optimizy":
            errors.append("replacement %s needs evidence.by = optimizy" % rid)
        if repl.get("state") not in (None, "pendiente"):
            errors.append("replacement %s must start as pendiente" % rid)
        valid_deps = set(live) - set(ids) | set(rids)
        bad = [d for d in (repl.get("depends_on") or []) if d not in valid_deps]
        if bad:
            errors.append("replacement %s has bad depends_on: %s" % (rid, bad))
        repl_by_hito[hid] = repl_by_hito.get(hid, 0) + 1
    for hid, n in counts_by_hito.items():
        if repl_by_hito.get(hid, 0) != n:
            errors.append("%s: %d move(s) need %d replacements, got %d"
                          % (hid, n, n, repl_by_hito.get(hid, 0)))
    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)
    print("plan: %d move(s) -> tasks_archive, %d replacement(s) -> open hitos"
          % (len(moves), len(replacements)))
    for move in moves:
        print("  done   %s (%s)" % (move["id"], move.get("hito_id")))
    for repl in replacements:
        print("  add    %s (%s)" % (repl["id"], repl.get("hito_id")))
    if not commit:
        print("dry run — re-run with --commit to write the register")
        return
    reasons = ((register.get("taskSet") or {}).get("archive_reasons") or {})
    reason = reasons.get("done", "Done in Work")
    today = date.today().isoformat()
    for move in moves:
        hid = move["hito_id"]
        hito = by_hito[hid]
        task = next(t for t in hito["tasks"] if t.get("id") == move["id"])
        hito["tasks"] = [t for t in hito["tasks"] if t.get("id") != move["id"]]
        archived_task = dict(task)
        archived_task.update({
            "state": "hecha",
            "hito_id": hid,
            "closed_reason": reason,
            "closed_on": move.get("moved_on") or today,
        })
        register["tasks_archive"].append(archived_task)
    for repl in replacements:
        task = {k: repl.get(k) for k in ("id", "en", "es", "stage", "effort", "state")
                if k in repl}
        task["evidence"] = repl.get("evidence") or {}
        task["depends_on"] = list(repl.get("depends_on") or [])
        by_hito[repl["hito_id"]]["tasks"].append(task)
    ts = register["taskSet"]
    ts["live"] = len(projection.live_tasks(register))
    ts["archived"] = len(register["tasks_archive"])
    MILESTONES_FILE.write_text(json.dumps(register, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    globals()["MILESTONES"] = register
    apply_milestones(DEGREES, register)
    old_archived = EXPECTED_ARCHIVED
    sync_archived_count(old_archived, ts["archived"])
    globals()["EXPECTED_ARCHIVED"] = ts["archived"]
    subprocess.run([sys.executable, str(ROOT / "scripts/build-common.py"), "--build"],
                   check=True, cwd=ROOT)
    do_build()
    path.unlink()
    print("committed: live %d, archived %d; %s consumed"
          % (ts["live"], ts["archived"], path.name))


def do_build():
    data = canonical()
    body = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
    block = BEGIN + "\n" + SCRIPT_OPEN + "\n" + body + "\n" + SCRIPT_CLOSE + "\n" + END
    html = HTML.read_text(encoding="utf-8")
    span, _ = extract_block(html)
    if span:
        html = html[:span[0]] + block + html[span[1]:]
    else:
        anchor = '<div data-webpanel-content="work" id="home-work" hidden>'
        if anchor not in html:
            sys.exit("work panel anchor not found")
        html = html.replace(anchor, anchor + "\n" + block, 1)
    HTML.write_text(html, encoding="utf-8")
    print("built %d rows into %s" % (len(data["rows"]), HTML.relative_to(ROOT.parent)))


def do_check():
    html = HTML.read_text(encoding="utf-8")
    span, raw = extract_block(html)
    if not span:
        sys.exit("FAIL: canonical block not found in " + str(HTML))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit("FAIL: invalid JSON: %s" % e)
    errors = []
    files, headings = load_heading_slugs()
    if data.get("schema") != "flove-work/1":
        errors.append("bad schema")
    if data.get("tabs") != TABS:
        errors.append("tabs must be the 6 canonical names")
    m_axis = [a.get("section") for a in (MILESTONES or {}).get("sections", [])]
    if m_axis != TABS:
        errors.append("milestones.json sections must follow TABS order exactly")
    if data.get("sections") != AXES:
        errors.append("sections must be the 6 planned categories and their domain sub-tabs")
    if data.get("phases") != PHASES:
        errors.append("phases must be F1-F5")
    if set(data.get("levels", {})) != set(LEVELS):
        errors.append("levels must be S1-S5")
    stages = data.get("stageNames", [])
    if stages != STAGE_NAMES:
        errors.append("stageNames must be seed/infant/mature/grown/full")
    degs = data.get("degrees", [])
    if [d.get("section") for d in degs] != TABS:
        errors.append("degrees must cover the 6 sections in canonical order")
    for d in degs:
        levels = d.get("levels", [])
        if len(levels) != 5:
            errors.append("%s: 5 stage levels required" % d.get("section"))
        for lv in levels:
            if lv.get("stage") not in STAGE_LABELS:
                errors.append("%s: bad stage label %r" % (d.get("section"), lv.get("stage")))
            for k in ("theme", "note"):
                if not lv.get(k):
                    errors.append("%s/%s: missing %s" % (d.get("section"), lv.get("stage"), k))
            note = lv.get("note") or {}
            if not all(note.get(x) for x in ("es", "en")):
                errors.append("%s/%s: bilingual note required" % (d.get("section"), lv.get("stage")))
            benefit = lv.get("benefit") or {}
            if not all(benefit.get(x) for x in ("es", "en")):
                errors.append("%s/%s: bilingual one-word benefit required"
                              % (d.get("section"), lv.get("stage")))
            for ft in lv.get("features", []):
                if ft.get("state") not in ("on", "part", "todo"):
                    errors.append("%s/%s: bad feature state" % (d.get("section"), lv.get("stage")))
                if not all(ft.get(x) for x in ("es", "en")):
                    errors.append("%s/%s: bilingual feature required" % (d.get("section"), lv.get("stage")))
    for lang in ("es", "en"):
        words = [(lv.get("benefit") or {}).get(lang)
                 for d in data.get("degrees", []) for lv in d.get("levels", [])]
        if len(words) != len(set(words)):
            errors.append("stage benefits must be unique in " + lang)
        if any(len(str(w).split()) != 1 for w in words):
            errors.append("stage benefits must be one word in " + lang)
    rows = data.get("rows", [])
    if not rows:
        errors.append("no rows")
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")
    required = ["id", "title", "state", "labels", "milestone", "field", "source",
                "updated", "phase", "category", "subtab", "section", "domain",
                "type", "subcategory", "fields", "refs"]
    for r in rows:
        rid = r.get("id", "?")
        for k in required:
            if k not in r:
                errors.append("%s: missing %s" % (rid, k))
        if r.get("category") not in TABS:
            errors.append("%s: bad category %r" % (rid, r.get("category")))
        cat = r.get("category")
        valid_subtabs = [d["id"] for d in AXES_BY_SLUG.get(cat, {}).get("domains", [])]
        if r.get("subtab") not in valid_subtabs:
            errors.append("%s: bad subtab %r for %s" % (rid, r.get("subtab"), cat))
        if r.get("section") not in valid_sections(cat):
            errors.append("%s: bad section %r for %s" % (rid, r.get("section"), cat))
        elif subtab_for_section(cat, r.get("section")) != r.get("subtab"):
            errors.append("%s: section %r does not belong to subtab %r"
                          % (rid, r.get("section"), r.get("subtab")))
        if r.get("phase") not in PHASES:
            errors.append("%s: bad phase %r" % (rid, r.get("phase")))
        if r.get("subcategory") not in LEVELS:
            errors.append("%s: bad subcategory %r" % (rid, r.get("subcategory")))
        if not isinstance(r.get("fields"), list):
            errors.append("%s: fields[] must be a list" % rid)
    feats = data.get("features", [])
    n_milestones = sum(len(lv.get("features", []))
                       for d in degs for lv in d.get("levels", []))
    n_new = len((MILESTONES or {}).get("new_tickets", []))
    if len(feats) != n_milestones + len(rows) + n_new:
        errors.append("features must be %d milestones + %d debate tickets + %d rows"
                      % (n_milestones, n_new, len(rows)))
    if n_milestones != EXPECTED_MILESTONES:
        errors.append("expected %d milestones, got %d"
                      % (EXPECTED_MILESTONES, n_milestones))
    if n_new != EXPECTED_TICKETS:
        errors.append("expected %d debate tickets, got %d" % (EXPECTED_TICKETS, n_new))
    if len(rows) != EXPECTED_ROWS:
        errors.append("expected %d pendings rows, got %d" % (EXPECTED_ROWS, len(rows)))
    for d in degs:
        for lv in d.get("levels", []):
            for ft in lv.get("features", []):
                if not ft.get("hito_id") or (not ft.get("tasks") and ft.get("state") not in ("on", "S5")):
                    errors.append("milestone feature %s lacks hito_id or tasks"
                                  % ft.get("en", "?"))
    fids = [f.get("id") for f in feats]
    if len(fids) != len(set(fids)):
        errors.append("duplicate feature ids")
    # Every one of the 30 subsections needs a milestone per titled part; a part id
    # without parts is its own section.
    for a in (MILESTONES or {}).get("sections", []):
        valid = required_sections(a["section"])
        subs = a.get("subsections", [])
        if len(subs) != 5:
            errors.append("%s: 5 stage subsections required" % a["section"])
        for box in subs:
            ms = box.get("milestones", [])
            if not ms:
                errors.append("%s/%s: at least 1 milestone required"
                              % (a["section"], box.get("ladder")))
            covered = {m.get("section") for m in ms}
            for sid in valid:
                if sid not in covered:
                    errors.append("%s/%s: missing subsection %s"
                                  % (a["section"], box.get("ladder"), sid))
    known = set(ids) | set(fids)
    # Q145: the group-label ticket field is gone; the opaque id is the only key.
    for a in (MILESTONES or {}).get("sections", []):
        for box in a.get("subsections", []):
            for m in box.get("milestones", []):
                if m.get("id"):
                    known.add(m["id"])
    edges = {f.get("id"): list(f.get("depends_on") or []) for f in feats}
    for a in (MILESTONES or {}).get("sections", []):
        for box in a.get("subsections", []):
            for m in box.get("milestones", []):
                key = m.get("id")
                if key:
                    edges[key] = list(m.get("depends_on") or [])
    for t in (MILESTONES or {}).get("new_tickets", []):
        edges[t["id"]] = list(t.get("deps") or [])
    for f in feats:
        for dep in f.get("depends_on") or []:
            if dep not in known:
                errors.append("%s: unknown dependency %s" % (f.get("id"), dep))
        refs = f.get("refs") or []
        if not refs or not str(refs[-1].get("url", "")).startswith(
                "https://flove.org/development/index.html#work?"):
            errors.append("%s: final referrer must be an absolute Work route"
                          % f.get("id"))
    for f in feats:
        fid = f.get("id", "?")
        for k in required:
            if k not in f:
                errors.append("%s: missing %s" % (fid, k))
        if f.get("hito_id"):
            tt = f.get("tasks") or []
            want = []
            if any(t.get("state") == "hecha" for t in tt):
                want.append("archived")
            want += [e for e in EFFORTS
                     if any(t.get("effort") == e for t in tt)]
            if f.get("taskcat") != want:
                errors.append("%s: taskcat %r differs from task data %r"
                              % (fid, f.get("taskcat"), want))
        if f.get("choice") not in projection.CHOICE_CLASSES:
            errors.append("%s: bad choice %r" % (fid, f.get("choice")))
        if f.get("category") not in TABS:
            errors.append("%s: bad category %r" % (fid, f.get("category")))
        valid_subtabs = [d["id"] for d in AXES_BY_SLUG.get(
            f.get("category"), {}).get("domains", [])]
        if f.get("section") not in valid_sections(f.get("category")):
            errors.append("%s: bad section %r" % (fid, f.get("section")))
        if f.get("phase") not in PHASES:
            errors.append("%s: bad phase %r" % (fid, f.get("phase")))
        if f.get("subcategory") not in LEVELS:
            errors.append("%s: bad subcategory %r" % (fid, f.get("subcategory")))
        for u in f.get("standards") or []:
            check_standard_url(u, files, headings, fid, errors)
        if f.get("title_es") and not f.get("title"):
            errors.append("%s: bilingual feature needs title" % f.get("id"))
    skills = data.get("skills") or []
    if len(skills) != 21:
        errors.append("expected 21 skills in the canonical registry")
    # Skills chips, rows and registry must agree on category and count.
    chips = {}
    for cat, num in re.findall(r'data-filter="skill:([a-z]+)">[^<]*·\s*(\d+)</button>', html):
        chips[cat] = int(num)
    if sorted(chips) != sorted(SKILL_CATEGORIES):
        errors.append("skill chips must match SKILL_CATEGORIES: %s" % sorted(chips))
    by_cat = {}
    for sk in skills:
        c = sk.get("category")
        by_cat[c] = by_cat.get(c, 0) + 1
    for cat in SKILL_CATEGORIES:
        if chips.get(cat) != by_cat.get(cat, 0):
            errors.append("skill chip %s says %s, registry has %s"
                          % (cat, chips.get(cat), by_cat.get(cat, 0)))
    skill_rows = re.findall(
        r'<tr data-type="skill" data-cat="([a-z]+)" data-skillcat="([a-z]+)"', html)
    if len(skill_rows) != len(skills):
        errors.append("expected %d skill rows in the page, found %d"
                      % (len(skills), len(skill_rows)))
    for cat, skillcat in skill_rows:
        if cat != skillcat or cat not in SKILL_CATEGORIES:
            errors.append("skill row category mismatch: %s / %s" % (cat, skillcat))
    claimed = {}
    for sk in skills:
        cat = sk.get("category")
        if cat not in SKILL_CATEGORIES:
            errors.append("%s: bad skill category %r" % (sk.get("name"), cat))
        for u in sk.get("checker_of") or []:
            check_standard_url(u, files, headings, sk.get("name"), errors)
            if u in claimed:
                errors.append("standard %s has two checkers: %s and %s"
                              % (u, claimed[u], sk.get("name")))
            claimed[u] = sk.get("name")
    # Q091–Q141: every hito owns an opaque id, a stage and coherent tasks.
    stages = (MILESTONES or {}).get("stageNames") or []
    all_hitos = [m for a in (MILESTONES or {}).get("sections", [])
                 for box in a.get("subsections", [])
                 for m in box.get("milestones", [])]
    task_ids = {t.get("id") for m in all_hitos for t in (m.get("tasks") or [])}
    if len(task_ids) != EXPECTED_TASKS:
        errors.append("expected %d live tasks, got %d" % (EXPECTED_TASKS, len(task_ids)))
    archived = list((MILESTONES or {}).get("tasks_archive") or [])
    archive_ids = {t.get("id") for t in archived}
    if len(archive_ids) != EXPECTED_ARCHIVED:
        errors.append("expected %d archived tasks, got %d"
                      % (EXPECTED_ARCHIVED, len(archive_ids)))
    if archive_ids & task_ids:
        errors.append("live and archived task ids overlap")
    embedded_ids = {t.get("id") for t in (data.get("archive") or [])}
    if embedded_ids != archive_ids:
        errors.append("embedded Work archive ids differ from tasks_archive")
    policy = data.get("queuePolicy") or {}
    want_policy = projection.queue_policy(MILESTONES or {})
    if policy != want_policy:
        errors.append("embedded queuePolicy differs from milestones.json taskSet")
    else:
        hard, rec, low = (policy.get("hardCap"), policy.get("recommendedMax"),
                          policy.get("replenishBelow"))
        if hard != EXPECTED_TASKS:
            errors.append("queuePolicy hardCap %r != expected %d"
                          % (hard, EXPECTED_TASKS))
        if not isinstance(rec, int) or not isinstance(hard, int) or rec > hard:
            errors.append("queuePolicy recommendedMax must be <= hardCap")
        if not isinstance(low, int) or not isinstance(rec, int) or low >= rec:
            errors.append("queuePolicy replenishBelow must be below recommendedMax")
        if isinstance(rec, int) and isinstance(hard, int) and "headroom" in policy:
            if policy.get("headroom") != hard - rec:
                errors.append("queuePolicy headroom must be hardCap - recommendedMax")
        if (not isinstance(policy.get("activeWindowFloor"), int)
                or not isinstance(policy.get("activeWindow"), int)
                or policy["activeWindowFloor"] > policy["activeWindow"]):
            errors.append("queuePolicy activeWindowFloor must be <= activeWindow")
    task_set = (MILESTONES or {}).get("taskSet") or {}
    if task_set.get("live") != len(task_ids) or task_set.get("archived") != len(archive_ids):
        errors.append("taskSet live/archived counts differ from the register")
    known_reasons = set((task_set.get("archive_reasons") or {}).keys())
    used_reasons = {projection.reason_code(t.get("closed_reason")) for t in archived}
    if used_reasons - known_reasons:
        errors.append("unknown archive reason code(s): %s"
                      % ", ".join(sorted(used_reasons - known_reasons)))
    for a in (MILESTONES or {}).get("sections", []):
        for box in a.get("subsections", []):
            for m in box.get("milestones", []):
                if not m.get("id"):
                    errors.append("hito %s has no id" % m.get("id", "?"))
                if m.get("stage") not in stages:
                    errors.append("hito %s has bad stage %r"
                                  % (m.get("id"), m.get("stage")))
                if m.get("state_mirror") != m.get("state"):
                    errors.append("hito %s: state_mirror %r differs from state %r"
                                  % (m.get("id"), m.get("state_mirror"),
                                     m.get("state")))
                if m.get("needs_split"):
                    errors.append("hito %s still flagged needs_split"
                                  % m.get("id"))
                tasks = m.get("tasks") or []
                if m.get("state") == "on":
                    if tasks:
                        errors.append("closed hito %s still has %d tasks"
                                      % (m.get("id"), len(tasks)))
                else:
                    want = 8 if m.get("stage") in ("grown", "full") else 7
                    if len(tasks) != want:
                        errors.append("open hito %s has %d tasks, expected %d"
                                      % (m.get("id"), len(tasks), want))
                note = m.get("notes") or ""
                for marker in ("Deliverable:", "Done when", "Decision:"):
                    if note.count(marker) != 1:
                        errors.append("hito %s: %s appears %d times"
                                      % (m.get("id"), marker, note.count(marker)))
                for t in tasks:
                    if t.get("stage") not in stages:
                        errors.append("%s: task %s has bad stage"
                                      % (m.get("id"), t.get("id")))
                    if t.get("state") not in ("hecha", "parcial", "pendiente"):
                        errors.append("%s: task %s has bad state"
                                      % (m.get("id"), t.get("id")))
                    if t.get("evidence", {}).get("by") != "optimizy":
                        errors.append("%s: task %s evidence is not by optimizy"
                                      % (m.get("id"), t.get("id")))
                    if not (t.get("evidence", {}).get("gaps") or [""])[0].strip():
                        errors.append("%s: task %s has no done criterion"
                                      % (m.get("id"), t.get("id")))
                    if t.get("effort") not in EFFORTS:
                        errors.append("%s: task %s has bad effort %r"
                                      % (m.get("id"), t.get("id"), t.get("effort")))
                    for dep in t.get("depends_on") or []:
                        if dep not in task_ids:
                            errors.append("%s: task %s has unknown task dependency %s"
                                          % (m.get("id"), t.get("id"), dep))
                for dep in m.get("depends_on") or []:
                    if dep not in known:
                        errors.append("%s: dependency %s is not a hito id"
                                      % (m.get("id"), dep))
    # Q130/Q143: C6 state inversions are registered exceptions, not a gate.
    hito_state = {m.get("id"): m.get("state") for m in all_hitos}
    state_rank = {"todo": 0, "part": 1, "on": 2}
    inversions = sorted(
        "%s←%s" % (m.get("id"), dep)
        for m in all_hitos for dep in (m.get("depends_on") or [])
        if state_rank.get(m.get("state"), -1) >
           state_rank.get(hito_state.get(dep), -1))
    if len(inversions) != 7:
        print("WARN: C6 exceptions changed (%d, expected 7): %s"
              % (len(inversions), ", ".join(inversions)))
    # Stage IDs are retired from hitos; the PROC policy lives in AGENTS.md only.
    if (MILESTONES or {}).get("procedures"):
        errors.append("milestones.json still has a procedures block; source it in AGENTS.md")
    for a in (MILESTONES or {}).get("sections", []):
        for box in a.get("subsections", []):
            for m in box.get("milestones", []):
                if m.get("procedures"):
                    errors.append("%s/%s: hito still has retired procedures[]"
                                  % (a.get("section"), m.get("id", "?")))
    procs = procedures_source.load()
    if not procs:
        errors.append("missing procedures in AGENTS.md")
    if data.get("procedures") != procs:
        errors.append("embedded procedures differ from AGENTS.md")
    proc_ids = []
    for proc in procs:
        pid = proc.get("id", "?")
        proc_ids.append(pid)
        for key in PROCEDURE_FIELDS:
            if not str(proc.get(key) or "").strip():
                errors.append("%s: missing procedure field %s" % (pid, key))
        check_standard_url(proc.get("standard"), files, headings, pid, errors)
        if claimed.get(proc.get("standard")) != proc.get("checker"):
            errors.append("%s: checker %s does not own %s"
                          % (pid, proc.get("checker"), proc.get("standard")))
    if len(proc_ids) != len(set(proc_ids)):
        errors.append("duplicate procedure ids")
    state = {}
    def visit(n):
        if state.get(n) == 1:
            return True
        if state.get(n) == 2:
            return False
        state[n] = 1
        for d in edges.get(n, []):
            if d in edges and visit(d):
                return True
        state[n] = 2
        return False
    cycles = [n for n in edges if visit(n)]
    if cycles:
        errors.append("dependency cycle(s): " + ", ".join(sorted(cycles)))
    # Q140/Q143: task loops are an exception, never a gate — warn and continue.
    task_edges = {t.get("id"): [d for d in (t.get("depends_on") or [])
                               if d in task_ids]
                  for m in all_hitos for t in (m.get("tasks") or [])}
    tstate = {}
    def tvisit(n):
        if tstate.get(n) == 1:
            return True
        if tstate.get(n) == 2:
            return False
        tstate[n] = 1
        for d in task_edges.get(n, []):
            if tvisit(d):
                return True
        tstate[n] = 2
        return False
    task_cycles = [n for n in task_edges if tvisit(n)]
    if task_cycles:
        print("WARN: task dependency cycle(s): " + ", ".join(sorted(task_cycles)))
    check_markdown_anchors(files, headings, errors)
    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)
    print("OK: %d features (%d milestones + %d debate tickets + %d rows), "
          "%d live + %d archived tasks, %d tabs, %d groups, schema %s"
          % (len(feats), n_milestones, n_new, len(rows), len(task_ids),
             len(archive_ids), len(TABS), len(data["groups"]), data["schema"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true", help="regenerate the canonical block")
    g.add_argument("--check", action="store_true", help="validate the embedded block")
    g.add_argument("--apply-moves", nargs="?", const=str(MOVES_INBOX), metavar="PATCH",
                   help="validate a reviewed Work export (dry run unless --commit)")
    ap.add_argument("--commit", action="store_true", help="write with --apply-moves")
    args = ap.parse_args()
    if args.apply_moves:
        if args.commit and not Path(args.apply_moves).exists():
            ap.error("no patch at %s" % args.apply_moves)
        apply_moves(Path(args.apply_moves), args.commit)
    elif args.build:
        do_build()
    else:
        do_check()
