"""Hook storyboard (§6.3): white background, header, moment 1 full width, 2 and 3 side by side, 4 full width,
a dark semi-transparent strip at the foot of each panel with number, speaker and exact dialogue."""
import json, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
d = ROOT / "hooks" / f"cap{n}"
spec = json.loads((d / "tomas.json").read_text(encoding="utf-8"))
W, GAP, HEAD = 1200, 16, 170
F_HEAD = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 58)
F_TXT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)


def panel(i, width):
    img = Image.open(d / f"toma{i}.jpg").convert("RGB")
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    m = spec["dialogos"][i - 1]
    text = f"{i} · {m['quien']}: \u201c{m['texto']}\u201d"
    chars = 55 if width > 700 else 26
    lines = textwrap.wrap(text, chars)
    strip_h = 30 + 46 * len(lines)
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(over)
    dr.rectangle([0, img.height - strip_h, img.width, img.height], fill=(10, 10, 10, 200))
    for k, line in enumerate(lines):
        dr.text((20, img.height - strip_h + 15 + 46 * k), line, font=F_TXT, fill=(255, 255, 255, 255))
    return Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")


p1, p2, p3, p4 = panel(1, W), panel(2, (W - GAP) // 2), panel(3, (W - GAP) // 2), panel(4, W)
H = HEAD + p1.height + GAP + max(p2.height, p3.height) + GAP + p4.height + GAP
board = Image.new("RGB", (W, H), "white")
dr = ImageDraw.Draw(board)
title = f"CAPÍTULO {n} — {spec['titulo']}"
tw = dr.textlength(title, font=F_HEAD)
dr.text(((W - tw) / 2, (HEAD - 58) / 2), title, font=F_HEAD, fill="black")
y = HEAD
board.paste(p1, (0, y)); y += p1.height + GAP
board.paste(p2, (0, y)); board.paste(p3, (W - p3.width, y)); y += max(p2.height, p3.height) + GAP
board.paste(p4, (0, y))
board.save(d / f"TABLERO_CAP{n}.jpg", quality=92)
print(f"tablero {W}x{H}")
