"""banner_capitulo.py N out.png -> title card "CAPÍTULO N DE 5" in subtitle yellow between thin yellow lines, with soft shadow."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

n, out = sys.argv[1], sys.argv[2]
S = 2
F = str(Path(__file__).parent / "cumple" / "fonts" / "Montserrat-ExtraBold.ttf")
W, H = 1080, 150
yellow = (255, 221, 0, 255)
im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
f = ImageFont.truetype(F, 66 * S)
text, track = f"CAPÍTULO {n} DE 5", 5 * S
wd = sum(f.getlength(c) + track for c in text) - track
x, y = (W * S - wd) / 2, 30 * S
for c in text:
    ds.text((x + 3 * S, y + 4 * S), c, font=f, fill=(0, 0, 0, 255))
    d.text((x, y), c, font=f, fill=yellow, stroke_width=2 * S, stroke_fill=(0, 0, 0, 255))
    x += f.getlength(c) + track
ly = y + f.getbbox("C")[3] // 2 + 10 * S
for a, b in ((40 * S, (W * S - wd) / 2 - 20 * S), ((W * S + wd) / 2 + 20 * S, W * S - 40 * S)):
    if b > a:
        ds.line((a + 3 * S, ly + 4 * S, b + 3 * S, ly + 4 * S), fill=(0, 0, 0, 255), width=4 * S)
        d.line((a, ly, b, ly), fill=yellow, width=4 * S)
sh = sh.filter(ImageFilter.GaussianBlur(6 * S))
Image.alpha_composite(sh, im).resize((W, H), Image.LANCZOS).save(out)
