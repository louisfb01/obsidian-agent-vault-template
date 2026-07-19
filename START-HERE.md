---
type: readme
tags: [start-here]
---

# Start Here

An Obsidian vault set up to run an AI agent as a personal operating system:
**skills** it loads, **notes** it grounds on, and a loop that makes it improve the
more you use it. Based on Louis-François Bouchard's working vault, genericized.

## Open it
**Obsidian → Open folder as vault → pick this folder.** That's the install. A vault
is just a folder of markdown files, so there is nothing to run — you can read every
file in plain text first.

The **Templates** core plugin is already turned on and pointed at `Templates/`, so
one-click note scaffolds work immediately (Command palette → *Insert template*, or
bind a hotkey).

## The layout
```
START-HERE.md      ← you are here
AGENT-RULES.md     ← the agent reads this first: how to behave + self-improve
Skills/            ← the "AI-OS": one folder per skill
  Skills Index.md  ← the map: which skill to load, layered hierarchy
  example-voice/   ← a worked example — copy it to make your own skill
    SKILL.md       ← what the skill does (source of truth)
    FEEDBACK.md ← the skill's self-improvement log  ← the key idea
working-dir/       ← agent scratch: one folder per task
Areas/             ← your real notes (Personal, Professional, add your own)
Templates/         ← one-click note scaffolds (used by the Templates plugin)
_archive/          ← stale notes, kept not deleted
```

## The one idea to understand
Every skill has a **`FEEDBACK.md`**. After each run the agent logs what worked
and what you corrected; when a correction repeats, it gets *promoted* into the
`SKILL.md` as a new default. That is the vault teaching itself your preferences
over time. See `AGENT-RULES.md` §2 and the live example in
`Skills/example-voice/FEEDBACK.md`.

## 3-step setup
1. Rename the `Areas/` folders to match your life; drop in your notes.
2. Copy `Skills/example-voice/` to create your first real skill, then add a block
   for it in `Skills Index.md`.
3. Point your agent at the vault and say: *"Read AGENT-RULES.md first."*

*Template by Louis-François Bouchard. Reuse and adapt freely.*
