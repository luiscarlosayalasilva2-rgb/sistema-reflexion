"""Burns srt/capN.ass onto a montage. quemar.py N input.mp4 [start_seconds] -> same name with _subs.
start_seconds shifts the subtitle clock for samples cut from the middle of the chapter."""
import enc, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n, src = int(sys.argv[1]), Path(sys.argv[2])
start = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
out = src.with_name(src.stem + "_subs.mp4")
vf = f"ass=srt/cap{n}.ass:fontsdir=fonts"
if start:
    vf = f"setpts=PTS+{start}/TB,{vf},setpts=PTS-{start}/TB"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src.resolve()), "-vf", vf, *enc.v(19), "-c:a", "copy", str(out.resolve())], check=True, cwd=ROOT)
probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,codec_name",
                        "-show_entries", "format=duration", "-of", "default=nw=1", str(out)], capture_output=True, text=True).stdout
print(out.name, probe.replace("\n", " "))
