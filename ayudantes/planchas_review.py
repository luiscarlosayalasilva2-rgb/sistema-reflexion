"""Planchas de revision de escenas: 16 imagenes por plancha (8 x 2), con el numero de cada una.
Uso: planchas_review.py CARPETA_SERIE N  -> visual/capN/_rev_01.jpg, _rev_02.jpg ..."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

raiz, n = Path(sys.argv[1]), int(sys.argv[2])
imgs = sorted((raiz / "visual" / f"cap{n}" / "imgs").glob("*.jpg"))
W, H, COLS, ROWS = 250, 444, 8, 2
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
por = COLS * ROWS
hojas = [imgs[i:i + por] for i in range(0, len(imgs), por)]
for k, grupo in enumerate(hojas, 1):
    sheet = Image.new("RGB", (W * COLS, H * ROWS), "black")
    for j, f in enumerate(grupo):
        x, y = (j % COLS) * W, (j // COLS) * H
        sheet.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
        d = ImageDraw.Draw(sheet)
        d.rectangle([x, y, x + 46, y + 30], fill="black")
        d.text((x + 4, y + 2), str(int(f.stem)), font=font, fill="yellow")
    out = raiz / "visual" / f"cap{n}" / f"_rev_{k:02d}.jpg"
    sheet.save(out, quality=85)
print(f"cap{n}: {len(hojas)} planchas")
