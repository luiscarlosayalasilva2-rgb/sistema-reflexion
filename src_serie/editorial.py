"""Writes Bloques 5 and 6 from editorial.json and checks the Bloque 5/6 rules."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECL = "Historia ficticia dramatizada · Ilustraciones generadas por IA · Narración con voz sintética"
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")
CTA = re.compile(r"coment|suscr|like|compart|s[ií]gue|opina|campanita|dale", re.I)
data = json.loads((Path(__file__).parent / "editorial.json").read_text(encoding="utf-8"))
for n, d in data.items():
    desc = "\n".join(d["desc"])  # sin preguntas ni declaración de IA (regla de Luis)
    tags = d["tags"].split()
    roots = [re.sub(r"(es|s)$", "", t[1:].lower()) for t in tags]
    words = [w for t in tags for w in re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", t[1:])]
    issues = []
    if len(d["titulo"]) > 70: issues.append(f"título {len(d['titulo'])} > 70")
    if EMOJI.search(d["titulo"]): issues.append("emoji en el título")
    if len(EMOJI.findall(desc)) != 3: issues.append(f"descripción con {len(EMOJI.findall(desc))} emojis")
    if "?" in desc or "¿" in desc: issues.append("pregunta en la descripción")
    if not 8 <= len(tags) <= 12: issues.append(f"{len(tags)} hashtags")
    dup = {w.lower() for w in words if [x.lower() for x in words].count(w.lower()) > 1}
    if len(set(roots)) != len(roots) or dup: issues.append(f"hashtags repetidos: {dup or roots}")
    c = d["comentario"]
    if len(EMOJI.findall(c)) != 3: issues.append(f"comentario con {len(EMOJI.findall(c))} emojis")
    if CTA.search(c): issues.append(f"posible llamado a la acción: {CTA.search(c).group()}")
    sentences = len(re.findall(r"[.!?…]|[\U0001F000-\U0001FAFF☀-➿]\s*$", c))
    (ROOT / f"REFLEXION_CAP{n}_BLOQUE5_TITULO.txt").write_text(f"{d['titulo']}\n\n{desc}\n\n{d['tags']}", encoding="utf-8")
    (ROOT / f"REFLEXION_CAP{n}_BLOQUE6_COMENTARIO.txt").write_text(c, encoding="utf-8")
    print(f"CAP{n}: título {len(d['titulo'])} car, {len(tags)} hashtags " + ("OK" if not issues else "| " + "; ".join(issues)))
