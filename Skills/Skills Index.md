---
type: skill-index
status: active
updated: 2026-07-19
tags: [skills, ai-os]
---

# Skills Index

The map. Use this first to pick which skill to load. Each `SKILL.md` is the source
of truth; this note just points to it. Follow [[AGENT-RULES]].

## Hierarchy (load lower layers to ground higher ones)

- **Grounding** — who you are, background, positioning.
- **Voice** — how things sound: [[Skills/example-voice/SKILL|example-voice]].
- **Research** — turn sources into a plan.
- **Output** — the deliverable skills (each loads grounding + voice).

## Choose the right skill

> One block per skill. Keep the six fields.

### Example Voice
- **File:** [[Skills/example-voice/SKILL]]
- **Use when:** a draft needs to sound like you (tone, anti-slop, first person).
- **Main output:** a voice pass on an existing draft, not a first draft.
- **Also load:** the output skill that wrote the draft.
- **Do not use for:** generating structure from scratch.
- **Guardrails:** never invent facts to make a line land better.

_Add a block here whenever you add a skill folder. Copy `example-voice/` to start
a new skill (it doubles as the template)._
