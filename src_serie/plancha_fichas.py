"""Contact sheet of fichas/*.jpg with tag labels: plancha_fichas.py out.jpg [TAG ...]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
tags = sys.argv[2:] or sorted(p.stem for p in (ROOT / "fichas").glob("*.jpg"))
H = 360
tiles = []
for t in tags:
    im = Image.open(ROOT / "fichas" / f"{t}.jpg").convert("RGB")
    im = im.resize((int(im.width * H / im.height), H))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 9 * len(t) + 10, 18], fill="black")
    d.text((5, 3), t, fill="yellow")
    tiles.append(im)
W = 1800
rows, row, w = [], [], 0
for im in tiles:
    if w + im.width > W and row:
        rows.append(row); row, w = [], 0
    row.append(im); w += im.width + 6
rows.append(row)
sheet = Image.new("RGB", (W, len(rows) * (H + 6)), "white")
for r, row in enumerate(rows):
    x = 0
    for im in row:
        sheet.paste(im, (x, r * (H + 6))); x += im.width + 6
sheet.save(sys.argv[1], quality=85)
