---
name: flow-connector-setup
description: Flow Connector (flow-auto CLI) is installed on this Windows machine; quirks of driving it from this session.
metadata:
  node_type: memory
  type: reference
  originSessionId: 43ba66ce-8084-4e55-8c47-8773587f6779
  modified: 2026-10-12T15:14:36.961Z
---

Installed 2026-10-11: Node v24 via winget, `flow-connector-cli` global, skill in ~/.claude/skills/flow-generate. User's plan: Pro since 2026-10-12 (batching 4, no daily limit; before that free: 40 img/day, one at a time).

- This session's shell PATH is stale: prefix commands with `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')`.
- 2026-10-12: user ran out of Nano Banana Pro generations; scenes now forced with `--model nano-banana-2` (src\escenas.ps1). Files in Downloads have [brackets] in names: always use -LiteralPath.
- Narrow (half-screen) Chrome window caused "clickTrusted ... is covered by" failures; maximise fixed it.
- User's Flow assets are named by tag (ENCINO, ARNULFO, CIMIENTO, LILIANA, FIDENCIO, GUSTAVO, JARDIN) and resolve via `--asset`.
- Default downloads are 768×1376, not the 1152×2048 his spec wants — see [[master-prompt-reflexion]].
- Batch script C:\Users\luisa\calude\cimiento\submit.ps1 (-From/-To) and renamer renumerar.ps1 are reusable; the CIMIENTO 123-prompt run itself was abandoned on 2026-10-11 (user restarted from scratch under the master prompt).
