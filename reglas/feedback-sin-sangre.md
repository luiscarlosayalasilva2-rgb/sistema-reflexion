---
name: feedback-sin-sangre
description: "Luis pide SIN SANGRE en las imágenes (delantales de carnicero manchados de rojo, salpicaduras): desde 2026-10-24 ningún prompt debe llevarla"
metadata:
  type: feedback
---

Luis dijo "sin sangre" al ver las imágenes de la serie carniceria (delantal blanco manchado de rojo en cientos de planos).

**Why:** contenido más limpio para Facebook y su gusto; vale para series nuevas.
**How to apply:** en toda ficha de ropa/oficio (carnicero, cirujano, cocinero...) escribir "spotless clean ... no stains, no blood". Las plantillas `build.py`, `hook_tomas.py`, `glabs_fichas.py` de `carniceria\src` ya llevan la cláusula "No blood, no blood stains, no gore, no red splatters" (copiarlas a series nuevas) y quité "blood" de la lista BANNED de build.py porque la cláusula negativa la dispara. Si hay que rehacer: borrar imágenes con ese personaje, clips y hooks, regenerar y montar ([[series-lote7-ideas-2-10]]).

**Ampliación (2026-10-24, Luis dijo "sí"):** en las ideas SIGUIENTES (de la 6 en adelante) evitar también cuchillos y carne a la vista: planos de manos, mostrador o vitrina con carne cruda, armas, etc. Mostrar el oficio con objetos neutros (herramientas, cajas, tortillas, ropa limpia). La serie carniceria (idea 5) ya en curso conserva la vitrina y el cuchillo; solo se quitó la sangre.
