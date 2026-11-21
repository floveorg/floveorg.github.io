#!/usr/bin/env bash
# AGENTS · ideas — checklist on screen (kdialog). Writes selected tags to
# ${TMPDIR:-/tmp}/agents-selection.txt, one per line.
set -euo pipefail
OUT="${TMPDIR:-/tmp}/agents-selection.txt"
if ! command -v kdialog >/dev/null 2>&1; then
  echo "kdialog not found" >&2; exit 1
fi
sel=$(kdialog --title "AGENTS · ideas" \
  --checklist "Marca las ideas que quieres añadir (varias posibles)" \
  --separate-output \
  2  "Verificación · Probar antes de decir hecho" off \
  3  "Verificación · Si no se verificó, decirlo" off \
  4  "Verificación · UI: render real" off \
  6  "Respuesta · Resultado primero" off \
  7  "Respuesta · Sin hype ni relleno" off \
  8  "Respuesta · Rutas exactas" off \
  10 "Decisiones · Doc dueño" off \
  11 "Decisiones · Registrar lo que queda" off \
  13 "Estándares · Gate/test" off \
  14 "Estándares · Si no se puede comprobar" off \
  16 "Publicación · No publicar sin pedirlo" off \
  17 "Publicación · sw.js solo en updaty4" off \
  19 "Contexto · Leer doc dueño" off \
  20 "Contexto · No sobrescribir cambios ajenos" off \
  21 "Contexto · Citar la fuente" off \
  23 "Rutas · URL completa desde skills" off \
  24 "Rutas · No romper al mover" off) || { printf 'cancelado\n' > "$OUT"; exit 0; }
printf '%s\n' "$sel" > "$OUT"
kdialog --title "AGENTS · ideas" --msgbox "Guardado en:\n$OUT\n\n$sel" 12 70 || true
