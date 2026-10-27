---
name: 
description: ""
updated: {{date:YYYY-MM-DD}}
---

# {{title}}

## Overview
What this skill produces and the one thing it must always do. What it is *not* for.

## Load First
1. Grounding skill (background, positioning) if it needs facts about the owner.
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
- What gets produced and where it is saved: a project folder in the right area (see [[AGENT-RULES]] §1 and §3), not `working-dir/`.

## Guardrails
- Never store secrets in the vault.
- Do not invent facts, metrics, quotes or personal history.

## Feedback log
After each run, add an entry to the sibling `FEEDBACK.md`. When a lesson repeats, promote it into this file. Rules: [[AGENT-RULES]] §5.
