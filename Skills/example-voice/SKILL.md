---
name: example-voice
description: "Apply the owner's writing voice to any draft. Use when a post, script, newsletter, or reply needs to sound like the owner instead of generic AI prose: tone, persona, sentence rhythm, anti-slop rules, and first-person grounding. This is a style layer, not a first-draft writer."
updated: 2026-07-19
---

# Example Voice

## Overview

A style layer that rewrites an existing draft into the owner's voice. It never
generates the first draft's structure and never invents facts. Pair it with an
output skill (post, script, newsletter).

## Load First

1. `<grounding skill>` — for the owner's background, opinions, and safe positioning.
2. The output skill that produced the draft (post / script / review).

## Inputs

- A complete first draft to rewrite.
- The target platform (post, video, email) so rhythm and length fit.
- If there is no draft yet, stop — this skill edits, it does not originate.

## Workflow

1. Read the draft and the platform.
2. Rewrite for voice: shorter sentences, concrete nouns, first person, no hype.
3. Run the anti-slop pass (see Guardrails).
4. Return the rewritten draft only. Show scores/notes only if asked.

## Output

- The rewritten draft, saved in the relevant `Areas/` folder (not `working-dir/`).
- This skill produces notes, not code, so nothing gets pushed to a repo. (Code
  tasks keep their code in an external repo — see [[AGENT-RULES]] §3.)

## Guardrails

- No em-dashes. No "in today's fast-paced world", "unlock", "delve", "tapestry",
  "game-changer", or filler transitions.
- Do not invent metrics, anecdotes, tools used, or feelings.
- Keep the owner's actual opinions; do not sand off the edges into neutral prose.

## Feedback

See [[Skills/example-voice/FEEDBACK|FEEDBACK]]. Append after every run;
promote repeated lessons here and bump `updated:`. See [[AGENT-RULES]] §2.
