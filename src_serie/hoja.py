"""Contact sheet for review: hoja.py N first last -> visual/capN/_hoja_first-last.jpg, each thumb labelled with its number."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
n, a, b = map(int, sys.argv[1:4])
W, H, COLS = 180, 322, 21
nums = list(range(a, b + 1))
rows = (len(nums) + COLS - 1) // COLS
sheet = Image.new("RGB", (W * COLS, H * rows), "black")
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
for k, i in enumerate(nums):
    f = ROOT / "visual" / f"cap{n}" / "imgs" / f"{i:03d}.jpg"
    x, y = (k % COLS) * W, (k // COLS) * H
    if f.exists():
        sheet.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
    d = ImageDraw.Draw(sheet)
    d.rectangle([x, y, x + 44, y + 28], fill="black")
    d.text((x + 4, y + 2), str(i), font=font, fill="yellow" if f.exists() else "red")
out = ROOT / "visual" / f"cap{n}" / f"_hoja_{a}-{b}.jpg"
sheet.save(out, quality=88)
print(out)
