# working-dir

The agent's scratch area. All messy, in-progress work lives here — one folder per
task — so it never clutters the vault or the Areas notes.

## Convention
```
working-dir/
  <task-name>/
    index.md   # what this task is + current status (use the "Working task" template)
    log.md     # append-only run log: what was tried, decided, and why
    raw/       # unprocessed inputs, dumps, downloads, transcripts
```

## Rules
- Final deliverables move to an Areas/ folder when done. They do not stay here.
- Keep index.md current so a future session can resume without re-reading log.md.
