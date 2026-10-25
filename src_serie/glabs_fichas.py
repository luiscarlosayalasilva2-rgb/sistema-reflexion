"""Bloque 1 fichas through the G-Labs webhook API: one model sheet per character (16:9) and one environment per
location (9:16), built from src/refs.json with the same wording as build.py. Writes fichas/TAG.jpg, skips existing.
Usage: glabs_fichas.py [TAG ...] [--parallel K]"""
import json, os, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"
only = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
par = int(sys.argv[sys.argv.index("--parallel") + 1]) if "--parallel" in sys.argv else 8
KEY = os.environ.get("GLABS_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GLABS_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
refs = json.loads((ROOT / "src" / "refs.json").read_text(encoding="utf-8"))
STYLE = "Bold ink outlines, dramatic cel shading, cinematic rim lighting, saturated comic book colors."
NEG = ("No text, no letters, no words, no writing, no signs, no labels, no captions, no watermarks, no logos, "
       "no numbers, no symbols visible anywhere in the image. No blood, no blood stains, no gore, no red splatters on clothes or floors.")


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if raw else json.loads(data)


jobs = []
for c, d in refs["chars"].items():
    jobs.append((c, "16:9",
                 f"Marvel comic 2D style professional model sheet in one single image on a plain empty white background, of {d['ficha']}. "
                 "The sheet shows the same character as a full body front view, side profile, back view and three-quarter view, three face close-ups "
                 "with neutral, sad and surprised expressions, a detail of the hands and a detail of the clothing, all perfectly consistent. "
                 f"Bold ink outlines, dramatic cel shading, warm golden rim light, saturated comic book colors. {NEG} No name labels."))
for l, d in refs["locs"].items():
    jobs.append((l, "9:16", f"Marvel Comics 2D style environment illustration, vertical 9:16, {d}. No people in frame. {STYLE} {NEG}"))
out = ROOT / "fichas"; out.mkdir(exist_ok=True)
jobs = [j for j in jobs if (not only or j[0] in only) and not (out / f"{j[0]}.jpg").exists()]


def run(job):
    tag, ar, prompt = job
    t = call("POST", "/api/image/generate", {"prompt": prompt, "model": os.environ.get("GLABS_IMG_MODEL", "nano_banana_2"), "aspect_ratio": ar, "upscale": ["2K"]})
    while True:
        time.sleep(5)
        s = call("GET", f"/api/status/{t['task_id']}")
        if s.get("status") in ("completed", "failed"):
            break
    if s["status"] == "failed":
        return f"{tag} FALLÓ: {s.get('error_code')} {s.get('error')}"
    url = s["results"][-1]
    ext = Path(url.split("?")[0]).suffix or ".jpg"
    data = call("GET", url.replace(BASE, ""), raw=True)
    tmp = out / f"{tag}{ext}"
    tmp.write_bytes(data)
    if ext.lower() != ".jpg":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-q:v", "2", str(out / f"{tag}.jpg")], check=True)
        tmp.unlink()
    return f"{tag} ok"


print(f"{len(jobs)} fichas por generar")
with ThreadPoolExecutor(par) as ex:
    for f in as_completed([ex.submit(run, j) for j in jobs]):
        try:
            print(f.result(), flush=True)
        except Exception as e:
            print("error:", e, flush=True)
