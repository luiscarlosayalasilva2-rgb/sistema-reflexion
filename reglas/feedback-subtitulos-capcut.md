---
name: feedback-subtitulos-capcut
description: "Subtitle spec for every video from 2026-10-15 — CapCut style, Montserrat ExtraBold, lower quarter of the screen with drop shadow (replaces the Baloo 2 / y=1350 spec of the master)."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-16T01:14:40.313Z
---

Subtítulos estilo CapCut: Montserrat ExtraBold (fonts\Montserrat-ExtraBold.ttf), MAYÚSCULAS, blanco con contorno negro (Outline 7), la palabra que se está diciendo en AMARILLO puro (&H0000FFFF&, mismo tamaño), ~3 palabras a la vez, grandes (92 en 1080×1920) y en el cuarto inferior de la pantalla (\an5\pos(540,1440)), con sombra negra semitransparente (Shadow 6, BackColour &H60000000). Applies to the chapter AND the hook subtitles.

**Why:** Luis pasted this spec on 2026-10-15; it replaces §10/§28 (Baloo 2, y=1350, enlarged word).
**How to apply:** `testamento\src\subs.py` and `subs_hook.py` already use it; copy them to new series. Keep 0 overlaps / no \kf / no \fad. See [[sistema-produccion]].
