"""Local clip (master prompt section 5, route LOCAL): a 4 s camera move over the still image, used when the video model
refuses or returns nothing for that image. clip_local.py CAP [NUM ...] -> visual/capN/clips/NNN.mp4 (1080x1920, 30 fps, no audio).
Without NUM it fills every missing clip of the chapter (images 1-4 and the last one). The move comes from visual/capN/moves.json."""
import enc, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cap = int(sys.argv[1])
V = ROOT / "visual" / f"cap{cap}"
moves = json.loads((V / "moves.json").read_text(encoding="utf-8"))
nums = [int(a) for a in sys.argv[2:]] or [int(k) for k in moves]
FPS, SECS = 30, 4.0
frames = int(FPS * SECS)
p = f"on/{frames - 1}"
ZOOM = {
    "in": f"z='1+0.15*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
    "out": f"z='1.15-0.15*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
    "hold": f"z='1.06+0.04*{p}':x='(iw-iw/zoom)*{p}':y='ih/2-ih/zoom/2'",
}
for n in nums:
    out = V / "clips" / f"{n:03d}.mp4"
    out.parent.mkdir(exist_ok=True)
    if out.exists():
        continue
    m = moves.get(str(n), "slow push in")
    kind = "out" if "pull" in m else ("hold" if "static" in m else "in")
    src = V / "imgs" / f"{n:03d}.jpg"
    vf = f"scale=2160:3840,setsar=1,zoompan={ZOOM[kind]}:d={frames}:s=1080x1920:fps={FPS}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(src), "-vf", vf, "-frames:v", str(frames), "-an",
                    *enc.v(18), str(out)], check=True)
    print(f"cap{cap}/{n:03d}.mp4 local ({kind})")
