"""Subtítulos spec v4 (§10): script words (Parte A spelling) timed with whisper word timestamps,
lines of max 3 words (break on pause > 0.45 s), one yellow enlarged word at a time, fixed position y=1350,
no \\kf, no \\fad. One ASS event per spoken word, each trimmed 5 ms before the next. Writes srt/capN.ass."""
import difflib, json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
YELLOW, BASE, BIG = "&H0000FFFF&", 92, 92  # CapCut: Montserrat ExtraBold, palabra activa amarilla, centrado


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def ts(t):
    cs = round(t * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


data = json.loads((ROOT / "srt" / f"cap{n}.words.json").read_text(encoding="utf-8"))
heard = data["words"]
script = (ROOT / f"REFLEXION_CAP{n}_GUION_PARTE_B.txt").read_text(encoding="utf-8").split()
sm = difflib.SequenceMatcher(None, [norm(w) for w in script], [norm(w["word"]) for w in heard], autojunk=False)
t = [None] * len(script)
for a, b, size in sm.get_matching_blocks():
    for k in range(size):
        t[a + k] = (heard[b + k]["start"], heard[b + k]["end"])
# interpolate words whisper did not hear the same way
known = [i for i, x in enumerate(t) if x]
for i in range(len(script)):
    if t[i] is None:
        lo = max((k for k in known if k < i), default=None)
        hi = min((k for k in known if k > i), default=None)
        s0 = t[lo][1] if lo is not None else 0.0
        s1 = t[hi][0] if hi is not None else data["duration"]
        span = (hi if hi is not None else len(script)) - (lo if lo is not None else -1)
        pos = i - (lo if lo is not None else -1)
        a = s0 + (s1 - s0) * (pos - 1) / span
        b = s0 + (s1 - s0) * pos / span
        t[i] = (a, b)

# lines: max 3 words, break on pause > 0.45 s or after sentence punctuation
lines, cur = [], []
for i, w in enumerate(script):
    if cur and (len(cur) == 3 or t[i][0] - t[cur[-1]][1] > 0.45 or re.search(r"[.?!]$", script[cur[-1]])):
        lines.append(cur); cur = []
    cur.append(i)
lines.append(cur)

events = []
for li, line in enumerate(lines):
    nxt_line_start = t[lines[li + 1][0]][0] if li + 1 < len(lines) else t[line[-1]][1]
    for k, wi in enumerate(line):
        start = t[wi][0]
        end = t[line[k + 1]][0] if k + 1 < len(line) else t[wi][1]
        if k + 1 == len(line) and nxt_line_start - end < 0.30:  # no mute micro-gaps under 0.30 s
            end = nxt_line_start
        words = []
        for wj in line:
            txt = script[wj].upper()
            words.append(f"{{\\c{YELLOW}}}{txt}{{\\r}}" if wj == wi else txt)
        events.append([start, end, " ".join(words)])
for i in range(len(events) - 1):  # trim 5 ms before the next event, never overlap
    events[i][1] = min(events[i][1], events[i + 1][0] - 0.005)

overlaps = sum(1 for a, b in zip(events, events[1:]) if a[1] > b[0])
gaps = sum(1 for a, b in zip(events, events[1:]) if 0 < b[0] - a[1] < 0.30 and b[0] - a[1] > 0.006)
bad = [e for e in events if "\\kf" in e[2] or "\\fad" in e[2]]

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Montserrat ExtraBold,{BASE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,0,0,1,7,6,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
body = "\n".join(f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{{\\an5\\pos(540,1440)}}{txt}" for a, b, txt in events)
(ROOT / "srt" / f"cap{n}.ass").write_text(head + body + "\n", encoding="utf-8")
print(f"cap{n}.ass: {len(lines)} líneas, {len(events)} eventos | solapes {overlaps} | microhuecos {gaps} | kf/fad {len(bad)} | "
      f"palabras sin tiempo de whisper {len(script) - len(known)}")
