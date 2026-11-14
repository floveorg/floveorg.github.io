#!/usr/bin/env bash
# narrate.sh — quick Piper + music-opener + ffmpeg narration.
#
# Usage:
#   scripts/narrate.sh clean-text.txt
#   scripts/narrate.sh clean-text.txt -o chapter-3.mp3 -v es_ES-davefx-medium
#   cat text.txt | scripts/narrate.sh - -o narration.mp3 --no-music
#
# The input should already be cleaned (plain text, one paragraph per line).
# The script preflights Piper, ffmpeg, the chosen voice and mkmusic.py, then:
#   music opener (mkmusic.py) + narration (Piper) -> 22050 mono -> MP3 160k.
set -euo pipefail

usage() {
  sed -n '4,11p' "$0" | sed 's/^# \{0,1\}//'
}

TEXT=""
OUT=""
VOICE="${NARRATY_VOICE:-es_ES-carlfm-x_low}"
SPK="${NARRATY_SPEAKER:-}"
MUSIC=1

while [ $# -gt 0 ]; do
  case "$1" in
    -o|--output)  OUT="${2:?missing output path}"; shift 2 ;;
    -v|--voice)   VOICE="${2:?missing voice}"; shift 2 ;;
    -s|--speaker) SPK="${2:?missing speaker id}"; shift 2 ;;
    --no-music)   MUSIC=0; shift ;;
    -h|--help)    usage; exit 0 ;;
    -)            TEXT="-"; shift ;;
    -*)           echo "narrate: unknown option: $1" >&2; usage; exit 2 ;;
    *)            TEXT="$1"; shift ;;
  esac
done

if [ -z "$TEXT" ]; then
  usage >&2
  exit 2
fi

# ── preflight ──────────────────────────────────────────────────────────────
command -v piper >/dev/null || { echo "narrate: piper not found" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "narrate: ffmpeg not found" >&2; exit 1; }
command -v ffprobe >/dev/null || { echo "narrate: ffprobe not found" >&2; exit 1; }
command -v python3 >/dev/null || { echo "narrate: python3 not found" >&2; exit 1; }
python3 -c 'import numpy' 2>/dev/null || { echo "narrate: python3 numpy is required" >&2; exit 1; }

SKILL_DIR="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
MKMUSIC="$SKILL_DIR/scripts/mkmusic.py"
[ -f "$MKMUSIC" ] || { echo "narrate: missing $MKMUSIC" >&2; exit 1; }

VOICES="${PIPER_VOICES:-$HOME/.local/share/piper/voices}"
MODEL="$VOICES/$VOICE.onnx"
[ -f "$MODEL" ] || { echo "narrate: voice model not found: $MODEL" >&2; exit 1; }
[ -f "$MODEL.json" ] || { echo "narrate: voice config not found: $MODEL.json" >&2; exit 1; }

# ── input / output names ───────────────────────────────────────────────────
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [ "$TEXT" = "-" ]; then
  cat > "$WORK/text.txt"
  BASE="narration-$(date +%Y%m%d-%H%M%S)"
  INPUT="$WORK/text.txt"
  DEFAULT_OUT="$PWD/$BASE.mp3"
else
  [ -f "$TEXT" ] || { echo "narrate: input not found: $TEXT" >&2; exit 1; }
  INPUT="$TEXT"
  BASE="$(basename "$TEXT")"
  BASE="${BASE%.*}"
  DEFAULT_OUT="$(cd "$(dirname "$TEXT")" && pwd)/$BASE.mp3"
fi
OUT="${OUT:-$DEFAULT_OUT}"
mkdir -p "$(dirname "$OUT")"

# ── music opener ───────────────────────────────────────────────────────────
if [ "$MUSIC" -eq 1 ]; then
  ( cd "$WORK" && python3 "$MKMUSIC" >/dev/null )
fi

# ── narration ──────────────────────────────────────────────────────────────
PIPER_ARGS=(-q -m "$MODEL" --sentence_silence 0.35 -f "$WORK/speech.raw.wav")
if [ -n "$SPK" ]; then
  PIPER_ARGS=(-s "$SPK" "${PIPER_ARGS[@]}")
fi
piper "${PIPER_ARGS[@]}" < "$INPUT" >/dev/null || {
  echo "narrate: piper failed (check the voice/model and the input text)" >&2
  exit 1
}
[ -s "$WORK/speech.raw.wav" ] || { echo "narrate: piper produced no audio" >&2; exit 1; }

ffmpeg -y -loglevel error -i "$WORK/speech.raw.wav" -ar 22050 -ac 1 "$WORK/speech.wav"

# ── assemble ───────────────────────────────────────────────────────────────
META=(-metadata "title=$BASE" -metadata "artist=Marc (marcflove)"
      -metadata "album=Flove" -metadata "genre=Spoken")

if [ "$MUSIC" -eq 1 ]; then
  ffmpeg -y -loglevel error -i "$WORK/musicA.wav" -ar 22050 -ac 1 "$WORK/music.wav"
  ffmpeg -y -loglevel error -f lavfi -i anullsrc=r=22050:cl=mono -t 0.45 \
    -c:a pcm_s16le "$WORK/gap.wav"
  {
    printf "file '%s'\n" "$WORK/music.wav"
    printf "file '%s'\n" "$WORK/gap.wav"
    printf "file '%s'\n" "$WORK/speech.wav"
  } > "$WORK/list.txt"
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$WORK/list.txt" \
    -c:a libmp3lame -b:a 160k "${META[@]}" "$OUT"
else
  ffmpeg -y -loglevel error -i "$WORK/speech.wav" \
    -c:a libmp3lame -b:a 160k "${META[@]}" "$OUT"
fi

DUR="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT" || true)"
echo "narrate: wrote $OUT${DUR:+ (${DUR}s)}"
