"""§7: hook (exactly 10.000 s) + chapter by plain concatenation. No audio crossfade; the chapter video alone
fades in from black over 0.4 s without losing a frame. Then verifies size, fps, codecs and duration = chapter + 10 s,
and transcribes the junction to confirm the first narration phrase enters complete right after the hook."""
import enc, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
hook = ROOT / "hooks" / f"cap{n}" / f"HOOK_CAP{n}.mp4"
chap = ROOT / "out" / f"cap{n}_base_m_subs.mp4"  # with music (caps 2-5)
if not chap.exists():
    chap = ROOT / "out" / f"cap{n}_base_subs.mp4"  # no music (cap 1)
out = ROOT / "out" / f"REFLEXION_CAP{n}_FINAL.mp4"
probe = lambda f, e: subprocess.run(["ffprobe", "-v", "error", *e, "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip()
chap_dur = float(probe(chap, ["-show_entries", "format=duration"]))
fc = (f"[0:v]trim=0:10,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=30,ass=srt/hook{n}.ass:fontsdir=fonts,format=yuv420p[hv];"
      "[0:a]atrim=0:10,asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,apad=whole_dur=10[ha];"
      "[1:v]fade=t=in:st=0:d=0.4,setsar=1,fps=30,format=yuv420p[cv];"
      "[1:a]aresample=44100,aformat=channel_layouts=stereo[ca];"
      "[hv][ha][cv][ca]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(hook), "-i", str(chap), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                *enc.v(19), "-r", "30", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(out)], check=True, cwd=ROOT)
dur = float(probe(out, ["-show_entries", "format=duration"]))
v = probe(out, ["-select_streams", "v:0", "-show_entries", "stream=codec_name,width,height,r_frame_rate"])
a = probe(out, ["-select_streams", "a:0", "-show_entries", "stream=codec_name"])
print(f"{out.name}: {v} | audio {a} | {dur:.3f}s (capítulo {chap_dur:.3f}s + 10 = {chap_dur + 10:.3f}s, diferencia {dur - chap_dur - 10:+.3f}s)")

# junction check: transcribe 9.0 -> 16.0 s
from faster_whisper import WhisperModel
import numpy as np
pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", "9", "-t", "7", "-i", str(out), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
sys.path.insert(0, str(Path(__file__).parent))
from groq_whisper import words_pcm
gw = words_pcm(pcm, offset=9)  # Groq whisper-large-v3 when GROQ_API_KEY is set
if gw is not None:
    words = [(round(s, 2), w) for w, s, _ in gw]
else:
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(
        np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0, language="es", word_timestamps=True)
    words = [(round(w.start + 9, 2), w.word.strip()) for s in segs for w in s.words]
print("unión 9-16 s:", " ".join(f"{w}@{t}" for t, w in words))
