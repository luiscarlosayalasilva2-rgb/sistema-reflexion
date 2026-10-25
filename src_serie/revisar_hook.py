"""Hook QA (user rule): transcribe hooks/capN/HOOK_CAPN.mp4 with whisper and check each approved dialogue line is said
completely (word coverage) and ends before 10 s; save 6 frames to hooks/capN/_qc.jpg for a visual check."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
import os
# Groq's hosted whisper-large-v3 when GROQ_API_KEY is set (seconds); otherwise local whisper (slow on this 2-core PC)
GROQ = os.environ.get("GROQ_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GROQ_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
model = None if GROQ else WhisperModel("medium", device="cpu", compute_type="int8")


def groq_words(path):
    import requests
    with open(path, "rb") as f:
        r = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers={"Authorization": f"Bearer {GROQ}"},
                          files={"file": (path.name, f, "video/mp4")},
                          data=[("model", "whisper-large-v3"), ("response_format", "verbose_json"),
                                ("timestamp_granularities[]", "word"), ("temperature", "0"), ("language", "es")], timeout=300)
    r.raise_for_status()
    return [(w["word"].strip(), w["end"]) for w in r.json()["words"]]


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


for n in map(int, sys.argv[1:]):
    d = ROOT / "hooks" / f"cap{n}"
    vid = d / f"HOOK_CAP{n}.mp4"
    if GROQ:
        words = groq_words(vid)
    else:
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(vid), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
        segs, _ = model.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0, language="es", word_timestamps=True)
        words = [(w.word.strip(), w.end) for s in segs for w in s.words]
    # whisper writes "36.000" and splits "sinvergüenza": expand digits and compare as one glued string
    sys.path.insert(0, str(Path(__file__).parent))
    from srt_num import num_es
    heard = [norm(num_es(w)) for w, _ in words]
    glued = "".join(heard)
    print(f"== cap{n} oído: {' '.join(w for w, _ in words)}")
    ok_all = True
    for k, dl in enumerate(json.loads((d / "tomas.json").read_text(encoding="utf-8"))["dialogos"], 1):
        line = [norm(w) for w in dl["texto"].split() if norm(w)]
        sm = difflib.SequenceMatcher(None, line, heard, autojunk=False)
        hit = sum(b.size for b in sm.get_matching_blocks())
        cover = hit / len(line)
        blocks = [b for b in sm.get_matching_blocks() if b.size]
        end = words[blocks[-1].b + blocks[-1].size - 1][1] if blocks else None
        target = "".join(line)
        cover = max(cover, difflib.SequenceMatcher(None, target, glued, autojunk=False).find_longest_match(0, len(target), 0, len(glued)).size / len(target))
        if cover < 0.8:  # fuzzy: best partial match of the whole line inside the transcript
            cover = max(cover, max((difflib.SequenceMatcher(None, target, glued[i:i + len(target)]).ratio() for i in range(0, max(1, len(glued) - len(target) + 1))), default=0))
        ok = cover >= 0.8
        ok_all &= ok
        print(f"  {k}. {dl['quien']}: {cover:.0%} de las palabras" + (f", termina en {end:.2f}s" if end else "") + ("" if ok else "  <-- INCOMPLETA"))
    frames = []
    for t in (0.5, 2, 4, 5.5, 7.5, 9.5):
        f = d / f"_qc_{t}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(vid), "-frames:v", "1", "-vf", "scale=240:-2", str(f)])
        frames.append(Image.open(f))
    sheet = Image.new("RGB", (sum(i.width for i in frames), frames[0].height))
    x = 0
    for i in frames:
        sheet.paste(i, (x, 0)); x += i.width
    sheet.save(d / "_qc.jpg", quality=85)
    print(f"  RESULTADO cap{n}: {'diálogos completos' if ok_all else 'FALTAN DIÁLOGOS -> regenerar'}")
