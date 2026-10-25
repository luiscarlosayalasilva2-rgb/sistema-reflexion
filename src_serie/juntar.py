"""Joins the 5 Parte B guiones of a series into one readable file: juntar.py "TÍTULO" out.txt"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parts = [sys.argv[1], ""]
for n in range(1, 6):
    b = (ROOT / f"REFLEXION_CAP{n}_GUION_PARTE_B.txt").read_text(encoding="utf-8")
    parts += [f"CAPÍTULO {n}  ({len(b)} caracteres, ~{round(len(b.split()) / 2.4 / 60, 1)} min)", "", b, ""]
(ROOT / sys.argv[2]).write_text("\n".join(parts), encoding="utf-8")
