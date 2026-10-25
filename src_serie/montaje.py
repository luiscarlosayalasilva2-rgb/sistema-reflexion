"""Montage of one chapter (sin subtítulos): visual/capN/imgs/NNN.jpg (+ visual/capN/clips/NNN.mp4 if present),
Bloque 4B times, audio/pulido/capN.mp3 -> out/capN_base.mp4 (1080x1920, 30 fps, H.264 + AAC).
Camera motion follows the shot type of each image (spec.txt) and never repeats on consecutive images."""
import enc, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
FIRST = int(sys.argv[2]) if len(sys.argv) > 3 else 1   # optional range for a sample: montaje.py N first last
LAST = int(sys.argv[3]) if len(sys.argv) > 3 else None
V = ROOT / "visual" / f"cap{n}"
FPS, T = 30, 0.35
times = [tuple(map(float, l.split()[1:])) for l in (ROOT / f"REFLEXION_CAP{n}_BLOQUE4B_TIEMPOS_MS.txt").read_text().splitlines() if l.strip()]
shots = [l.split("|")[1] for l in (V / "spec.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(times) == len(shots), "4B y spec no coinciden"
LAST = LAST or len(times)
START = times[FIRST - 1][0]

# story-guided motion per shot type: tension (C, D) -> push in; reveal/ubicar (G) -> pull back or drift; M/B -> drifts and rise
PREF = {"C": ["in", "in_slow", "rise"], "D": ["in_slow", "in", "right"], "G": ["out", "left", "right"],
        "M": ["right", "left", "in_slow"], "B": ["rise", "out", "left"]}
motions, prev = [], None
for s in shots:
    m = next(x for x in PREF[s] if x != prev)
    motions.append(m)
    prev = m


def zp(m, frames):
    p = f"on/{max(frames - 1, 1)}"
    return {
        "in": f"z='1+0.15*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
        "in_slow": f"z='1+0.10*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
        "out": f"z='1.15-0.15*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
        "right": f"z='1.12':x='(iw-iw/zoom)*{p}':y='ih/2-ih/zoom/2'",
        "left": f"z='1.12':x='(iw-iw/zoom)*(1-{p})':y='ih/2-ih/zoom/2'",
        "rise": f"z='1.12':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*(1-{p})'",
    }[m]


seg_dir = V / "seg"; seg_dir.mkdir(exist_ok=True)
idx = list(range(FIRST, LAST + 1))
for i in idx:
    a, b = times[i - 1]
    L = (b - a) + (T if i < LAST else 0)
    frames = round(L * FPS)
    out = seg_dir / f"{i:03d}.mp4"
    clip = V / "clips" / f"{i:03d}.mp4"
    if clip.exists():  # clips keep their own motion: fit to 1080x1920, freeze last frame if short, trim if long
        vf = f"scale=1080:1920,setsar=1,fps={FPS},tpad=stop_mode=clone:stop_duration={L}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf", vf, "-t", f"{L:.3f}", "-an"]
    else:
        src = V / "imgs" / f"{i:03d}.jpg"
        if not src.exists():  # semantic coverage (§0): nearest existing image of the same beat, declared
            near = min((k for k in range(1, len(times) + 1) if (V / "imgs" / f"{k:03d}.jpg").exists()), key=lambda k: (abs(k - i), k < i))
            print(f"\n  cobertura temporal: imagen {i} -> {near}")
            src = V / "imgs" / f"{near:03d}.jpg"
        vf = f"scale=2160:3840,setsar=1,zoompan={zp(motions[i - 1], frames)}:d={frames}:s=1080x1920:fps={FPS}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(src), "-vf", vf, "-frames:v", str(frames)]
    subprocess.run(cmd + [*enc.v(18), str(out)], check=True)
    print(f"\rseg {i}/{LAST}", end="", flush=True)
print()

TRANS = ["fade", "dissolve", "smoothleft", "smoothright", "smoothup", "smoothdown"]
inputs, chain, last, offset = [], [], "[0:v]", 0.0
for i in idx:
    inputs += ["-i", str(seg_dir / f"{i:03d}.mp4")]
for k in range(1, len(idx)):
    i = idx[k]
    offset += times[i - 2][1] - times[i - 2][0]
    t = "fadeblack" if (i - 1) % 24 == 0 else TRANS[(i - 1) % len(TRANS)]
    lbl = f"[v{k}]"
    chain.append(f"{last}[{k}:v]xfade=transition={t}:duration={T}:offset={offset:.3f}{lbl}")
    last = lbl
(ROOT / "out").mkdir(exist_ok=True)
graph = V / "xfade.txt"; graph.write_text(";\n".join(chain) if chain else "[0:v]null[v0]", encoding="utf-8")
if not chain: last = "[v0]"
audio = ROOT / "audio" / "pulido" / f"cap{n}.mp3"
dur_total = times[LAST - 1][1] - START
sample = (FIRST, LAST) != (1, len(times))
out = ROOT / "out" / (f"cap{n}_muestra_{FIRST}-{LAST}.mp4" if sample else f"cap{n}_base.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-ss", f"{START:.3f}", "-t", f"{dur_total:.3f}", "-i", str(audio),
                "-/filter_complex", str(graph), "-map", last, "-map", f"{len(idx)}:a", *enc.v(19), "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-t", f"{dur_total:.3f}", str(out)], check=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
print(f"{out.name}: {dur}s (esperado {dur_total:.2f}s, inicio {START:.2f}s)")
