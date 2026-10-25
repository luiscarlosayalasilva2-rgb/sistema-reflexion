"""Hook board shots through the G-Labs API: hooks/capN/tomas.txt ("i || prompt") -> hooks/capN/tomaI.jpg
(fichas from the [TAG] header as references, 9:16, Nano Banana 2, 2K). Skips existing shots. Usage: glabs_tomas.py N [N...]"""
import json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"
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
for n in map(int, sys.argv[1:]):
    d = ROOT / "hooks" / f"cap{n}"
    for b in (d / "tomas.txt").read_text(encoding="utf-8").split("\n\n"):
        if not b.strip():
            continue
        i, prompt = b.strip().split(" || ", 1)
        out = d / f"toma{i}.jpg"
        if out.exists():
            continue
        head = prompt.split("vertical 9:16")[0]
        refs = [{"path": str((ROOT / "fichas" / f"{t}.jpg").resolve())} for t in re.findall(r"\[([A-Z]+)\]", head)]
        jobs.append((out, prompt[len(head):].strip(), refs))


def run(job):
    out, prompt, refs = job
    tid = call("POST", "/api/image/generate", {"prompt": prompt, "model": os.environ.get("GLABS_IMG_MODEL", "nano_banana_2"), "aspect_ratio": "9:16",
                                               "reference_images": refs, "upscale": ["2K"]})["task_id"]
    while (s := call("GET", f"/api/status/{tid}"))["status"] not in ("completed", "failed"):
        time.sleep(5)
    if s["status"] == "failed":
        return f"{out.parent.name}/{out.name} FALLÓ: {s.get('error_code')} {s.get('error')}"
    url = s["results"][-1]
    tmp = out.with_suffix(Path(url.split("?")[0]).suffix or ".jpg")
    tmp.write_bytes(call("GET", url.replace(BASE, ""), raw=True))
    if tmp != out:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-q:v", "2", str(out)], check=True)
        tmp.unlink()
    return f"{out.parent.name}/{out.name} ok"


print(f"{len(jobs)} tomas por generar")
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run, jobs):
        print(r, flush=True)
