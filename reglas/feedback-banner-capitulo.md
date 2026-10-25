---
name: feedback-banner-capitulo
description: "Próximas series: agregar un panel/bandera \"CAPÍTULO N\" en los primeros 5 s de cada video"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-19T01:41:04.905Z
---

Idea del usuario (2026-10-18): en las **próximas series**, cada video debe llevar una bandera o panel que diga "Capítulo 1, 2, 3, 4, 5" durante los **primeros 5 segundos**. NO aplicarlo a las series ya entregadas (cumple / regreso / restaurante, ni las anteriores): el usuario dijo explícitamente "ya para la próxima".

**Why:** que el espectador sepa qué capítulo ve y que son una serie de 5.

**ÚLTIMO AJUSTE (2026-10-18, prevalece):** el usuario pidió "más arriba, de color amarillo y que diga 2 de 5": texto "CAPÍTULO N DE 5" en amarillo de subtítulos (255,221,0) con contorno negro y líneas amarillas, overlay en y=90 (banner_capitulo.py ya actualizado; ejemplo calude\ejemplo_banner_amarillo.mp4). **APROBADO por el usuario ("deja así para las próximas").** Aplicar en TODAS las series nuevas: generar con calude\banner_capitulo.py N out.png y superponer sobre out\REFLEXION_CAPN_FINAL.mp4 (overlay x=0, y=90, fade in 0.2–0.8 s, fade out 4.4–5.0 s, loop de 5.2 s, preset veryfast) antes de entregar.py. Filtro de ejemplo en calude\fg3.txt.

**Diseño anterior (2026-10-18):** estilo "título de cine" sin caja: texto blanco ExtraBold con sombra suave, líneas finas naranja a los lados, arriba (y≈210), sube suave con fade-in 0.6 s y fade-out antes del s 5. El usuario dijo "me gusta, nomás que salga en capítulo" → interpreté: SOLO "CAPÍTULO N" (sin nombre de serie). Si responde que quería otra cosa, ajustar. Scripts listos: calude\banner_capitulo.py N out.png (solo capítulo) y calude\banner_titulo.py (con nombre de serie); overlay con ffmpeg usando "-/filter_complex" archivo (esta build no tiene -filter_complex_script); ejemplo en calude\ejemplo_banner_solo_capitulo.mp4.

**How to apply (original):** en la próxima serie, antes de entregar.py, superponer sobre out\REFLEXION_CAPN_FINAL.mp4 un PNG (pastilla naranja como la de las miniaturas, Montserrat ExtraBold, "CAPÍTULO N", posición arriba, y=~140 para no chocar con subtítulos en y=1440 ni los del hook) con fade in/out, visible 0–5 s (ffmpeg overlay con enable='lte(t,5)'). Hacerlo dentro de unir.py o como paso final, usando preset veryfast. Ver [[sistema-produccion]] y [[series-cumple-regreso-restaurante]].

**Implementado (2026-10-18):** restaurante\src es la copia canónica para la próxima serie (copiar su src entero): poner_banner.py N (después de unir.py, antes de entregar.py), enc.py (env QSV=1), montar_al_vuelo.ps1 (monta cada capítulo en cuanto tiene 5 clips + hook, solapado con glabs_clips). Ver [[velocidad-pipeline]].
