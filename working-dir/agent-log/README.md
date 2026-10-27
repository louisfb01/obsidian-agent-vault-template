---
type: log
status: active
created: 2026-10-27
updated: 2026-10-27
summary: "Format of the shared agent log, so Claude Code, Codex and scheduled runs can see what each other did in the vault."
tags:
  - agent-log
---

# Agent log

One file per month (`YYYY-MM.md`). Every agent run that writes to the vault adds one line at the bottom of the current month:

```
- YYYY-MM-DD HH:MM · <agent> · <task> · <paths touched> · <outcome>
```

- **agent:** `claude-code`, `codex`, `codex-automation:<name>`, or the harness name.
- **paths touched:** the folders or notes written, shortest form that is still clear.
- **outcome:** done, partial (what is left), or blocked (why).

Append only. Never edit or remove another run's line. Read-only runs do not log.
