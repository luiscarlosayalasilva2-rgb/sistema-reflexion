"""Updates the status table in CONTEXTO.md and copies it to the desktop context folder.
Usage: estado.py CAP "col1|col2|...|col7"  (the 7 cells after the chapter name)"""
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOMBRE = "CONTEXTO CLAUDE - Sistema de produccion"
# Copia del contexto: escritorio (OneDrive o normal) si existe; si no, la carpeta del proyecto (ROOT\..\)
DESK = next((p for p in (Path.home() / "OneDrive" / "Escritorio" / NOMBRE, Path.home() / "Desktop" / NOMBRE,
                         Path.home() / "Escritorio" / NOMBRE, ROOT.parent / NOMBRE) if p.is_dir()), None)
f = ROOT / "CONTEXTO.md"
t = f.read_text(encoding="utf-8")
for cap, cells in zip(sys.argv[1::2], sys.argv[2::2]):
    row = "| Cap " + cap + " | " + " | ".join(cells.split("|")) + " |"
    t = re.sub(r"\| Cap " + cap + r" \|[^\n]*", lambda m: row, t)
f.write_text(t, encoding="utf-8")
if DESK:
    shutil.copy(f, DESK / "CONTEXTO.md")
    print("CONTEXTO.md actualizado y copiado a", DESK)
else:
    print("CONTEXTO.md actualizado (no hay carpeta de contexto donde copiarlo)")
