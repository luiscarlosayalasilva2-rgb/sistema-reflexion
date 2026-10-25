"""Writes the 4 hook-board shot prompts for one chapter (hooks/capN/tomas.txt) from hooks/capN/tomas.json + refs.json.
Tags may carry a variant, e.g. [ZEFIRO:joven]: the variant description is injected and the reference is the base ficha."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
refs = json.loads((Path(__file__).parent / "refs.json").read_text(encoding="utf-8"))["chars"]
spec = json.loads((ROOT / "hooks" / f"cap{n}" / "tomas.json").read_text(encoding="utf-8"))
NEG = "No text, no letters, no words, no writing, no signs, no labels, no captions, no watermarks, no logos, no numbers, no symbols visible anywhere in the image, no onomatopoeia or sound-effect lettering. No blood, no blood stains, no gore, no red splatters."
out = []
for i, t in enumerate(spec["tomas"], 1):
    body = t["body"]
    keys = []
    for tag in t["tags"]:
        key, _, var = tag.partition(":")
        keys.append(key)
        body = body.replace(f"[{tag}]", f"[{key}] ({refs[key][var or 'scene']})", 1).replace(f"[{tag}]", f"[{key}]")
    names = ", ".join(f"[{x}]" for x in keys)
    head = " ".join(f"[{x}]" for x in keys) + f" [{spec['loc']}]"
    extra = " Any other person appears without a visible face and without a name." if t.get("extras") else ""
    out.append(f"{i} || {head} vertical 9:16 portrait composition, Marvel Comics 2D style, {t['shot']} of {body}. "
               f"Only {names} as named characters in frame.{extra} Use only: {head}. Do not use any other item from the folder. "
               f"Bold ink outlines, dramatic cel shading, cinematic rim lighting, saturated comic book colors. {NEG}")
(ROOT / "hooks" / f"cap{n}" / "tomas.txt").write_text("\n\n".join(out), encoding="utf-8")
print(f"{len(out)} tomas escritas")
