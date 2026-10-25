# PLAYBOOK — cómo se produce una serie "Sistema Reflexión" (5 capítulos, 9:16, estilo cómic Marvel 2D)

Este documento es el método exacto, en orden, con los comandos y las trampas. Un Claude nuevo que lo siga
debe entregar lo mismo que las series mozo, terreno, cochera, boda, laredo y carniceria.
Las reglas creativas de texto (estructura de guion, ganchos, frase-lección) están en `contexto/MASTER_PROMPT_v8.0.txt`.
Las preferencias de Luis, una por archivo, están en `reglas/` (léelas todas antes de empezar).

## 0. Qué se entrega por serie
- 5 videos `REFLEXION_CAPN_FINAL.mp4`, 1080×1920, 30 fps, ~3:50–4:20 cada uno:
  gancho (hook) de 10 s con diálogo + narración con imágenes y 5 clips animados por capítulo.
- Subtítulos estilo CapCut, banner amarillo "CAPÍTULO N DE 5" los primeros 5 s, marca de agua
  "Reflexiones con Raíces" todo el video (series desde el 2026-10-24).
- 5 miniaturas JPG 1080×1920 + `TEXTOS_EDITORIALES.txt` (título, descripción, hashtags, comentario).
- Todo copiado a Google Drive en una carpeta con nombre de la serie, con md5 verificado.
- Series de bondad (mozo, terreno): igual, pero el comentario pide "AMÉN". Lote 7: pregunta abierta, sin AMÉN.
- Sin música en las series nuevas (lote 7 y bondad). Música solo si Luis la pide: 0.10 con ducking.

## 1. Preparar el PC (una sola vez)
1. Python 3.13, ffmpeg 9 "full" (con libass), G-Labs Studio escuchando en `http://127.0.0.1:8765`, Chrome con las cuentas de Google en G-Labs (varias cuentas rotan; cada una tiene cuota diaria).
2. Claves como variables de USUARIO de Windows (nunca en archivos, nunca impresas, Claude no las ve):
   `FISH_API_KEY`, `GLABS_API_KEY`, `GROQ_API_KEY`. Las guarda Luis con `orquestacion\guardar_claves.ps1`
   (pide la clave oculta) y se revisan con `orquestacion\comprobar_claves.ps1`.
