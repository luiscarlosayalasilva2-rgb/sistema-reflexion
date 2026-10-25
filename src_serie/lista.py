"""Prints visual/capN/imagenes.json as 'n | text' lines for writing spec.txt: lista.py N"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
for o in json.loads((ROOT / "visual" / f"cap{sys.argv[1]}" / "imagenes.json").read_text(encoding="utf-8")):
    print(f"{o['n']} | {o['text']}")
