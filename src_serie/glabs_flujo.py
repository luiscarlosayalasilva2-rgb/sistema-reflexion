"""Builds a G-Labs Studio workflow (WORKFLOW_JSON_SPEC) for one chapter's Bloque 2:
one `reference` node per ficha (testamento/fichas/TAG.jpg), and for every distinct set of tags a `batch_prompt`
(those scenes, in order) wired with its fichas into a `generate` node (Nano Banana 2, 9:16, 2K).
Usage: glabs_flujo.py N [first last]  ->  glabs/capN_flujo.json (+ capN_flujo_mapa.txt: group/line -> scene)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1])
first, last = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, 10**6)
blocks = [b.strip() for b in (ROOT / f"REFLEXION_CAP{n}_BLOQUE2_IMAGENES.txt").read_text(encoding="utf-8").split("\n\n") if b.strip()]
groups = {}  # tag tuple -> [(scene, prompt)]
for b in blocks:
    num, prompt = b.split(" || ", 1)
    num = int(num)
    if not first <= num <= last:
        continue
    head = prompt.split("vertical 9:16")[0]
    tags = tuple(re.findall(r"\[([A-Z]+)\]", head))
    body = prompt[len(head):]  # drop the [TAG] header: the fichas go in as real reference images
    groups.setdefault(tags, []).append((num, body.replace("\n", " ").strip()))

nodes, edges, ref_idx, mapa = [], [], {}, []
y_ref = 0
for tags in groups:
    for t in tags:
        if t not in ref_idx:
            path = (ROOT / "fichas" / f"{t}.jpg").resolve()
            assert path.exists(), f"falta la ficha {path}"
            ref_idx[t] = len(nodes)
            nodes.append({"id": len(nodes) + 1, "type": "reference", "title": t, "x": -900, "y": y_ref, "w": 300, "h": 300,
                          "inputs": [], "outputs": ["Image"], "ref_mode": "pro", "values": {"file_path": str(path).replace("\\", "/")}})
            y_ref += 340
y = 0
for g, (tags, scenes) in enumerate(groups.items(), 1):
    bp = len(nodes)
    nodes.append({"id": bp + 1, "type": "batch_prompt", "title": f"Grupo {g}: {' '.join(tags)}", "x": -400, "y": y, "w": 400, "h": 300,
                  "inputs": [], "outputs": ["Prompt"], "values": {"prompt_list": "\n".join(p for _, p in scenes)}})
    gen = len(nodes)
    nodes.append({"id": gen + 1, "type": "generate", "title": f"Escenas grupo {g}", "x": 60, "y": y, "w": 400, "h": 400,
                  "inputs": ["Prompt"] + [f"Ref {k}" for k in range(1, len(tags) + 1)], "outputs": ["Image"],
                  "values": {"model": "NARWHAL", "ratio": "IMAGE_ASPECT_RATIO_PORTRAIT", "res_group": "2K"}})
    edges.append({"start_node": bp, "start_socket": 0, "end_node": gen, "end_socket": 0})
    for k, t in enumerate(tags, 1):
        edges.append({"start_node": ref_idx[t], "start_socket": 0, "end_node": gen, "end_socket": k})
    for line, (num, _) in enumerate(scenes, 1):
        mapa.append(f"grupo {g} línea {line} -> escena {num:03d}")
    y += 460
suffix = "" if (first, last) == (1, 10**6) else f"_prueba_{first}-{last}"
out = ROOT / "glabs" / f"cap{n}_flujo{suffix}.json"
out.write_text(json.dumps({"nodes": nodes, "edges": edges, "groups": []}, ensure_ascii=False, indent=1), encoding="utf-8")
(ROOT / "glabs" / f"cap{n}_flujo{suffix}_mapa.txt").write_text("\n".join(mapa) + "\n", encoding="utf-8")
print(f"{out.name}: {sum(len(s) for s in groups.values())} escenas en {len(groups)} grupos, {len(ref_idx)} fichas")
