---
name: narraty
description: >-
  Turn any text (a book chapter, essay, article, poem, document, or a questy
  session's answers) into a narrated audio file (MP3) using local offline tools
  — a short music opener, then the full text read in a chosen voice. Use
  whenever the user asks to narrate / read aloud / "make an audiobook" /
  "hazme el audio" / "nárralo" / "léemelo en voz alta" of a text. Built on
  Piper (neural TTS, offline, free voices), numpy-synthesised jingles, and
  ffmpeg. Spanish-first (default voice es_ES-carlfm-x_low), but works for any
  language with an installed voice. Inherits the local TTS setup in the
  reference_tts_piper_voces memory.
---

# narraty

Produce a narrated MP3 from a text, with a short music opener and the full
text read in the chosen voice — no extra spoken intro or summary, just the text
that is there. Everything is **offline**: Piper (TTS) + Python/numpy (music) +
ffmpeg (assembly). No cloud, no API keys.

## The shape of the deliverable

```
[ music A: short warm opener ~4s ]
[ the full text, read in the chosen voice ]
```

No spoken resume is synthesised: if the user gives a text, narrate exactly that
text. (There was once a ~1-min spoken context intro summing up the work; that
is gone — the narration is just the text.)

## Default output and URL

The default file is named **`questy-intro.mp3`** — the narration of a questy
session (the questions and answers). It is published at

```
https://flove.org/development/standards/skills/questy/questy-intro.mp3
```

(URL reserved; the file is uploaded later.) Write the MP3 to that name by
default unless the user gives another target.

## Voices (Piper, in `~/.local/share/piper/voices/`)

The `.onnx` + `.onnx.json` voice models live in `~/.local/share/piper/voices/`,
and the generation scripts (`scripts/mkmusic.py`) ship with this skill. Both
are mirrored on the flove repo:

- repo: `https://github.com/floveorg/floveorg.github.io`
- skill folder (script + docs): `https://flove.org/development/standards/skills/narraty/`

Fetch the voices from there (or from HuggingFace `rhasspy/piper-voices`) if
`~/.local/share/piper/voices/` is empty. Speaker inventory (Spanish): `es_ES-
davefx-medium` (ES m), `es_ES-sharvard-medium` (multi: `-s 0` M, `-s 1` F),
`es_MX-ald-medium` (MX m), `es_ES-carlfm-x_low` (ES m, **fast, default**),
`es_AR-daniela-high` (AR f, **very slow — ~15× real-time, avoid for long texts**).
English original: `en_US-lessac-medium`.

If the user hasn't picked a voice, offer a quick **5-voice demo** (each voice
reads the same 2–3 sentences and self-labels "Voz número N"), let them choose,
then narrate. Confirm language too (original vs a translation) if ambiguous.

## Steps

1. **Get + clean the text.** Strip Markdown (`> `, `*`, `#`, `---`), collapse
   blank lines to one paragraph per line (Piper makes one utterance per line →
   natural paragraph pauses). **Omit foreign-language epigraphs** (e.g. Latin)
   that a Spanish/English TTS would mangle — keep their translation — and **tell
   the user** what you dropped. Never silently cut content.

2. **Generate the music** with `scripts/mkmusic.py` → `musicA.wav` (short warm
   opener). Tweak the key/mood in the script to fit the text's tone if you
   like. 22050 Hz mono.

3. **Synthesise the text:**
   `echo/‹file› | piper -q -m "$V/<voice>.onnx" -s <spk> --sentence_silence 0.35 -f out.raw.wav`
   The text is **long → run it in the background** (`run_in_background: true`);
   Piper writes the `-f` WAV only at the very end (file stays 0 bytes, no
   progress bar) — confirm it's alive via CPU time, not file size. Poll with an
   `until grep -q "DONE" …; do sleep 3; done` loop.

4. **Assemble** with the ffmpeg concat demuxer. **Normalise every piece to
   22050 mono first** (x_low voices output 16 kHz; medium/high 22050 — mismatched
   rates break concat). Insert short silences (0.3–0.5 s) between blocks. Add
   ID3 metadata (`-metadata title/artist/album/genre="Spoken"`). Encode
   `-c:a libmp3lame -b:a 160k`.

5. **Deliver**: the MP3 path (`questy-intro.mp3` by default), total duration,
   and the block breakdown. Offer variants (other voice, English original,
   split per section, WAV).

## Gotchas (learned the hard way)

- **`-m` path MUST end in `.onnx`.** Passing the stem → `Model file doesn't
  exist` / core dump.
- **Sample-rate mismatch**: normalise all WAVs to 22050 mono before concat.
- **Don't download big voice models while Piper is synthesising** → OOM /
  0-byte output.
- **`-high` models are ~15× real-time here** — impractical for whole chapters;
  steer the user to medium/x_low for long texts.
- Piper writes the output WAV **at the end**; a 0-byte file mid-run is normal.

## Example (default questy narration, voice es_ES-carlfm-x_low)

Session wrapped → narrate the answers. The output is `questy-intro.mp3`
(~straight read of the Q&A, no intro or summary), published at the URL above.
The plain narration and the music-opened edition live together at the target
path; the markdown stays the source of truth.