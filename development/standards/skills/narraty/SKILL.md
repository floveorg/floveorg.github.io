---
name: narraty
description: >-
  Turn any text into a narrated MP3 with local offline tools — a short music
  opener, then the full text in a chosen voice (Piper + numpy + ffmpeg). Use for
  "narrate this", "make an audiobook", "hazme el audio", "léemelo en voz alta".
---

# narraty

Produce a narrated MP3 from a text: a short music opener, then the full text in
the chosen voice. No spoken intro, no summary — just the text that is there.
Everything is **offline**: Piper (TTS) + Python/numpy (music) + ffmpeg
(assembly). No cloud, no API keys.

```
[ music: short warm opener ~4 s ]
[ the full text, read in the chosen voice ]
```

## Output name

Use the target the owner gives. Otherwise derive it from the source:

- **A file** → same basename with `.mp3`, next to the source
  (`chapter-3.md` → `chapter-3.mp3`).
- **Pasted text** → `narration-<short-slug>.mp3` in the current folder.
- **A questy session** → `questy-intro.mp3` — the one reserved exception. Its
  published copy is the R2 object
  `https://pub-e19f5fad18fb474fb6d6c4f91194e333.r2.dev/Shared/audio/questy-advanced-case.mp3`;
  overwrite it only if the owner asks.

Report the path. Do not invent a flove.org upload for other texts, and do not
reuse `questy-intro.mp3` for them.

## Quick path

```bash
development/scripts/narrate.sh clean-text.txt
# -o out.mp3 · -v es_ES-davefx-medium · -s 1 · --no-music
```

The wrapper preflights everything, generates the opener, synthesises, normalises
to 22050 mono and assembles the MP3 (160k, spoken metadata). Pass already-cleaned
text: one paragraph per line.

## Voices

Models live in `~/.local/share/piper/voices/` as `.onnx` + `.onnx.json`; fetch
from `rhasspy/piper-voices` on HuggingFace (or the flove repo mirror) if empty.

| Voice | Notes |
|---|---|
| `es_ES-carlfm-x_low` | ES male — **fast, default** |
| `es_ES-davefx-medium` | ES male |
| `es_ES-sharvard-medium` | multi: `-s 0` male, `-s 1` female |
| `es_MX-ald-medium` | MX male |
| `es_AR-daniela-high` | AR female — **~15× real-time, avoid for long texts** |
| `en_US-lessac-medium` | English original |

No voice picked → offer a **5-voice demo** (each reads the same 2–3 sentences and
self-labels "Voz número N"), let them choose, then narrate. Confirm language
(original vs translation) if ambiguous.

## Preflight

```bash
command -v piper && command -v ffmpeg && command -v python3
ls ~/.local/share/piper/voices/*.onnx 2>/dev/null | head
test -f development/scripts/mkmusic.py
```

Missing `piper`/`ffmpeg` → stop and say what to install. Empty voices folder →
fetch the chosen model first. Missing `mkmusic.py` → run from the repo root.

## Manual path (custom variants)

1. **Clean the text.** Strip Markdown (`> `, `*`, `#`, `---`), collapse blank
   lines to one paragraph per line (Piper speaks one utterance per line, so
   paragraphs get natural pauses). **Omit foreign-language epigraphs** (e.g.
   Latin) that the voice would mangle — keep the translation — and **say what you
   dropped**. Never cut content silently.
2. **Generate the music** with `development/scripts/mkmusic.py` → `musicA.wav`, 22050 Hz mono.
   Tweak key/mood in the script to fit the text's tone.
3. **Synthesise:**
   `echo/‹file› | piper -q -m "$V/<voice>.onnx" -s <spk> --sentence_silence 0.35 -f out.raw.wav`.
   Long text → run it in the background; Piper writes the `-f` WAV only at the very
   end, so a 0-byte file mid-run is normal (check CPU time, not file size). Poll
   with `until grep -q "DONE" …; do sleep 3; done`.
4. **Assemble** with ffmpeg's concat demuxer. Normalise every piece to **22050
   mono first** — x_low voices output 16 kHz, medium/high 22050, and mismatched
   rates break concat. Insert 0.3–0.5 s silences between blocks. Add ID3 metadata
   (`title`/`artist`/`album`/`genre="Spoken"`) and encode
   `-c:a libmp3lame -b:a 160k`.
5. **Deliver** the path, total duration and the block breakdown. Offer variants
   (other voice, English original, split per section, WAV).

## Gotchas

- **`-m` must point at the `.onnx` file.** Passing the stem → "Model file doesn't
  exist" and a core dump.
- **Don't download voice models while Piper is synthesising** → OOM or a 0-byte
  output.
- **`-high` models are ~15× real-time** — steer long texts to medium or x_low.

## questy sessions

The one reserved name. Narrate the answers as a straight read (no intro or
summary) to `questy-intro.mp3`; its published copy is the R2 object
`Shared/audio/questy-advanced-case.mp3`. Every other text gets a source-derived
name; the markdown stays the source of truth.

Standing rules: `https://flove.org/development/standards/skills/standing.md`.
