"""§11 music under the narration only: out/capN_base.mp4 -> out/capN_base_m.mp4 (video copied).
The series track is doubled with a 4 s crossfade to cover the chapter, set to 0.18, then ducked by the narration
(sidechaincompress keyed on the voice) so it never covers any word; 1.5 s fade-in, 3 s fade-out."""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
base = ROOT / "out" / f"cap{n}_base.mp4"
music = ROOT / "audio" / "musica" / "musica_serie.mp3"
out = ROOT / "out" / f"cap{n}_base_m.mp4"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(base)],
                           capture_output=True, text=True).stdout)
fc = (f"[1:a][2:a]acrossfade=d=4[mm];"
      f"[mm]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume=0.18,afade=t=in:st=0:d=1.5,afade=t=out:st={dur - 3:.3f}:d=3[mus];"
      f"[0:a]asplit=2[voice][key];"
      f"[mus][key]sidechaincompress=threshold=0.015:ratio=8:attack=15:release=450:makeup=1[duck];"
      f"[voice][duck]amix=inputs=2:duration=first:normalize=0[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(music), "-i", str(music), "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
# loudness check: voice must dominate -> compare mean volume of the voice-only base vs the mix
vol = lambda f: subprocess.run(["ffmpeg", "-i", str(f), "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr.split("mean_volume:")[1].split(" dB")[0].strip()
print(f"{out.name}: {dur:.2f}s | volumen medio voz sola {vol(base)} dB -> con música {vol(out)} dB")
