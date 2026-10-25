"""Splits Parte A lines longer than 9 words into two lines of 4-9 words at a natural point
(after a comma first, otherwise near the middle) so no line ends in a weak word. Rewrites src/capN.txt."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BAD = set("con de para y que a en por el la los las un una mi su sus del al o e ni sin como lo le les me se te tu nos mis".split())


def weak(w):
    return w.strip(".,¿?¡!").lower() in BAD


def split(words):
    if len(words) <= 9:
        return [words]
    n = len(words)
    cands = [k for k in range(4, n - 3) if not weak(words[k - 1]) and k <= 9 and n - k <= 9]
    if not cands:
        cands = [k for k in range(4, n - 3) if not weak(words[k - 1])]
    if not cands:
        return [words]
    best = min(cands, key=lambda k: (not words[k - 1].endswith((",", ".")), abs(k - n / 2)))
    return split(words[:best]) + split(words[best:])


def merge_short(lines):
    """Lines under 4 words join the next line (or the previous one) when the result stays at 9 words or fewer."""
    lines = [l.split() for l in lines]
    i = 0
    while i < len(lines):
        if len(lines[i]) < 4 and len(lines) > 1:
            if i + 1 < len(lines) and len(lines[i]) + len(lines[i + 1]) <= 9:
                lines[i:i + 2] = [lines[i] + lines[i + 1]]
                continue
            if i > 0 and len(lines[i - 1]) + len(lines[i]) <= 9 and not weak(lines[i - 1][-1]):
                lines[i - 1:i + 1] = [lines[i - 1] + lines[i]]
                i -= 1
                continue
            if i + 1 < len(lines):  # too long together: merge anyway, split() rebalances it
                lines[i:i + 2] = [lines[i] + lines[i + 1]]
                continue
        i += 1
    return lines


for n in (sys.argv[1:] or range(1, 6)):
    p = ROOT / "src" / f"cap{n}.txt"
    out = []
    raw = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    for words in merge_short(raw):
        out += [" ".join(x) for x in split(words)]
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
