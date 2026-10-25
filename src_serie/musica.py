"""§11: one instrumental track for the whole series with Google Lyria (Gemini API, key in GEMINI_API_KEY).
Saves audio/musica/<name> and prints duration. Usage: musica.py MODEL "prompt" name"""
import base64, json, os, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
model, prompt, name = sys.argv[1], sys.argv[2], sys.argv[3]
key = os.environ.get("GEMINI_API_KEY") or subprocess.run(
    ["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')"],
    capture_output=True, text=True).stdout.strip()
req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8"),
    headers={"x-goog-api-key": key, "Content-Type": "application/json"})
try:
    resp = json.loads(urllib.request.urlopen(req, timeout=600).read())
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")
out_dir = ROOT / "audio" / "musica"; out_dir.mkdir(parents=True, exist_ok=True)
saved = []
for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    if "inlineData" in part:
        mime = part["inlineData"]["mimeType"]
        ext = {"audio/mpeg": ".mp3", "audio/mp3": ".mp3", "audio/wav": ".wav", "audio/x-wav": ".wav"}.get(mime, ".bin")
        f = out_dir / (name + ext)
        f.write_bytes(base64.b64decode(part["inlineData"]["data"]))
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                             capture_output=True, text=True).stdout.strip()
        saved.append(f"{f.name} ({mime}, {dur}s)")
    elif "text" in part:
        print("texto del modelo:", part["text"][:300])
print("guardado:", ", ".join(saved) or f"sin audio — respuesta: {json.dumps(resp)[:600]}")
