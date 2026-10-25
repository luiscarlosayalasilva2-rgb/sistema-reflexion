---
name: feedback-marca-agua
description: "Desde 2026-10-24 todas las series nuevas llevan marca de agua 'Reflexiones con Raíces' durante todo el video (la pidió Luis contra robos de contenido)"
metadata:
  type: feedback
---

Luis pidió una marca de agua "REFLEXIONES CON RAÍCES" visible TODO el video, en letra elegante y en una zona que no estorbe, para que no le roben el contenido.

**Why:** protección contra robo de contenido; aplica a las ideas nuevas (las series ya entregadas antes del 2026-10-24 no la llevan, salvo que él lo pida).
**How to apply:** `src\poner_marca.py N` (Georgia cursiva blanca semitransparente con sombra y línea fina, centrada abajo y=1550, debajo de los subtítulos) ya está en `montar_serie.ps1` como último paso tras el banner; copiar `poner_marca.py` y `fonts\georgiai.ttf` a toda carpeta de serie nueva (se copian con los scripts de mozo\src). Guarda `REFLEXION_CAPN_sin_marca.mp4` y es idempotente. Relacionado: [[feedback-banner-capitulo]].
