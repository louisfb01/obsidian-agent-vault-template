---
type: hub
status: active
updated: 2026-10-27
summary: "Front door of the vault: what it is, the layout, and where agents start. Links hubs only, never single notes."
tags:
  - start-here
---

# Start Here

An Obsidian vault set up to run AI agents as a personal operating system: **skills** they load, **notes** they ground on, **rules** every agent follows, and a loop that makes the vault better the more you use it.

## Open it

**Obsidian → Open folder as vault → pick this folder.** That's the install. A vault is just a folder of Markdown files, so there is nothing to run, and you can read every file as plain text first.

The **Templates** core plugin is already on and pointed at `Templates/`, so note scaffolds work right away (Command palette → *Insert template*).

## Hubs

- [[Areas/Professional/Professional|Professional]]
- [[Areas/Personal/Personal|Personal]]
- [[Skills/Skills Index|Skills Index]]: every skill and which one to load.

## The layout

```
START-HERE.md      ← you are here
AGENT-RULES.md     ← every agent reads this first: folder map, ownership, note rules, feedback loop
CLAUDE.md          ← pointer so Claude Code loads AGENT-RULES.md
AGENTS.md          ← pointer so Codex and other agents load AGENT-RULES.md
Skills/            ← one folder per skill: SKILL.md + FEEDBACK.md
  Skills Index.md  ← the map: which skill to load
Areas/             ← your real notes, one hub per area, one folder per project
working-dir/       ← agent scratch, research projects, agent log, maintenance state
Templates/         ← note scaffolds: project index, progress log, skill, feedback, task
_archive/          ← stale notes, kept not deleted
```

## The ideas to understand

1. **One rules file for every agent.** `AGENT-RULES.md` is the contract. `CLAUDE.md` and `AGENTS.md` only point to it, so Claude Code, Codex or anything else lands on the same rules.
2. **Every skill learns.** Each skill has a `FEEDBACK.md`. After a run the agent logs what worked and what you corrected; when a correction repeats it is promoted into `SKILL.md` as a new default. See `AGENT-RULES.md` §5 and `Skills/example-voice/FEEDBACK.md`.
3. **Projects resume themselves.** Each project folder has an `index.md` (current version first) and a `progress-log.md`, so a new session picks up where the last one stopped. See `Areas/Professional/example-project/`.
4. **Scheduled tasks run skills.** A scheduled task's prompt only points to a skill (`Templates/Scheduled task prompt.md`), so its procedure improves through the same feedback loop. `Skills/scheduled-runs/` holds what every unattended run shares.
5. **Maintenance runs on a schedule.** `Skills/vault-maintenance/` keeps hubs and links healthy and reports where the rules are not followed.

## 3-step setup

1. Fill in the owner line and the folder map in `AGENT-RULES.md` §1. Rename the `Areas/` folders to match your life.
2. Copy `Skills/example-voice/` to make your first real skill, then add its block to `Skills Index.md`.
3. Open your agent in this folder, or add the user-level pointer from the README so it finds the vault from anywhere.
