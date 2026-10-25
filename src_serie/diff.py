"""Shows where the whisper transcript differs from the script (Parte B) for one chapter."""
import difflib, json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


script = (ROOT / f"REFLEXION_CAP{n}_GUION_PARTE_B.txt").read_text(encoding="utf-8").split()
heard = [w["word"] for w in json.loads((ROOT / "srt" / f"cap{n}.words.json").read_text(encoding="utf-8"))["words"]]
words = json.loads((ROOT / "srt" / f"cap{n}.words.json").read_text(encoding="utf-8"))["words"]
sm = difflib.SequenceMatcher(None, [norm(w) for w in script], [norm(w) for w in heard], autojunk=False)
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op != "equal":
        t = words[b1]["start"] if b1 < len(words) else words[-1]["end"]
        print(f"{t:7.2f}s {op:8} GUION: {' '.join(script[a1:a2])!r}  OIDO: {' '.join(heard[b1:b2])!r}")
