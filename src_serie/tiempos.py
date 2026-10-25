"""Sección 8: cues of srt/capN.srt -> images in 1.7–4.0 s (split long cues, merge short ones),
contiguous from 0.00 to the real audio duration. Writes visual/capN/imagenes.json + Bloques 4 and 4B."""
import json, math, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN, MAX = 1.7, 4.0
caps = [int(c) for c in sys.argv[1:]] or [1, 2, 3, 4, 5]


def sec(t):
    h, m, s = t.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def split_text(text, k):
    """k pieces, cutting after a comma/period when one is near each ideal cut, else at a word boundary."""
    w = text.split()
    cuts, prev = [], 0
    for j in range(1, k):
        ideal = round(len(w) * j / k)
        cand = [i for i in range(max(prev + 1, ideal - 2), min(len(w), ideal + 3)) if re.search(r"[,.?!]$", w[i - 1])]
        c = min(cand, key=lambda i: abs(i - ideal)) if cand else max(prev + 1, min(ideal, len(w) - 1))
        cuts.append(c)
        prev = c
    edges = [0] + cuts + [len(w)]
    return [" ".join(w[a:b]) for a, b in zip(edges, edges[1:])]


for n in caps:
    raw = (ROOT / "srt" / f"cap{n}.srt").read_text(encoding="utf-8").strip().split("\n\n")
    cues = []
    for block in raw:
        lines = block.splitlines()
        a, b = lines[1].split(" --> ")
        cues.append([sec(a), sec(b), " ".join(lines[2:]), 1])  # last field: original cue count
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(ROOT / "audio" / "pulido" / f"cap{n}.mp3")], capture_output=True, text=True).stdout)
    cues[0][0] = 0.0
    cues[-1][1] = dur
    for i in range(len(cues) - 1):
        cues[i][1] = cues[i + 1][0]

    merges = 0
    while True:  # merge passes
        short = next((i for i, c in enumerate(cues) if c[1] - c[0] < MIN), None)
        if short is None:
            break
        j = short if short < len(cues) - 1 else short - 1  # merge with the next one (last merges backwards)
        a, b = cues[j], cues[j + 1]
        cues[j:j + 2] = [[a[0], b[1], a[2] + " " + b[2], a[3] + b[3]]]
        merges += 1

    out, splits = [], 0
    for s, e, t, _ in cues:
        k = max(1, math.ceil((e - s) / MAX - 1e-9))
        while k > 1 and (e - s) / k < MIN:
            k -= 1
        if k > 1:
            splits += k - 1
        for p, piece in enumerate(split_text(t, k)):
            out.append({"start": round(s + (e - s) * p / k, 2), "end": round(s + (e - s) * (p + 1) / k, 2), "text": piece})
    for i in range(len(out) - 1):
        out[i]["end"] = out[i + 1]["start"]
    out[-1]["end"] = round(dur, 2)
    for i, o in enumerate(out, 1):
        o["n"] = i

    bad = [o for o in out if not (MIN - 0.011 <= o["end"] - o["start"] <= MAX + 0.011)]
    d = ROOT / "visual" / f"cap{n}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "imagenes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    m_s = lambda t: f"{int(round(t)) // 60}:{int(round(t)) % 60:02}"
    (ROOT / f"REFLEXION_CAP{n}_BLOQUE4_TIEMPOS.txt").write_text(
        "\n".join(f"{o['n']}= {m_s(o['start'])} a {m_s(o['end'])}" for o in out), encoding="utf-8")
    (ROOT / f"REFLEXION_CAP{n}_BLOQUE4B_TIEMPOS_MS.txt").write_text(
        "\n".join(f"{o['n']} {o['start']:.2f} {o['end']:.2f}" for o in out), encoding="utf-8")
    print(f"CAP{n} Cues del SRT: {len(raw)} — Cortes por exceso: {splits} — Fusiones por defecto: {merges} — "
          f"Imágenes finales: {len(out)}  (dur {dur:.2f}s, fuera de rango: {len(bad)})")
