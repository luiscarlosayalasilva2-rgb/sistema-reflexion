---
name: gemini-api
description: "User's Google AI Studio (Gemini API) key is stored in the user env var GEMINI_API_KEY; which models work."
metadata:
  node_type: memory
  type: reference
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-12T21:24:21.370Z
---

Stored 2026-10-12 as user env var `GEMINI_API_KEY` (never print it). Key format starts "AQ." and works with header `x-goog-api-key` on https://generativelanguage.googleapis.com/v1beta.

Tested OK: `gemini-3.1-pro-preview`, `gemini-3.8-flash` (generateContent). `gemini-2.5-pro` failed. The model list also shows `gemini-nano-banana-2.1` and `gemini-omni-1.1-flash` (image/video via API — untested, may need billing).

Purpose: the user wants an app that turns a topic into the full series without Claude — see [[master-prompt-reflexion]] and [[serie-testamento-progreso]] for the pipeline it should reproduce.
