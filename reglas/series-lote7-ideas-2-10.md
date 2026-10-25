---
name: series-lote7-ideas-2-10
description: "Lote 7 (ideas 2-10 pasadas 2026-10-24): carpetas cochera y boda COMPLETAS en Drive; ideas 4-10 pendientes, con pasos y trampas aprendidas"
metadata:
  type: project
---

Luis pasó 9 ideas (2 a 10) del Lote 7; las ideas 9 y 10 (carril bondad) vienen en 3 bloques, no en 5 capítulos. Se producen EN ORDEN. Formato: 5 capítulos, voz de narradora mujer = Fish "Abuela" 0baf4054bf624d388ad755ed3da939fc a 1.25 (queda en ~3:30-3:50; Luis no objetó), narrador hombre = Valentino. Sin música. Pregunta de comentarios abierta, sin "escribe AMÉN" (eso era solo de las series de bondad mozo/terreno, ver [[series-bondad-mozo-terreno]]).

**HECHAS y en Drive (md5 verificado, 2026-10-24):**
- IDEA 2 → carpeta `cochera`, Drive "Diecinueve años esperando a mi hija en Dallas (5 capítulos)" (Amparo / Maricela / Ulises; tags XAMPARO, ZARICELA, XULISES...).
- IDEA 3 → carpeta `boda`, Drive "Mi papá pagó mi boda desde Charlotte (5 capítulos)" (Yesenia narra desde el velorio de Fidel).

**PENDIENTES:** ideas 4 (Trinidad/Laredo), 5 (Ramiro/El Paso), 6 (Anselmo/Fresnillo), 7 (Erlinda/Hialeah, cámara), 8 (Isidro/Tijuana), 9 y 10 (bondad). Luis aún no aprobó guiones de esas; hay que escribir, validar con check.ps1 y pedir "dale".

**Flujo rápido usado:** copiar scripts de `mozo\src` a carpeta nueva; guion capN.txt → `partir.py` (parte líneas >9 palabras) → check.ps1; `audio_serie.ps1 -Series x -VoiceId .. -Speed ..`; refs.json/editorial.json/miniaturas.json/hooks tomas.json; `tiempos.py`; `_spec_capN.txt` con alias + autofix.py + conv_spec.py (en el scratchpad de la sesión, copiarlos de ahí) → build.py; `produccion_serie.ps1 -Serie x` (fichas+imágenes+clips) con Flow (`flow_serie.ps1`) en paralelo; `post_serie.ps1` (hooks); `montar_serie.ps1 -SoloBase` y luego sin flag; miniaturas.py; editorial.py; entregar.py.

**Trampas:** nombres de refs que chocan por prefijo de 3 letras con palabras inglesas (usar K/X/Z al inicio); palabras prohibidas en prompts (chain, wound, photograph, gripping her); personajes con vestido de novia solo en la boda (variante casual para flashbacks); Vids/Flow rechazan hooks con matón gordo/calvo enojado (IDENTIFIABLE_PERSON_SAFETY): rehacer hook con los protagonistas; revisar_hook puede dar el hook de un capítulo en la carpeta de otro (revisar que cada HOOK_CAPN diga sus diálogos); tomas.json personajes: tag sin variante + campo "var".
