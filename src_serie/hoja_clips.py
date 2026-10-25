"""Frames at 0.5 s and 3.5 s of every clip -> visual/_hoja_clips.jpg (labelled capN/NNN)."""
import subprocess, io
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
clips = sorted(ROOT.glob("visual/cap*/clips/*.mp4"))
W, H = 162, 288
sheet = Image.new("RGB", (W * 2 * 10, H * ((len(clips) + 9) // 10)), "black")
for i, c in enumerate(clips):
    for j, t in enumerate((0.5, 3.5)):
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(c), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                             capture_output=True).stdout
        im = Image.open(io.BytesIO(png)).convert("RGB").resize((W, H))
        if j == 0:
            ImageDraw.Draw(im).text((4, 4), f"{c.parent.parent.name}/{c.stem}", fill="yellow")
        sheet.paste(im, ((i % 10) * 2 * W + j * W, (i // 10) * H))
sheet.save(ROOT / "visual" / "_hoja_clips.jpg", quality=85)
print(len(clips), "clips")
