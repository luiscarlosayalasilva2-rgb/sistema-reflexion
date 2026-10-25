"""poner_banner.py N [video_in video_out] -> overlays "CAPÍTULO N DE 5" (subtitle yellow, y=90, fade in/out, first 5 s) on out/REFLEXION_CAPN_FINAL.mp4.
Without paths: keeps the original as out/REFLEXION_CAPN_sin_banner.mp4 and overwrites FINAL. Run it after unir.py, before entregar.py."""
import enc, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
final = ROOT / "out" / f"REFLEXION_CAP{n}_FINAL.mp4"
src, dst = (Path(sys.argv[2]), Path(sys.argv[3])) if len(sys.argv) > 3 else (ROOT / "out" / f"REFLEXION_CAP{n}_sin_banner.mp4", final)
if len(sys.argv) <= 3:
    if not src.exists():
        shutil.copyfile(final, src)

S, W, H = 2, 1080, 150
yellow = (255, 221, 0, 255)
im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
f = ImageFont.truetype(str(ROOT / "fonts" / "Montserrat-ExtraBold.ttf"), 66 * S)
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
png = ROOT / "out" / f"_banner_cap{n}.png"
Image.alpha_composite(sh, im).resize((W, H), Image.LANCZOS).save(png)
graph = ROOT / "out" / "_banner_filter.txt"
graph.write_text("[1:v]format=rgba,fade=in:st=0.2:d=0.6:alpha=1,fade=out:st=4.4:d=0.6:alpha=1[b];\n"
                 "[0:v][b]overlay=x=0:y='if(lt(t,0.8),90+30*(1-t/0.8),90)':eof_action=pass[v]\n", encoding="ascii")
tmp = dst.with_suffix(".tmp.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-loop", "1", "-t", "5.2", "-i", str(png), "-/filter_complex", str(graph),
                "-map", "[v]", "-map", "0:a", *enc.v(19), "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
tmp.replace(dst)
print(f"cap{n}: banner puesto -> {dst.name}")
