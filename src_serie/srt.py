"""Whisper word timestamps on the polished audio -> words.json, then an SRT whose cues are the
Parte A lines (text taken verbatim from the script, times from the real audio)."""
import difflib, json, re, subprocess, sys, unicodedata
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
caps = [int(c) for c in sys.argv[1:]] or [1, 2, 3, 4, 5]


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)


UNI = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete veintiocho veintinueve".split()
DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
CEN = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos",
       7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def words_es(n):
    if n < 30:
        return UNI[n]
    if n < 100:
        return DEC[n // 10] + ("" if n % 10 == 0 else " y " + UNI[n % 10])
    if n < 1000:
        return "cien" if n == 100 else CEN[n // 100] + ("" if n % 100 == 0 else " " + words_es(n % 100))
    if n < 1_000_000:
        k = n // 1000
        return ("mil" if k == 1 else words_es(k) + " mil") + ("" if n % 1000 == 0 else " " + words_es(n % 1000))
    m = n // 1_000_000
    return ("un millón" if m == 1 else words_es(m) + " millones") + ("" if n % 1_000_000 == 0 else " " + words_es(n % 1_000_000))


def num_es(token):
    """'2004.' -> 'dos mil cuatro.'; anything that is not a plain number is returned unchanged."""
    m = re.fullmatch(r"([^\d]*)([\d.,]*\d)([^\d]*)", token)
    if not m:
        return token
    digits = re.sub(r"[.,]", "", m.group(2))
    return m.group(1) + words_es(int(digits)) + m.group(3)


def ts(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


import os
# Groq's hosted whisper-large-v3 (seconds per chapter) is used when GROQ_API_KEY is set; otherwise local whisper.
# "small" is ~3x faster than "medium" and enough here: cue text comes from the script, whisper only supplies word times (this PC has 2 cores)
GROQ = os.environ.get("GROQ_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GROQ_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
NAMES = "Víctor López, Tomás, Sofía, Elena, Mauricio, Hialeah, Miami, Houston, Key Biscayne"
model = None if GROQ else WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")


def groq_words(path):
    import requests
    with open(path, "rb") as f:
        r = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers={"Authorization": f"Bearer {GROQ}"},
                          files={"file": (path.name, f, "audio/mpeg")},
                          data=[("model", "whisper-large-v3"), ("response_format", "verbose_json"), ("timestamp_granularities[]", "word"),
                                ("timestamp_granularities[]", "segment"), ("temperature", "0"), ("language", "es")],  # no "prompt": names in the prompt made whisper loop on them
                          timeout=300)
    r.raise_for_status()
    j = r.json()
    return [{"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in j["words"]], float(j.get("duration") or j["words"][-1]["end"])


(ROOT / "srt").mkdir(exist_ok=True)
for n in caps:
    audio = ROOT / "audio" / "pulido" / f"cap{n}.mp3"
    lines = [re.sub(r"^\d+ \| ", "", l).strip()
             for l in (ROOT / f"REFLEXION_CAP{n}_GUION_PARTE_A.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    if GROQ:
        words, dur_audio = groq_words(audio)
    else:
        # decode with ffmpeg: the installed PyAV is too new for faster-whisper's own decoder
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                             capture_output=True, check=True).stdout
        samples = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
        # no initial_prompt: feeding the script made whisper hallucinate the first 30 s
        segs, info = model.transcribe(samples, language="es", word_timestamps=True, beam_size=5,
                                      condition_on_previous_text=False)
        words = [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in segs for w in s.words]
        dur_audio = info.duration
    # whisper writes "2004"; the script says "dos mil cuatro" -> expand digits so both sides compare as words
    expanded = []
    for w in words:
        parts = num_es(w["word"]).split()
        step = (w["end"] - w["start"]) / len(parts)
        expanded += [{"word": p, "start": round(w["start"] + k * step, 3), "end": round(w["start"] + (k + 1) * step, 3)}
                     for k, p in enumerate(parts)]
    words = expanded
    dur = round(dur_audio, 3)
    (ROOT / "srt" / f"cap{n}.words.json").write_text(json.dumps({"duration": dur, "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")

    # map each script word to a whisper word
    script = [(i, norm(w)) for i, l in enumerate(lines) for w in l.split() if norm(w)]
    heard = [norm(w["word"]) for w in words]
    sm = difflib.SequenceMatcher(None, [s for _, s in script], heard, autojunk=False)
    idx = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            idx[a + k] = b + k
    matched = len(idx) / len(script)

    # line start = first matched word of the line; unmatched lines interpolate between neighbours
    starts = [None] * len(lines)
    pos = 0
    for li in range(len(lines)):
        n_words = sum(1 for i, _ in script if i == li)
        for k in range(pos, pos + n_words):
            if k in idx:
                starts[li] = words[idx[k]]["start"]
                break
        pos += n_words
    starts[0] = words[0]["start"] if words else 0.0
    for li in range(1, len(lines)):
        if starts[li] is None or starts[li] <= starts[li - 1]:
            nxt = next((s for s in starts[li + 1:] if s and s > starts[li - 1]), dur)
            starts[li] = starts[li - 1] + (nxt - starts[li - 1]) / 2
    # same cut advance as the user's SRT page (jm_srt_exacto.html): every cue but the first starts 0.15 s early so the image changes just before the voice
    ADV = float(os.environ.get("ADELANTO", "0.15"))
    starts = [starts[0]] + [max(s - ADV, starts[0]) for s in starts[1:]]
    ends = starts[1:] + [words[-1]["end"] if words else dur]

    srt = "\n".join(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{t}\n" for i, (s, e, t) in enumerate(zip(starts, ends, lines)))
    (ROOT / "srt" / f"cap{n}.srt").write_text(srt, encoding="utf-8")
    missing = len(script) - len(idx)
    print(f"cap{n}: dur={dur:.2f}s words={len(words)} cues={len(lines)} match={matched:.1%} script_words_unheard={missing}")
