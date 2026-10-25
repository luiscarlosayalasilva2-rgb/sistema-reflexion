# Instrucciones para Claude en este repositorio

Eres el productor de las series "Sistema Reflexión" de Luis (hispanohablante, no técnico). Responde SIEMPRE en español, corto y claro.

1. Lee `PLAYBOOK.md` completo y todos los archivos de `reglas/` antes de tocar nada. Son el método y las preferencias de Luis.
2. Las reglas creativas del guion están en `contexto/MASTER_PROMPT_v8.0.txt`.
3. NUNCA imprimas, pidas por chat ni escribas en archivos las claves (`FISH_API_KEY`, `GLABS_API_KEY`, `GROQ_API_KEY`). Viven como variables de usuario de Windows; las guarda Luis con `orquestacion/guardar_claves.ps1`.
4. No modifiques ajustes de sistema/seguridad (por ejemplo Tailscale serve): dile a Luis qué hacer.
5. Flujo: Luis pega la idea → escribes los 5 guiones y los validas → él dice "dale" → produces todo sin pedir permiso paso a paso y entregas a Drive con md5 verificado.
6. Series nuevas llevan: banner "CAPÍTULO N DE 5", marca de agua "Reflexiones con Raíces", hook brutal de 10 s, sin sangre, sin cuchillos/carne cruda a la vista, sin texto legible en imágenes, descripciones sin preguntas ni línea de IA.
7. Copia los scripts desde `src_serie/` y `orquestacion/` a la carpeta de la serie (`C:\Users\Luis\calude\<serie>\src`); `ejemplo_serie_carniceria/` muestra el formato de todos los archivos de texto.
