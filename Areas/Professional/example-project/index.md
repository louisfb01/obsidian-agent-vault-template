---
type: project-index
status: active
created: 2026-10-27
updated: 2026-10-27
summary: "Example of a project folder: front note, progress log, one folder per version, and project rules for agents. Delete it when you have your own projects."
tags:
  - example
---

# Example project: launch talk

A 20-minute talk about a product launch. This folder is an example of the project pattern in [[AGENT-RULES]] §3: everything below is illustrative.

## Current version

- `v2-long/` (example): 30 slides, the one to present from. What changed is in the [progress log](progress-log.md).

## Earlier versions

- `v1/` (example): first 18-slide draft. Kept, never overwritten.

## Open items

- Re-check the user numbers on slide 12 the week of the talk (as of 2026-10-27 they come from the September dashboard).

## Where things live

- Repo for any code or generated charts: your projects folder, for example `~/github/launch-talk`.
- Raw recordings: outside the vault, for example `~/Projects/launch-talk-source/`.

## For agents

- Every new deck version gets its own folder here and a dated entry in the [progress log](progress-log.md).
- Never edit `talk-notes.md` (the owner's own notes); add agent notes in a separate file.
