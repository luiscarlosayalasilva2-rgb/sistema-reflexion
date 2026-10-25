"""Hook subtitles with the same spec v4: approved dialogue text (hooks/capN/tomas.json) timed with whisper on the
hook's own audio. Writes srt/hookN.ass (clock starts at 0 = first frame of the hook)."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
YELLOW, BIG, DUR = "&H0000FFFF&", 92, 10.0


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def ts(t):
    cs = round(t * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


hook = ROOT / "hooks" / f"cap{n}" / f"HOOK_CAP{n}.mp4"
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(hook), "-t", str(DUR), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
sys.path.insert(0, str(Path(__file__).parent))
from groq_whisper import words_pcm
heard = words_pcm(pcm)  # Groq whisper-large-v3 when GROQ_API_KEY is set
if heard is None:
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(
        np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0, language="es", word_timestamps=True)
    heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
print("oído:", " ".join(h[0] for h in heard))

lines_txt = [d["texto"] for d in json.loads((ROOT / "hooks" / f"cap{n}" / "tomas.json").read_text(encoding="utf-8"))["dialogos"]]
script = [(li, w) for li, l in enumerate(lines_txt) for w in l.split()]
sm = difflib.SequenceMatcher(None, [norm(w) for _, w in script], [norm(h[0]) for h in heard], autojunk=False)
t = [None] * len(script)
for a, b, size in sm.get_matching_blocks():
    for k in range(size):
        t[a + k] = (heard[b + k][1], heard[b + k][2])
known = [i for i, x in enumerate(t) if x]
for i in range(len(script)):
    if t[i] is None:
        lo = max((k for k in known if k < i), default=None); hi = min((k for k in known if k > i), default=None)
        s0 = t[lo][1] if lo is not None else 0.0; s1 = t[hi][0] if hi is not None else DUR
        span = (hi if hi is not None else len(script)) - (lo if lo is not None else -1); pos = i - (lo if lo is not None else -1)
        t[i] = (s0 + (s1 - s0) * (pos - 1) / span, s0 + (s1 - s0) * pos / span)

lines, cur = [], []
for i, (li, w) in enumerate(script):
    if cur and (len(cur) == 3 or script[cur[-1]][0] != li or t[i][0] - t[cur[-1]][1] > 0.45 or re.search(r"[.?!]$", script[cur[-1]][1])):
        lines.append(cur); cur = []
    cur.append(i)
lines.append(cur)
events = []
for li, line in enumerate(lines):
    nxt = t[lines[li + 1][0]][0] if li + 1 < len(lines) else min(t[line[-1]][1], DUR)
    for k, wi in enumerate(line):
        end = t[line[k + 1]][0] if k + 1 < len(line) else t[wi][1]
        if k + 1 == len(line) and nxt - end < 0.30:
            end = nxt
        txt = " ".join(f"{{\\c{YELLOW}}}{script[wj][1].upper()}{{\\r}}" if wj == wi else script[wj][1].upper() for wj in line)
        events.append([t[wi][0], min(end, DUR), txt])
for i in range(len(events) - 1):
    events[i][1] = min(events[i][1], events[i + 1][0] - 0.005)
head = (ROOT / "srt" / f"cap{n}.ass").read_text(encoding="utf-8").split("[Events]")[0]
body = "\n".join(f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{{\\an5\\pos(540,1440)}}{x}" for a, b, x in events)
(ROOT / "srt" / f"hook{n}.ass").write_text(head + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + body + "\n", encoding="utf-8")
overlaps = sum(1 for a, b in zip(events, events[1:]) if a[1] > b[0])
print(f"hook{n}.ass: {len(events)} eventos, solapes {overlaps}, palabras sin tiempo {len(script) - len(known)}, última termina {events[-1][1]:.2f}s")
