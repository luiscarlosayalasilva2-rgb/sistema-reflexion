"""Side-by-side zoom of chosen scenes for text checks: zoom.py N out.jpg n1 n2 ... (labelled, 432 px wide each)"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
n, out, nums = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
W, H = 432, 774
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
s = Image.new("RGB", (W * len(nums), H), "black")
for i, k in enumerate(nums):
    im = Image.open(ROOT / "visual" / f"cap{n}" / "imgs" / f"{k:03d}.jpg").convert("RGB").resize((W, H))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 70, 38], fill="black"); d.text((6, 2), str(k), fill="yellow", font=font)
    s.paste(im, (i * W, 0))
s.save(out, quality=88)
