# flove — agent context

**Working directory:** Always `/home/kdeneon/Documents/flove` — never other flove
folders (e.g. `flove-apk`).

## How to work with me

1. Duplicados
   1.1 Unir o borrar; no añadir un tercero
   1.2 Si no hay solución práctica, preguntar
   1.3 Si un cambio duplica o añade bloat, revertir y decirlo
2. Propiedad
   2.1 Buscar el dueño del hecho antes de crear un doc o sección
3. Estándares y skills
   3.1 El estándar lleva el detalle
   3.2 La skill lo referencia
   3.3 Nombres canónicos: Data Depth, Apps, Tree/Types, whole/; no sinónimos
4. Niveles
   4.1 `<skill>N` = 1 → N, acumulativos, para en N
   4.2 Sin número → multiselect
   4.3 Separar mínimo / función / craft
5. Tablas
   5.1 Una tabla vive en su fuente
   5.2 Si otra doc la necesita, exportarla; no reescribirla
   5.3 Retirado → `debates/archive.md`
   5.4 Datos reales: leer la fuente (docs/index, development/index, routing.json); si falta, N/A o missing; no inventar filas, apps ni paradigmas
6. Rutas
   6.1 Tras un traslado, actualizar todas las referencias
   6.2 Una corrección se aplica en todos los sitios, no solo en el archivo actual
7. Mapas
   7.1 AGENTS = cómo trabajo
   7.2 README = qué hay
   7.3 worldview = porqué + mapa
   7.4 contract = reglas
   7.5 No repetir el mismo mapa
8. Interacción
   8.1 Responder en el idioma del último mensaje
   8.2 Ejecutar; preguntar solo si es destructivo o ambiguo
9. Seguridad
   9.1 No tocar `~/agents` (credenciales)
   9.2 `sw.js` solo en `updaty4`
   9.3 No commit/push sin pedirlo
10. Scripts
   10.1 `tools/` = generalistas
   10.2 `development/scripts/` = específicos + el procedimiento de release (`check-distro.sh`, `publish-web.sh`)
11. Cambios
   11.1 Editar solo lo pedido; no reformatear el resto
   11.2 Si el encargo es amplio, hacer la parte segura y listar lo que queda
   11.3 En tareas grandes, si aparece un conflicto o riesgo en la edición, avisar antes de tocar nada y mostrar las opciones (formato 12.3)
12. Formato
   12.1 Tablas para matrices y comparaciones
   12.2 En documentos, numerar con IDs únicos y jerárquicos: 1, 1.1, 1.2 — no listas planas
   12.3 Sugerencias: cuando pidas ideas o yo te ofrezca acciones concretas (siguientes pasos, opciones, alternativas), presentarlas en el terminal con este formato exacto:
        12.3.1 Numeración continua 1–N; los títulos de sección también llevan número (1, 5, 9…)
        12.3.2 Título de sección: encabezado Markdown `### N. Título` — negrita y color
        12.3.3 Ideas: lista ordenada que continúa la numeración (2, 3, 4…), una por línea
        12.3.4 Una línea en blanco entre secciones
        12.3.5 Al final, aparte del listado, ofréceme una encuesta multiselect como opción adicional si lo ves conveniente
13. Idioma
   13.1 Todo el contenido de `flove/` (apps, webs, docs y código) va en inglés
   13.2 Excepciones en español: `liberada`, `futbolia` y `dinámicas electrónicas`

## Where things live

**Standards index:** `README.md` — what exists and where it is specified.

**Vocabulary:** [`vocabulary/index.html`](vocabulary/index.html) — canonical names,
the field data model and the interactive matrix.

## Editing rule

Integrate new content into the section that already owns the fact — do not add a
new file (or a new section) for every change; a new file only when the fact has no
existing home.

**Voice:** write affirmatively — name what holds and the test that proves it; keep
prohibitions for safety edges.

## Home-directory layout

Retired note: [`debates/archive.md`](debates/archive.md#home-directory-layout).
