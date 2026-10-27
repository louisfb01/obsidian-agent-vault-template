---
type: hub
status: active
created: 2026-10-27
updated: 2026-10-27
summary: "How the agents' scratch area is organised: one folder per task, research projects, the agent log, and vault maintenance."
tags:
  - working-dir
---

# working-dir

The agents' scratch area. Messy, in-progress work lives here, one folder per task, so it never clutters the area folders. Rules: [[AGENT-RULES]] §3.

## Task folders

```
working-dir/
  <task>/
    index.md   # what this task is and its current status (Templates/Working task.md)
    log.md     # append-only run log: what was tried, decided, and why
    raw/       # unprocessed inputs, dumps, downloads, transcripts
```

The finished result is written into its project folder in the right area. The scratch folder stays.

## Research projects

`research-<topic>/` folders keep sources and synthesis apart:

```
research-<topic>/
  raw/        # sources as captured, never edited
  wiki/       # derived pages: overview, synthesis, open questions, sources/, concepts/
  index.md    # generated from index.yaml when the header says so; rebuild it, do not hand-edit
  log.md      # rounds of research, newest last
```

## Shared folders

- `agent-log/`: one file per month, one line per run that wrote to the vault ([[working-dir/agent-log/README|format]]).
- `vault-maintenance/`: state snapshot and weekly log of [[Skills/vault-maintenance/SKILL|Vault Maintenance]].
