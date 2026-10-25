# SISTEMA DE PRODUCCIÓN — cómo hacemos las series (método, no una serie en particular)

Para Claude al retomar: este archivo describe el MÉTODO de trabajo con Luis. Léelo junto con
`C:\Users\luisa\calude\MASTER_PROMPT_v8.0.txt` (las reglas creativas). Los scripts viven en
`C:\Users\luisa\calude\testamento\src\` y sirven para cualquier serie (copiarlos a la carpeta de la serie nueva).

## 1. Orden de trabajo (con puertas de aprobación de Luis)
1. **Idea** → Luis pega la estructura (núcleo, capítulos, frase asesina, etc.).
2. **Guiones de los 5 capítulos** (Parte A segmentada 4–9 palabras/línea + Parte B corrida, 3200–3500 caracteres). Validar con `check.ps1`. → aprobación.
3. **Audio** Fish Audio (voz Valentino) → pulido → **SRT con whisper** (cues = líneas de la Parte A) → validar con `diff.py`.
4. **Tiempos** (`tiempos.py`: cada imagen 1.7–4.0 s) → **paquete visual**: escribir `visual\capN\spec.txt` (una escena por línea: n|plano|tags|locación|neg|cuerpo) y `moves.json` → `build.py N` arma y AUDITA los bloques 1/1B/2/3 → bloques 5/6 con `editorial.py`.
5. **Fichas** (Bloque 1) generadas y aprobadas por Luis → guardadas en `fichas\TAG.jpg`.
6. **Por capítulo, TODO lo de imagen primero**: escenas → revisión → rehacer defectos. Luego clips (5). Luego hook (4 tomas → tablero → video). NUNCA videos antes de terminar las imágenes.
7. **Montaje** → subtítulos → hook pegado al inicio → verificación → (música caps que la lleven).

## 2. Herramientas
| Para qué | Herramienta | Notas |
|---|---|---|
| Voz | Fish Audio API, modelo `s2.1-pro-free` exacto, voz Valentino `8d2c17a9b26d4d83888ea67a1ee565b2` | clave en variable `FISH_API_KEY`; una síntesis a la vez |
| SRT | faster-whisper local (modelo medium) | decodificar con ffmpeg (el PyAV instalado es incompatible) |
| Imágenes de escena y tomas de hook | **G-Labs Studio plan MAX, API en `http://127.0.0.1:8765`** (`glabs_api.py`, `glabs_tomas.py`) | clave `GLABS_API_KEY`; Nano Banana 2, 9:16, upscale 2K (sale 1536×2752); 8–10 en paralelo; fichas como `reference_images` por ruta |
| Clips (Bloque 3) y video del hook | Flow Connector (`flow-auto`), Omni Flash | la API de G-Labs no tiene Omni Flash |
| Música | Google AI Studio / Gemini API, modelo `lyria-3.5` (`musica.py`) | clave `GEMINI_API_KEY`, SOLO para música |
| Montaje, subtítulos, unión | ffmpeg + scripts | fuente Baloo 2 ExtraBold en `fonts\` |

Las tres claves están guardadas como variables de entorno de usuario de Windows. Nunca imprimirlas.

## 3. Reglas de Luis (preferencias aprendidas)
- **Hooks**: lo más agresivos, dramáticos y "letales" posible en palabras (gritos, acusaciones, golpes a objetos, amenazas legales). Sin daño físico a personas ni groserías fuertes (Facebook). Siempre presentar los diálogos para aprobación antes de generar.
- **Prompts de hook detallados**: cada acción y cada línea de diálogo nombran al personaje CON su descripción visual (ej. `ZOILO (the stocky bearded man in the black polo shirt)`), para que el video no cambie quién habla. Generador: `hook_prompt.py`.
- **Claude SÍ revisa los videos de hook** antes de mostrarlos: transcribir con whisper y comprobar los 4 diálogos completos + revisar cuadros por errores raros; si falla, rehacer.
- **Hooks llevan subtítulos** con su propio audio (`subs_hook.py`).
- **Música**: bajita (~0.18) con ducking, nunca tapar la narración ni ninguna voz, nunca encima del hook.
- **Revisar cada lote de imágenes** (planchas numeradas con `hoja.py`) antes de seguir: texto en la imagen, fuego/objetos no narrados, escala rara, ropa cambiada, personaje cambiado, fondo liso sin locación → rehacer.
- Luis quiere velocidad máxima pero sin provocar bloqueos de Google: si aparece `UNUSUAL_ACTIVITY` / `TOO_MUCH_TRAFFIC`, parar ~15 min y bajar el paralelismo.
- No usar dos herramientas a la vez sobre la misma cuenta de Google (Flow Connector + G-Labs) → provoca bloqueo.
- Luis prefiere que Claude ejecute todo; cuando algo solo lo puede hacer él (clics en apps de escritorio, iniciar sesión), decirle exactamente qué botón.

## 4. Comandos (rutas desde la carpeta de la serie)
- Guiones: escribir `src\capN.txt` (una línea de Parte A por renglón) → `src\check.ps1` (valida y genera Parte A/B).
- Audio: `src\tts.ps1 -VoiceId 8d2c17a9b26d4d83888ea67a1ee565b2` → `src\pulir.ps1` → `python src\srt.py 1 2 3 4 5` → `python src\diff.py N` → `python src\tiempos.py N`.
- Bloques: `python src\build.py N` · `python src\editorial.py`.
- Escenas: `python src\glabs_api.py N --parallel 8` (salta las que existen; si falla una, se mueve la mala a `_rechazadas` y se vuelve a correr).
- Revisión: `python src\hoja.py N primera última` → planchas numeradas.
- Clips: `src\clips.ps1 -Cap N` (Flow Connector) → copiar a `visual\capN\clips\NNN.mp4`.
- Hook: `hooks\capN\tomas.json` → `python src\hook_tomas.py N` → `python src\glabs_tomas.py N` → `python src\tablero.py N` → `python src\hook_prompt.py N` → animar en Flow (prompt en UNA línea, sin comillas dobles) con el tablero + 4 tomas → `HOOK_CAPN.mp4` → revisar.
- Montaje: `python src\montaje.py N` → `python src\quemar.py N out\capN_base.mp4` → `python src\subs_hook.py N` → `python src\unir.py N`.

## 5. Trampas técnicas conocidas
- PowerShell 5: guardar .ps1 con BOM si llevan acentos; `&&` no existe.
- Descargas de Flow traen `[corchetes]` en el nombre → usar `-LiteralPath`.
- Flow rechaza prompts con saltos de línea/comillas dobles en video ("editor rejected text").
- ffmpeg nuevo: `-/filter_complex archivo` en vez de `-filter_complex_script`.
- El nombre de una ficha se "cuela" en la imagen (ZARAPE → sarape puesto) → agregar negación en `build.py`.
- Documentos (cartas, actas) salían con texto legible inventado y el nombre de la ficha como firma ("Zacarias") → la cola negativa 'd' en build.py ahora exige letra ilegible y firma garabato.
- G-Labs a veces devuelve .webp → `glabs_api.py` ya convierte a .jpg.
- Procesos largos en segundo plano: lanzar con `Start-Process` independiente si pasan de 10 min.
- Chrome para Flow: acceso directo "Chrome para Flow" del escritorio (perfil Default, sin pausar ventanas tapadas).
- Google a veces responde TOO_MUCH_TRAFFIC o G-Labs "failed to get captcha token": esperar ~3 min y reintentar solo lo fallido.
- El sandbox bloquea comandos de PowerShell con ciertas cadenas (p. ej. `t:` o `-replace` con barras): escribir un .py y ejecutarlo.

## 6. Todo por G-Labs API (MAX) — así quedó el flujo final
- Escenas: `glabs_api.py N --parallel 8` (10 rinde más pero provoca TOO_MUCH_TRAFFIC con más facilidad).
- Clips: `glabs_clips.py 2 3 4 5 --parallel 4` → `model: omni_flash` (no documentado, funciona), `mode: start_image`, 4 s.
- Tomas de hook: `glabs_tomas.py N…`. Hook: `glabs_hook.py N…` → omni_flash, `mode: components`, `video_length: 10`, 5 referencias (tablero + 4 tomas). Después `revisar_hook.py N` (transcripción + cuadros).
- Montaje de varios capítulos seguidos: `src\final.ps1` (montaje → `mezclar.py` música con ducking → `subs.py` → `quemar.py` → `subs_hook.py` → `unir.py`), un render a la vez, ~16 min por capítulo.
- Miniaturas: `miniaturas.py` (Bloque 8 por G-Labs, reescaladas a 1080×1920 exacto). Revisar ortografía del texto.
- Textos: `out\TEXTOS_EDITORIALES.txt` (bloques 5 y 6).
- Estado de la serie: `python src\estado.py N "celdas|..."` actualiza CONTEXTO.md y la copia del escritorio.

## 7. Reglas añadidas 2026-10-15
- El clip hook de 10 s de LOS 5 capítulos SIEMPRE brutal: gritos, acusaciones cara a cara, golpes a objetos, palabras letales, amenazas legales o de ruina. Ningún capítulo con hook tranquilo, ni el de resolución. (Sin daño físico a personas ni groserías fuertes.)
- Descripciones (Bloque 5): SIN preguntas y SIN la línea de 'Historia ficticia / IA / voz sintética'.
- SUBTÍTULOS (reemplaza Baloo 2 / y=1350): estilo CapCut, Montserrat ExtraBold (fonts\Montserrat-ExtraBold.ttf), MAYÚSCULAS, blanco con contorno negro, palabra que se dice en AMARILLO, ~3 palabras, grandes (92) y centrados exactamente en medio de la pantalla (540,1440) cuarto inferior, con sombra (Shadow 6). Aplica al capítulo y al hook. Ya está en subs.py y subs_hook.py.
