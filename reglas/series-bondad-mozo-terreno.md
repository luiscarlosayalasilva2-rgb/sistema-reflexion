---
name: series-bondad-mozo-terreno
description: "IDEAS 9 y 10 (carril BONDAD, 2026-10-20): carpetas calude\\mozo y calude\\terreno — nombres y físicos nuevos pedidos por Luis, lectura canónica y estado"
metadata:
  type: project
---

Dos series del carril "bondad" (tono de fe, justicia poética, sin antagonista violento; la pregunta de comentarios es un CTA de fe "escribe AMÉN" y va SOLO en el Bloque 6, no en la narración). Luis pidió: **cambiar los nombres de los personajes y que sean físicamente raros (muy flacos, muy gordos, gigantes, etc.)**. Carpetas `C:\Users\Luis\calude\mozo` y `...\terreno` (scripts copiados de `llamadas\src`, datos de la serie anterior en `src\_plantillas_llamadas`). Voz: Valentino (narran hombres). Se produce UNA serie detrás de otra (el montaje es lento en este PC, ver [[pc-nuevo-luis]]); sin música ([[serie-treinta-anos-llamando]]).

**IDEA 9 → carpeta `mozo`, "El mozo que salvó la empresa" (Drive: "El mozo que salvó la empresa (5 capítulos)")**
- Narra Eustaquio Bermúdez (antes Aurelio Mendoza): flaquísimo, casi 2 m y 55 kg, "el espantapájaros"; 23 años en la historia, 61 cuando vuelve Homero, 63 al narrar. Mozo de almacén en Autopartes Villaseñor, Querétaro.
- Homero Villaseñor (el empresario, yerno del fundador don Anselmo): enorme, 150 kg, bigote de morsa, sudoroso; viejo y enfermo en silla de ruedas con tanque de oxígeno.
- Basilisa Bermúdez (la hermana, antes Patricia): 1.45 m, redonda como pelota, risa de cuerpo entero; deja una bolsa con ropa nueva en la cama el domingo antes.
- Canon aplicado: la idea que salvó el contrato con una armadora = kits por rotación en el almacén (despacho de tres días a uno); él hizo DOS copias y guardó una en el sobre; oyó a Homero presentarla cuando llevó cajas a la sala de juntas; la confesión llega en una carta de 38 años; Homero admite que donaba al "Fondo Mozo" y de ahí salió la beca del sobrino Rubén (hijo de Basilisa) — añadido mío; el museo guarda uniforme y hoja; Homero muere un año después y deja la Fundación Eustaquio Bermúdez; el primer premio es un mozo de 23 años.
- "Narrador D, el que volvió" = lo interpreté como que narra Eustaquio y el que vuelve es Homero.
- "Formato corto" = sin recapitulación; mantuve ~4 min por capítulo.

**IDEA 10 → carpeta `terreno`, "El terreno que no vendí" (Drive: "El terreno que no vendí (5 capítulos)")**
- Narra Ceferino Ibarra (antes Jésus García), 75: gigante de 2.01 m, manos como palas; cuatro acres al sur de Phoenix con el único pozo y el único camino; su padre don Crescencio está enterrado bajo el mezquite; esposa Remedios fallecida; hijo Beto y nuera Lupita.
- Gerald Fenwick (constructora de Nueva York): flaquísimo, pálido, lentes redondos, nariz larga, dientes enormes. Doña Tomasa Sepúlveda: 1.35 m, sombrero de paja como llanta. Nacho Palafox: taquero calvo de 170 kg. Profesora Ivonne Castellanos: casi 2 m, delgada como lápiz, lentes de fondo de botella.
- Canon aplicado: la idea decía que muere y el parque ya existe; como narra vivo, dona el parque en vida ("Parque Herencia"), la tierra queda no vendible por escritura, la placa "El millonario que dijo que no" está en la casita-museo junto al papel de la oferta y la maqueta con equis rojas; el terreno es la LLAVE (pozo y camino) → efecto dominó; cada 9 de abril la comunidad planta un árbol; añadí una tarjeta final de Fenwick desde Florida ("usted tuvo razón").

**Estado 2026-10-20 (23:30):** LAS DOS SERIES COMPLETAS y entregadas en I:\Mi unidad (md5 verificado): "El mozo que salvó la empresa (5 capítulos)" y "El terreno que no vendí (5 capítulos)".
Lecciones de esta producción: (1) Flow (nano_banana_2 / omni_flash) volvió a funcionar a las 18:45 y se usó con `--parallel 5` a la vez que Pics (4) y Vids; (2) los renombres de refs por choque de prefijo (CALLE→KALLEJA…) también cambian los textos de miniaturas.json (ej. "CASA"→"KOCINA"): revisar tras renombrar; (3) la ficha del uniforme no debe decir "name patch" (sale texto); (4) hooks: tomas.json `personajes.tag` no lleva variante, va en `var`; (5) `montar_serie.ps1 -SoloBase` monta sin esperar hooks; ENC_PRESET=ultrafast baja el montaje a ~8-10 min/capítulo; (6) `srt.py` adelanta 0.15 s; (7) `cola_clips_serie.ps1` reparte clips Vids (caps 1-3) y Flow (4-5).