3. Lanzar siempre scripts con `powershell -NoProfile -ExecutionPolicy Bypass -File ...`.
4. Carpeta de trabajo: `C:\Users\Luis\calude\`. Cada serie es una subcarpeta: `calude\<serie>\{src,audio,srt,visual,hooks,fichas,fonts,out}`.
5. Drive en `I:\Mi unidad` (`entregar.py` detecta la unidad; `DRIVE_ROOT` la fuerza).

## 2. Nueva serie: crear la carpeta
```
copiar src_serie\*  ->  calude\<serie>\src\
copiar fonts\*      ->  calude\<serie>\fonts\    (+ georgiai.ttf de C:\Windows\Fonts, para la marca de agua)
copiar orquestacion\*.ps1 y banner_capitulo.py -> calude\
copiar ayudantes\*  -> carpeta temporal de trabajo
```
Usa como base los scripts de `carniceria\src` (los más nuevos: cláusula "no blood", marca de agua, audit de nombres).

## 3. Puertas de aprobación (Luis)
1. Idea (Luis la pega) → 2. Guiones de los 5 capítulos → **"dale"** → 3. todo lo demás sin preguntar.
Después de aprobar guiones NO hay que pedir permiso por cada paso; solo avisar resultados. Los nombres de personajes los elige Claude.

## 4. Guiones
- Escribe `src\cap1.txt … cap5.txt`: una línea de Parte A por renglón (4–9 palabras), luego Parte B corrida (3200–3500 caracteres en total por capítulo según el master prompt).
- `ayudantes\partir.py` parte líneas de más de 9 palabras.
- Valida con `src\check.ps1` (cuenta palabras, caracteres, reglas). Genera `REFLEXION_CAPN_GUION_PARTE_A/B.txt`.
- Narradora mujer = Fish "Abuela" `0baf4054bf624d388ad755ed3da939fc` speed 1.25. Narrador hombre = Valentino `8d2c17a9b26d4d83888ea67a1ee565b2` speed 1.
- Sin sangre, sin manchas rojas; desde la idea 6: sin cuchillos ni carne cruda a la vista (ver `reglas/feedback-sin-sangre.md`).

## 5. Audio y subtítulos (por serie)
```
powershell -NoProfile -ExecutionPolicy Bypass -File audio_serie.ps1 -Series <serie> -VoiceId <id> -Speed <1|1.25>
```
(= `tts.ps1` Fish `s2.1-pro-free`, una síntesis a la vez → `pulir.ps1` → `srt.py` con Groq whisper-large-v3, adelanto 0.15 s → `diff.py` valida que el SRT coincide con el guion → `tiempos.py` calcula la duración de cada imagen, 1.7–4.0 s.)

## 6. Paquete visual (lo más delicado)
1. `src\refs.json`: personajes y locaciones con **tags de nombre inventado de 1 letra especial + nombre** (K/X/Z al inicio: KCARNE, ZPANTEON, XRAMIRO). Regla: ningún tag puede compartir las 3 primeras letras con una palabra común en inglés del vocabulario de los prompts (la auditoría de `build.py` lo detecta).
   Variantes de ropa (traje, joven, novia) como variantes del mismo tag, solo donde la historia lo pide.
2. Cada capítulo: `src\_spec_capN.txt`, una escena por línea `n|plano|tags|locación|neg|cuerpo`:
   plano ∈ M (medio), C (primer plano), B (busto/over-the-shoulder), D (detalle de objeto), G (gran plano).
   - Nunca dos planos iguales seguidos; un G al menos cada 10 escenas; ≥30 % planos D/B; ≥33 % sin rostro.
   - `neg` = `d` en documentos/objetos con texto (letra ilegible, firma garabato), `t` por defecto.
   - Nunca texto legible, billetes legibles, globos de diálogo, collages.
   - Se escribe con alias cortos (E=ESPIGON…); `ayudantes\autofix.py` corrige repetidos y huecos; `ayudantes\conv_spec.py` convierte el archivo de alias (ver `ayudantes\ejemplo_alias_carniceria.json`) a `visual\capN\spec.txt` + `moves.json`.
3. `python src\build.py N` arma y AUDITA los bloques 1/1B/2/3 (palabras prohibidas BANNED, choques de nombres, planos). Arreglar hasta 0 errores.
4. `python src\editorial.py` genera título (≤65 car.), descripción (SIN preguntas, SIN línea de IA, 3 emojis, palabra clave primero), 10 hashtags, comentario. Datos en `editorial.json`. `miniaturas.json` define las miniaturas.

## 7. Producción de imágenes y clips (G-Labs API, 127.0.0.1:8765)
```
powershell ... produccion_serie.ps1 -Serie <serie>        # fichas -> imágenes -> clips (5 por capítulo)
powershell ... flow_serie.ps1  -Serie <serie>             # en paralelo si hace falta repartir cuota entre Flow y Pics
```
- Modelo de imagen por variable `IMG_MODEL` (por defecto `nano_pics`; alternativas `nano_banana_2`, `nano_banana_lite`, `nano_banana_pro`, `imagen_4`). Clips: `omni_flash` (Flow) / `omni_vids` (Vids), 4 s, `mode: start_image`.
- Cuota diaria por cuenta de Google: "Cuota diaria de imágenes agotada" / NO_PICS_ACCOUNT → cambiar de modelo o esperar; se pueden añadir más cuentas en G-Labs. Si aparece UNUSUAL_ACTIVITY o TOO_MUCH_TRAFFIC: parar ~3–15 min y bajar el paralelismo (8 imágenes en paralelo es el tope cómodo, 4 clips).
- Fichas (referencias de personaje/locación) primero y aprobadas; después escenas. **Todas las imágenes antes que cualquier clip.**
- **Revisión visual obligatoria**: `ayudantes\planchas_review.py` (o `src\hoja.py N a b`) genera planchas numeradas. Buscar: texto legible, burbujas, collages, ropa cambiada, personaje equivocado, fondo liso, escala rara, sangre/manchas. Borrar las malas (a `_rechazadas`) y volver a correr: salta las que existen.
- Un nombre de ficha puede "colarse" en la imagen como rótulo → agregar negación en `build.py`.

## 8. Hooks (10 s, brutales)
Por capítulo: `hooks\capN\tomas.json` (personajes SIN variante en `tag` + campo `var`) →
`hook_tomas.py N` → `glabs_tomas.py N` (4 tomas) → `tablero.py N` → `hook_prompt.py N` → `glabs_hook.py N` (omni_flash/omni_vids, `mode: components`, 10 s, 5 referencias) → `revisar_hook.py N`.
- Diálogos al máximo de agresividad en los 5 capítulos (gritos, acusaciones, amenazas legales/ruina). Sin daño físico ni groserías fuertes. Presentarlos a Luis antes de generar solo si él lo pidió; en el lote 7 se aprobaron junto con los guiones.
- Cada línea de diálogo nombra al personaje con su descripción visual.
- **Claude revisa cada hook**: transcribir con whisper y comprobar que los 4 diálogos estén completos y que el audio corresponda al capítulo correcto (Vids a veces guarda un hook en la carpeta de otro capítulo).
- CONTENT_POLICY / NO_OUTPUT / IDENTIFIABLE_PERSON_SAFETY: reintentar alternando `omni_flash` y `omni_vids`; si insiste, rehacer el hook con los protagonistas en vez del personaje secundario (matón gordo/calvo enojado suele bloquearse).

## 9. Montaje (largo; es reanudable)
```
powershell ... montar_serie.ps1 -Serie <serie> [-SoloBase]
```
Por capítulo, en este orden: `montaje.py` (ENC_PRESET=ultrafast) → `subs.py` → `quemar.py` → `subs_hook.py` → `unir.py` (hook + capítulo; debe dar 10 s + capítulo exacto) → `poner_banner.py` (CAPÍTULO N DE 5, amarillo 255,221,0, y=90) → `poner_marca.py` (Georgia cursiva, y=1520, opacidad ~0.62; deja `REFLEXION_CAPN_sin_marca.mp4`).
- Salta capítulos sin 5 clips o sin hook; se puede montar la "base" mientras se generan los hooks y luego volver a correr.
- Subtítulos: Montserrat ExtraBold, MAYÚSCULAS, blanco con contorno negro, palabra activa amarilla, ~3 palabras, tamaño 92, centrados en (540,1440), sombra. 0 solapes.
- Verificación final: 1080×1920, 30 fps, duración = 10 + capítulo, tamaño ~230–330 MB (un video de ~6 MB indica que el overlay se truncó: el filtro NO debe llevar `shortest=1`).
- PC actual de Luis: Intel i3-3220 (2 núcleos físicos / 4 hilos, 3,3 GHz), 7,9 GB de RAM, discos C/D/I con espacio de sobra. Con `ENC_PRESET=ultrafast` el montaje de un capítulo tarda ~20–45 min (con `veryfast` hasta ~54 min). Pedir keep-awake y no cerrar la sesión.

## 10. Miniaturas, textos, entrega
```
python src\miniaturas.py        # G-Labs, reescala a 1080x1920 exacto; revisar ortografía del texto
python src\editorial.py         # TEXTOS_EDITORIALES.txt
python src\entregar.py "<Nombre de la carpeta en Drive (5 capítulos)>"
```
`entregar.py` copia VID 1–5, MINIATURA_CAP1–5.jpg y TEXTOS_EDITORIALES.txt a `I:\Mi unidad\<nombre>` y compara md5 uno por uno. Nombre de carpeta: frase en primera persona de la historia + "(5 capítulos)".
Después: actualizar la memoria/`reglas\` con lo aprendido y avisar a Luis en español, corto, sin tecnicismos.

## 11. Trampas conocidas (resumen)
- PowerShell 5: `.ps1` con acentos → guardar con BOM; no existe `&&`; el sandbox bloquea ciertas cadenas → escribir un `.py`.
- `-filter_complex_script` no existe en este ffmpeg: usar `-/filter_complex archivo`.
- Flow rechaza prompts de video con saltos de línea o comillas dobles.
- G-Labs a veces devuelve .webp (el script convierte a .jpg); descargas de Flow traen `[corchetes]` → `-LiteralPath`.
- Vestido de novia solo en la boda; variante casual para recuerdos.
- Palabras prohibidas en prompts (chain, wound, photograph, gripping her, clutched, snap) → reformular.
- Procesos > 10 min: lanzarlos independientes (Start-Process) y vigilarlos con logs; si la sesión se cierra, el montaje se reanuda.
- No usar Flow Connector y G-Labs sobre la misma cuenta a la vez.

## 12. Cómo retomar una sesión
1. Leer `reglas/MEMORY.md`, `contexto/CONTEXTO.md` y este playbook.
2. Revisar `montaje_<serie>.log`, `out\`, `visual\capN\`, `hooks\capN\` para saber en qué paso quedó.
3. Correr de nuevo el script de orquestación del paso pendiente: todos son reanudables y saltan lo ya hecho.
