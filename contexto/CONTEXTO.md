# CONTEXTO — Serie "El testamento" (Sistema Reflexión)

Leer esto primero al retomar. Última actualización: 2026-10-12 ~17:45.

## La serie
- Título: *El testamento que mi compadre escribió antes de morir, confesando que robó nuestro negocio juntos* — 5 capítulos, Puerto Vallarta.
- Narrador: Aurelio Montoya (66). Compadre: Nicanor Salcedo (muere 2022). Esposa: María (63). Ahijado (hijo de Nicanor) sin nombre.
- Línea de tiempo: 1991 fundan Transportes Bahía · 2004 empieza el robo · 2022 muere Nicanor · 2024 María entrega la carta · 2026 venta + placa.
- Reglamento: `..\MASTER_PROMPT_v8.0.txt` (manda sobre el v7 / master completo).

## Referencias (fichas aprobadas, en `fichas\TAG.jpg`)
| Tag | Qué es |
|---|---|
| ZACARIAS | Aurelio presente (62–66), guayabera crema |
| NEFTALI | Aurelio joven, camisa azul + jeans |
| ZEFERINO | Nicanor joven, camisa blanca, reloj de oro |
| OBDULIO | Nicanor 62 (variante "gown" = bata de hospital) |
| YESENIA | María joven, blusa mostaza, trenza |
| NOEMI | María 63, cárdigan morado |
| ZOILO | el ahijado, polo negro, barba |
| Locaciones | VITRAL (parroquia), NIXTAMAL (cocina), VOLANTE (oficina), OMNIBUS (patio camiones, ficha horizontal), OLEAJE (malecón), ZARAPE (recámara), ZAGUAN (fachada), NOPALERA (cabina pickup), CIPRES (panteón), ZAFIRO (villa), NOGAL (despacho), NIQUEL (pasillo hospital), YODO (cuarto hospital), JURISTA (notaría) |

## Estado
| | Guion | Audio | SRT | Escenas | Clips | Hook | Montaje |
|---|---|---|---|---|---|---|---|
| Cap 1 | ✅ | ✅ | ✅ | ✅ 83 | ✅ 5 | ✅ aprobado | ✅ en Drive |
| Cap 2 | ✅ | ✅ | ✅ | ✅ 83 | ✅ 5 | ✅ aprobado | ✅ en Drive |
| Cap 3 | ✅ | ✅ | ✅ | ✅ 80 | ✅ 5 | ✅ aprobado | ✅ en Drive |
| Cap 4 | ✅ | ✅ | ✅ | ✅ 84 | ✅ 5 | ✅ aprobado | ✅ en Drive |
| Cap 5 | ✅ | ✅ | ✅ | ✅ 81 | ✅ 5 | ✅ aprobado | ✅ en Drive |

Bloques 1/1B/2/3/4/4B/5/6 de los 5 capítulos ya escritos en esta carpeta (`REFLEXION_CAPn_*`).

## Decisiones del usuario (no olvidar)
- Orden por capítulo: TODAS las escenas → clips → hook → montaje. Nunca videos antes de terminar imágenes.
- Hooks: más brutales y dramáticos (gritos, acusaciones, cara a cara), sin golpes a personas ni groserías. Siempre se aprueban los diálogos antes de generar.
- Hooks llevan subtítulos con su propio audio (`src\subs_hook.py`).
- NUEVA REGLA del usuario (anula el §6.5 del v8): Claude SÍ revisa cada video de hook antes de mostrarlo — transcribir con whisper y comprobar que se digan los 4 diálogos completos, y revisar cuadros por errores visuales raros; si falla, regenerar.
- Hooks: lo más agresivos y letales posible en palabras (gritos, acusaciones, golpes a objetos, amenazas legales), sin daño físico a personas ni groserías fuertes.
- Música: solo caps 2–5 (`audio\musica\musica_serie.mp3`, Lyria 3.5), bajita (~0.18) con ducking; nunca tapar la voz; nunca encima del hook.
- Duración real del audio manda (caps duran 3:44–3:54).
- Medida: G-Labs entrega 2K (1536×2752); el montaje escala a 1080×1920.

## Herramientas y claves (variables de entorno de usuario, nunca imprimir)
- `FISH_API_KEY` — Fish Audio, voz Valentino `8d2c17a9b26d4d83888ea67a1ee565b2`, modelo `s2.1-pro-free`.
- `GEMINI_API_KEY` — Google AI Studio, SOLO para música (Lyria).
- `GLABS_API_KEY` — G-Labs Studio plan MAX, API en `http://127.0.0.1:8765` (pestaña "API De Webhook", servidor encendido).
- Flow Connector (`flow-auto`) — Chrome perfil Default, acceso directo "Chrome para Flow" del escritorio (no se pausa si se tapa). Detenido; ya no usar a la vez que G-Labs (provoca "UNUSUAL_ACTIVITY").
- Escenas ahora por G-Labs API con 10 en paralelo (mejor ritmo medido).

## Comandos (desde PowerShell, rutas absolutas)
- Escenas por G-Labs: `python src\glabs_api.py N --parallel 10` (salta las existentes, guarda `visual\capN\imgs\NNN.jpg`).
- Rearmar prompts tras cambiar `visual\capN\spec.txt` o `src\refs.json`: `python src\build.py N` (audita solo).
- Clips (hoy por Flow Connector): `src\clips.ps1 -Cap N` → copiar a `visual\capN\clips\NNN.mp4`.
- Hook: `hooks\capN\tomas.json` → `src\hook_tomas.py N` → tomas → `src\tablero.py N` → animar en Flow con `hooks\capN\prompt_hook.txt` (en UNA línea, sin comillas dobles) → `HOOK_CAPN.mp4`.
- Montaje: `python src\montaje.py N` → `python src\quemar.py N out\capN_base.mp4` → `python src\subs_hook.py N` → `python src\unir.py N` (verifica duración y unión).
- Música: `python src\musica.py lyria-3.5 "<prompt>" nombre`.

## Lecciones (errores ya cometidos)
- Nombres de descargas de Flow traen corchetes → usar `-LiteralPath`.
- El nombre de la ficha ZARAPE hacía que el modelo le pusiera el sarape encima a ZACARIAS → `build.py` ya agrega "nobody wears it".
- Flow a veces mezcla resultados en lotes o deja fondo liso → revisar cada lote antes de seguir.
- PowerShell 5 rompe scripts .ps1 con caracteres no ASCII si no tienen BOM.
