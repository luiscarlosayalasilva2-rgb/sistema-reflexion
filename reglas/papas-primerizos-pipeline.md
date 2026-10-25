---
name: papas-primerizos-pipeline
description: "Cómo está armado y cómo se retoma el pipeline de Papás Primerizos en C:\\Users\\luisa\\calude (papas1..papas6, G-Labs webhook, Meta Vibes, Veo, trampas)"
metadata:
  node_type: memory
  type: project
  originSessionId: 435c217c-925a-437c-91d6-0e3fc31dbdb7
  modified: 2026-10-18T23:12:22.720Z
---

Pipeline de [[master-prompt-papas-primerizos]]. Estado 2026-10-14: video 1 ("Estoy bien cuando no lo estás") terminado en `papas1`; videos 2-6 (separación, "¿Cómo se dice?", bailar, abrigo, pañal) con guion aprobado en `papas2..papas6`, producidos por `C:\Users\luisa\calude\orquestador.ps1` (log `orquestador_log.txt`). Salida final en `OneDrive\Escritorio\Papás Primerizos\<nombre>\` (video + miniatura + txt).

Piezas reutilizables (cada papasN tiene copia): `whisper_srt.py` (faster-whisper; hay que pasarle el audio como array numpy vía ffmpeg porque PyAV falla), `gen_generic.py` (lee `defs.py` por video: CH/SETS/SEG/CLOTH/TITLE… genera los 8 bloques + camaras.json; en calude\), `imagenes_glabs.ps1`, `meta_vibes.ps1`, `montaje.py` (MODO=meta usa clips_meta\meta_NN.mp4, el resto Ken Burns), fuentes\Baloo2-ExtraBold.ttf.

G-Labs webhook: corre en el PC del usuario `http://127.0.0.1:8765`, llave en user env `GLABS_KEY`, header `X-API-Key`. `/api/image/generate` (prompt, aspect_ratio 9:16) tarda ~3 min por imagen, ~6 en paralelo; `/api/meta/generate` (mode i2v, start_image data URI, 720p) ~5 min/clip. `/api/video/generate` (Flow): body correcto = `{prompt, model:"omni_flash", mode:"start_image", aspect_ratio:"9:16", reference_images:["data:image/jpeg;base64,..."], resolution:["360p","720p"], video_length:4}` (los nombres start_image/duration/model:'omni-flash' NO sirven: ignora la imagen y genera 8 s; doc completa en Downloads\WEBHOOK_INTEGRATION.en (1).md). El 403 UNUSUAL_ACTIVITY se quitó cambiando en G-Labs "Autenticación de Flow" a modo **Integrado** (en vez de Extensión de Chrome). Orquestador vigente: `calude\orquestador2.ps1` (Flow omni_flash 4s → montaje → escritorio). No hay endpoint de cancelar. Cuidado: ConvertTo-Json de strings sacados de Get-Content → castear con [string]. Meta: la cookie expira (401), el usuario re-loguea en G-Labs.

Otros: llave Veo en user env `GEMINI_VIDEO_KEY` (veo-3.1-lite-generate-preview, 4s, 9:16; se acaba la cuota tras ~10 videos → 429). flow-auto (extensión) con video falló ("Start frame slot not found" / "no result reported"); la pestaña de Flow debe estar visible. Los guiones aprobados quedaron en 240-286 palabras (debajo del 300-450 de la regla) — el usuario los aprobó así.

Subtítulos (desde 2026-10-15): estilo CapCut en `montaje.py` — Montserrat ExtraBold 92, mayúsculas, blanco con contorno negro, palabra activa amarilla, 3 palabras, `\an5\pos(540,1440)`; ver [[feedback-subtitulos-capcut]]. Los 6 videos se rehacen con esto (`rehacer_subs.ps1` → `papasN_final_subsCapcut_1080x1920.mp4`).

Video 7 ("Detrás de la cámara", 2026-10-15) terminado en `papas7` con subtítulos CapCut, música provisional (copia de la del video 1: Lyria sigue pidiendo pago; prompt de música pendiente de que el usuario genere la pista) y miniatura con titular (`miniatura7.py <escena>`). Salida: `Escritorio\Papás Primerizos\7 - Detrás de la cámara\`. El usuario vació las carpetas de entrega de los videos 1-6 (los originales siguen en papasN) y pidió NO rehacer esos videos con los subtítulos nuevos.

Videos 8 (pelea entre niños), 9 (cambios sin aviso), 10 ("Lee" pero nunca te ve leer) — guiones aprobados 2026-10-17 (324/316/314 palabras, ya ≥300) en `papas8..10`; los produce `orquestador_8_10.ps1` (log `orq_8_10_log.txt`; imágenes de 9 y 10 las adelanta `imgs_9_10.ps1`). Salida: `Escritorio\Papás Primerizos\{8,9,10} - ...\`. Miniatura con titular: `miniatura_n.py N` lee `THUMB` de defs.py. Música PROVISIONAL (copias de pistas existentes: 8←papas3, 9←papas2, 10←papas5) porque Lyria pide pago; el usuario debe generar pistas con prompts propios.

Videos 11-16 (charco, monstruos, nombre completo, nota en lonchera, gracias a la pareja, "a tu edad yo ya") — guiones aprobados 2026-10-17/18 (≥300 palabras) en `papas11..16`. 11 terminado como muestra (orquestador_11.ps1); 12-16 los produce `orquestador_12_16.ps1` (log `orq_12_16_log.txt`) con imágenes adelantadas por `imgs_12_16.ps1`. Música provisional copiada de pistas existentes. Titular inicial grande y abajo en montaje.py (ya validado por el usuario).

Videos 17-26 ("Hilos de Crianza": peluche roto, leche derramada, abuelos, "no quiero al bebé", decir no sin culpa, pregunta en voz alta, luchas, foto en redes, dinosaurios, "te quiero" en un mal día) — guiones aprobados 2026-10-18 (300-314 palabras) en `papas17..26`, hashtags con `#hilosdecrianza #papasprimerizos`. Producción automática: `prep_videos.ps1` (TTS+whisper), `gen_cuando_listo.ps1` (bloques cuando hay SRT+defs), `imgs_17_26.ps1`, `orquestador_17_26.ps1` (log `orq_17_26_log.txt`). OJO: si G-Labs (127.0.0.1:8765) está cerrado las imágenes no avanzan — pedir al usuario que lo abra. Filtro CHILD_SAFETY de Flow bloquea escenas con bebés recién nacidos/fotos de bebé (usar toddler o dejar zoom suave).

**Why:** evitar redescubrir endpoints, límites y errores en cada sesión.
**How to apply:** para un video nuevo: guion → `papasN\guion_segmentado.txt` → TTS Fish + whisper → `defs.py` (ropa nueva) → `python gen_generic.py papasN` → imágenes → Meta → montaje (ver orquestador.ps1).
