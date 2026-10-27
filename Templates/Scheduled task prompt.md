---
type: template
status: active
created: 2026-10-27
updated: 2026-10-27
summary: "The prompt to paste into a scheduler (Codex automation, Claude scheduled task, cron) so the task runs a vault skill instead of carrying its own procedure. Replace the angle-bracket parts."
tags:
  - template
  - scheduled
---

# Scheduled task prompt

Paste the block below into the scheduler and replace each `<...>`. Keep it this short: the steps, what the owner approved and every lesson belong in the skill, not here ([[AGENT-RULES]] §5). Before switching an existing task over, save its old prompt verbatim next to the task (for example `prompt-before-YYYY-MM-DD.md`) as the fallback.

```text
Scheduled run: <task name>. This prompt only points to the skill that holds the procedure, so the procedure can improve without editing this task. Earlier versions of this prompt in this chat are superseded.

1. Read <vault path>/AGENT-RULES.md, then <vault path>/<skills folder>/scheduled-runs/SKILL.md (start, browser, report email and end-of-run rules for every scheduled run).
2. Open <vault path>/<skills folder>/<skill>/<SKILL.md or scheduled-run.md>, read the open entries in the FEEDBACK.md in that folder, and follow the skill exactly: its steps, its guardrails, what the owner approved, and its final-response format.
3. State between runs: <state file or folder>.
4. During this run, do not edit the skill, the scheduled-runs skill or this prompt. If a step failed, a rule was unclear, or the owner corrected an earlier result, add an entry to that FEEDBACK.md (a browser, email or scheduler problem that any task could hit goes in scheduled-runs/FEEDBACK.md).
5. If the vault or the skill cannot be read, follow the previous full prompt saved at <fallback path> and say so in the final response. If that cannot be read either, stop and report.
```
