"""Generic fixer for _spec_capN.txt (alias form): body edits, untagged mentions, repeated shots, G gaps, faceless ratio.
Usage: autofix.py <series root> <edits.json> caps..."""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
edits = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if sys.argv[2] != "-" else {}
caps = [int(x) for x in sys.argv[3:]]

ALT = {"D": ["C", "B"], "M": ["C", "B", "G"], "C": ["M", "B"], "G": ["M", "C"], "B": ["M", "C"]}
for n in caps:
    p = root / "src" / f"_spec_cap{n}.txt"
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            num, shot, tags, loc, neg, body = line.split("|", 5)
            rows.append([int(num), shot, tags.split(), loc, neg, body])
    for a, b in edits.get('_all', []):
        for r in rows:
            r[5] = r[5].replace(a, b)
    for k, v in edits.get(str(n), {}).items():
        r = rows[int(k) - 1]
        if "tags" in v: r[2] = v["tags"].split()
        if "body" in v: r[5] = v["body"]
        if "shot" in v: r[1] = v["shot"]
        if "loc" in v: r[3] = v["loc"]
    # untagged mentions
    for r in rows:
        for a in re.findall(r"\[([A-Za-z]+)\]", r[5]):
            if a not in r[2]:
                r[2].append(a)
        for t in list(r[2]):
            if f"[{t}]" not in r[5]:
                r[5] += f", [{t}] nearby"
    last = len(rows)
    protected = {1, 2, 3, 4, last}
    # repeated shots
    for i in range(1, len(rows)):
        if rows[i][1] == rows[i - 1][1]:
            nxt = rows[i + 1][1] if i + 1 < len(rows) else ""
            for c in ALT[rows[i][1]]:
                if c != rows[i - 1][1] and c != nxt:
                    rows[i][1] = c
                    break
    # G gaps
    def gaps():
        gi = [i for i, r in enumerate(rows) if r[1] == "G"]
        for a, b in zip([-1] + gi, gi + [len(rows)]):
            if b - a > 10:
                return a, b
        return None
    g = gaps()
    guard = 0
    while g and guard < 40:
        a, b = g
        mid = (a + b) // 2
        for off in (0, 1, -1, 2, -2, 3, -3):
            i = mid + off
            if a < i < b and rows[i][1] in "MC" and rows[i - 1][1] != "G" and (i + 1 >= len(rows) or rows[i + 1][1] != "G"):
                rows[i][1] = "G"
                break
        else:
            break
        g = gaps(); guard += 1
    # faceless ratio: M then C lines with one tag become shot-from-behind
    def faceless():
        return sum(1 for r in rows if r[1] in "DB") / len(rows)
    for kind in ("M", "C"):
        for i in range(1, len(rows) - 1):
            if faceless() >= 0.34:
                break
            r = rows[i]
            if r[1] == kind and r[0] not in protected and rows[i - 1][1] != "B" and rows[i + 1][1] != "B" and len(r[2]) == 1:
                r[1] = "B"
    print(f"cap{n}: sin rostro {faceless():.0%}")
    p.write_text("\n".join("|".join([str(r[0]), r[1], " ".join(r[2]), r[3], r[4], r[5]]) for r in rows) + "\n", encoding="utf-8")
