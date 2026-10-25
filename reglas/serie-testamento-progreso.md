---
name: serie-testamento-progreso
description: "Estado de la serie \"El testamento\" (Aurelio/Nicanor, Puerto Vallarta) — dónde retomar."
metadata:
  node_type: memory
  type: project
  originSessionId: 43ba66ce-8084-4e55-8c47-8773587f6779
  modified: 2026-10-12T22:42:09.511Z
---

Serie "El testamento que mi compadre escribió antes de morir" — carpeta C:\Users\luisa\calude\testamento. Sigue el master v8.0 ([[master-prompt-reflexion]]).

Hecho al 2026-10-12 ~08:45:
- Guiones 1–5 (Parte A/B), audios Fish pulidos (audio\pulido, 3:44–3:54), SRT validados (srt\capN.srt, cues = líneas de Parte A).
- Paquete visual completo y auditado para los 5 caps: REFLEXION_CAPn_BLOQUE1/1B/2/3/4/4B/5/6 en la raíz de la serie. Imágenes por cap: 83, 83, 80, 84, 81.
- Pipeline: src\srt.py → src\tiempos.py → visual\capN\spec.txt (+moves.json) → src\build.py N (arma y audita) ; src\editorial.py (bloques 5/6). Fichas en src\refs.json.
- Referencias: ZACARIAS (Aurelio 66), NEFTALI (Aurelio joven), ZEFERINO (Nicanor joven), OBDULIO (Nicanor 62, variante "gown"), YESENIA (María joven), NOEMI (María 63), ZOILO (ahijado); locs VITRAL, NIXTAMAL, VOLANTE, OMNIBUS, OLEAJE, ZARAPE, ZAGUAN, NOPALERA, CIPRES, ZAFIRO, NOGAL, NIQUEL, YODO, JURISTA.

2026-10-12: fichas aprobadas (testamento\fichas\TAG.jpg) y subidas a Flow como TAG.jpg; escenas lanzadas con src\escenas.ps1 -Cap N (descargan a Downloads\testamento_capN). Antes pendiente: aprobación del paquete; luego generar fichas (sheets) en Flow y que el usuario las apruebe; decidir la medida (Flow descarga 768×1376, v8 pide 1152×2048); el usuario no respondió si acepta caps <4:00.

2026-10-12 tarde: CAPÍTULO 1 TERMINADO → out\REFLEXION_CAP1_FINAL.mp4 (243.4 s, hook con subtítulos, sin música por decisión del usuario). Usuario aprobó subtítulos (muestra) y hook. Lección: el usuario quiere TODO lo de Flow de un capítulo (escenas → clips → hook) antes de montar, y nunca videos antes de terminar imágenes. Pipeline montaje: src\montaje.py N → src\quemar.py N out\capN_base.mp4 → src\subs_hook.py N → src\unir.py N. Prompts de hook a Flow: en UNA línea y sin comillas dobles (si no, "editor rejected text"). Capítulos 2–5: nada generado aún.

Música: audio\musica\musica_serie.mp3 (Lyria 3.5 vía src\musica.py, 2:56). Decisión del usuario: el CAP1 se queda SIN música; caps 2–5 sí la llevan, y la música nunca debe tapar la narración ni ninguna voz → mezclarla bajita (~0.18) con ducking (sidechaincompress) bajo la narración, repetida con cruce para cubrir el capítulo, y nunca encima del hook.

ESTADO VIVO: leer primero C:\Users\luisa\calude\testamento\CONTEXTO.md (tabla de avance, decisiones, comandos). Desde 2026-10-12 17:30 las escenas van por G-Labs Studio API (MAX) con src\glabs_api.py --parallel 10; Flow Connector detenido.

**Why:** retomar sin rehacer trabajo.
**How to apply:** leer esto y los archivos antes de continuar.
