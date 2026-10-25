---
name: series-cumple-regreso-restaurante
description: "Second batch of 3 new Reflexión series (IDEAS 4-6) started 2026-10-17 — folders, voices, canonical fixes and status"
metadata:
  node_type: memory
  type: project
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-17T20:29:48.405Z
---

Folders under C:\Users\luisa\calude\ (scripts copied from lavaplatos\src):
- **cumple**: "Me prohibió ir al cumpleaños". Carmen narrates (69, Queens), so it needs the FEMALE voice. Reuse Fish "Abuela" 0baf4054bf624d388ad755ed3da939fc at speed 1.25 ([[series-cobro-lavaplatos-nieta]]).
- **regreso**: "El día que mi hijo regresó". Alonso narrates (64, Denver), voice Valentino 8d2c17a9b26d4d83888ea67a1ee565b2.
- **restaurante**: "Quince años en la cocina de mi hijo". Rogelio narrates (63, Los Ángeles), voice Valentino.

Canonical fixes applied to Luis's ideas:
- cumple: Silvia is 49, not 42, so that the 30 years fit (she left at 19). Marco already knows who his grandmother is, because he found the box ("para tirar" with the letter, the scapular and the returned chamarra) and invited her. Silvia's husband Gregory also thought Carmen was dead.
- regreso: the velorio is Lupita's (Alonso's wife). David did not come because nobody told him. His letter dates from 3 years ago and says 17 years. He learns of Alonso's cancer through tía Patricia.
- restaurante: Juanita is the daughter of Lupe, Rogelio's eldest daughter (Carlos is 38, so he cannot be her father). Rogelio did invest $85,000 from his house in Fresno; Carlos booked it as a "donación".
- None of the three uses a comment question.

2026-10-17 STATUS (Luis said "dale" and approved; running autonomously):
- Fichas done for all 3 series.
- All 15 hook tomas and tableros done; the hook VIDEOS are not generated yet (images first).
- Audio: cumple is complete; regreso has audio and whisper in progress; restaurante TTS runs separately (log tts_rest.log). Master script: calude\audio_lote2.ps1, log audio_lote2.log.
- Scenes: per chapter, write visual\capN\spec.txt + moves.json, then run `calude\listo.ps1 -Serie X -Cap N` (build + audit; creates _ok when clean).
- The image queue calude\cola_lote2.ps1 (log cola_lote2.log) picks up every chapter that has _ok. It switches to nano_banana_pro on quota exhaustion.
- cumple specs: all 5 done and audited. regreso: caps 1-2 done. restaurante: none yet (it needs srt).
- Next steps: clips (glabs_clips.py), hooks (hooks_todo.ps1 skips the tomas if they exist; use glabs_hook.py + revisar_hook.py), montage (final_sm.ps1 then mezclar_subs.py N 0.10 then unir.py), thumbnails (miniaturas.json per series), editorial.json, entregar.py with the Drive folder names.
- Drive folder names: "Me prohibió ir al cumpleaños (5 capítulos)", "El día que mi hijo regresó (5 capítulos)", "Quince años en la cocina de mi hijo (5 capítulos)".

2026-10-17: all 15 guiones written and passing check.ps1, with GUIONES_*.txt files for reading. Waiting for Luis's approval, then run audio via src\tts.ps1 (cumple: -VoiceId Abuela -Speed 1.25), whisper, scenes, hooks, montage with music 0.10 and delivery to Drive. The pipeline is documented in [[series-cobro-lavaplatos-nieta]] and [[sistema-produccion]].

## Progreso 2026-10-18 08:30
- Imágenes, clips, hooks (15/15) y miniaturas (15/15) listos. Cuota de imágenes banana agotada: se usó model nano_pics (Google Pics, cuota aparte; glabs_api.py, glabs_tomas.py y miniaturas.py lo soportan con env GLABS_IMG_MODEL=nano_pics; 768x1376; lanzar de a pocos, la ráfaga de 15 falla ALL_ACCOUNTS_FAILED).
- Hook regreso cap1 rechazado por CHILD_SAFETY (David adolescente): se rehízo con David solo de espaldas con capucha.
- Antes de montar, verificar que no falten imágenes (se perdieron algunas por 429/UNSAFE: cumple3, regreso1, restaurante4 ya regeneradas).
- Montaje en marcha: calude\montaje_lote2.ps1 (log montaje_lote2.log, ~25 min por capítulo). Después: revisar uniones, entregar.py a las 3 carpetas de Drive.

## COMPLETO 2026-10-18 20:30
- Las 3 series (15 videos, miniaturas, textos) entregadas a Drive con MD5 verificado: 'Me prohibió ir al cumpleaños (5 capítulos)', 'El día que mi hijo regresó (5 capítulos)', 'Quince años en la cocina de mi hijo (5 capítulos)'.
- Lección: si la PC se duerme el montaje se congela (usar request_keep_awake); preset veryfast en montaje/quemar/unir baja a ~14 min por capítulo (medium era ~25).
