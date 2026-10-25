"""Builds out/TEXTOS_EDITORIALES.txt from the Bloque 5/6 files and copies the series to Google Drive:
VID N.mp4 (= REFLEXION_CAPN_FINAL.mp4), MINIATURA_CAPN.jpg, TEXTOS_EDITORIALES.txt, verifying each copy by MD5.
Usage: entregar.py "Nombre de la carpeta en Drive" """
import hashlib, os, shutil, string, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def mi_unidad():
    """Carpeta 'Mi unidad' de Google Drive: env DRIVE_ROOT, o la primera letra que la tenga (G: primero)."""
    cands = []
    if os.environ.get("DRIVE_ROOT"):
        cands.append(Path(os.environ["DRIVE_ROOT"]))
    cands += [Path(f"{l}:/Mi unidad") for l in "G" + string.ascii_uppercase.replace("G", "")]
    for p in cands:
        try:
            if p.is_dir():
                return p
        except OSError:
            pass
    sys.exit("No encuentro 'Mi unidad' (Google Drive cerrado o sin sesion). Define DRIVE_ROOT con la ruta si esta en otro sitio.")


dest = mi_unidad() / sys.argv[1]
out = ROOT / "out"
parts = []
for n in range(1, 6):
    b5 = (ROOT / f"REFLEXION_CAP{n}_BLOQUE5_TITULO.txt").read_text(encoding="utf-8").strip()
    b6 = (ROOT / f"REFLEXION_CAP{n}_BLOQUE6_COMENTARIO.txt").read_text(encoding="utf-8").strip()
    parts.append(f"===== CAPÍTULO {n} =====\n{b5}\n\nComentario anclado:\n{b6}\n")
(out / "TEXTOS_EDITORIALES.txt").write_text("\n".join(parts), encoding="utf-8")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


files = [(out / f"REFLEXION_CAP{n}_FINAL.mp4", f"VID {n}.mp4") for n in range(1, 6)]
files += [(out / f"MINIATURA_CAP{n}.jpg", f"MINIATURA_CAP{n}.jpg") for n in range(1, 6)]
files += [(out / "TEXTOS_EDITORIALES.txt", "TEXTOS_EDITORIALES.txt")]
dest.mkdir(parents=True, exist_ok=True)
parcial = os.environ.get("PARCIAL") == "1"  # PARCIAL=1: deliver only what already exists (the rest comes in a later run)
for src, name in files:
    if not src.exists():
        if parcial:
            print(f"{name}: todavia no existe, se entrega despues", flush=True)
            continue
        sys.exit(f"falta {src}")
    d = dest / name
    if d.exists() and d.stat().st_size == src.stat().st_size and md5(src) == md5(d):  # already delivered and identical: do not upload again
        print(f"{name}: ya estaba en Drive, md5 igual", flush=True)
        continue
    shutil.copyfile(src, d)
    ok = md5(src) == md5(d)
    print(f"{name}: {src.stat().st_size // 1024} KB {'OK (md5 igual)' if ok else 'ERROR md5 distinto'}", flush=True)
