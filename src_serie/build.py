"""Builds Bloques 1, 1B, 2 and 3 for one chapter from visual/capN/spec.txt + refs.json, and audits them
against the master rules (Secciones 10, 11, 12, 15, 19, 21)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
refs = json.loads((Path(__file__).parent / "refs.json").read_text(encoding="utf-8"))
CHARS, LOCS = refs["chars"], refs["locs"]
SHOT = {"G": "wide shot", "M": "medium shot", "C": "close-up", "D": "detail shot", "B": "shot from behind"}
STYLE = "Bold ink outlines, dramatic cel shading, cinematic rim lighting, saturated comic book colors."
HEADER = "Marvel Comics 2D style, bold ink outlines, dramatic cel-shading, saturated comic book colors, cinematic rim lighting"
NEG = {
    "t": "No text, no letters, no words, no writing, no signs, no labels, no captions, no watermarks, no logos, no numbers, no symbols visible anywhere in the image. No blood, no blood stains, no gore, no red splatters on clothes or floors.",
    "d": "Any handwriting on paper is drawn only as abstract wavy scribble lines like a seismograph with no letters at all: no readable names, no character names, no words, no Latin filler text, no numbers, dates or currency signs anywhere, any signature is an unreadable scribble. No text or writing anywhere else in the image, no signs, no labels, no captions, no watermarks, no logos, no numbers, no symbols on hands or background.",
    "m": "Numbers and denomination markings are allowed only on the peso bills. No text, no letters, no words, no writing anywhere else in the image, no signs, no labels, no captions, no watermarks, no logos, no other numbers, no symbols.",
}
EXTRAS = re.compile(r"\b(manager|client|waiter|neighbor|mourners|guests|parishioners|workers|drivers|mechanic|unseen|nurse|notary|guard|crowd|people|attendant|daughter-in-law|lawyer|expert|employees|men|attendees|journalists|students|reporters|audience|crowd|retirees|relatives|mourners)\b")
BANNED = ["stab", "pierce", "crush", "grind", "punch", "kick", "snap", "coil", "bulge", "chain", "skull", "strangle",
          "shriek", "wound", "reference", "tight embrace", "clutched", "gripping her", "pressed against",
          "hyperrealistic", "photorealistic", "realistic", "3d render", "photograph"]
CLIP_BANNED = ["tear", "sunken eyes", "scream", "anguish", "grief"]
MOVES = json.loads((ROOT / "visual" / f"cap{n}" / "moves.json").read_text(encoding="utf-8"))

spec = []
for line in (ROOT / "visual" / f"cap{n}" / "spec.txt").read_text(encoding="utf-8").splitlines():
    if line.strip():
        num, shot, tags, loc, neg, body = line.split("|", 5)
        spec.append(dict(n=int(num), shot=shot, tags=tags.split(), loc=loc, neg=neg, body=body.strip()))
imgs = json.loads((ROOT / "visual" / f"cap{n}" / "imagenes.json").read_text(encoding="utf-8"))
problems = []
if [s["n"] for s in spec] != [i["n"] for i in imgs]:
    problems.append(f"spec numbering {len(spec)} != imagenes {len(imgs)}")


def tag_clause(body, tags):
    for t in tags:
        key, _, variant = t.partition(":")
        desc = CHARS[key][variant or "scene"]
        body = body.replace(f"[{t}]", f"[{key}] ({desc})", 1).replace(f"[{t}]", f"[{key}]")
    return body


def prompt(s, move=None):
    tags = [t.partition(":")[0] for t in s["tags"]]
    head = " ".join(f"[{t}]" for t in tags) + (f" [{s['loc']}]" if s["loc"] not in "*-" else "")
    shot = SHOT[s["shot"]] + (f" with a {move}" if move else "")
    body = tag_clause(s["body"], s["tags"])
    if s["loc"] == "ZARAPE" and s["tags"]:  # the model kept draping the bedroom's sarape on the character
        body += ", the striped sarape blanket stays spread flat on the bed and nobody wears it, no blanket or shawl over anyone's shoulders"
    names = ", ".join(f"[{t}]" for t in tags)
    only = f"Only {names} in frame." if not EXTRAS.search(s["body"]) else f"Only {names} as named characters in frame, any other person without a visible face and without a name."
    use = "Use only: " + " ".join(f"[{t}]" for t in tags) + (f" [{s['loc']}]" if s["loc"] not in "*-" else "") + "."
    rest = "Do not use any other item from the folder" + (" and no place at all." if s["loc"] == "-" else ".")
    style = "Marvel Comics 2D animated style" if move else "Marvel Comics 2D style"
    p = f"{head} vertical 9:16 portrait composition, {style}, {shot} of {body}. {only} {use} {rest} {STYLE} {NEG[s['neg']]}"
    return p + (" 4 second clip. No text or writing anywhere in the frame." if move else "")


b2 = [f"{s['n']} || {prompt(s)}" for s in spec]
last = spec[-1]["n"]
clip_nums = [1, 2, 3, 4, last]
b3 = [f"{s['n']} || {prompt(s, MOVES[str(s['n'])])}" for s in spec if s["n"] in clip_nums]

# ---- Bloque 1: only refs that appear for the first time in this chapter
prev = set()
for k in range(1, n):
    f = ROOT / f"REFLEXION_CAP{k}_BLOQUE1B_NOMBRES_REFERENCIA.txt"
    if f.exists():
        prev |= set(f.read_text(encoding="utf-8").split())
used_chars, used_locs = [], []
for s in spec:
    for t in s["tags"]:
        t = t.partition(":")[0]
        if t not in used_chars:
            used_chars.append(t)
    if s["loc"] not in "*-" and s["loc"] not in used_locs:
        used_locs.append(s["loc"])
new_chars = [c for c in used_chars if c not in prev]
new_locs = [l for l in used_locs if l not in prev]
b1 = [f"Marvel comic 2D style professional model sheet in one single image on a plain empty white background, {c}: {CHARS[c]['ficha']}. "
      f"The sheet shows the same character as a full body front view, side profile, back view and three-quarter view, three face close-ups "
      f"with neutral, sad and surprised expressions, a detail of the hands and a detail of the clothing, all perfectly consistent. "
      f"Bold ink outlines, dramatic cel shading, warm golden rim light, saturated comic book colors. {NEG['t']}" for c in new_chars]
b1 += [f"Marvel Comics 2D style environment illustration, {l}: {LOCS[l]}. No people in frame. {STYLE} {NEG['t']}" for l in new_locs]

# ---- audits
counts = {r: sum(1 for s in spec if r in [t.partition(':')[0] for t in s["tags"]] or s["loc"] == r) for r in used_chars + used_locs}
shots = [s["shot"] for s in spec]
for i in range(1, len(shots)):
    if shots[i] == shots[i - 1]:
        problems.append(f"plano repetido en {i}-{i + 1}: {shots[i]}")
gi = [i for i, s in enumerate(shots) if s == "G"]
for a, b in zip([-1] + gi, gi + [len(shots)]):
    if b - a > 10:
        problems.append(f"sin plano general entre {a + 2} y {b}")
faceless = sum(1 for s in shots if s in "DB") / len(shots)
if faceless < 0.30:
    problems.append(f"planos sin rostro {faceless:.0%} < 30%")
text_all = " ".join(b2 + b3 + b1) + " " + HEADER
for w in BANNED:
    if re.search(rf"\b{re.escape(w)}", " ".join(b2 + b3 + b1), re.I):
        problems.append(f"palabra prohibida: {w}")
for w in CLIP_BANNED:
    if re.search(rf"\b{re.escape(w)}", " ".join(b3), re.I):
        problems.append(f"palabra que dispara filtro de video: {w}")
all_names = set(CHARS) | set(LOCS)
vocab = {w for w in re.findall(r"[a-záéíóúñ]+", text_all.lower())} - {x.lower() for x in all_names}
for r in all_names & (set(used_chars) | set(used_locs)):
    hits = sorted(w for w in vocab if w.startswith(r[:3].lower()))
    if hits:
        problems.append(f"prefijo {r[:3]} de {r} choca con: {', '.join(hits)}")
for s in spec:
    for t in s["tags"]:
        if f"[{t}]" not in s["body"]:
            problems.append(f"img {s['n']}: [{t}] etiquetado sin acción en el cuerpo")

out = ROOT
(out / f"REFLEXION_CAP{n}_BLOQUE1_PERSONAJES_LOCACIONES.txt").write_text("\n\n".join(b1), encoding="utf-8")
(out / f"REFLEXION_CAP{n}_BLOQUE1B_NOMBRES_REFERENCIA.txt").write_text("\n".join(new_chars + new_locs), encoding="utf-8")
(out / f"REFLEXION_CAP{n}_BLOQUE2_IMAGENES.txt").write_text("\n\n".join(b2), encoding="utf-8")
(out / f"REFLEXION_CAP{n}_BLOQUE3_CLIPS.txt").write_text("\n\n".join(b3), encoding="utf-8")
print(f"CAP{n}: {len(b2)} prompts, clips {clip_nums}, planos sin rostro {faceless:.0%}")
print("Personajes: " + ", ".join(new_chars))
print("Locaciones: " + ", ".join(new_locs))
print("Referencias nuevas: " + ", ".join(new_chars + new_locs))
print("Referencias que se reutilizan: " + (", ".join(r for r in used_chars + used_locs if r in prev) or "ninguna"))
for r in used_chars + used_locs:
    print(f"{r} — aparece en {counts[r]} imágenes")
print("PROBLEMAS:" if problems else "Auditoría sin problemas.")
for p in problems:
    print("  " + p)
