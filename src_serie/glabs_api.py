"""Bloque 2 scenes through the G-Labs Studio webhook API (MAX): POST /api/image/generate with the scene prompt,
its fichas as local-path references, 9:16, Nano Banana 2, upscale 2K; polls /api/status/{id}; downloads the result to
visual/capN/imgs/NNN.<ext>. Skips scenes already present. Usage: glabs_api.py N [first last] [--parallel K]"""
import json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
n = int(args[0])
first, last = (int(args[1]), int(args[2])) if len(args) > 2 else (1, 10**6)
par = int(sys.argv[sys.argv.index("--parallel") + 1]) if "--parallel" in sys.argv else 8
KEY = os.environ.get("GLABS_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GLABS_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
assert KEY, "falta GLABS_API_KEY"


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if raw else json.loads(data)


imgs = ROOT / "visual" / f"cap{n}" / "imgs"; imgs.mkdir(parents=True, exist_ok=True)
jobs = []
for b in (ROOT / f"REFLEXION_CAP{n}_BLOQUE2_IMAGENES.txt").read_text(encoding="utf-8").split("\n\n"):
    if not b.strip():
        continue
    num, prompt = b.strip().split(" || ", 1)
    num = int(num)
    if not first <= num <= last or list(imgs.glob(f"{num:03d}.*")):
        continue
    head = prompt.split("vertical 9:16")[0]
    tags = re.findall(r"\[([A-Z]+)\]", head)
    refs = [{"path": str((ROOT / "fichas" / f"{t}.jpg").resolve())} for t in tags]
    jobs.append((num, prompt[len(head):].strip(), refs))


import threading
blocked = threading.Event()  # set on UNUSUAL_ACTIVITY / TOO_MUCH_TRAFFIC: stop sending more work so the block does not get longer


def run(job):
    num, prompt, refs = job
    if blocked.is_set():
        return f"{num:03d} saltada (Google pidió esperar)"
    model = os.environ.get("GLABS_IMG_MODEL", "nano_banana_2")
    body = {"prompt": prompt, "model": model, "aspect_ratio": "9:16", "reference_images": refs}
    if model == "nano_pics":
        body.update(keep=1, remove_logo=True)
    else:
        body["upscale"] = ["2K"]
    t = call("POST", "/api/image/generate", body)
    tid = t["task_id"]
    while True:
        time.sleep(5)
        s = call("GET", f"/api/status/{tid}")
        if s.get("status") in ("completed", "failed"):
            break
    if s["status"] == "failed":
        if re.search(r"UNUSUAL_ACTIVITY|TOO_MUCH_TRAFFIC", f"{s.get('error_code')} {s.get('error')}"):
            blocked.set()
        return f"{num:03d} FALLÓ: {s.get('error_code')} {s.get('error')}"
    url = s["results"][-1]
    ext = Path(url.split("?")[0]).suffix or ".jpg"
    data = call("GET", url.replace(BASE, ""), raw=True)
    (imgs / f"{num:03d}{ext}").write_bytes(data)
    if ext.lower() != ".jpg":  # montage expects NNN.jpg; G-Labs sometimes returns webp/png
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(imgs / f"{num:03d}{ext}"), "-q:v", "2", str(imgs / f"{num:03d}.jpg")], check=True)
        (imgs / f"{num:03d}{ext}").unlink()
    return f"{num:03d} ok ({len(data) // 1024} KB) <- {Path(url).name}"


print(f"cap{n}: {len(jobs)} escenas por generar, {par} en paralelo")
with ThreadPoolExecutor(par) as ex:
    for f in as_completed([ex.submit(run, j) for j in jobs]):
        try:
            print(f.result(), flush=True)
        except Exception as e:
            print("error:", e, flush=True)
