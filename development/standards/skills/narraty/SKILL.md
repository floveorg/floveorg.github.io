---
name: narraty
description: >-
  Turn any text (a book chapter, essay, article, poem, document) into a narrated
  audio file (MP3) using local offline tools — a spoken ~1-minute context
  introduction (the work, its author, their time, the method of creation),
  opening music, and a DIFFERENT short music sting that separates the intro from
  the body, then the full text read in a chosen voice. Use whenever the user
  asks to narrate / read aloud / "make an audiobook" / "hazme el audio" /
  "nárralo" / "léemelo en voz alta" of a text, or references "como Walden" (the
  established format). Built on Piper (neural TTS, offline, free voices),
  numpy-synthesised jingles, and ffmpeg. Spanish-first (default voice carlfm),
  but works for any language with an installed voice. Inherits the local TTS
  setup in the reference_tts_piper_voces memory.
---

# narraty

Produce a narrated MP3 from a text, with a spoken context intro and two distinct
music pieces. Everything is **offline**: Piper (TTS) + Python/numpy (music) +
ffmpeg (assembly). No cloud, no API keys.

## The shape of the deliverable

```
[ music A: warm opener ~6s ]
[ spoken context intro  ≤ 1 min ]
[ music B: short separator sting ~2s ]   ← must sound clearly DIFFERENT from A
[ the full text, read in the chosen voice ]
```

## Voices (Piper, in `~/.local/share/piper/voices/`)

See the `reference_tts_piper_voces` memory for the current inventory. Spanish:
`es_ES-davefx-medium` (ES m), `es_ES-sharvard-medium` (multi: `-s 0` M, `-s 1`
F), `es_MX-ald-medium` (MX m), `es_ES-carlfm-x_low` (ES m, **fast, default**),
`es_AR-daniela-high` (AR f, **very slow — ~15× real-time, avoid for long texts**).
English original: `en_US-lessac-medium`. More at HuggingFace
`rhasspy/piper-voices`.

If the user hasn't picked a voice, offer a quick **5-voice demo** (each voice
reads the same 2–3 sentences and self-labels "Voz número N"), let them choose,
then narrate. Confirm language too (original vs a translation) if ambiguous.

## Steps

1. **Get + clean the text.** Strip Markdown (`> `, `*`, `#`, `---`), collapse
   blank lines to one paragraph per line (Piper makes one utterance per line →
   natural paragraph pauses). **Omit foreign-language epigraphs** (e.g. Latin)
   that a Spanish/English TTS would mangle — keep their translation — and **tell
   the user** what you dropped. Never silently cut content.

2. **Write the context intro (≤ 1 minute).** ~120–150 words covering: the work,
   the author, their time/movement, and the method of creation (how it was
   written). End with a one-line lead-in to the passage. At ~190 wpm (carlfm),
   ~120 words ≈ 40–50 s — measure the synthesised duration and trim if it
   exceeds 60 s.

3. **Generate the two music pieces** with `scripts/mkmusic.py` → `musicA.wav`
   (warm major I–IV–V–I opener) and `musicB.wav` (bright, higher, short bell
   arpeggio separator). They are deliberately different in register/mood/length.
   Tweak the keys/mood in the script to fit the text's tone if you like. 22050
   Hz mono.

4. **Synthesise intro and body separately** (so the body can be reused / the
   intro re-timed):
   `echo/‹file› | piper -q -m "$V/<voice>.onnx" -s <spk> --sentence_silence 0.35 -f out.raw.wav`
   The **body is long → run it in the background** (`run_in_background: true`);
   Piper writes the `-f` WAV only at the very end (file stays 0 bytes, no
   progress bar) — confirm it's alive via CPU time, not file size. Poll with an
   `until grep -q DONE …; do sleep 3; done` loop.

5. **Assemble** with the ffmpeg concat demuxer. **Normalise every piece to 22050
   mono first** (x_low voices output 16 kHz; medium/high 22050 — mismatched rates
   break concat). Insert short silences (0.3–0.5 s) between blocks. Add ID3
   metadata (`-metadata title/artist/album/genre="Spoken"`). Encode
   `-c:a libmp3lame -b:a 160k`.

6. **Deliver**: the MP3 path, total duration, and the block breakdown. Offer
   variants (other voice, English original, split per section, WAV).

## Gotchas (learned the hard way)

- **`-m` path MUST end in `.onnx`.** Passing the stem → `Model file doesn't
  exist` / core dump.
- **Sample-rate mismatch**: normalise all WAVs to 22050 mono before concat.
- **Don't download big voice models while Piper is synthesising** → OOM /
  0-byte output.
- **`-high` models are ~15× real-time here** — impractical for whole chapters;
  steer the user to medium/x_low for long texts.
- Piper writes the output WAV **at the end**; a 0-byte file mid-run is normal.

## Example (Walden, ch. "Conclusión", Spanish, voice carlfm)

Produced `~/walden-conclusion-voz5-con-intro.mp3` (~26 min): musicA → 48 s
context intro (Thoreau, New England transcendentalism, 1845–47 cabin at Walden
Pond, revised until 1854) → musicB separator → the full chapter. The plain
narration (no intro/music) lived at `~/walden-conclusion-voz5.mp3`.
