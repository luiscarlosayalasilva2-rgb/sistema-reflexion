"""Expands the short aliases of src/_spec_capN.txt into visual/capN/spec.txt + moves.json; patches refs/build once."""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
ALIAS = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
caps = [int(x) for x in sys.argv[3:]]
for n in caps:
    src = (root / "src" / f"_spec_cap{n}.txt").read_text(encoding="utf-8").splitlines()
    out = []
    for line in src:
        if not line.strip():
            continue
        num, shot, tags, loc, neg, body = line.split("|", 5)
        tags = " ".join(ALIAS.get(t, t) for t in tags.split())
        for a in sorted(ALIAS, key=len, reverse=True):
            body = body.replace(f"[{a}]", f"[{ALIAS[a]}]")
        out.append("|".join([num, shot, tags, loc, neg, body]))
    d = root / "visual" / f"cap{n}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "spec.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    last = len(out)
    mv = {"1": "slow push in", "2": "slow pull back", "3": "static hold with ambient motion", "4": "slow push in", str(last): "slow push in"}
    (d / "moves.json").write_text(json.dumps(mv), encoding="utf-8")
    print(f"cap{n}: {len(out)} líneas")
