"""poner_marca.py N | poner_marca.py --prueba video.mp4 -> overlays the channel watermark 'Reflexiones con Raíces' (elegant serif italic,
semi-transparent white with soft shadow, lower third, all video long) on out/REFLEXION_CAPN_FINAL.mp4. Idempotent: keeps out/REFLEXION_CAPN_sin_marca.mp4."""
import enc, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
TEXT = "Reflexiones con Raíces"
S, W, H = 2, 1080, 130


def marca_png(path):
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    f = ImageFont.truetype(str(ROOT / "fonts" / "georgiai.ttf"), 46 * S)
    track = 3 * S
    wd = sum(f.getlength(c) + track for c in TEXT) - track
    x, y = (W * S - wd) / 2, 24 * S
    for c in TEXT:
        ds.text((x + 2 * S, y + 3 * S), c, font=f, fill=(0, 0, 0, 255))
        d.text((x, y), c, font=f, fill=(255, 255, 255, 255))
        x += f.getlength(c) + track
    ly = y + 66 * S
    a, b = (W * S - wd * 0.62) / 2, (W * S + wd * 0.62) / 2
    ds.line((a + 2 * S, ly + 3 * S, b + 2 * S, ly + 3 * S), fill=(0, 0, 0, 255), width=3 * S)
    d.line((a, ly, b, ly), fill=(255, 255, 255, 255), width=2 * S)
    sh = sh.filter(ImageFilter.GaussianBlur(5 * S))
    out = Image.alpha_composite(sh, im)
    r, g, bb, al = out.split()
    out = Image.merge("RGBA", (r, g, bb, al.point(lambda v: int(v * 0.62))))
    out.resize((W, H), Image.LANCZOS).save(path)


def poner(src, dst, png):
    tmp = dst.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(png), "-filter_complex", "[0:v][1:v]overlay=x=0:y=1520:eof_action=repeat[v]",
                    "-map", "[v]", "-map", "0:a", *enc.v(19), "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(dst)


if sys.argv[1] == "--prueba":
    png = ROOT / "out" / "_marca.png"
    marca_png(png)
    frame = ROOT / "out" / "_prueba_marca.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "60", "-i", sys.argv[2], "-frames:v", "1", str(ROOT / "out" / "_f.png")], check=True)
    base = Image.open(ROOT / "out" / "_f.png").convert("RGBA")
    base.alpha_composite(Image.open(png), (0, 1520))
    base.convert("RGB").save(frame, quality=90)
    print(frame)
else:
    n = int(sys.argv[1])
    final = ROOT / "out" / f"REFLEXION_CAP{n}_FINAL.mp4"
    keep = ROOT / "out" / f"REFLEXION_CAP{n}_sin_marca.mp4"
    if not keep.exists():
        shutil.copyfile(final, keep)
    png = ROOT / "out" / "_marca.png"
    marca_png(png)
    poner(keep, final, png)
    print(f"cap{n}: marca de agua puesta -> {final.name}")
