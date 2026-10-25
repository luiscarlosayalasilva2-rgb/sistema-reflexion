"""Bloque 8 thumbnails through the G-Labs API (Nano Banana 2, 9:16, 2K, fichas as references) -> out/MINIATURA_CAPN.jpg
resized to exactly 1080x1920. Usage: miniaturas.py [N ...]"""
import json, os, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"
KEY = os.environ.get("GLABS_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GLABS_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
refs = json.loads((Path(__file__).parent / "refs.json").read_text(encoding="utf-8"))["chars"]
STYLE = "Marvel Comics 2D style, bold ink outlines, dramatic cel shading, cinematic rim lighting, saturated comic book colors"
M = {
    1: ("ZACARIAS", "VOLANTE", "holding an old handwritten notebook sheet with a trembling hand near his mouth, eyes looking down to the side",
        "the old handwritten partnership sheet and a small carved wooden chest", "two young partners shaking hands in front of white trucks at sunrise",
        "JURAMOS SER SOCIOS", "A LA MITAD... Y ME ROBÓ"),
    2: ("ZACARIAS", "VOLANTE", "staring down at a thin cash envelope in his hand, forehead creased with worry",
        "a thin cash envelope with only two peso bills", "a stocky man in round glasses closing a black notebook in an office",
        "DE 90 MIL A 36 MIL", "Y ÉL DECÍA: ES EL MERCADO"),
    3: ("ZACARIAS", "YODO", "standing by a hospital bed with his hand over his mouth, eyes wet and looking to the side",
        "a sealed testament envelope on a hospital bedside table", "a bearded man in a black polo shirt blocking a hospital door",
        "SE ESTABA MURIENDO", "Y NO ME DIJO QUÉ DECÍA SU TESTAMENTO"),
    4: ("ZACARIAS", "NIXTAMAL", "reading a handwritten letter under a bare bulb, hand trembling near his face, devastated",
        "a torn yellow envelope and handwritten pages on a flowered tablecloth", "a gray-haired woman in a plum cardigan placing a yellow envelope on a table",
        "MI ESPOSA GUARDÓ 2 AÑOS", "LA CONFESIÓN DE MI COMPADRE"),
    5: ("ZACARIAS", "VITRAL", "with silent devastation, eyes lowered, one hand on a small brass plaque",
        "a ring of truck keys and a small brass plaque", "a man in a black polo shirt dropping truck keys on a gray desk",
        "ME ROBÓ 11 MILLONES", "Y AUN ASÍ NO LO DEMANDÉ"),
}


def prompt(n):
    who, loc, gesture, obj, inset, gold, red = M[n]
    return (f"vertical 9:16 portrait composition, {STYLE}, dramatic Facebook video thumbnail poster. "
            f"Extreme close-up of {refs[who.partition(':')[0]][who.partition(':')[2] or 'scene']}, {gesture}, never smiling and not looking at the viewer, "
            f"hard side lighting carving deep shadows over half of the face against a darkened background with a dark vignette, "
            f"the clue object clearly visible: {obj}. "
            f"A small comic-panel inset with a bold black border in the lower corner showing {inset}. "
            f"Headline text rendered natively in the image, centered: on top in huge bold condensed comic lettering, golden yellow with a thick black outline: "
            f"'{gold}'; below it, in the same heavy lettering in white inside a solid red rectangular box: '{red}'. "
            f"In the top-left corner an orange rounded badge with the white bold text 'CAPÍTULO {n}'. "
            f"Spell every word of the text exactly as written, with its accents. The headline and the chapter badge are the ONLY text in the whole image: any paper, card, letter, receipt or screen shows only abstract wavy scribble lines with no letters, no English words and no numbers. "
            f"No watermarks, no logos, safe for all audiences, no graphic content.")


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = r.read()
    return d if raw else json.loads(d)


def run(n):
    who, loc = M[n][0], M[n][1]
    model = os.environ.get("GLABS_IMG_MODEL", "nano_banana_2")
    body = {"prompt": prompt(n), "model": model, "aspect_ratio": "9:16",
            "reference_images": [{"path": str((ROOT / "fichas" / f"{t}.jpg").resolve())} for t in (who.partition(":")[0], loc)]}
    body.update(keep=1, remove_logo=True) if model == "nano_pics" else body.update(upscale=["2K"])
    tid = call("POST", "/api/image/generate", body)["task_id"]
    while (s := call("GET", f"/api/status/{tid}"))["status"] not in ("completed", "failed"):
        time.sleep(5)
    if s["status"] == "failed":
        return f"cap{n} FALLÓ: {s.get('error')}"
    raw = ROOT / "out" / f"_miniatura_cap{n}_2k{Path(s['results'][-1]).suffix}"
    raw.write_bytes(call("GET", s["results"][-1].replace(BASE, ""), raw=True))
    out = ROOT / "out" / f"MINIATURA_CAP{n}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf", "scale=1080:1920:flags=lanczos", "-q:v", "2", str(out)], check=True)
    return f"cap{n}: {out.name} 1080x1920"


if (Path(__file__).parent / "miniaturas.json").exists():  # per-series table: {"N": [who, loc, gesture, obj, inset, gold, red]}
    M = {int(k): v for k, v in json.loads((Path(__file__).parent / "miniaturas.json").read_text(encoding="utf-8")).items()}
caps = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(run, caps):
        print(r, flush=True)
