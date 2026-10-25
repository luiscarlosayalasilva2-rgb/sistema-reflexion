import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
mp = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
pat = re.compile(r"\b(" + "|".join(map(re.escape, mp)) + r")\b")
files = [root / "src" / "refs.json", root / "src" / "miniaturas.json"] + list((root / "src").glob("_spec_cap*.txt")) \
    + list((root / "hooks").glob("cap*/tomas.json")) + list((root / "visual").glob("cap*/spec.txt"))
for f in files:
    if f.exists():
        t = f.read_text(encoding="utf-8")
        t2 = pat.sub(lambda m: mp[m.group(1)], t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8")
for f in list((root / "fichas").glob("*")):
    if f.stem in mp:
        f.rename(f.with_name(mp[f.stem] + f.suffix))
al = Path(sys.argv[3]) if len(sys.argv) > 3 else None
if al and al.exists():
    d = json.loads(al.read_text(encoding="utf-8"))
    d = {k: pat.sub(lambda m: mp[m.group(1)], v) for k, v in d.items()}
    al.write_text(json.dumps(d), encoding="utf-8")
print("renombrado")
