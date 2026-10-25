"""Exports Bloque 2 of a chapter as a G-Labs Studio batch file: one prompt per line, [TAG] -> @TAG
(G-Labs character library tags). Writes glabs/capN_prompts.txt and glabs/capN_indice.txt (line -> image number)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
out_dir = ROOT / "glabs"; out_dir.mkdir(exist_ok=True)
for n in [int(x) for x in sys.argv[1:]]:
    blocks = [b.strip() for b in (ROOT / f"REFLEXION_CAP{n}_BLOQUE2_IMAGENES.txt").read_text(encoding="utf-8").split("\n\n") if b.strip()]
    lines, index = [], []
    for b in blocks:
        num, prompt = b.split(" || ", 1)
        prompt = re.sub(r"\[([A-Z]+)\]", r"@\1", prompt)
        prompt = prompt.replace("Do not use any other item from the folder", "Do not use any other reference")
        lines.append(prompt)
        index.append(f"{len(lines)} -> imagen {int(num):03d}")
    (out_dir / f"cap{n}_prompts.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / f"cap{n}_indice.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    tags = sorted({t for l in lines for t in re.findall(r"@([A-Z]+)", l)})
    print(f"cap{n}: {len(lines)} prompts | etiquetas usadas: {', '.join(tags)}")
