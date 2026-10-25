"""Splits capN.txt lines longer than 9 words at the best point (sentence end > comma > word), keeping 4-9 words
per piece and never ending a piece on a stopword. Prints lines it could not fix. Usage: partir.py <src dir>"""
import re, sys
from pathlib import Path

BAD = set("con de para y que a en por el la los las un una mi su sus del al o e ni sin como lo le les me se te tu nos mis".split())


def ok(ws):
    return 4 <= len(ws) <= 9 and re.sub(r"[^\wáéíóúñü]", "", ws[-1].lower()) not in BAD


def split(ws):
    if len(ws) <= 9:
        return [ws]
    best = None
    for i in range(4, len(ws) - 3):
        a, b = ws[:i], ws[i:]
        if not ok(a):
            continue
        score = (3 if re.search(r"[.?!]$", a[-1]) else 2 if a[-1].endswith(",") else 0) - abs(len(a) - len(b)) * 0.1
        rest = split(b)
        if rest is None:
            continue
        if best is None or score > best[0]:
            best = (score, [a] + rest)
    return best[1] if best else None


for f in sorted(Path(sys.argv[1]).glob("cap[0-9].txt")):
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        ws = line.split()
        if not ws:
            continue
        if len(ws) <= 9:
            out.append(line.strip())
            continue
        parts = split(ws)
        if parts is None:
            print(f"{f.name}: no pude partir: {line}")
            out.append(line.strip())
        else:
            out += [" ".join(p) for p in parts]
    f.write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
