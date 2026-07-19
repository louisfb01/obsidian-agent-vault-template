# Obsidian Agent Vault Template

A ready-to-use **Obsidian vault** for running an AI agent (Claude, Codex, or any
assistant) as a personal operating system: **skills** it loads, **notes** it
grounds on, and a **feedback loop** that makes it improve the more you use it.

Based on the working vault of [Louis-François Bouchard](https://www.louisbouchard.ai/)
(Towards AI / What's AI), genericized so anyone can clone it and start.

## Get it

```bash
git clone https://github.com/louisfb01/obsidian-agent-vault-template.git
```

Or click **Code → Download ZIP** above. Then in Obsidian:
**Open folder as vault → pick this folder.** That's the whole install — a vault is
just a folder of markdown files, so there is nothing to run and you can read every
file as plain text first.

The **Templates** core plugin comes pre-configured (pointed at `Templates/`), so
one-click note scaffolds work immediately — *Command palette → Insert template*.

## What's inside

```
START-HERE.md      ← open this first in Obsidian
AGENT-RULES.md     ← the agent reads this first: how to behave + self-improve
Skills/            ← the "AI-OS": one folder per skill
  Skills Index.md  ← the map: which skill to load, layered hierarchy
  example-voice/   ← a worked example — copy it to make your own skill
    SKILL.md       ← what the skill does (source of truth)
    FEEDBACK.md    ← the skill's self-improvement log  ← the key idea
working-dir/       ← agent scratch: one folder per task
Areas/             ← your real notes (Personal, Professional, add your own)
Templates/         ← one-click note scaffolds (Templates plugin)
_archive/          ← stale notes, kept not deleted
```

## The idea

- **Skills are capabilities.** Each `SKILL.md` tells the agent how to do one job.
  `Skills Index.md` maps them, layered **grounding → voice → research → output**,
  so a task combines a grounding skill with an output skill.
- **Notes are grounding.** `Areas/` holds your real notes. Skills read facts from
  here and write finished work back — they never invent what isn't written.
- **The feedback loop is the point.** Every skill has a `FEEDBACK.md`. After each
  run the agent logs what worked and what you corrected; when a correction
  repeats, it gets *promoted* into `SKILL.md` as a new default. The vault teaches
  itself your preferences over time. See `AGENT-RULES.md` §2 and the live example
  in `Skills/example-voice/FEEDBACK.md`.
- **Code stays external.** The vault holds notes and skills, not code. Code lives
  in its own git repo wherever you keep projects. Never commit secrets.

## Setup (2 minutes)

1. *Open folder as vault* in Obsidian.
2. Rename the `Areas/` folders to match your life; drop in your notes.
3. Copy `Skills/example-voice/` to make your first real skill; add its block to
   `Skills Index.md`.
4. Point your agent at the vault: *"Read AGENT-RULES.md first."*

## License

MIT — see [LICENSE](LICENSE). Reuse and adapt freely.
