---
name: 
description: ""
updated: {{date:YYYY-MM-DD}}
---

# {{title}}

## Overview
What this skill produces and the one thing it must always do. What it is *not* for.

## Load First
1. Grounding skill (background/positioning) if it needs facts about you.
2. Voice skill if the output is public-facing.
3. Review skill for a final quality pass.

## Inputs
- What the skill needs to start, and where those inputs live.
- What to do if an input is missing (usually: stop and ask).

## Workflow
1. 
2. 
3. 

## Output
- What gets produced and where it is saved (an `Areas/` folder, not `working-dir/`).

## Guardrails
- Never store secrets in the vault.
- Do not invent facts, metrics, quotes, or personal history.

## Feedback
See the sibling `FEEDBACK.md`. Append after every run; promote repeated lessons
into this file. See [[AGENT-RULES]] §2.
