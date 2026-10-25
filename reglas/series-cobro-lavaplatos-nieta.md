---
name: series-cobro-lavaplatos-nieta
description: "Status of the 3 new Reflexión series started 2026-10-16 (folders cobro, lavaplatos, nieta) and the canonical fixes applied to Luis's ideas"
metadata:
  node_type: memory
  type: project
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-17T04:48:59.423Z
---

Three new comic-Marvel Reflexión series, folders under C:\Users\luisa\calude\ (scripts copied from testamento\src):
- **cobro**: "Ella me cobró por comer en su casa". Francisca narrates, so it VOICE CHOSEN (2026-10-16): Fish "Abuela" 0baf4054bf624d388ad755ed3da939fc at speed 1.25. Command: `src\tts.ps1 -VoiceId 0baf4054bf624d388ad755ed3da939fc -Speed 1.25`.
  - The $2,450 adds up because Marcela booked the cash envelopes as "ayuda de mamá para el súper", never as payments.
  - Francisca ends alive in Dallas.
- **lavaplatos**: Roberto narrates with Valentino.
  - "Salvador" is the surname of the father who abandoned them.
  - Javier gets his title at 30 and expels Roberto at his clinic at 40.
  - The rosario is returned by mail, with a dictated letter.
- **nieta**: Héctor narrates with Valentino.
  - His regret: he went back on the road after his wife Rosa died.
  - The document is the consulate registration with the note "No dar información al abuelo materno".
  - Ages: 3 / 8 (moved away) / 16 / 18 / 19; there are 180 bracelets.

2026-10-16: Luis asked for "ultra adictivos" guiones, so they were rewritten (v2: open loops, short lines, cliffhangers). The v1 backup is in src\v1. Luis APPROVED v2 ("perfectos").
2026-10-16 evening: Luis said "sigues trabajando todo sin mi aprobación", so the full pipeline is running autonomously.
Status:
- All 15 specs are written and audited.
- Fichas and hooks for all 3 series are done.
- cobro has all images, clips and hooks reviewed; its montage is running.
- lavaplatos images are in progress; nieta images are queued.
- Music is BLOCKED: Gemini prepay credits depleted (HTTP 402), so the chapters are being made without music via `src\final_sm.ps1`.

2026-10-16 21:00: cobro is COMPLETE and in Drive ("Ella me cobró por comer en su casa (5 capítulos)"), MD5-verified, delivered via src\entregar.py.
lavaplatos: montage is running. nieta: clips are running, then hooks.

2026-10-16 23:48: ALL 3 SERIES COMPLETE and in Drive, MD5-verified. Folders: "Ella me cobró por comer en su casa (5 capítulos)", "Dieciséis años lavando platos en Chicago (5 capítulos)", "Cinco horas de camión (5 capítulos)". No music (Gemini credits depleted).
- The Google daily image quota ran out after about 1750 images. G-Labs `nano_banana_pro` has a separate quota. Scripts now honour env GLABS_IMG_MODEL.
- The clip prompts leaked the location tag ("TAQUILLA") as a sign. glabs_clips.py now strips "Use only" and brackets.

Lessons:
- G-Labs leaked the ficha tag name ("Ximena") as handwriting. Fixed by changing NEG 'd' in build.py to "abstract wavy scribble lines".
- G-Labs blocks child+adult touching (UNSAFE_GENERATION). Avoid that contact in prompts.
- If G-Labs gives connection refused, the app closed and Luis must reopen it.

Audio for the 3 series runs via C:\Users\luisa\calude\audio_3series.ps1 (tts → pulir → srt → diff). Next: tiempos → visual blocks → fichas.
New helpers: src\reseg.py (splits lines over 9 words), juntar.py, voces.py (Fish voice search), muestra_voz.py.
