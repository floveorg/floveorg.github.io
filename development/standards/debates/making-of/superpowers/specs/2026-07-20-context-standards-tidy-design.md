# Tidy de `~/Documents/context` — estándares & development

**Fecha:** 2026-07-20 · **Estado:** EJECUTADO.

## Update — chapterizado (dirección final de Marc)

Marc extendió el objetivo: tratar todo `context` como un **libro de capítulos**,
CLAUDE mínimo (solo redirige, no contiene estándares), y un **fichero-matriz
estable** por área desde el que profundizar. Resultado final implementado:

```
flove/standards/
  README.md   ← matriz estable (índice §13.1–14 nombre+1línea+enlace)
  contract.md ← reglas mandatorias (ex CLAUDE §0–8)
  frontend.md ← catálogo §13 completo + regions/elements/impl (ex frontend_standards.md)
  adoption.md ← checklist §14 por-app (tabla viva)
flove/AGENTS.md ← mapa mínimo de redirecciones (sin estándares dentro)
flove/backend_plan.md ← 3999→1884 líneas (§A,§0-12,§15; §13/§14 = puntero)
principles.md ← ex development.md
```

Regla del libro: cada hecho un único hogar; la matriz solo nombra+enlaza (no
diverge); el detalle vive una vez en `frontend.md`. overview §3 y CLAUDE §9
dejaron de re-listar. El detalle de Approach A debajo se conserva como registro.

---

## Problema

Los estándares de frontend viven **duplicados a mano en 4 sitios** y ya han
divergido:

| Fichero | Rol hoy | Estado |
|---------|---------|--------|
| `flove/backend_plan.md §13/§14` | fuente de verdad (según memoria) | al día |
| `flove/AGENTS.md §9` | lista-puntero re-listada | al día |
| `flove/frontend_standards.md` | "consolidated reference" (resumen) | **stale** — falta §13.13, §13.14 |
| `flove/overview.md §3` | tabla-mapa | **stale** — corta en §13.11; §13.10 con casing viejo |

Además: `backend_plan.md` tiene **3999 líneas** que mezclan backend real
(§A, §0–12, §15) con el catálogo de frontend (§13 ≈ 2100 líneas, §14). Y
`development.md` es *principios* de desarrollo, no un blogy/plan — el nombre
confunde.

## Principio rector

**Cada hecho tiene un único hogar; el resto son punteros.** El catálogo de
estándares de frontend deja de estar copiado; vive en un solo fichero y los
demás lo enlazan.

## Diseño (Approach A)

Reparto de responsabilidades tras el tidy:

- **`flove/AGENTS.md`** — el *contrato* mandatorio (§0–8), que se auto-carga.
  Se queda con las reglas inline. §9 pasa a **puntero puro** a
  `frontend_standards.md` (mantiene solo la nota de *trigger keywords* + "busca
  §13.x en frontend_standards.md"); deja de re-listar los 14 estándares.
- **`flove/frontend_standards.md`** — **fuente de verdad completa** del
  frontend. Recibe el §13/§14 **entero** movido desde backend_plan.
  - Part I (contrato) → se reduce a un **puntero** a `AGENTS.md §0–8` (deja de
    duplicar el contrato).
  - Parts III+ → el contenido **completo** de §13, conservando las etiquetas
    `§13.x` para que toda referencia existente siga resolviendo.
  - Part VII = §14 (adoption checklist). Part VIII (migration debt) se mantiene.
- **`flove/backend_plan.md`** — solo backend real (§A, §0–12, §15). §13 y §14 se
  sustituyen por un **puntero de una línea** a frontend_standards.md.
  Objetivo: ~3999 → ~1900 líneas.
- **`flove/overview.md §3`** — sigue siendo un **mapa de lectura** (útil), pero
  con nota *"lista canónica: frontend_standards.md"* y el **drift arreglado**
  (casing §13.10 = `<App> · FLOVE`; añadir §13.12/13/14).
- **`development.md`** → `principles.md` (git mv) + actualizar inbound links.
- **`_sidebar.md`** — reetiquetar para dejar claro el orden de lectura:
  overview → principles → frontend_standards (la biblia) → backend_plan (backend).

## Barrido de referencias

Cambiar `backend_plan.md §13` → `frontend_standards.md §13` en los `.md` que lo
citan: `oasis.md`, `worldview.md`, `overview.md`, `README.md` (y cualquier otro
que aparezca en el grep). Las etiquetas `§13.x` en sí **no cambian** (solo el
fichero que las hospeda), así que las citas "§13.7"-a-secas siguen válidas.

**Memoria a actualizar:** `project_flove_standards_catalog` (§13 ahora vive en
`frontend_standards.md`, no en backend_plan). Marcar la vieja como corregida.

## Plan de ejecución (checklist con verificación)

1. **Mover §13/§14** (backend_plan líneas 1676–3801) → frontend_standards.md.
   - Verificar: `grep -c '§13\.' ` conserva las 14 subsecciones; conteo de
     líneas movidas ≈ 2126; ningún `## 13`/`## 14` queda en backend_plan salvo
     el puntero.
2. **Punteros + drift**: backend_plan §13/§14 → puntero; CLAUDE §9 → puntero;
   frontend_standards Part I → puntero; overview §3 arreglado.
3. **Retoques**: `git mv development.md principles.md` + inbound links;
   `_sidebar.md` reetiquetado; barrido de refs; memoria.
4. **Commit scoped** (nunca `git add -A`) + push a `marc/context` (gitea),
   mensaje con el prompt + explicación.

## No se toca (fuera de alcance)

Contenido de los estándares en sí (solo se reubica), `flovenet/`, `research/`,
`theory/`, `vendor/`, la matrix HTML.
