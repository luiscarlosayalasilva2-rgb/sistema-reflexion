"""Bloque 3 clips through the G-Labs API: Omni Flash, start-frame mode (the Bloque 2 image is the first frame), 4 s, 9:16,
720p -> visual/capN/clips/NNN.mp4. Skips existing clips. Usage: glabs_clips.py N [N...] [--parallel K]"""
import json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"
argv = sys.argv[1:]
par = 4
if "--parallel" in argv:
    k = argv.index("--parallel")
    par = int(argv[k + 1])
    del argv[k:k + 2]
caps = sorted({int(a) for a in argv})
KEY = os.environ.get("GLABS_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GLABS_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = r.read()
    return d if raw else json.loads(d)


jobs = []
for n in caps:
    clips = ROOT / "visual" / f"cap{n}" / "clips"; clips.mkdir(parents=True, exist_ok=True)
    for b in (ROOT / f"REFLEXION_CAP{n}_BLOQUE3_CLIPS.txt").read_text(encoding="utf-8").split("\n\n"):
        if not b.strip():
            continue
        num, prompt = b.strip().split(" || ", 1)
        num = int(num)
        out = clips / f"{num:03d}.mp4"
        img = ROOT / "visual" / f"cap{n}" / "imgs" / f"{num:03d}.jpg"
        if out.exists() or not img.exists():
            continue
        prompt = re.sub(r"Use only:.*?Do not use any other item from the folder( and no place at all)?\.", "", prompt[prompt.index("vertical 9:16"):]).replace("[", "").replace("]", "")  # no tag names: the video model writes them as signs
        jobs.append((out, prompt, img))


def run(job):
    out, prompt, img = job
    # CLIP_MODEL=omni_vids -> Google Vids (own Google-account quota in seconds, no Flow); default omni_flash
    tid = call("POST", "/api/video/generate", {"prompt": prompt, "model": os.environ.get("CLIP_MODEL", "omni_flash"), "aspect_ratio": "9:16", "mode": "start_image",
                                               "reference_images": [{"path": str(img.resolve())}], "video_length": 4,
                                               "resolution": ["720p"]})["task_id"]
    while (s := call("GET", f"/api/status/{tid}"))["status"] not in ("completed", "failed"):
        time.sleep(10)
    if s["status"] == "failed":
        return f"{out.parent.parent.name}/{out.name} FALLÓ: {s.get('error_code')} {s.get('error')}"
    out.write_bytes(call("GET", s["results"][-1].replace(BASE, ""), raw=True))
    return f"{out.parent.parent.name}/{out.name} ok"


print(f"{len(jobs)} clips por generar, {par} en paralelo", flush=True)
with ThreadPoolExecutor(par) as ex:
    for r in ex.map(run, jobs):
        print(r, flush=True)
