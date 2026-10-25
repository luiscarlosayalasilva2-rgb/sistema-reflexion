---
name: feedback-musica-volumen
description: "Music bed volume rule — 0.10 (not 0.18), ducked under narration, never on the hook; reuse the existing track when no new music is available"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-17T06:03:27.405Z
---

On 2026-10-17 Luis said the music in the earlier videos (El testamento caps 2-5, mixed at volume 0.18) still sounded too loud. The new rule is volume **0.10** with the same sidechain ducking. Music never plays over the hook.

When Lyria/AI Studio is unavailable, reuse `testamento\audio\musica\musica_serie.mp3` ("usa música que ya usamos antes").

**Why:** the music competed with the narration.
**How to apply:** mix it with `src\mezclar_subs.py N [vol]` on `out\capN_base_subs.mp4`, then run `unir.py`. See [[sistema-produccion]].
