"""Music under the narration of an already-subtitled chapter: out/capN_base_subs.mp4 -> out/capN_base_m_subs.mp4
(video copied, so unir.py picks it up). Track: audio/musica/musica_serie.mp3, or testamento's track if the series has none.
Doubled with a 4 s crossfade, volume (default 0.10), ducked by the voice via sidechaincompress, 1.5 s fade-in, 3 s fade-out.
Usage: mezclar_subs.py N [volume]"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
vol = float(sys.argv[2]) if len(sys.argv) > 2 else 0.10
base = ROOT / "out" / f"cap{n}_base_subs.mp4"
music = ROOT / "audio" / "musica" / "musica_serie.mp3"
if not music.exists():
    music = ROOT.parent / "testamento" / "audio" / "musica" / "musica_serie.mp3"
out = ROOT / "out" / f"cap{n}_base_m_subs.mp4"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(base)],
                           capture_output=True, text=True).stdout)
fc = (f"[1:a][2:a]acrossfade=d=4[m1];[m1][3:a]acrossfade=d=4[mm];"
      f"[mm]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:st=0:d=1.5,afade=t=out:st={dur - 3:.3f}:d=3[mus];"
      f"[0:a]asplit=2[voice][key];"
      f"[mus][key]sidechaincompress=threshold=0.015:ratio=8:attack=15:release=450:makeup=1[duck];"
      f"[voice][duck]amix=inputs=2:duration=first:normalize=0[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(music), "-i", str(music), "-i", str(music),
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
vol_of = lambda f: subprocess.run(["ffmpeg", "-i", str(f), "-af", "volumedetect", "-vn", "-f", "null", "-"],
                                  capture_output=True, text=True).stderr.split("mean_volume:")[1].split(" dB")[0].strip()
print(f"{out.name}: {dur:.2f}s | música {vol} | volumen medio voz sola {vol_of(base)} dB -> con música {vol_of(out)} dB")
