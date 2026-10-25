---
name: papas-primerizos-mejoras
description: "Mejoras aprobadas (2026-10-14) para los PRÓXIMOS videos de Papás Primerizos: miniatura/primer cuadro cerrados, titular afirmativo, descripción larga, 1 video de \"dato\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: 435c217c-925a-437c-91d6-0e3fc31dbdb7
  modified: 2026-10-17T15:38:22.522Z
---

Tras revisar la página de Facebook Papás Primerizos (6,4 M seguidores; solo 10 reels visibles sin login; los de ~550 mil vistas son datos médicos sorprendentes, los de crianza emocional 17-46 mil), el usuario aprobó aplicar esto a los PRÓXIMOS videos (no a los 6 ya hechos):

1. **Miniatura y primer cuadro:** plano más cerrado de la cara/personaje, ocupando más espacio, con emoción clara (no planos abiertos con mucho cuarto). Prompt de la imagen 1 = hook en primer plano.
2. **Titular de miniatura:** afirmación firme, no solo consejo (ej. "Esto le enseña a tu hijo que sentir es normal"); usar palabras como "tu hijo"; texto grande, abajo-medio, sin franja oscura, última línea en amarillo (miniaturas.py en calude\).
3. **Descripción:** más larga, 2-3 frases de contexto + hashtags temáticos; SIN "comparte", SIN preguntas a la audiencia, sin invitar a comentar (reglas del master prompt siguen).
4. **Experimento:** probar 1 video de "dato" (ej. "Un niño necesita oír que estás triste para aprender a sentir") junto a los reflexivos, y comparar rendimiento.

Añadido 2026-10-17 (tras revisar los reels de la página de referencia; usuario dijo "aplica los 3"): (a) **titular en pantalla** los primeros 2.8 s de cada video (`hook.txt` en la carpeta del video → montaje.py lo dibuja arriba, Montserrat ExtraBold, última línea amarilla; gen_generic.py lo crea desde `THUMB` de defs.py); (b) **más primeros planos de cara** con emoción clara en las escenas; (c) **2-3 planos de detalle** (objeto/mano/símbolo) por video, usando algunos segmentos como macro (se mantiene 1 segmento = 1 imagen). AJUSTE del usuario (2026-10-17, tras ver el video 11): el titular del inicio va GRANDE y ABAJO (misma zona de los subtítulos, \an2 y=1640, ~150 px, líneas equilibradas), durante 0-3.0 s SIN subtítulos; los subtítulos CapCut entran cuando el titular desaparece (los eventos antes de 3.0 s se descartan). Ya implementado en montaje.py. Opcionales que NO se aprobaron aún: video "mito y realidad", personajes fijos de la serie.

**Why:** buscar más alcance sin perder el tono cálido propio ni romper las reglas de copy.
**How to apply:** al escribir ideas/guiones/miniaturas/copy de un video nuevo de [[master-prompt-papas-primerizos]]; el pipeline está en [[papas-primerizos-pipeline]].
