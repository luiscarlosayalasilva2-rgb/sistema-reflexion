"""Hook video through the G-Labs API: Omni Flash, ingredients ("components") mode, 9:16, 10 s, 720p.
Ingredients: TABLERO_CAPN.jpg + toma1..4 (trimmed to the API limit if it rejects). Prompt: hooks/capN/prompt_hook.txt.
Saves hooks/capN/HOOK_CAPN.mp4. Usage: glabs_hook.py N [N...]"""
import json, os, subprocess, sys, time, urllib.error, urllib.request
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


def run(n):
    d = ROOT / "hooks" / f"cap{n}"
    out = d / f"HOOK_CAP{n}.mp4"
    prompt = (d / "prompt_hook.txt").read_text(encoding="utf-8").strip()
    refs = [d / f"TABLERO_CAP{n}.jpg"] + [d / f"toma{i}.jpg" for i in range(1, 5)]
    model = os.environ.get("HOOK_MODEL", "omni_flash")  # HOOK_MODEL=omni_vids -> Google Vids (1-3 ingredients, 3-10 s)
    # Vids / Muse take at most 3 references and refuse (CONTENT_POLICY) some image combinations: try the board + first + last shot first
    sets = [[refs[0], refs[1], refs[4]], [refs[0]], [refs[0], refs[2], refs[3]]] if model in ("omni_vids", "meta_muse") else [refs[:5], refs[:3], refs[:1]]
    err = "la API no aceptó el hook"
    for rs in sets:
        body = {"prompt": prompt, "model": model, "aspect_ratio": "9:16", "mode": "components",
                "reference_images": [{"path": str(p.resolve())} for p in rs], "video_length": 10, "resolution": ["720p"]}
        if model == "meta_muse":  # Meta Muse: 2-3 images = references; no resolution field
            body.update(mode="image_to_video", count=1)
            body.pop("resolution")
        try:
            tid = call("POST", "/api/video/generate", body)["task_id"]
        except urllib.error.HTTPError as e:
            err = f"{len(rs)} referencias rechazadas -> " + e.read().decode("utf-8", "replace")[:200]
            print(f"cap{n}: {err}", flush=True)
            continue
        while (s := call("GET", f"/api/status/{tid}"))["status"] not in ("completed", "failed"):
            time.sleep(10)
        if s["status"] == "failed":
            err = f"FALLÓ ({len(rs)} refs): {s.get('error_code')} {s.get('error')}"
            if "CONTENT_POLICY" in str(s.get("error")) or "CONTENT_POLICY" in str(s.get("error_code")):
                print(f"cap{n}: {err}; pruebo otras referencias", flush=True)
                continue
            return f"cap{n} {err}"
        out.write_bytes(call("GET", s["results"][-1].replace(BASE, ""), raw=True))
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                             capture_output=True, text=True).stdout.strip()
        return f"cap{n}: HOOK_CAP{n}.mp4 ok ({dur}s, {len(rs)} referencias)"
    return f"cap{n} {err}"


with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run, [int(a) for a in sys.argv[1:]]):
        print(r, flush=True)
