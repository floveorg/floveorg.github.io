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

## Default output name

Use the target the user gives. If none, derive one from the source instead of a
fixed name:

- **A file** → same basename with `.mp3` (e.g. `chapter-3.md` → `chapter-3.mp3`),
  next to the source.
- **Pasted text** → `narration-<short-slug>.mp3` in the current folder.
- **A questy session** → `questy-intro.mp3` is the one reserved exception; that
  file can later be published at
  `https://flove.org/development/standards/skills/questy/questy-intro.mp3` if
  the owner asks.

Report the path. Do not invent a flove.org upload for unrelated texts and do
not reuse `questy-intro.mp3` for them.

## Quick path (the normal way)

```bash
~/.agents/skills/narraty/scripts/narrate.sh clean-text.txt
# -o out.mp3 · -v es_ES-davefx-medium · -s 1 · --no-music
```

The wrapper preflights `piper`/`ffmpeg`/numpy/the voice/`mkmusic.py`, generates
the opener, synthesises the text, normalises to 22050 mono and assembles the MP3
(160k, spoken metadata). Pass already-cleaned text (one paragraph per line). The
manual steps below are the reference/fallback for custom variants.

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

## Preflight (quick, before synthesising)

```bash
command -v piper && command -v ffmpeg && command -v python3
ls ~/.local/share/piper/voices/*.onnx 2>/dev/null | head
test -f scripts/mkmusic.py || test -f ~/.agents/skills/narraty/scripts/mkmusic.py
```

- If `piper` or `ffmpeg` is missing → stop and say what to install.
- If the voices folder is empty → fetch the chosen `.onnx` + `.onnx.json` from
  the voices section above before starting.
- If `mkmusic.py` is missing, run from the skill folder (or copy the script).

## Steps

Use the quick wrapper above for the normal case. The manual steps below are
the reference/fallback for custom work (other voices, variants, per-section
splits).

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

5. **Deliver**: the MP3 path (derived as above), total duration, and the block
   breakdown. Offer variants (other voice, English original, split per section,
   WAV).

## Gotchas (learned the hard way)

- **`-m` path MUST end in `.onnx`.** Passing the stem → `Model file doesn't
  exist` / core dump.
- **Sample-rate mismatch**: normalise all WAVs to 22050 mono before concat.
- **Don't download big voice models while Piper is synthesising** → OOM /
  0-byte output.
- **`-high` models are ~15× real-time here** — impractical for whole chapters;
  steer the user to medium/x_low for long texts.
- Piper writes the output WAV **at the end**; a 0-byte file mid-run is normal.

## Example — questy session (the reserved name)

Session wrapped → narrate the answers. This is the one special case: the output
is `questy-intro.mp3` (a straight read of the Q&A, no intro or summary), and it
can be published at the reserved URL above if the owner asks. Every other text
uses a source-derived name (`chapter-3.mp3`, `narration-<slug>.mp3`); the
markdown stays the source of truth.